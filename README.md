# ElasticSearch Proyecto - Grupo 1

## Bases de Datos NoSQL

Este proyecto implementa un entorno completo de ElasticSearch usando Docker, con un dataset de productos de tecnología y ejemplos de consultas avanzadas.

## 🎯 Objetivos del Proyecto

- Instalar y ejecutar ElasticSearch en contenedores Docker
- Conectar con Kibana para visualización y análisis
- Crear un índice `productos` con datos simulados
- Demostrar capacidades de búsqueda y agregaciones de ElasticSearch
- Proporcionar ejemplos prácticos para aprendizaje

## 📋 Requisitos Previos

- **Docker** y **Docker Compose** instalados
- **Python 3.7+** (para el script de carga)
- **curl** (para pruebas manuales)
- Al menos **4GB de RAM** disponible para los contenedores

## 🚀 Instalación y Ejecución

### 1. Clonar o descargar el proyecto

```bash
git clone https://github.com/FranciscoLima18/ElasticSearch-Grupo1/
cd ElasticSearch-Grupo1
```

### 2. Iniciar los servicios con Docker

```bash
# Iniciar ElasticSearch y Kibana
docker compose up -d

# Verificar que los servicios estén ejecutándose
docker compose ps
```

### 3. Verificar que ElasticSearch esté disponible

```bash
# Debe devolver información del cluster
curl http://localhost:9200

# Verificar salud del cluster
curl http://localhost:9200/_cluster/health?pretty
```

### 4. Instalar dependencias de Python

```bash
# Instalar python3-venv si no está disponible (Ubuntu/Debian)
sudo apt update && sudo apt install -y python3-venv python3-pip

# Crear entorno virtual (recomendado)
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 5. Cargar datos de ejemplo

```bash
# Ejecutar script de carga
python3 cargar_datos.py
```

## 🌐 Acceso a las Interfaces

| Servicio              | URL                                    | Descripción                |
| --------------------- | -------------------------------------- | -------------------------- |
| **ElasticSearch API** | http://localhost:9200                  | API REST principal         |
| **Kibana**            | http://localhost:5601                  | Interface de visualización |
| **Cluster Health**    | http://localhost:9200/\_cluster/health | Estado del cluster         |

### Acceder a Kibana

1. Abrir http://localhost:5601 en el navegador
2. Ir a **Dev Tools** para ejecutar consultas
3. Usar **Discover** para explorar datos
4. Crear **Dashboards** para visualizaciones

## 📊 Dataset de Productos

El dataset incluye **10 productos de tecnología** con los siguientes campos:

```json
{
  "id": 1,
  "nombre": "Laptop HP Envy 13",
  "categoria": "Computadoras",
  "descripcion": "Ultrabook liviana con pantalla táctil Full HD...",
  "precio": 1200,
  "marca": "HP",
  "stock": 15,
  "calificacion": 4.5,
  "fecha_lanzamiento": "2023-06-15"
}
```

### Categorías incluidas:

- **Computadoras** (Laptops, Tablets)
- **Periféricos** (Monitores, Webcams, Impresoras)
- **Accesorios** (Mouse, Teclados)
- **Audio** (Auriculares)
- **Almacenamiento** (SSDs)
- **Redes** (Routers)

## 🔍 Ejemplos de Consultas

### Consultas Básicas

#### 1. Buscar todos los productos

```bash
curl -X GET "localhost:9200/productos/_search?pretty"
```

#### 2. Buscar por nombre

```bash
curl -X GET "localhost:9200/productos/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "nombre": "Logitech"
    }
  }
}'
```

#### 3. Buscar por rango de precios

```bash
curl -X GET "localhost:9200/productos/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "range": {
      "precio": {
        "gte": 100,
        "lte": 300
      }
    }
  }
}'
```

### Consultas Avanzadas

#### 4. Búsqueda combinada con filtros

```bash
curl -X GET "localhost:9200/productos/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [
        {"range": {"precio": {"gte": 100, "lte": 500}}},
        {"range": {"calificacion": {"gte": 4.0}}}
      ],
      "should": [
        {"match": {"descripcion": "inalámbrico"}},
        {"term": {"categoria": "Accesorios"}}
      ]
    }
  }
}'
```

#### 5. Agregaciones - Análisis por categoría

```bash
curl -X GET "localhost:9200/productos/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "productos_por_categoria": {
      "terms": {
        "field": "categoria"
      }
    }
  }
}'
```

## 📝 Consultas en Kibana Dev Tools

En Kibana (http://localhost:5601/app/dev_tools#/console), puedes usar estas consultas:

```json
# Buscar todos los productos
GET productos/_search

# Buscar productos HP
GET productos/_search
{
  "query": {
    "match": {
      "marca": "HP"
    }
  }
}

# Análisis de precios por categoría
GET productos/_search
{
  "size": 0,
  "aggs": {
    "categorias": {
      "terms": {
        "field": "categoria"
      },
      "aggs": {
        "precio_promedio": {
          "avg": {
            "field": "precio"
          }
        }
      }
    }
  }
}
```

## 🛠️ Funcionalidades Demostradas

### 1. **Búsquedas de Texto**

- Match queries para búsqueda de texto
- Multi-match en múltiples campos
- Búsqueda fuzzy (tolerante a errores)
- Búsqueda con wildcards

### 2. **Filtros y Rangos**

- Filtros por precio, calificación y stock
- Búsquedas por categoría exacta
- Rangos de fechas
- Combinación de múltiples filtros

### 3. **Agregaciones**

- Conteo por categorías y marcas
- Estadísticas de precios (min, max, promedio)
- Distribución por rangos
- Métricas combinadas

### 4. **Características Avanzadas**

- Highlighting de resultados
- Ordenamiento personalizado
- Bool queries complejas
- Mapping con analizador en español

## 📁 Estructura del Proyecto

```
ElasticSearch-Grupo1/
├── docker-compose.yml          # Configuración de servicios Docker
├── productos.json              # Dataset de productos
├── cargar_datos.py            # Script Python para carga y consultas
├── requirements.txt           # Dependencias Python
├── consultas_ejemplo.md       # Ejemplos de consultas curl y Kibana
└── README.md                  # Esta documentación
```

## 🔧 Comandos Útiles

### Docker

```bash
# Ver logs de ElasticSearch
docker compose logs elasticsearch

# Ver logs de Kibana
docker compose logs kibana

# Reiniciar servicios
docker compose restart

# Detener servicios
docker compose down

# Eliminar volúmenes (datos)
docker compose down -v
```

### ElasticSearch

```bash
# Estado del cluster
curl http://localhost:9200/_cluster/health?pretty

# Listar índices
curl http://localhost:9200/_cat/indices?v

# Ver mapping del índice
curl http://localhost:9200/productos/_mapping?pretty

# Estadísticas del índice
curl http://localhost:9200/productos/_stats?pretty
```

## 🐛 Solución de Problemas

### ElasticSearch no inicia

```bash
# Verificar memoria disponible
free -h

# Aumentar memoria virtual si es necesario
sudo sysctl -w vm.max_map_count=262144

# Verificar logs
docker compose logs elasticsearch
```

### Kibana no se conecta

```bash
# Verificar que ElasticSearch esté disponible
curl http://localhost:9200/_cluster/health

# Reiniciar Kibana
docker compose restart kibana
```

### Script Python falla

```bash
# Verificar conexión a ElasticSearch
curl http://localhost:9200

# Verificar que el archivo productos.json existe
ls -la productos.json

# Reinstalar dependencias
pip install -r requirements.txt
```

## 📚 Recursos Adicionales

- **Documentación ElasticSearch**: https://www.elastic.co/guide/en/elasticsearch/reference/current/
- **Guía de Query DSL**: https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html
- **Kibana User Guide**: https://www.elastic.co/guide/en/kibana/current/
- **Docker Compose**: https://docs.docker.com/compose/

## 👥 Información del Proyecto

- **Curso**: Big Data
- **Grupo**: 1
- **Tecnología**: ElasticSearch (Modelo de Documentos)
- **Autor**: Francisco Lima, Mateo Rodriguez, Ana Clara Sena
- **Fecha**: Octubre 2025
