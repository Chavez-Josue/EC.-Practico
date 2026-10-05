# Informe de Aplicación al Caso de Big Data

## 5. Las 5 V aplicadas al proyecto

| V de Big Data | Relación con el sistema de sensores | Ejemplo concreto | Tipo de origen |
| :--- | :--- | :--- | :--- |
| **Volumen** | Se refiere a la cantidad masiva de datos generados. Al escalar a miles de sensores midiendo cada segundo, la cantidad de datos almacenados crece a Terabytes o Petabytes por año. | El archivo actual contiene 100,000 registros, pero la ampliación futura generará aproximadamente 432 millones de registros diarios al monitorear miles de sensores por segundo. | Corresponde a la futura ampliación del sistema. |
| **Velocidad** | Es la rapidez con la que se reciben, procesan y analizan las lecturas para reaccionar ante anomalías a tiempo. | Recepción de lecturas cada segundo para emitir alertas automáticas en milisegundos cuando la temperatura supere los 85 °C. | Corresponde a la futura ampliación del sistema. |
| **Variedad** | Se refiere a la diversidad de tipos y formatos de datos generados por el sistema (estructurados, no estructurados y semiestructurados). | La adición de fotografías mecánicas/térmicas de las máquinas y reportes de mantenimiento en texto libre junto a las mediciones. | Corresponde a la futura ampliación del sistema. |
| **Veracidad** | Es la certidumbre o precisión de los datos recopilados por los sensores, considerando ruido o descalibración. | Lecturas anómalas o atípicas causadas por fallas en la transmisión o sensores defectuosos en la planta. | Aparece en el CSV actual (y en la futura ampliación). |
| **Valor** | Es el beneficio de negocio obtenido al transformar los datos en decisiones operativas estratégicas. | Identificar que Planta_3 concentró la mayor cantidad de alertas para priorizar mantenimiento preventivo y evitar paros no programados. | Aparece en el CSV actual (y en la futura ampliación). |

---

## 6. Tipos de datos y procesamiento tradicional

### Clasificación de elementos:
* **El CSV de sensores:** Estructurado (datos numéricos y de texto organizados en filas y columnas fijas).
* **Un mensaje JSON enviado por un sensor:** Semiestructurado (contiene etiquetas y claves para organizar los datos sin un esquema rígido de tabla).
* **Una fotografía de una máquina:** No estructurado (archivo binario de imagen sin estructura tabular).
* **El texto libre de un reporte de mantenimiento:** No estructurado (texto continuo en lenguaje natural sin formato predefinido).

### Por qué 100,000 registros no convierten automáticamente al archivo en Big Data:
Un archivo de 100,000 registros ocupa alrededor de 4.4 MiB. Esto cabe cómodamente en la memoria RAM de cualquier computadora personal y puede ser procesado en menos de un segundo con scripts convencionales de Python. Big Data se define cuando el volumen, velocidad o variedad supera la capacidad de procesamiento de una sola máquina y herramientas tradicionales.

### Limitaciones al aumentar la escala:
1. Saturación de Memoria RAM: Cargar archivos de gigabytes o terabytes simultáneamente provocará errores de falta de memoria (Out of Memory).
2. Cuellos de botella en Disco (I/O): La lectura y escritura continuas en almacenamiento local tradicional ralentizan significativamente el sistema.
3. Procesamiento Monolítico: La ejecución en un solo hilo de CPU no puede procesar millones de eventos por segundo en tiempo real.

---

## 7. Batch y Streaming

1. Tipo de procesamiento realizado: Batch (Por lotes).
   - Justificación: Se analizó un conjunto de datos estático (archivo CSV) recopilado y guardado previamente en su totalidad.
2. Enfoque para alerta en pocos segundos (> 85 °C): Streaming (Tiempo real).
   - Justificación: Permite evaluar cada evento en el momento exacto en que se genera, emitiendo alertas inmediatas con latencia de milisegundos para evitar daños en la maquinaria.
3. Enfoque para generar un resumen al terminar el día: Batch (Por lotes).
   - Justificación: Es un cálculo consolidado y periódico sobre el acumulado del día, donde la latencia de procesamiento no es crítica.

---

## 8. Arquitecturas Lambda y Kappa

### Escenario A:
* Arquitectura elegida: Arquitectura Lambda.
* Justificación: Esta arquitectura combina dos capas independientes: una capa por lotes (Batch Layer) para recalcular y reprocesar el historial completo con precisión, y una capa rápida (Speed Layer) para procesar las mediciones recientes con baja latencia.

Diagrama Escenario A:
[ Sensores ] ---> ( Batch Layer / Lotes ) ---------> [ Serving Layer ]
             ---> ( Speed Layer / Tiempo Real ) ----> [ Serving Layer ]

### Escenario B:
* Arquitectura elegida: Arquitectura Kappa.
* Justificación: Elimina la capa de lotes y utiliza una única canalización de procesamiento de transmisiones (Stream Processing) sobre un registro inmutable (como Kafka), lo que permite volver a procesar datos históricos simplemente reproduciendo el flujo de eventos nuevamente.

Diagrama Escenario B:
[ Sensores ] ---> [ Stream Ingestion (Kafka) ] ---> [ Stream Processor ] ---> [ Serving Layer ]

---

## 9. Analítica descriptiva, predictiva y prescriptiva

* Descriptiva:
  - Hallazgo 1: El sistema registró un total de 100,000 mediciones provenientes de 40 sensores distintos entre las 4 plantas.
  - Hallazgo 2: Se detectó una temperatura máxima de 104.99 °C en 4 registros empatados (sensores S023, S019, S014 y S030), y Planta_3 fue la instalación con mayor cantidad de alertas (> 85 °C) acumulando 1,777 registros.

* Predictiva:
  - Pregunta: ¿Existe un patrón en el nivel de vibración de los sensores que anticipe un pico de temperatura crítica antes de que la máquina sufra un sobrecalentamiento?
  - Datos adicionales necesarios: Historial técnico de fallas, registros de reemplazo de piezas, horas continuas de operación y especificaciones de tolerancia de los fabricantes.

* Prescriptiva:
  - Acción propuesta: Si un sensor registra vibraciones superiores a la norma combinadas con temperaturas en ascenso constante durante más de 10 minutos, reducir la carga de operación de la máquina automáticamente y programar una revisión técnica.
  - Información a revisar antes de decidir: Disponibilidad de técnicos en turno, estatus del inventario de repuestos y programas de producción vigentes de la planta.