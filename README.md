#Store Sales — Demand Forecasting

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas)
![XGBoost](https://img.shields.io/badge/XGBoost-1.7-orange)
![Prophet](https://img.shields.io/badge/Prophet-1.1-blue)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

---

## 🇦🇷 Español

### ¿De qué trata este proyecto?

Proyecto end-to-end de forecasting de demanda para una cadena de supermercados
con 54 tiendas y 33 familias de productos. Se desarrollaron y compararon tres
modelos de predicción (SARIMA, Prophet y XGBoost) sobre datos reales de ventas
de 4.6 años.

> **Problema de negocio:** Un forecast incorrecto genera overstock (capital inmovilizado,
> productos vencidos) o stockout (ventas perdidas, daño de marca). En empresas de consumo
> masivo, un error del 10% puede representar millones de dólares en pérdidas operativas.

---

### 📊 Resultados

| Modelo | MAE | RMSE | MAPE |
|--------|-----|------|------|
| SARIMA | 332.34 | 472.63 | 17.27% |
| XGBoost | 303.79 | 416.00 | 13.03% |
| **Prophet** ✅ | **298.34** | **377.47** | **13.15%** |

**Modelo recomendado: Prophet**
Prophet supera a XGBoost en MAE y RMSE con diferencias significativas (+5 y +38 unidades),
mientras que la diferencia en MAPE es de apenas 0.12% — irrelevante para el negocio.
Un RMSE más bajo significa menos errores grandes, lo cual es crítico para minimizar
costos de overstock y stockout.

### 🏆 Kaggle Submission

Submission oficial a la competencia [Store Sales - Time Series Forecasting](https://www.kaggle.com/competitions/store-sales-time-series-forecasting):

| Métrica | Score |
|---|---|
| **RMSLE** | ⏳ pendiente |

📓 [Ver notebook de submission](notebooks/07_kaggle_submission_prophet.ipynb)
---

### 🔍 Hallazgos Clave del EDA

- Tendencia de ventas creciente del 150% en 4.6 años
- Patrón semanal fuerte — domingo es el día pico, jueves el mínimo
- Diciembre es el mes de mayor venta, febrero el más bajo
- GROCERY I concentra el mayor volumen (regla 80/20)
- Caída macroeconómica 2014-2015 visible en los datos (precio del petróleo)

---

### 🧠 Features más importantes (XGBoost)

| Feature | Importancia |
|---------|-------------|
| `dia_semana` | 23% |
| `es_fin_de_semana` | 15% |
| `es_feriado` | 14% |
| `onpromotion` | 9% |
| `rolling_7` | 6% |

---

### 📁 Estructura del Proyecto

```
store-sales-forecasting/
│
├── data/
│   ├── raw/              ← datos originales de Kaggle (no versionados)
│   └── processed/        ← datos limpios con features
│
├── notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_modeling_sarima.ipynb
│   ├── 04_modeling_prophet.ipynb
│   ├── 05_modeling_xgboost.ipynb
│   └── 06_evaluation.ipynb
│
├── reports/
│   └── figures/          ← gráficos exportados
│
├── src/                  ← funciones reutilizables
├── ADR.md                ← decisiones técnicas documentadas
├── requirements.txt
└── README.md
```

---

### ⚙️ Cómo reproducir el proyecto

**1. Clonar el repositorio**
```bash
git clone https://github.com/TU_USUARIO/store-sales-forecasting.git
cd store-sales-forecasting
```

**2. Crear y activar el entorno virtual**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Instalar dependencias**
```bash
pip install -r requirements.txt
```

**4. Descargar el dataset**

Los datos provienen de la competencia
[Store Sales — Time Series Forecasting](https://www.kaggle.com/competitions/store-sales-time-series-forecasting/data)
de Kaggle. Descargá los siguientes archivos y guardalos en `data/raw/`:
- `train.csv`
- `stores.csv`
- `oil.csv`
- `holidays_events.csv`

**5. Ejecutar los notebooks en orden**

Abrí VS Code, seleccioná el kernel `Python (store-sales)` y ejecutá los
notebooks en orden del 01 al 06.

---

### 🏗️ Decisiones Técnicas

Este proyecto incluye un documento de **Architecture Decision Records (ADR)**
con 19 decisiones documentadas — desde la elección del dataset hasta la
selección del modelo ganador, incluyendo los trade-offs aceptados en cada etapa.

📄 [Ver ADR completo](./ADR.md)

---

### 🚀 Mejoras Futuras

- [ ] Optimizar hiperparámetros con Optuna
- [ ] Escalar el pipeline a todas las combinaciones tienda-familia
- [ ] Implementar MLflow para tracking de experimentos
- [ ] Agregar modelos de Deep Learning (LSTM, N-BEATS)
- [ ] Crear dashboard interactivo con Streamlit
- [ ] Dockerizar el entorno

---

### 🛠️ Tecnologías

- **Lenguaje:** Python 3.12
- **Manipulación de datos:** Pandas, NumPy
- **Visualización:** Matplotlib, Seaborn
- **Modelos:** Statsmodels (SARIMA), Prophet, XGBoost
- **Entorno:** Jupyter Notebooks, VS Code
- **Control de versiones:** Git + GitHub

---
---

## 🇺🇸 English

### What is this project about?

End-to-end demand forecasting project for a supermarket chain with 54 stores
and 33 product families. Three prediction models (SARIMA, Prophet and XGBoost)
were developed and compared using 4.6 years of real sales data.

> **Business problem:** An incorrect forecast leads to overstock (tied-up capital,
> expired products) or stockout (lost sales, brand damage). In FMCG companies,
> a 10% forecasting error can represent millions of dollars in operational losses.

---

### 📊 Results

| Model | MAE | RMSE | MAPE |
|-------|-----|------|------|
| SARIMA | 332.34 | 472.63 | 17.27% |
| XGBoost | 303.79 | 416.00 | 13.03% |
| **Prophet** ✅ | **298.34** | **377.47** | **13.15%** |

**Recommended model: Prophet**
Prophet outperforms XGBoost in both MAE and RMSE by significant margins (+5 and +38 units),
while the MAPE difference is only 0.12% — negligible from a business perspective.
A lower RMSE means fewer large errors, which is critical for minimizing overstock
and stockout costs.

### 🏆 Kaggle Submission

Official submission to the [Store Sales - Time Series Forecasting](https://www.kaggle.com/competitions/store-sales-time-series-forecasting) competition:

| Metric | Score |
|---|---|
| **RMSLE** | ⏳ pending |

📓 [View submission notebook](notebooks/07_kaggle_submission_prophet.ipynb)
---

### ⚙️ How to reproduce

```bash
git clone https://github.com/TU_USUARIO/store-sales-forecasting.git
cd store-sales-forecasting
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

Download the dataset from
[Kaggle](https://www.kaggle.com/competitions/store-sales-time-series-forecasting/data)
and place the files in `data/raw/`. Then run the notebooks in order from 01 to 06.

---

### 🏗️ Technical Decisions

This project includes an **Architecture Decision Records (ADR)** document
with 19 documented decisions — from dataset selection to model choice,
including trade-offs accepted at each stage.

📄 [View full ADR](./ADR.md)

---

*Dataset: [Store Sales — Time Series Forecasting](https://www.kaggle.com/competitions/store-sales-time-series-forecasting) — Kaggle*
