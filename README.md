# ElasticSearch-Grupo1 🚀

## Proyecto de Demostración: ElasticSearch vs PostgreSQL

Este proyecto demuestra las capacidades de **ElasticSearch** como base de datos NoSQL, comparándolo con una base de datos SQL tradicional (PostgreSQL). El caso de uso implementado es la **indexación y búsqueda de reseñas de productos**, mostrando cómo ElasticSearch indexa y busca texto de manera más rápida y flexible.

---

## 📋 Tabla de Contenidos

- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Uso del Sistema](#-uso-del-sistema)
- [Ejemplos de Búsqueda](#-ejemplos-de-búsqueda)
- [Comparación de Rendimiento](#-comparación-de-rendimiento)
- [Ventajas de ElasticSearch](#-ventajas-de-elasticsearch)
- [Acceso a Herramientas de Gestión](#-acceso-a-herramientas-de-gestión)
- [Estructura del Proyecto](#-estructura-del-proyecto)

---

## 🎯 Descripción del Proyecto

Este proyecto implementa un sistema de gestión de reseñas de productos que permite:

1. **Generar datos de ejemplo**: 1000 reseñas de productos en diferentes categorías
2. **Indexar en ElasticSearch**: Utilizando el analizador de texto en español
3. **Almacenar en PostgreSQL**: Con índices de texto completo
4. **Comparar rendimiento**: Búsquedas de texto, filtros y agregaciones
5. **Visualizar datos**: Mediante Kibana y PgAdmin

### Objetivos de Aprendizaje

- ✅ Instalar y configurar ElasticSearch con Docker
- ✅ Comprender el modelo de datos de ElasticSearch (documentos e índices)
- ✅ Realizar búsquedas de texto completo con análisis morfológico
- ✅ Comparar el rendimiento con bases de datos SQL tradicionales
- ✅ Utilizar herramientas de gestión (Kibana, PgAdmin)

---

## 🛠️ Tecnologías Utilizadas

- **ElasticSearch 8.11.1**: Motor de búsqueda y análisis distribuido
- **Kibana 8.11.1**: Herramienta de visualización para ElasticSearch
- **PostgreSQL 15**: Base de datos relacional para comparación
- **PgAdmin 4**: Herramienta de gestión para PostgreSQL
- **Docker & Docker Compose**: Contenedorización de servicios
- **Python 3**: Scripts de generación de datos y búsquedas
  - `elasticsearch`: Cliente de ElasticSearch
  - `psycopg2`: Cliente de PostgreSQL
  - `Faker`: Generación de datos de prueba

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                   Docker Compose                         │
├──────────────┬──────────────┬──────────────┬───────────┤
│              │              │              │            │
│ ElasticSearch│   Kibana     │  PostgreSQL  │  PgAdmin  │
│   :9200      │   :5601      │   :5432      │  :5050    │
│              │              │              │            │
└──────────────┴──────────────┴──────────────┴───────────┘
       ▲              ▲              ▲             ▲
       │              │              │             │
       └──────────────┴──────────────┴─────────────┘
                      │
                Python Scripts
          ┌───────────┴───────────┐
          │                       │
    Data Generation         Search & Compare
    (generate_data.py)     (search_comparison.py)
```

---

## 📦 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Docker**: versión 20.10 o superior
- **Docker Compose**: versión 2.0 o superior
- **Python**: versión 3.8 o superior
- **pip**: Gestor de paquetes de Python

### Verificar instalaciones

```bash
docker --version
docker-compose --version
python3 --version
pip --version
```

---

## 🚀 Instalación y Configuración

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/FranciscoLima18/ElasticSearch-Grupo1.git
cd ElasticSearch-Grupo1
```

### Paso 2: Instalar Dependencias de Python

```bash
pip install -r requirements.txt
```

O si usas Python 3 explícitamente:

```bash
pip3 install -r requirements.txt
```

### Paso 3: Iniciar los Servicios con Docker Compose

```bash
docker-compose up -d
```

Este comando iniciará:
- ElasticSearch en http://localhost:9200
- Kibana en http://localhost:5601
- PostgreSQL en localhost:5432
- PgAdmin en http://localhost:5050

**Espera 30-60 segundos** para que todos los servicios estén completamente iniciados.

### Paso 4: Verificar que los Servicios Están Funcionando

```bash
# Verificar ElasticSearch
curl http://localhost:9200

# Verificar contenedores
docker-compose ps
```

Deberías ver 4 contenedores en estado "Up".

### Paso 5: Generar Datos de Ejemplo

```bash
python generate_data.py
```

Este script genera 1000 reseñas de productos y las guarda en `sample_reviews.json`.

### Paso 6: Cargar Datos en ElasticSearch

```bash
python load_elasticsearch.py
```

### Paso 7: Cargar Datos en PostgreSQL

```bash
python load_postgresql.py
```

---

## 💻 Uso del Sistema

### Ejecutar Comparación de Búsquedas

Una vez cargados los datos, puedes ejecutar el script de comparación:

```bash
python search_comparison.py
```

Este script ejecutará diferentes tipos de búsquedas en ambas bases de datos y mostrará:
- Tiempo de respuesta
- Número de resultados
- Ejemplos de resultados
- Comparación de rendimiento

---

## 🔍 Ejemplos de Búsqueda

### 1. Búsqueda de Texto Completo

**ElasticSearch**:
```python
GET /product_reviews/_search
{
  "query": {
    "match": {
      "review_text": {
        "query": "excelente calidad",
        "fuzziness": "AUTO"
      }
    }
  }
}
```

**PostgreSQL**:
```sql
SELECT * FROM product_reviews
WHERE to_tsvector('spanish', review_text) 
      @@ plainto_tsquery('spanish', 'excelente calidad');
```

### 2. Búsqueda por Categoría y Rating

**ElasticSearch**:
```python
GET /product_reviews/_search
{
  "query": {
    "bool": {
      "must": [
        {"term": {"category": "Electrónica"}},
        {"range": {"rating": {"gte": 4}}}
      ]
    }
  }
}
```

**PostgreSQL**:
```sql
SELECT * FROM product_reviews
WHERE category = 'Electrónica' AND rating >= 4;
```

### 3. Búsqueda Compleja con Filtros

**ElasticSearch**:
```python
GET /product_reviews/_search
{
  "query": {
    "bool": {
      "must": [
        {"match": {"review_text": "buena calidad"}},
        {"term": {"category": "Ropa"}},
        {"range": {"rating": {"gte": 4}}}
      ]
    }
  }
}
```

### 4. Agregaciones y Estadísticas

**ElasticSearch**:
```python
GET /product_reviews/_search
{
  "query": {"term": {"category": "Libros"}},
  "size": 0,
  "aggs": {
    "avg_rating": {"avg": {"field": "rating"}},
    "rating_distribution": {"terms": {"field": "rating"}}
  }
}
```

---

## ⚡ Comparación de Rendimiento

### Resultados Típicos

| Tipo de Búsqueda | ElasticSearch | PostgreSQL | Mejora |
|------------------|---------------|------------|--------|
| Texto completo simple | ~5 ms | ~15 ms | 3x más rápido |
| Filtros por categoría | ~2 ms | ~5 ms | 2.5x más rápido |
| Búsqueda compleja | ~8 ms | ~25 ms | 3x más rápido |
| Agregaciones | ~10 ms | ~30 ms | 3x más rápido |

### Factores de Rendimiento

**ElasticSearch es más rápido porque**:
1. **Índices invertidos**: Optimizados para búsqueda de texto
2. **Análisis morfológico**: Maneja plurales, conjugaciones, etc.
3. **Búsqueda difusa**: Encuentra resultados incluso con errores tipográficos
4. **Relevancia**: Ordena resultados por puntuación de relevancia
5. **Cache inteligente**: Memoriza búsquedas frecuentes

---

## ✨ Ventajas de ElasticSearch

### 1. Búsqueda de Texto Avanzada
- **Análisis morfológico**: Reconoce "correr", "corriendo", "corrió" como el mismo concepto
- **Búsqueda difusa**: Tolera errores tipográficos
- **Sinónimos**: Puede configurarse para reconocer palabras similares
- **Puntuación de relevancia**: Ordena resultados por qué tan bien coinciden

### 2. Escalabilidad Horizontal
- Fácil de escalar añadiendo más nodos
- Distribución automática de datos
- Alta disponibilidad con réplicas

### 3. Búsqueda en Tiempo Real
- Los documentos son buscables casi instantáneamente
- Ideal para aplicaciones que requieren resultados inmediatos

### 4. Flexibilidad en el Schema
- No requiere schema rígido
- Fácil de añadir nuevos campos
- Perfecto para datos semi-estructurados

### 5. Agregaciones Potentes
- Análisis de datos complejos
- Estadísticas en tiempo real
- Facetas para navegación

---

## 🌐 Acceso a Herramientas de Gestión

### Kibana (ElasticSearch)
- **URL**: http://localhost:5601
- **Uso**: Visualización de datos, consola de desarrollo, monitoreo
- **Dev Tools**: http://localhost:5601/app/dev_tools#/console

**Consultas de ejemplo en Kibana**:
```
# Ver todos los índices
GET _cat/indices?v

# Ver datos del índice
GET product_reviews/_search

# Búsqueda de ejemplo
GET product_reviews/_search
{
  "query": {
    "match": {"review_text": "excelente"}
  }
}
```

### PgAdmin (PostgreSQL)
- **URL**: http://localhost:5050
- **Email**: admin@admin.com
- **Password**: admin123

**Configurar conexión a PostgreSQL**:
1. Clic derecho en "Servers" → "Create" → "Server"
2. Name: `PostgreSQL Local`
3. Connection tab:
   - Host: `postgres` (nombre del contenedor)
   - Port: `5432`
   - Database: `products_db`
   - Username: `admin`
   - Password: `admin123`

---

## 📁 Estructura del Proyecto

```
ElasticSearch-Grupo1/
├── README.md                    # Este archivo
├── docker-compose.yml           # Configuración de Docker Compose
├── requirements.txt             # Dependencias de Python
├── .gitignore                   # Archivos ignorados por git
├── generate_data.py             # Genera datos de ejemplo
├── load_elasticsearch.py        # Carga datos en ElasticSearch
├── load_postgresql.py           # Carga datos en PostgreSQL
└── search_comparison.py         # Compara rendimiento de búsquedas
```

---

## 🎓 Casos de Uso de ElasticSearch

ElasticSearch es ideal para:

1. **Motores de búsqueda**: Sitios web, e-commerce, documentación
2. **Análisis de logs**: Centralización y análisis de logs (ELK Stack)
3. **Monitoreo**: Métricas de aplicaciones y sistemas
4. **Búsqueda de productos**: Tiendas online con filtros complejos
5. **Autocompletado**: Sugerencias de búsqueda en tiempo real
6. **Análisis de texto**: Procesamiento de lenguaje natural
7. **Búsqueda geoespacial**: Búsquedas por ubicación

---

## 🔧 Comandos Útiles

### Docker Compose

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (datos)
docker-compose down -v

# Reiniciar un servicio específico
docker-compose restart elasticsearch
```

### ElasticSearch

```bash
# Ver salud del cluster
curl http://localhost:9200/_cluster/health?pretty

# Ver todos los índices
curl http://localhost:9200/_cat/indices?v

# Eliminar un índice
curl -X DELETE http://localhost:9200/product_reviews

# Ver estadísticas del índice
curl http://localhost:9200/product_reviews/_stats?pretty
```

---

## 📊 Demostración en Clase

### Guión Sugerido

1. **Introducción** (2 min)
   - Presentar el problema: búsqueda de texto en grandes volúmenes
   - Explicar qué es ElasticSearch

2. **Demostración de Instalación** (3 min)
   - Mostrar `docker-compose.yml`
   - Iniciar servicios con `docker-compose up -d`
   - Verificar que los servicios están activos

3. **Carga de Datos** (3 min)
   - Explicar el dataset generado
   - Ejecutar scripts de carga
   - Mostrar datos en Kibana y PgAdmin

4. **Comparación de Búsquedas** (5 min)
   - Ejecutar `search_comparison.py`
   - Explicar las diferencias de rendimiento
   - Mostrar búsquedas en Kibana Dev Tools

5. **Ventajas de ElasticSearch** (2 min)
   - Búsqueda difusa
   - Análisis morfológico
   - Relevancia
   - Agregaciones

6. **Preguntas y Respuestas** (5 min)

---

## 🐛 Solución de Problemas

### ElasticSearch no inicia
```bash
# Aumentar memoria virtual en Linux
sudo sysctl -w vm.max_map_count=262144
```

### Los contenedores no se comunican
```bash
# Verificar la red de Docker
docker network ls
docker network inspect elasticsearch-grupo1_elastic-network
```

### Error de conexión en los scripts
```bash
# Verificar que los servicios están ejecutándose
docker-compose ps

# Ver logs de un servicio específico
docker-compose logs elasticsearch
docker-compose logs postgres
```

### Puerto ya en uso
```bash
# Cambiar los puertos en docker-compose.yml
# Por ejemplo: "9201:9200" en lugar de "9200:9200"
```

---

## 📚 Referencias y Recursos

- [Documentación oficial de ElasticSearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Documentación de Kibana](https://www.elastic.co/guide/en/kibana/current/index.html)
- [Tutorial de ElasticSearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html)
- [Elasticsearch Python Client](https://elasticsearch-py.readthedocs.io/)

---

## 👥 Equipo

**Grupo 1 - ElasticSearch**

---

## 📄 Licencia

Este proyecto es de código abierto y está disponible para fines educativos.

---

## 🎉 ¡Éxito con tu Demostración!

Si tienes alguna pregunta o problema, revisa la sección de solución de problemas o consulta la documentación oficial de ElasticSearch.