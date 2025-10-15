#!/bin/bash

echo "=========================================="
echo "   ElasticSearch Demo - Setup Script"
echo "=========================================="
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

# Verificar Docker
print_info "Verificando Docker..."
if ! command -v docker &> /dev/null; then
    print_error "Docker no está instalado. Por favor instala Docker primero."
    exit 1
fi
print_success "Docker encontrado"

# Verificar Docker Compose
print_info "Verificando Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose no está instalado. Por favor instala Docker Compose primero."
    exit 1
fi
print_success "Docker Compose encontrado"

# Verificar Python
print_info "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 no está instalado. Por favor instala Python 3 primero."
    exit 1
fi
print_success "Python 3 encontrado"

echo ""
echo "=========================================="
echo "   Paso 1: Instalar dependencias Python"
echo "=========================================="
echo ""

pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    print_success "Dependencias de Python instaladas"
else
    print_error "Error al instalar dependencias de Python"
    exit 1
fi

echo ""
echo "=========================================="
echo "   Paso 2: Iniciar servicios Docker"
echo "=========================================="
echo ""

docker-compose up -d
if [ $? -eq 0 ]; then
    print_success "Servicios Docker iniciados"
else
    print_error "Error al iniciar servicios Docker"
    exit 1
fi

echo ""
print_info "Esperando a que los servicios estén listos (60 segundos)..."
sleep 60

echo ""
echo "=========================================="
echo "   Paso 3: Generar datos de ejemplo"
echo "=========================================="
echo ""

python3 generate_data.py
if [ $? -eq 0 ]; then
    print_success "Datos de ejemplo generados"
else
    print_error "Error al generar datos"
    exit 1
fi

echo ""
echo "=========================================="
echo "   Paso 4: Cargar datos en ElasticSearch"
echo "=========================================="
echo ""

python3 load_elasticsearch.py
if [ $? -eq 0 ]; then
    print_success "Datos cargados en ElasticSearch"
else
    print_error "Error al cargar datos en ElasticSearch"
    exit 1
fi

echo ""
echo "=========================================="
echo "   Paso 5: Cargar datos en PostgreSQL"
echo "=========================================="
echo ""

python3 load_postgresql.py
if [ $? -eq 0 ]; then
    print_success "Datos cargados en PostgreSQL"
else
    print_error "Error al cargar datos en PostgreSQL"
    exit 1
fi

echo ""
echo "=========================================="
echo "   ✓ Setup Completado Exitosamente"
echo "=========================================="
echo ""
echo "Servicios disponibles:"
echo ""
echo "  📊 ElasticSearch: http://localhost:9200"
echo "  📈 Kibana:        http://localhost:5601"
echo "  🐘 PostgreSQL:    localhost:5432"
echo "  🔧 PgAdmin:       http://localhost:5050"
echo ""
echo "Credenciales de PgAdmin:"
echo "  Email:    admin@admin.com"
echo "  Password: admin123"
echo ""
echo "Para ejecutar la comparación de búsquedas:"
echo "  python3 search_comparison.py"
echo ""
echo "Para detener los servicios:"
echo "  docker-compose down"
echo ""
