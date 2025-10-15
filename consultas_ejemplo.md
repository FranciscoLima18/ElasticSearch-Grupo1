# EJEMPLOS DE CONSULTAS ELASTICSEARCH - GRUPO 1

# ================================================

## CONSULTAS BÁSICAS CON CURL

### 1. Verificar el estado del cluster

curl -X GET "localhost:9200/\_cluster/health?pretty"

### 2. Listar todos los índices

curl -X GET "localhost:9200/\_cat/indices?v"

### 3. Ver el mapping del índice productos

curl -X GET "localhost:9200/productos/\_mapping?pretty"

### 4. Obtener todos los productos (limitado a 10)

curl -X GET "localhost:9200/productos/\_search?pretty&size=10"

### 5. Buscar productos por nombre (match query)

curl -X GET "localhost:9200/productos/\_search?pretty" -H 'Content-Type: application/json' -d'
{
"query": {
"match": {
"nombre": "Logitech"
}
}
}'

### 6. Buscar por rango de precios

curl -X GET "localhost:9200/productos/\_search?pretty" -H 'Content-Type: application/json' -d'
{
"query": {
"range": {
"precio": {
"gte": 100,
"lte": 300
}
}
},
"sort": [
{"precio": {"order": "asc"}}
]
}'

### 7. Buscar por categoría exacta

curl -X GET "localhost:9200/productos/\_search?pretty" -H 'Content-Type: application/json' -d'
{
"query": {
"term": {
"categoria": "Accesorios"
}
}
}'

### 8. Búsqueda de texto completo en descripción

curl -X GET "localhost:9200/productos/\_search?pretty" -H 'Content-Type: application/json' -d'
{
"query": {
"match": {
"descripcion": "inalámbrico pantalla"
}
},
"highlight": {
"fields": {
"descripcion": {}
}
}
}'

### 9. Búsqueda combinada (bool query)

curl -X GET "localhost:9200/productos/\_search?pretty" -H 'Content-Type: application/json' -d'
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
],
"minimum_should_match": 1
}
},
"sort": [
{"calificacion": {"order": "desc"}},
{"precio": {"order": "asc"}}
]
}'

### 10. Agregaciones - Productos por categoría

curl -X GET "localhost:9200/productos/\_search?pretty" -H 'Content-Type: application/json' -d'
{
"size": 0,
"aggs": {
"productos_por_categoria": {
"terms": {
"field": "categoria",
"size": 10
}
}
}
}'

### 11. Agregaciones - Estadísticas de precios

curl -X GET "localhost:9200/productos/\_search?pretty" -H 'Content-Type: application/json' -d'
{
"size": 0,
"aggs": {
"estadisticas_precio": {
"stats": {
"field": "precio"
}
}
}
}'

### 12. Búsqueda con filtros múltiples

curl -X GET "localhost:9200/productos/\_search?pretty" -H 'Content-Type: application/json' -d'
{
"query": {
"bool": {
"filter": [
{"term": {"marca": "HP"}},
{"range": {"stock": {"gt": 10}}}
]
}
}
}'

### 13. Búsqueda fuzzy (tolerante a errores de escritura)

curl -X GET "localhost:9200/productos/\_search?pretty" -H 'Content-Type: application/json' -d'
{
"query": {
"fuzzy": {
"nombre": {
"value": "Logitec",
"fuzziness": "AUTO"
}
}
}
}'

### 14. Obtener un producto específico por ID

curl -X GET "localhost:9200/productos/\_doc/1?pretty"

### 15. Actualizar el stock de un producto

curl -X POST "localhost:9200/productos/\_update/1?pretty" -H 'Content-Type: application/json' -d'
{
"doc": {
"stock": 20
}
}'

## CONSULTAS PARA KIBANA (Dev Tools)

# Estas consultas se pueden ejecutar directamente en Kibana Dev Tools (http://localhost:5601/app/dev_tools#/console)

GET productos/\_search
{
"query": {
"match_all": {}
}
}

GET productos/\_search
{
"query": {
"match": {
"nombre": "HP"
}
}
}

GET productos/\_search
{
"query": {
"range": {
"precio": {
"gte": 200,
"lte": 400
}
}
}
}

GET productos/\_search
{
"query": {
"bool": {
"must": [
{"match": {"descripcion": "Full HD"}},
{"range": {"precio": {"lte": 300}}}
]
}
}
}

GET productos/\_search
{
"size": 0,
"aggs": {
"precio_promedio_por_categoria": {
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

## CONSULTAS AVANZADAS

### Búsqueda con wildcard

GET productos/\_search
{
"query": {
"wildcard": {
"nombre.keyword": "_Monitor_"
}
}
}

### Búsqueda por fecha de lanzamiento

GET productos/\_search
{
"query": {
"range": {
"fecha_lanzamiento": {
"gte": "2023-01-01",
"lte": "2023-12-31"
}
}
}
}

### Multi-match en varios campos

GET productos/\_search
{
"query": {
"multi_match": {
"query": "HP monitor",
"fields": ["nombre", "descripcion", "marca"]
}
}
}

## NOTAS IMPORTANTES:

# - Todas las consultas curl asumen que ElasticSearch está ejecutándose en localhost:9200

# - Para usar en Kibana, copia las consultas JSON sin el comando curl

# - Reemplaza "localhost:9200" por la URL de tu cluster si es diferente

# - Algunas consultas pueden requerir que el índice "productos" ya esté creado y poblado
