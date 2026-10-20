
---
name: Physiological system identification notebooks
description: Reglas para analizar notebooks científicos de identificación no paramétrica.
applyTo: "**/*.ipynb"
---

# Análisis de notebooks científicos

- Lee el código y las celdas Markdown relacionadas antes de modificar una celda.
- Mantén la continuidad entre las variables creadas en celdas anteriores.
- Comprueba si las variables se sobrescriben o si dependen del orden de ejecución.
- Distingue las variables de identificación, validación y visualización.
- Verifica que las señales comparadas correspondan al mismo intervalo temporal.
- Comprueba las dimensiones de las convoluciones y el truncamiento de sus resultados.
- No supongas que dos vectores están alineados por tener la misma longitud.
- Comprueba las unidades de las señales y los factores de escalado.
- Si corriges una función matemática, revisa también las celdas que la llaman.
- No elimines gráficos ni resultados intermedios que permitan interpretar el método.
- Conserva las explicaciones necesarias para el informe académico.
- Separa las modificaciones de código de las conclusiones científicas.
- No inventes resultados numéricos: ejecútalos únicamente si los datos y el entorno están disponibles.
