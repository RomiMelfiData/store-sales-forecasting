# Registro de Decisiones de Arquitectura (ADR)
## Proyecto: Sales Demand Forecasting — End-to-End
**Autor:** Marcela Romina Melfi
**Fecha:** Marzo 2026
**Estado:** Terminado

---

## Contexto del Proyecto

Este proyecto aborda el problema de forecasting de demanda en un entorno de retail multi-tienda.
El objetivo es predecir las ventas futuras por familia de productos para optimizar la toma de decisiones
operativas y financieras.

---

## ADR-001: Elección del Problema de Negocio

**Decisión:** Trabajar sobre forecasting de demanda y no sobre otro problema de ML.

**Razonamiento:**
El forecasting de demanda es uno de los problemas más críticos y frecuentes en empresas de consumo
masivo y retail. Un forecast incorrecto genera dos tipos de consecuencias directas:

- **Overstock:** se produce o compra más de lo necesario → capital inmovilizado, costos de
  almacenamiento, riesgo de vencimiento de productos.
- **Stockout:** se produce o compra menos de lo necesario → ventas perdidas, clientes insatisfechos,
  daño de marca.

Adicionalmente, un mal forecast afecta la planificación financiera: sin una estimación confiable
de ventas, no es posible presupuestar costos, personal ni logística correctamente.

En empresas como Quilmes (AB InBev) o Carrefour, un error del 10% en el forecast puede
representar millones de dólares en pérdidas operativas.

**Trade-off aceptado:**
Es un problema complejo que requiere conocimiento del dominio (estacionalidad, feriados, eventos).
Se priorizó la complejidad del problema por sobre la simplicidad, porque el aprendizaje obtenido
es directamente aplicable a roles de Data Science en consumo masivo.

---

## ADR-002: Elección del Dataset

**Decisión:** Usar "Store Sales — Time Series Forecasting" de Kaggle (Corporación Favorita, Ecuador).

**Razonamiento:**
- Contiene datos reales de una cadena de supermercados (1.800+ tiendas, 33 familias de productos).
- Incluye variables externas relevantes: precio del petróleo, feriados nacionales y locales,
  eventos especiales — lo que permite demostrar feature engineering avanzado.
- Es un dataset utilizado en competencias activas de Kaggle, lo que permite contrastar resultados
  con soluciones de la comunidad.

**Trade-off aceptado:**
El contexto es Ecuador, no Argentina. Los patrones de consumo y feriados son distintos.
Se decidió priorizar la riqueza del dataset por sobre la contextualización local,
documentando esta limitación explícitamente en el README.

---

## ADR-003: Elección de los Modelos

**Decisión:** Comparar tres enfoques: SARIMA, Prophet y XGBoost.

**Razonamiento:**
Cada modelo captura una dimensión diferente del problema:

| Modelo   | Fortaleza principal                                      | Limitación conocida                          |
|----------|----------------------------------------------------------|----------------------------------------------|
| SARIMA   | Captura patrones estadísticos puros y estacionalidad fija | No incorpora variables externas fácilmente  |
| Prophet  | Maneja múltiples estacionalidades, feriados y cambios de tendencia | Menor control sobre el proceso de modelado |
| XGBoost  | Aprende relaciones no lineales e incorpora variables externas | No comprende el orden temporal nativamente  |

Usar los tres modelos permite demostrar que se entiende **cuándo aplicar cada herramienta**,
en lugar de aplicar siempre el mismo enfoque. Esta es una habilidad crítica en entornos
productivos donde los datos y el contexto cambian.

**Trade-off aceptado:**
Tres modelos implica mayor tiempo de desarrollo y complejidad de mantenimiento.
En un entorno productivo real, se elegiría un único modelo ganador. En este proyecto,
la comparación es intencional con fines de aprendizaje y demostración técnica.

---

## ADR-004: Elección de Métricas de Evaluación

**Decisión:** Usar MAPE, WAPE y RMSE como métricas principales. No usar MAE como métrica única.

**Razonamiento:**

- **MAE (Mean Absolute Error):** mide el error en unidades absolutas. Su problema es que depende
  de la escala: un error de 500 unidades es enorme para un producto que vende 1.000/mes,
  pero irrelevante para uno que vende 1.000.000/mes. No es comparable entre productos distintos.

- **MAPE (Mean Absolute Percentage Error):** expresa el error como porcentaje.
  Es independiente de la escala, lo que permite comparar la performance entre distintas tiendas,
  productos y períodos de tiempo. Es la métrica más usada en contextos de negocio porque
  los stakeholders pueden interpretarla directamente ("nos equivocamos un 8%").

- **WAPE (Weighted Absolute Percentage Error):** variante del MAPE que pondera el error
  por el volumen de ventas. Evita que productos de bajo volumen (con errores porcentuales
  naturalmente altos) distorsionen la métrica global.

- **RMSE (Root Mean Squared Error):** penaliza más los errores grandes. Útil para detectar
  si el modelo tiene fallas graves en ciertos períodos (picos de demanda, feriados).

**Trade-off aceptado:**
El MAPE tiene un problema conocido: es indefinido cuando las ventas reales son 0
(división por cero). Se documentará este caso y se aplicará un tratamiento específico
(exclusión o uso de SMAPE como alternativa) cuando corresponda.

---

## ADR-005: Estructura del Proyecto

**Decisión:** Separar notebooks de exploración del código fuente reutilizable (src/).

**Razonamiento:**
Los notebooks son ideales para exploración y comunicación de resultados, pero no para
producción: son difíciles de testear, versionar y reutilizar. Se adoptó la siguiente separación:

- `notebooks/` → exploración, visualizaciones, narrativa del análisis
- `src/` → funciones reutilizables de procesamiento, features y evaluación

Esta estructura refleja buenas prácticas de ingeniería de software aplicadas a Data Science,
alineadas con estándares de equipos como el de Mercado Libre o PwC.

**Trade-off aceptado:**
Para un proyecto de portfolio, esta separación puede parecer sobreingeniería.
Se mantiene conscientemente para demostrar conocimiento de buenas prácticas,
documentando que en un proyecto real de mayor escala se agregaría testing unitario (pytest).

---

## ADR-006: Entorno Virtual (venv)

**Decisión:** Usar entorno virtual de Python (`venv`) en lugar de instalar librerías globalmente.

**Razonamiento:**
Distintos proyectos pueden requerir versiones distintas de la misma librería. Sin un entorno
virtual, estas versiones colisionan y generan errores difíciles de diagnosticar. Con `venv`:

- Cada proyecto tiene sus propias librerías aisladas del sistema.
- El archivo `requirements.txt` captura las versiones exactas usadas.
- Cualquier persona que clone el repo puede reproducir el entorno ejecutando
  `pip install -r requirements.txt`, garantizando que el proyecto funciona igual
  en cualquier computadora.

**Contexto adicional:**
Durante el setup se identificó que Windows bloquea por defecto la ejecución de scripts `.ps1`
de PowerShell por razones de seguridad. Se resolvió cambiando la terminal a Command Prompt (CMD),
que no tiene esta restricción. Esta decisión evita modificar políticas de seguridad del sistema.

**Trade-off aceptado:**
El entorno virtual debe activarse manualmente en cada sesión de trabajo (`venv\Scripts\activate`).
Es un paso adicional, pero se prioriza la reproducibilidad y el aislamiento por sobre la comodidad.

---

## ADR-007: Carpetas Vacías en Git

**Decisión:** No forzar el tracking de carpetas vacías con archivos `.gitkeep`.

**Razonamiento:**
Git no versiona carpetas vacías por diseño — solo trackea archivos. Existen dos enfoques:

1. Agregar un archivo `.gitkeep` en cada carpeta vacía para forzar su aparición en GitHub.
2. Dejar que las carpetas aparezcan naturalmente cuando se agregue contenido en cada fase.

Se eligió la opción 2 porque:
- Las carpetas van a poblarse con contenido real en cada fase del proyecto.
- Agregar archivos artificiales solo para satisfacer una limitación de Git agrega ruido
  al repositorio sin aportar valor real.

**Trade-off aceptado:**
El repositorio no muestra la estructura completa de carpetas hasta que cada fase esté iniciada.
Se documenta la estructura completa en el README para que sea visible desde el primer día.

---

## ADR-008: Conversión de la columna `date` a datetime

**Decisión:** Convertir la columna `date` de tipo string a datetime con `pd.to_datetime()`.

**Razonamiento:**
Al inspeccionar el dataset se detectó que la columna `date` estaba almacenada como string.
Para trabajar con series temporales es imprescindible que Python reconozca la columna como
fecha real, ya que permite:
- Ordenar cronológicamente los registros
- Extraer componentes temporales (día de semana, mes, año)
- Calcular diferencias entre fechas
- Resamplear la serie a distintas frecuencias

Sin esta conversión, ninguna operación temporal sería posible.

**Trade-off aceptado:**
Ninguno — es una corrección obligatoria sin alternativa válida.

---

## ADR-009: Tratamiento de valores nulos en el precio del petróleo

**Decisión:** Interpolar linealmente los 43 valores nulos en la columna `dcoilwtico`.

**Razonamiento:**
Los 43 valores nulos corresponden a fines de semana y feriados, días en que los mercados
financieros no operan y por lo tanto no registran precio. Se evaluaron tres opciones:

- **Eliminar filas:** no resuelve el problema porque al hacer el merge con `train`,
  los días de fin de semana seguirían sin precio de petróleo. Solo elimina filas
  que técnicamente no existían.
- **Rellenar con el promedio global:** introduce un valor artificial que no respeta
  la continuidad temporal del precio. Un promedio de 4 años no representa
  el precio de un día específico.
- **Interpolación lineal:** estima el valor faltante basándose en los días
  anteriores y posteriores. Es la solución estándar en series temporales financieras
  porque el precio del petróleo tiene continuidad temporal — no cambia abruptamente
  entre un viernes y un lunes.

Se eligió interpolación porque respeta la naturaleza continua de los datos financieros
y es la práctica más utilizada en proyectos de Data Science con variables macroeconómicas.

**Trade-off aceptado:**
La interpolación asume que el precio varía linealmente entre dos puntos conocidos,
lo cual es una simplificación. En períodos de alta volatilidad podría no ser precisa.
Se acepta esta limitación dado que los nulos son fines de semana — períodos naturalmente
cortos de 1 a 2 días.

---

## ADR-010: Tratamiento de registros con ventas = 0

**Decisión:** Mantener los registros con ventas = 0 en el dataset.

**Razonamiento:**
El 31.3% de los registros tiene ventas igual a cero. Estos registros son legítimos
y representan combinaciones reales de tienda-producto-día donde no hubo ventas por:
- Feriados nacionales donde las tiendas cierran
- Productos no disponibles en determinadas tiendas
- Días de baja demanda para ciertas categorías

Eliminarlos distorsionaría el modelo, ya que le impediría aprender que ciertos días
o productos tienen ventas nulas de forma sistemática. Predecir correctamente un cero
es tan importante como predecir correctamente un valor alto.

**Trade-off aceptado:**
Mantener los ceros puede afectar el cálculo del MAPE (división por cero).
Se documentó en ADR-004 que se aplicará SMAPE como alternativa cuando corresponda.

---

## ADR-011: Inclusión del precio del petróleo como variable externa

**Decisión:** Incluir `dcoilwtico` como variable externa en el modelo XGBoost.

**Razonamiento:**
Ecuador es una economía fuertemente dependiente del petróleo. El análisis temporal
mostró una caída histórica del precio entre 2014 y 2015 (de ~100 USD a ~45 USD),
lo que generó una contracción económica que impactó directamente en el consumo.

Esta variable captura un tipo de variación que los modelos de series temporales puras
(SARIMA, Prophet) no pueden explicar — cambios estructurales en el poder adquisitivo
de la población que no responden a patrones estacionales sino a contexto macroeconómico.

**Trade-off aceptado:**
Esta variable es específica del contexto ecuatoriano. En un proyecto para Argentina
u otro país, habría que evaluar qué variable macroeconómica local tiene mayor
correlación con el consumo (tipo de cambio, inflación, etc.).

---

## Limitaciones Conocidas del Proyecto

1. El dataset corresponde a Ecuador — los patrones culturales y de consumo difieren de Argentina.
2. No se implementa un pipeline de MLOps completo (CI/CD, monitoreo de drift).
   Esto queda fuera del alcance como mejora futura documentada.
3. Los modelos no están desplegados en producción (API/endpoint).
   Se prioriza la calidad del análisis sobre el deployment.

---

## Mejoras Futuras (Backlog)

- [ ] Implementar MLflow para tracking de experimentos
- [ ] Agregar modelos de Deep Learning (LSTM, N-BEATS)
- [ ] Crear un dashboard interactivo con Streamlit
- [ ] Agregar tests unitarios con pytest para las funciones de src/
- [ ] Dockerizar el entorno para reproducibilidad

---

*Este documento se actualiza a medida que el proyecto evoluciona.*
