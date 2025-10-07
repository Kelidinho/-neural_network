# Fichero: data_pipeline.py (Versión 5 - Robusta y Optimizada)

import pandas as pd
import requests
from pathlib import Path
import time
import holidays
from calendar import monthrange
import json
import shutil


class DataPipeline:
    """
    Una pipeline de datos robusta y optimizada para la extracción y enriquecimiento
    de datos de la MTA. Procesa los datos por semanas, puede reanudar el trabajo
    si falla y aplica un tipado fuerte para optimizar el almacenamiento.
    """

    def __init__(self, years: list[str], routes: list[str], base_path: str = "data"):
        self.years = years
        self.routes = routes
        self.base_path = Path(base_path)
        self.temp_path = self.base_path / "_tmp"
        self.state_file = self.temp_path / "progress.json"

    def _get_weekly_periods(self, year: str) -> list[tuple[str, str]]:
        """Genera tuplas de (fecha_inicio, fecha_fin) para cada semana del año."""
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        # pd.date_range genera fechas con frecuencia semanal (semana que termina el domingo)
        mondays = pd.date_range(start=start_date, end=end_date, freq='W-MON')
        periods = []
        last_start = pd.to_datetime(start_date)
        for day in mondays:
            periods.append((last_start.strftime('%Y-%m-%d'), day.strftime('%Y-%m-%d')))
            last_start = day + pd.Timedelta(days=1)
        if last_start <= pd.to_datetime(end_date):
            periods.append((last_start.strftime('%Y-%m-%d'), end_date))
        return periods

    def _fetch_data_for_period(self, start_date: str, end_date: str) -> pd.DataFrame | None:
        """Descarga los datos de todas las rutas para un periodo de tiempo específico."""
        period_data_frames = []
        for route in self.routes:

            print(f"    > Ruta: {route}...", end="")
            API_LIMIT = 50000;
            offset = 0;
            all_data = [];
            base_url = "https://data.ny.gov/resource/kv7t-n8in.json"
            while True:
                params = {"$select": "transit_timestamp,bus_route,ridership,transfers",
                          "$where": f"transit_timestamp between '{start_date}T00:00:00.000' and '{end_date}T23:59:59.000' AND bus_route='{route}'",
                          "$limit": API_LIMIT, "$offset": offset}
                try:
                    response = requests.get(base_url, params=params, timeout=300)
                    response.raise_for_status()
                    page_data = response.json()
                    if not page_data: break
                    all_data.extend(page_data)
                    offset += API_LIMIT
                except requests.exceptions.RequestException as e:
                    print(f" ¡Error! {e}")
                    return None
            print(f" {len(all_data)} registros.")
            if all_data:
                period_data_frames.append(pd.DataFrame(all_data))
            time.sleep(1)

        if not period_data_frames:
            return None
        return pd.concat(period_data_frames, ignore_index=True)

    def _get_final_schema(self) -> dict:
        """Define el tipado fuerte para el DataFrame final."""
        return {
            'transit_timestamp': 'datetime64[ns]',
            'bus_route': 'category',
            'ridership': 'uint32',
            'transfers': 'uint32',
            'hour': 'uint8',
            'day_of_week': 'uint8',
            'month': 'uint8',
            'year': 'uint16',
            'is_weekend': 'bool',
            'is_holiday': 'bool',
            'temperature_2m': 'float32',
            'relative_humidity_2m': 'float32',
            'precipitation': 'float32',
            'rain': 'float32',
            'snowfall': 'float32',
            'weather_code': 'uint8',
            'wind_speed_10m': 'float32'
        }

    def _enrich_and_type_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica todo el enriquecimiento y el tipado fuerte a un DataFrame."""
        # Procesamiento inicial
        df['transit_timestamp'] = pd.to_datetime(df['transit_timestamp'])
        df['ridership'] = pd.to_numeric(df['ridership'])
        df['transfers'] = pd.to_numeric(df['transfers'])

        # Enriquecimiento de Calendario
        dt_col = df['transit_timestamp']
        df['hour'] = dt_col.dt.hour
        df['day_of_week'] = dt_col.dt.dayofweek
        df['month'] = dt_col.dt.month
        df['year'] = dt_col.dt.year
        df['is_weekend'] = (df['day_of_week'] >= 5)
        years_in_data = df['year'].unique()
        ny_holidays = holidays.country_holidays('US', state='NY', years=years_in_data)
        df['is_holiday'] = df['transit_timestamp'].dt.date.apply(lambda date: date in ny_holidays)

        # Enriquecimiento de Clima
        start_date = df['transit_timestamp'].min().strftime('%Y-%m-%d')
        end_date = df['transit_timestamp'].max().strftime('%Y-%m-%d')
        LAT, LON = 40.78, -73.96
        weather_url = (
            f"https://archive-api.open-meteo.com/v1/archive?latitude={LAT}&longitude={LON}&start_date={start_date}&end_date={end_date}&hourly="
            "temperature_2m,relative_humidity_2m,precipitation,rain,snowfall,weather_code,wind_speed_10m")
        response = requests.get(weather_url)
        if response.status_code == 200:
            weather_data = response.json()['hourly']
            df_weather = pd.DataFrame(weather_data)
            df_weather.rename(columns={'time': 'transit_timestamp'}, inplace=True)
            df_weather['transit_timestamp'] = pd.to_datetime(df_weather['transit_timestamp'])
            df = pd.merge(df, df_weather, on='transit_timestamp', how='left')
            weather_cols = [col for col in df_weather.columns if col != 'transit_timestamp']
            df[weather_cols] = df[weather_cols].ffill().bfill()

        # Aplicar el tipado fuerte y final
        schema = self._get_final_schema()
        # Asegurarnos de que solo aplicamos el schema a las columnas existentes
        final_cols = {col: dtype for col, dtype in schema.items() if col in df.columns}
        df = df[final_cols.keys()].astype(final_cols)

        return df

    def run(self):
        """Ejecuta la pipeline completa de forma robusta y resumible."""
        print("🚀 Iniciando pipeline robusta...")
        self.temp_path.mkdir(parents=True, exist_ok=True)

        last_completed_week = -1
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                last_completed_week = json.load(f).get('last_completed_week', -1)
                print(f"🔄 Reanudando trabajo. Última semana completada: {last_completed_week + 1}")

        for year in self.years:
            weekly_periods = self._get_weekly_periods(year)
            for i, (start_date, end_date) in enumerate(weekly_periods):
                if i <= last_completed_week:
                    print(f"⏭️  Saltando semana {i + 1}/{len(weekly_periods)} (ya procesada)...")
                    continue

                print(f"\n--- Procesando Semana {i + 1}/{len(weekly_periods)} ({start_date} a {end_date}) ---")

                # 1. Descargar
                df_week = self._fetch_data_for_period(start_date, end_date)
                if df_week is None or df_week.empty:
                    print("  > No se encontraron datos para esta semana.")
                    continue

                # 2. Enriquecer y Tipar
                df_week_processed = self._enrich_and_type_data(df_week)

                # 3. Guardar temporalmente
                temp_file = self.temp_path / f"{year}_week_{i}.parquet"
                df_week_processed.to_parquet(temp_file, engine='pyarrow')
                print(f"  > Datos de la semana guardados temporalmente en {temp_file}")

                # 4. Guardar progreso
                with open(self.state_file, 'w') as f:
                    json.dump({'last_completed_week': i}, f)

        # 5. Consolidación Final
        print("\n--- Consolidación Final ---")
        all_week_files = list(self.temp_path.glob("*.parquet"))
        if not all_week_files:
            print("No hay datos para consolidar. Finalizando.")
            return

        print(f"  > Uniendo {len(all_week_files)} archivos semanales...")

        df_final = pd.read_parquet(all_week_files) # type: ignore

        # Ordenar y guardar el archivo final particionado
        df_final.sort_values(by=['transit_timestamp', 'ridership'], ascending=[True, False], inplace=True)
        final_path = self.base_path / "ridership_enriched_final.parquet"
        df_final.to_parquet(final_path, engine='pyarrow', partition_cols=['year', 'bus_route'])

        print(f"✅ ¡Éxito! Dataset final guardado en: {final_path}")

        # 6. Limpieza
        # shutil.rmtree(self.temp_path)
        # print("  > Archivos temporales eliminados.")