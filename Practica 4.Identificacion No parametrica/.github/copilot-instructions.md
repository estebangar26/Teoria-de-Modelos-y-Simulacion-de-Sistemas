
# Proyecto: Identificación no paramétrica de sistemas fisiológicos

## 1. Objetivo y contexto
Este proyecto estudia la identificación no paramétrica de sistemas fisiológicos a partir de señales de entrada y salida, utilizando:
- Desconvolución.
- Mínimo error cuadrático (MSE, según la terminología del curso).

El objetivo es estimar una representación del sistema, reconstruir o predecir su salida y comparar las predicciones con las mediciones disponibles.

Prioriza los apuntes, el código de referencia, los enunciados del laboratorio y las convenciones del curso. No sustituyas silenciosamente los métodos estudiados por otros algoritmos.

## 2. Fuentes de referencia
- Consulta los notebooks y documentos relevantes antes de proponer cambios matemáticos.
- Utiliza el código de referencia como evidencia de las convenciones del proyecto, pero comprueba su consistencia matemática.
- Si hay discrepancias entre los apuntes, el enunciado y el código, explica la discrepancia y solicita aclaración cuando afecte al resultado.
- Distingue entre lo establecido por el curso, lo implementado y tus propias recomendaciones.
- No inventes fórmulas ni atribuyas ecuaciones a los documentos sin verificarlas.

## 3. Modelo del sistema
- Identifica claramente la señal de entrada u, la salida medida y, el sistema estimado h y la salida predicha.
- Considera la representación del sistema mediante una respuesta impulsional y su relación con la convolución.
- Comprueba las hipótesis necesarias para aplicar cada método.
- No supongas que el sistema fisiológico es lineal, invariante en el tiempo o libre de ruido sin justificación.
- Distingue la identificación del sistema de la validación de sus predicciones.

## 4. Desconvolución
- Explica qué operación realiza la función utilizada y qué representa su resultado.
- Comprueba el orden de las señales, las longitudes, el relleno con ceros y la alineación temporal.
- Examina los efectos del ruido y la sensibilidad de la estimación.
- Comprueba si la operación implementada corresponde a la desconvolución matemática requerida por el curso.
- No interpretes automáticamente el residuo de una función de software como el error de predicción del sistema.
- Verifica la reconstrucción mediante convolución y especifica qué muestras se comparan.

## 5. Mínimo error cuadrático
- Explica cómo se construye la matriz de regresores a partir de las muestras de entrada.
- Comprueba el orden de los retardos, la causalidad y la alineación con la salida.
- Verifica las dimensiones de la matriz, el vector de salida y el vector de coeficientes.
- Comprueba la función objetivo que se minimiza y la convención de escalado utilizada.
- Examina la singularidad o el mal condicionamiento de la matriz normal.
- Prefiere soluciones numéricamente estables, como numpy.linalg.solve o numpy.linalg.lstsq, cuando sean matemáticamente apropiadas.
- No cambies factores como el periodo de muestreo T sin derivar y justificar la ecuación correspondiente.
- Diferencia los coeficientes estimados de los valores predichos.

## 6. Señales fisiológicas y muestreo
- Comprueba que las señales comparadas tengan unidades y escalas compatibles.
- Verifica el periodo de muestreo y la uniformidad temporal cuando sean relevantes.
- No confundas índices de muestra con tiempo físico.
- Comprueba las longitudes de las señales y la correspondencia entre muestras.
- Considera ruido, deriva, artefactos, valores faltantes y limitaciones de los datos cuando estén presentes.
- No inventes propiedades fisiológicas ni diagnósticos que no se desprendan de los datos.

## 7. Validación y métricas
- Distingue los datos usados para identificar el sistema de los datos usados para validarlo.
- Cuando existan datos adicionales, evalúa la capacidad predictiva fuera de los datos de identificación.
- Calcula las métricas solo después de alinear las señales y verificar sus dimensiones.
- Diferencia MSE, RMSE, error absoluto y error relativo.
- No llames MSE a una métrica diferente.
- Explica las unidades y limitaciones de cada métrica.
- No interpretes un error pequeño en los datos de identificación como prueba suficiente de generalización.

## 8. Calidad del código
- Mantén las variables, nombres y convenciones existentes salvo que haya una razón justificada para cambiarlos.
- Divide los cálculos complejos en funciones verificables.
- Añade validaciones de entradas, dimensiones y parámetros.
- Evita inversiones explícitas de matrices cuando exista una solución numérica más apropiada.
- Utiliza comentarios en español que expliquen las decisiones matemáticas, no comentarios redundantes.
- No cambies simultáneamente el algoritmo, el escalado y la visualización sin explicar cada modificación.

## 9. Protocolo de análisis
Antes de modificar una función:
1. Explica qué intenta calcular.
2. Escribe la ecuación matemática correspondiente.
3. Identifica las dimensiones de las variables.
4. Comprueba el código frente a la ecuación.
5. Señala errores confirmados y posibles problemas.
6. Propón el cambio mínimo necesario.
7. Verifica el resultado con datos de prueba cuando sea posible.

Al terminar, resume qué se modificó, por qué y qué pruebas se ejecutaron. Nunca afirmes haber ejecutado o validado algo que no hayas comprobado.


## 10. Referencia de evaluación: Quiz práctico de identificación no paramétrica

El archivo de referencia es el quiz práctico de identificación no
paramétrica del curso Teoría de Modelos y Simulación de Sistemas.

Usa este quiz como especificación de los objetivos, las variables
esperadas, las comparaciones y los criterios de evaluación.

### Datos y señales
- u: señal de entrada.
- y: señal de salida medida.
- t: vector de tiempo.
- N: longitud o número de muestras definido por el ejercicio.
- dataset1.csv: conjunto de datos cuando esté disponible.

No inventes el contenido del CSV ni supongas valores de N sin
inspeccionar los datos reales.

### Métodos y pruebas
Implementa y compara los dos métodos solicitados:
1. Desconvolución.
2. Mínimo error cuadrático.

El ejercicio considera dos pruebas, cada una con su propio valor
del parámetro p.

Prueba 1:
- p = 0.5*N, 0.3*N o 0.6*N, según la versión asignada.
- h_desc_p1: sistema estimado por desconvolución.
- h_lse_p1: sistema estimado por mínimo error cuadrático.

Prueba 2:
- p = N, 0.8*N o 0.9*N, según la versión asignada.
- h_desc_p2: sistema estimado por desconvolución.
- h_lse_p2: sistema estimado por mínimo error cuadrático.

Comprueba qué versión y qué valores de p corresponden al enunciado
asignado antes de realizar los cálculos. No mezcles versiones.

### Predicción y visualización
- Obtén las salidas predichas con cada sistema identificado.
- Conserva los nombres y las correspondencias entre las variables
  de cada prueba.
- Grafica la salida real y las dos salidas predichas en función de t.
- Incluye títulos, nombres de ejes, leyendas y unidades disponibles.
- Verifica que las señales comparadas estén temporalmente alineadas.

### Evaluación del error
Calcula para cada salida predicha:

MSE = mean((y_real - y_predicha)**2)

Evalúa por separado:
- y_desc_p1 frente a y real.
- y_lse_p1 frente a y real.
- y_desc_p2 frente a y real.
- y_lse_p2 frente a y real.

Organiza los cuatro resultados en una tabla comparativa.

No confundas el MSE con el error relativo ni con el residuo interno
devuelto por una función de desconvolución.

### Selección del mejor método y parámetro
- Compara los errores de los cuatro sistemas identificados.
- Identifica el menor error observado entre los candidatos.
- Justifica la elección utilizando tanto las gráficas como las métricas.
- Distingue el mejor resultado de identificación de la capacidad
  de generalización del modelo.

### Validación con datos adicionales
Propón una validación independiente utilizando nuevas señales
de entrada y salida que no se hayan utilizado para estimar el sistema.

- Aplica los sistemas identificados a las nuevas entradas.
- Compara las salidas predichas con las salidas medidas.
- Calcula las mismas métricas para todos los candidatos.
- Comprueba si se mantiene el método y el parámetro seleccionados.
- No uses los datos de validación para volver a ajustar el modelo
  durante la evaluación final.

### Restricciones
- No inventes datos, resultados, gráficas ni valores de error.
- No afirmes que un método es mejor sin comparar resultados.
- No cambies las fórmulas del curso sin justificarlo.
- Comprueba las dimensiones, los retardos, el escalado y la alineación
  temporal antes de concluir que una predicción es correcta.

