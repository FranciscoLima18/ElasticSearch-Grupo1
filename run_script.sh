#!/bin/bash

# Script simple para ejecutar cargar_datos.py con el entorno virtual
# =================================================================

echo "🚀 Ejecutando script de carga de datos..."

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Error: Entorno virtual no encontrado. Ejecuta primero:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activar entorno virtual y ejecutar script
source venv/bin/activate
python3 cargar_datos.py

echo ""
echo "✅ Script completado. Revisa la salida arriba para ver los resultados."