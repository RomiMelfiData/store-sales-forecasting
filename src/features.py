"""
features.py
-----------
Funciones reutilizables para el feature engineering del proyecto
de forecasting de demanda.

Features implementados:
- Variables temporales (día, mes, año, trimestre, etc.)
- Variables de lag (ventas de días anteriores)
- Variables de rolling (promedios móviles)
- Variables externas (precio del petróleo, feriados)

Uso:
    from src.features import agregar_features_temporales
    from src.features import agregar_lags
    from src.features import agregar_rolling
    from src.features import agregar_precio_petroleo
    from src.features import agregar_feriados
"""

import pandas as pd
import numpy as np


def agregar_features_temporales(df: pd.DataFrame,
                                 col_fecha: str = 'date') -> pd.DataFrame:
    """
    Agrega variables temporales extraídas de la columna de fecha.

    Variables creadas:
    - dia_semana: 0=Lunes, 6=Domingo
    - mes: 1 a 12
    - año: año del registro
    - trimestre: 1 a 4
    - dia_mes: 1 a 31
    - semana_año: semana ISO del año (1 a 52)
    - es_fin_de_semana: 1 si sábado o domingo, 0 si no

    Args:
        df: DataFrame con columna de fecha
        col_fecha: nombre de la columna de fecha

    Returns:
        DataFrame con las nuevas variables agregadas
    """
    df = df.copy()
    df[col_fecha] = pd.to_datetime(df[col_fecha])

    df['dia_semana']     = df[col_fecha].dt.dayofweek
    df['mes']            = df[col_fecha].dt.month
    df['año']            = df[col_fecha].dt.year
    df['trimestre']      = df[col_fecha].dt.quarter
    df['dia_mes']        = df[col_fecha].dt.day
    df['semana_año']     = df[col_fecha].dt.isocalendar().week.astype(int)
    df['es_fin_de_semana'] = (df['dia_semana'] >= 5).astype(int)

    print(f"Features temporales agregados ✅ (+7 columnas)")
    return df


def agregar_lags(df: pd.DataFrame,
                 col_target: str = 'sales',
                 col_grupo: list = ['store_nbr', 'family'],
                 lags: list = [7, 14, 28]) -> pd.DataFrame:
    """
    Agrega variables de lag agrupadas por tienda y familia.

    Un lag de N días le dice al modelo cuánto se vendió
    N días atrás para la misma combinación tienda-familia.
    Evita que el historial de una tienda contamine a otra.

    Nota: los primeros N días de cada grupo generarán NaN
    porque no existe historial previo suficiente.

    Args:
        df: DataFrame ordenado por fecha
        col_target: columna objetivo (ventas)
        col_grupo: columnas de agrupación
        lags: lista de días de lag a calcular

    Returns:
        DataFrame con las nuevas variables de lag
    """
    df = df.copy()
    df = df.sort_values(col_grupo + ['date']).reset_index(drop=True)

    for lag in lags:
        nombre = f'lag_{lag}'
        df[nombre] = df.groupby(col_grupo)[col_target].shift(lag)

    print(f"Lags agregados ✅ (+{len(lags)} columnas): {['lag_' + str(l) for l in lags]}")
    return df


def agregar_rolling(df: pd.DataFrame,
                    col_target: str = 'sales',
                    col_grupo: list = ['store_nbr', 'family'],
                    ventanas: list = [7, 28]) -> pd.DataFrame:
    """
    Agrega promedios móviles agrupados por tienda y familia.

    El .shift(1) previo al cálculo es obligatorio para evitar
    data leakage — sin él, el promedio incluiría las ventas
    del día actual, usando información del futuro para predecir
    el presente.

    Args:
        df: DataFrame ordenado por fecha
        col_target: columna objetivo (ventas)
        col_grupo: columnas de agrupación
        ventanas: lista de ventanas de días para el rolling

    Returns:
        DataFrame con las nuevas variables de rolling
    """
    df = df.copy()

    for ventana in ventanas:
        nombre = f'rolling_{ventana}'
        df[nombre] = df.groupby(col_grupo)[col_target].transform(
            lambda x: x.shift(1).rolling(window=ventana).mean()
        )

    print(f"Rolling features agregados ✅ (+{len(ventanas)} columnas): "
          f"{['rolling_' + str(v) for v in ventanas]}")
    return df


def agregar_precio_petroleo(df: pd.DataFrame,
                             oil: pd.DataFrame,
                             col_fecha: str = 'date') -> pd.DataFrame:
    """
    Incorpora el precio del petróleo al dataset principal.

    Los valores nulos (fines de semana y feriados donde el
    mercado no opera) se resuelven mediante interpolación
    lineal complementada con ffill y bfill para los extremos.

    Args:
        df: DataFrame principal de ventas
        oil: DataFrame con columnas ['date', 'dcoilwtico']
        col_fecha: nombre de la columna de fecha

    Returns:
        DataFrame con el precio del petróleo incorporado
    """
    oil = oil.copy()
    oil['date'] = pd.to_datetime(oil['date'])

    # Reindexar para cubrir todos los días del calendario
    oil = oil.set_index('date').reindex(
        pd.date_range(oil['date'].min(), oil['date'].max(), freq='D')
    ).rename_axis('date').reset_index()

    # Interpolación + relleno de bordes
    oil['dcoilwtico'] = oil['dcoilwtico'].interpolate(method='linear')
    oil['dcoilwtico'] = oil['dcoilwtico'].ffill().bfill()

    # Merge con el dataset principal
    df = df.merge(oil, on='date', how='left')
    df['dcoilwtico'] = df['dcoilwtico'].ffill().bfill()

    nulos = df['dcoilwtico'].isnull().sum()
    print(f"Precio del petróleo incorporado ✅ — Nulos restantes: {nulos}")
    return df


def agregar_feriados(df: pd.DataFrame,
                     holidays: pd.DataFrame,
                     col_fecha: str = 'date',
                     locale: str = 'National') -> pd.DataFrame:
    """
    Agrega una variable binaria indicando si el día es feriado.

    Solo se consideran feriados del alcance especificado
    (por defecto: Nacional) para que el efecto sea consistente
    en todas las tiendas.

    Args:
        df: DataFrame principal de ventas
        holidays: DataFrame con columnas ['date', 'locale', ...]
        col_fecha: nombre de la columna de fecha
        locale: alcance del feriado ('National', 'Regional', 'Local')

    Returns:
        DataFrame con la variable es_feriado agregada
    """
    df = df.copy()
    holidays = holidays.copy()
    holidays['date'] = pd.to_datetime(holidays['date'])

    feriados = holidays[holidays['locale'] == locale]['date'].unique()
    df['es_feriado'] = df[col_fecha].isin(feriados).astype(int)

    total = df['es_feriado'].sum()
    print(f"Variable es_feriado agregada ✅ — Registros con feriado: {total}")
    return df


def pipeline_features(df: pd.DataFrame,
                      oil: pd.DataFrame,
                      holidays: pd.DataFrame) -> pd.DataFrame:
    """
    Pipeline completo de feature engineering.

    Aplica todas las transformaciones en el orden correcto:
    1. Variables temporales
    2. Lags
    3. Rolling
    4. Precio del petróleo
    5. Feriados

    Args:
        df: DataFrame principal de ventas
        oil: DataFrame con precio del petróleo
        holidays: DataFrame con feriados

    Returns:
        DataFrame con todos los features agregados
    """
    print("=== PIPELINE DE FEATURES ===")
    df = agregar_features_temporales(df)
    df = agregar_lags(df)
    df = agregar_rolling(df)
    df = agregar_precio_petroleo(df, oil)
    df = agregar_feriados(df, holidays)
    print(f"\nShape final: {df.shape}")
    print("Pipeline completado ✅")
    return df
