#!/bin/bash

# Script de setup automático para ElasticSearch Grupo 1
# ====================================================

echo "🚀 INICIANDO SETUP DE ELASTICSEARCH - GRUPO 1"
echo "=============================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con colores
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar que Docker esté instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker no está instalado. Por favor instala Docker primero."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose no está instalado. Por favor instala Docker Compose primero."
        exit 1
    fi
    
    print_success "Docker y Docker Compose están instalados"
}

# Verificar que Python esté instalado
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 no está instalado. Por favor instala Python 3 primero."
        exit 1
    fi
    
    print_success "Python 3 está instalado: $(python3 --version)"
}

# Configurar memoria virtual para ElasticSearch
setup_vm_memory() {
    print_status "Configurando memoria virtual para ElasticSearch..."
    
    # Verificar valor actual
    current_value=$(sysctl vm.max_map_count | cut -d' ' -f3)
    required_value=262144
    
    if [ "$current_value" -lt "$required_value" ]; then
        print_warning "Configurando vm.max_map_count a $required_value"
        sudo sysctl -w vm.max_map_count=$required_value
        
        # Hacer el cambio permanente
        if ! grep -q "vm.max_map_count" /etc/sysctl.conf; then
            echo "vm.max_map_count=$required_value" | sudo tee -a /etc/sysctl.conf
        fi
    fi
    
    print_success "Memoria virtual configurada correctamente"
}

# Iniciar servicios Docker
start_services() {
    print_status "Iniciando servicios de ElasticSearch y Kibana..."
    
    # Detener servicios existentes si están ejecutándose
    docker-compose down 2>/dev/null
    
    # Iniciar servicios
    docker-compose up -d
    
    if [ $? -eq 0 ]; then
        print_success "Servicios iniciados correctamente"
    else
        print_error "Error al iniciar los servicios"
        exit 1
    fi
}

# Esperar a que ElasticSearch esté disponible
wait_for_elasticsearch() {
    print_status "Esperando a que ElasticSearch esté disponible..."
    
    max_attempts=30
    attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:9200/_cluster/health >/dev/null 2>&1; then
            print_success "ElasticSearch está disponible"
            return 0
        fi
        
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    print_error "Timeout esperando a ElasticSearch"
    exit 1
}

# Esperar a que Kibana esté disponible
wait_for_kibana() {
    print_status "Esperando a que Kibana esté disponible..."
    
    max_attempts=30
    attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:5601/api/status >/dev/null 2>&1; then
            print_success "Kibana está disponible"
            return 0
        fi
        
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    print_error "Timeout esperando a Kibana"
    exit 1
}

# Configurar entorno Python
setup_python_env() {
    print_status "Configurando entorno Python..."
    
    # Verificar si python3-venv está instalado
    if ! dpkg -l | grep -q python3.*-venv; then
        print_warning "Instalando python3-venv..."
        sudo apt update && sudo apt install -y python3-venv python3-pip
    fi
    
    # Crear entorno virtual si no existe
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Entorno virtual creado"
    fi
    
    # Activar entorno virtual e instalar dependencias
    source venv/bin/activate
    pip install -q -r requirements.txt
    
    if [ $? -eq 0 ]; then
        print_success "Dependencias Python instaladas"
    else
        print_error "Error al instalar dependencias Python"
        exit 1
    fi
}

# Cargar datos de ejemplo
load_sample_data() {
    print_status "Cargando datos de ejemplo..."
    
    source venv/bin/activate
    python3 cargar_datos.py
    
    if [ $? -eq 0 ]; then
        print_success "Datos cargados exitosamente"
    else
        print_error "Error al cargar datos"
        exit 1
    fi
}

# Mostrar información de acceso
show_access_info() {
    echo ""
    echo "🎉 ¡SETUP COMPLETADO EXITOSAMENTE!"
    echo "================================="
    echo ""
    echo "📊 SERVICIOS DISPONIBLES:"
    echo "   • ElasticSearch API: http://localhost:9200"
    echo "   • Kibana Dashboard:   http://localhost:5601"
    echo ""
    echo "🔍 PRUEBAS RÁPIDAS:"
    echo "   • Estado del cluster: curl http://localhost:9200/_cluster/health?pretty"
    echo "   • Ver productos:      curl http://localhost:9200/productos/_search?pretty&size=5"
    echo ""
    echo "📖 DOCUMENTACIÓN:"
    echo "   • README.md: Documentación completa"
    echo "   • consultas_ejemplo.md: Ejemplos de consultas"
    echo ""
    echo "🐳 COMANDOS DOCKER:"
    echo "   • Ver logs:     docker-compose logs -f"
    echo "   • Detener:      docker-compose down"
    echo "   • Reiniciar:    docker-compose restart"
    echo ""
}

# Función principal
main() {
    echo ""
    print_status "Verificando prerrequisitos..."
    check_docker
    check_python
    
    print_status "Configurando sistema..."
    setup_vm_memory
    
    print_status "Iniciando servicios..."
    start_services
    
    print_status "Esperando servicios..."
    wait_for_elasticsearch
    wait_for_kibana
    
    print_status "Configurando Python..."
    setup_python_env
    
    print_status "Cargando datos..."
    load_sample_data
    
    show_access_info
}

# Ejecutar función principal
main