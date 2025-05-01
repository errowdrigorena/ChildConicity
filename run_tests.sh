#!/bin/bash

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🚀 Ejecutando pruebas y generando informe de cobertura..."

# Crear directorio para el informe si no existe
mkdir -p coverage_report

# Ejecutar pruebas con cobertura, excluyendo examples/
python3 -m pytest test/ -v --cov=src --cov-report=html --cov-report=term-missing --cov-config=.coveragerc

# Verificar si las pruebas pasaron
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Todas las pruebas pasaron correctamente${NC}"
    
    # Verificar el umbral de cobertura
    python3 -m pytest test/ --cov=src --cov-fail-under=80 --cov-config=.coveragerc
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ La cobertura de código es mayor al 80%${NC}"
    else
        echo -e "${RED}❌ La cobertura de código es menor al 80%${NC}"
    fi
    
    # Mover el informe de cobertura al directorio coverage_report
    mv htmlcov coverage_report/
    mv .coverage* coverage_report/ 2>/dev/null || true
    
    echo -e "\n📊 Para ver el informe de cobertura, abre:"
    echo -e "${GREEN}file://$(pwd)/coverage_report/htmlcov/index.html${NC}"
else
    echo -e "${RED}❌ Algunas pruebas fallaron${NC}"
    exit 1
fi 