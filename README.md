# ChildConicity

[![Python Tests](https://github.com/TU_USUARIO/ChildConicity/actions/workflows/python-tests.yml/badge.svg)](https://github.com/TU_USUARIO/ChildConicity/actions/workflows/python-tests.yml)

## Ejecución de Pruebas

### Ejecución Local

Para ejecutar las pruebas y generar el informe de cobertura localmente:

1. Asegúrate de tener todas las dependencias instaladas:
   ```bash
   pip install -r requirements.txt
   ```

2. Ejecuta el script de pruebas:
   ```bash
   ./run_tests.sh
   ```

El script:
- Ejecutará todas las pruebas
- Generará un informe de cobertura HTML
- Verificará que la cobertura sea mayor al 80%
- Guardará el informe en el directorio `coverage_report/`

Para ver el informe de cobertura, abre el archivo `coverage_report/htmlcov/index.html` en tu navegador.

### Pipeline de GitHub Actions

La cobertura de código se genera automáticamente en cada ejecución del pipeline. Puedes encontrar el informe detallado en los artefactos de la última ejecución de GitHub Actions.

Para ver el informe de cobertura:
1. Ve a la pestaña "Actions" en GitHub
2. Selecciona la última ejecución exitosa
3. Descarga el artefacto "coverage-report"
4. Abre el archivo `htmlcov/index.html` en tu navegador