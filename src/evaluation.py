"""
evaluation.py
-------------
Funciones reutilizables para evaluar modelos de forecasting.

Métricas implementadas:
- MAE  (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- MAPE (Mean Absolute Percentage Error)
- WAPE (Weighted Absolute Percentage Error)

Uso:
    from src.evaluation import calcular_metricas, comparar_modelos
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def mae(real: np.ndarray, predicho: np.ndarray) -> float:
    """
    Calcula el Error Absoluto Medio (MAE).

    Mide el error promedio en unidades absolutas.
    No penaliza especialmente los errores grandes.

    Args:
        real: valores reales
        predicho: valores predichos

    Returns:
        MAE como float
    """
    return np.mean(np.abs(real - predicho))


def rmse(real: np.ndarray, predicho: np.ndarray) -> float:
    """
    Calcula la Raíz del Error Cuadrático Medio (RMSE).

    Penaliza más los errores grandes que el MAE.
    Útil para detectar si el modelo tiene fallas graves
    en ciertos períodos (picos de demanda, feriados).

    Args:
        real: valores reales
        predicho: valores predichos

    Returns:
        RMSE como float
    """
    return np.sqrt(np.mean((real - predicho) ** 2))


def mape(real: np.ndarray, predicho: np.ndarray) -> float:
    """
    Calcula el Error Porcentual Absoluto Medio (MAPE).

    Expresa el error como porcentaje del valor real.
    Independiente de la escala — permite comparar entre
    productos, tiendas y períodos de distinto volumen.

    Nota: excluye automáticamente los registros donde
    real == 0 para evitar división por cero.

    Args:
        real: valores reales
        predicho: valores predichos

    Returns:
        MAPE como float (en porcentaje)
    """
    mask = real != 0
    return np.mean(np.abs((real[mask] - predicho[mask]) / real[mask])) * 100


def wape(real: np.ndarray, predicho: np.ndarray) -> float:
    """
    Calcula el Error Porcentual Absoluto Ponderado (WAPE).

    Variante del MAPE que pondera por volumen de ventas.
    Evita que productos de bajo volumen distorsionen
    la métrica global.

    Args:
        real: valores reales
        predicho: valores predichos

    Returns:
        WAPE como float (en porcentaje)
    """
    return np.sum(np.abs(real - predicho)) / np.sum(np.abs(real)) * 100


def calcular_metricas(real: np.ndarray, predicho: np.ndarray,
                      nombre_modelo: str = "Modelo") -> dict:
    """
    Calcula todas las métricas de evaluación para un modelo.

    Args:
        real: valores reales
        predicho: valores predichos
        nombre_modelo: nombre del modelo para el reporte

    Returns:
        Diccionario con todas las métricas
    """
    metricas = {
        "Modelo": nombre_modelo,
        "MAE":    round(mae(real, predicho), 2),
        "RMSE":   round(rmse(real, predicho), 2),
        "MAPE":   round(mape(real, predicho), 2),
        "WAPE":   round(wape(real, predicho), 2)
    }

    print(f"\n=== MÉTRICAS — {nombre_modelo} ===")
    for k, v in metricas.items():
        if k != "Modelo":
            unidad = "%" if k in ["MAPE", "WAPE"] else ""
            print(f"{k:>6}: {v}{unidad}")

    return metricas


def comparar_modelos(lista_metricas: list) -> pd.DataFrame:
    """
    Genera una tabla comparativa de múltiples modelos.

    Args:
        lista_metricas: lista de diccionarios retornados por calcular_metricas()

    Returns:
        DataFrame con la comparativa ordenada por MAPE
    """
    df = pd.DataFrame(lista_metricas)
    df = df.sort_values("MAPE").reset_index(drop=True)

    print("\n=== COMPARATIVA DE MODELOS ===")
    print(df.to_string(index=False))

    return df


def graficar_prediccion(fechas, real: np.ndarray, predicho: np.ndarray,
                        nombre_modelo: str, guardar_en: str = None):
    """
    Grafica la predicción vs los valores reales.

    Args:
        fechas: índice de fechas
        real: valores reales
        predicho: valores predichos
        nombre_modelo: nombre del modelo para el título
        guardar_en: ruta donde guardar el gráfico (opcional)
    """
    plt.figure(figsize=(14, 5))
    plt.plot(fechas, real, color='orange', linewidth=1.5, label='Real')
    plt.plot(fechas, predicho, color='steelblue', linewidth=1.5,
             linestyle='--', label=f'Predicción {nombre_modelo}')
    plt.title(f'{nombre_modelo} — Predicción vs Real',
              fontsize=14, fontweight='bold')
    plt.legend()
    plt.tight_layout()

    if guardar_en:
        plt.savefig(guardar_en, dpi=150)
        print(f"Gráfico guardado en {guardar_en} ✅")

    plt.show()
