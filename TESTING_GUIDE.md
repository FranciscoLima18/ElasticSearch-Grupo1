# Manual de Pruebas y Validación

Este documento describe cómo validar que el proyecto está funcionando correctamente.

## ✅ Checklist de Validación Completa

### 1. Validación de Dependencias

```bash
# Docker
docker --version
# Esperado: Docker version 20.10.x o superior

# Docker Compose
docker-compose --version
# Esperado: Docker Compose version 2.x o superior

# Python
python3 --version
# Esperado: Python 3.8 o superior

# pip
pip3 --version
# Esperado: pip 20.x o superior
```

### 2. Instalación de Dependencias Python

```bash
cd /path/to/ElasticSearch-Grupo1
pip3 install -r requirements.txt
```

**Validar**: No debe haber errores de instalación.

### 3. Iniciar Servicios Docker

```bash
docker-compose up -d
```

**Validar**:
```bash
docker-compose ps
```

**Resultado esperado**: 4 contenedores en estado "Up"
- elasticsearch
- kibana
- postgres
- pgadmin

### 4. Validar ElasticSearch

**Opción 1: curl**
```bash
curl http://localhost:9200
```

**Resultado esperado**:
```json
{
  "name" : "...",
  "cluster_name" : "docker-cluster",
  "version" : {
    "number" : "8.11.1",
    ...
  },
  "tagline" : "You Know, for Search"
}
```

**Opción 2: navegador**
- Abrir: http://localhost:9200
- Debe mostrar JSON con información del cluster

### 5. Validar Kibana

**Navegador**:
- Abrir: http://localhost:5601
- Debe cargar la página de inicio de Kibana
- Puede tardar 30-60 segundos en estar listo

**Nota**: La primera vez que se inicia puede tomar más tiempo.

### 6. Validar PostgreSQL

```bash
docker exec -it postgres psql -U admin -d products_db -c "SELECT version();"
```

**Resultado esperado**: Versión de PostgreSQL 15.x

### 7. Validar PgAdmin

**Navegador**:
- Abrir: http://localhost:5050
- Email: admin@admin.com
- Password: admin123
- Debe cargar la interfaz de PgAdmin

### 8. Generar Datos de Prueba

```bash
python3 generate_data.py
```

**Resultado esperado**:
```
Generando datos de ejemplo...
✓ Se generaron 1000 reseñas
✓ Datos guardados en: sample_reviews.json

📊 Estadísticas:

Reseñas por categoría:
  Alimentos: ~125
  Belleza: ~125
  Deportes: ~125
  ...
```

**Validar**: 
- El archivo `sample_reviews.json` debe existir
- Debe tener aproximadamente 1000 reseñas

```bash
ls -lh sample_reviews.json
wc -l sample_reviews.json
```

### 9. Cargar Datos en ElasticSearch

```bash
python3 load_elasticsearch.py
```

**Resultado esperado**:
```
=== Carga de datos en ElasticSearch ===

✓ Conexión exitosa con ElasticSearch
✓ Índice 'product_reviews' eliminado
✓ Índice 'product_reviews' creado con éxito

Cargando 1000 reseñas a ElasticSearch...
✓ Documentos indexados exitosamente: 1000
✓ Total de documentos en el índice: 1000

📊 Información del índice:
  Tamaño: X.XX MB
  Documentos: 1000

✓ Proceso completado exitosamente
```

**Validar en Kibana**:
```bash
curl -X GET "localhost:9200/product_reviews/_count?pretty"
```

Debe retornar `"count" : 1000`

### 10. Cargar Datos en PostgreSQL

```bash
python3 load_postgresql.py
```

**Resultado esperado**:
```
=== Carga de datos en PostgreSQL ===

✓ Conexión exitosa con PostgreSQL
✓ Tabla eliminada (si existía)
✓ Tabla 'product_reviews' creada
✓ Índices creados

Cargando 1000 reseñas a PostgreSQL...
✓ Registros insertados exitosamente: 1000

📊 Información de la tabla:
  Tamaño: XX MB
  Registros: 1000

✓ Proceso completado exitosamente
```

**Validar**:
```bash
docker exec -it postgres psql -U admin -d products_db -c "SELECT COUNT(*) FROM product_reviews;"
```

Debe retornar: `1000`

### 11. Ejecutar Comparación de Búsquedas

```bash
python3 search_comparison.py
```

**Resultado esperado**:
```
================================================================================
🚀 COMPARACIÓN DE RENDIMIENTO: ElasticSearch vs PostgreSQL
================================================================================

✓ Conexiones establecidas correctamente

================================================================================

🔍 BÚSQUEDA DE TEXTO: 'excelente calidad'

================================================================================

📊 ElasticSearch:
  ⏱️  Tiempo: X.XX ms
  📄 Resultados encontrados: XXX
  📋 Mostrando: 10 primeros

  Ejemplo de resultado:
    Producto: XXX
    Rating: ⭐⭐⭐⭐⭐
    Reseña: XXX...

📊 PostgreSQL:
  ⏱️  Tiempo: X.XX ms
  📄 Resultados encontrados: XXX
  📋 Mostrando: 10 primeros

⚡ ElasticSearch es X.XXx más rápido en esta búsqueda

...
```

**Validar**: No debe haber errores y debe mostrar comparaciones de tiempo.

### 12. Probar Consultas en Kibana Dev Tools

**Abrir**: http://localhost:5601/app/dev_tools#/console

**Consulta 1: Ver documentos**
```json
GET product_reviews/_search
{
  "size": 5
}
```

**Resultado esperado**: JSON con 5 documentos de reseñas.

**Consulta 2: Búsqueda de texto**
```json
GET product_reviews/_search
{
  "query": {
    "match": {
      "review_text": "excelente"
    }
  }
}
```

**Resultado esperado**: Documentos que contienen la palabra "excelente".

**Consulta 3: Agregación**
```json
GET product_reviews/_search
{
  "size": 0,
  "aggs": {
    "categories": {
      "terms": {
        "field": "category"
      }
    }
  }
}
```

**Resultado esperado**: Lista de categorías con conteo de documentos.

### 13. Probar Consultas en PgAdmin

**Abrir**: http://localhost:5050

**Conectar al servidor PostgreSQL**:
- Host: `postgres`
- Port: `5432`
- Database: `products_db`
- Username: `admin`
- Password: `admin123`

**Consulta 1**:
```sql
SELECT COUNT(*) FROM product_reviews;
```

**Resultado esperado**: 1000

**Consulta 2**:
```sql
SELECT category, AVG(rating) as avg_rating
FROM product_reviews
GROUP BY category
ORDER BY avg_rating DESC;
```

**Resultado esperado**: Lista de categorías con rating promedio.

### 14. Validar Índices en ElasticSearch

```bash
curl -X GET "localhost:9200/_cat/indices?v"
```

**Resultado esperado**: Debe mostrar el índice `product_reviews` con ~1000 documentos.

### 15. Validar Índices en PostgreSQL

```bash
docker exec -it postgres psql -U admin -d products_db -c "\d product_reviews"
```

**Resultado esperado**: Descripción de la tabla con todas las columnas y índices.

---

## 🔍 Pruebas de Rendimiento

### Búsqueda Simple de Texto

**ElasticSearch**:
```bash
time curl -X GET "localhost:9200/product_reviews/_search?pretty" -H 'Content-Type: application/json' -d'
{
  "query": {
    "match": {
      "review_text": "excelente calidad"
    }
  }
}
'
```

**PostgreSQL**:
```bash
time docker exec -it postgres psql -U admin -d products_db -c "SELECT * FROM product_reviews WHERE to_tsvector('spanish', review_text) @@ plainto_tsquery('spanish', 'excelente calidad') LIMIT 10;"
```

**Comparar**: ElasticSearch debe ser más rápido.

### Búsqueda con Filtros

**ElasticSearch**:
```bash
time curl -X GET "localhost:9200/product_reviews/_search?pretty" -H 'Content-Type: application/json' -d'
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
'
```

**PostgreSQL**:
```bash
time docker exec -it postgres psql -U admin -d products_db -c "SELECT * FROM product_reviews WHERE category = 'Electrónica' AND rating >= 4 LIMIT 10;"
```

---

## 🐛 Problemas Comunes y Soluciones

### Problema: ElasticSearch no inicia

**Síntomas**:
```bash
docker-compose ps
# elasticsearch: Exit 137 o Restarting
```

**Solución**:
```bash
# En Linux, aumentar vm.max_map_count
sudo sysctl -w vm.max_map_count=262144

# Reiniciar ElasticSearch
docker-compose restart elasticsearch
```

### Problema: Kibana muestra "Kibana server is not ready yet"

**Causa**: Kibana aún está inicializando o ElasticSearch no está listo.

**Solución**:
```bash
# Esperar 1-2 minutos más
# O revisar logs
docker-compose logs kibana

# Reiniciar si es necesario
docker-compose restart kibana
```

### Problema: PostgreSQL no acepta conexiones

**Solución**:
```bash
docker-compose logs postgres
docker-compose restart postgres
# Esperar 30 segundos
```

### Problema: Script Python falla con "Connection refused"

**Causa**: Los servicios no están listos aún.

**Solución**:
```bash
# Verificar que los servicios estén corriendo
docker-compose ps

# Esperar más tiempo (los scripts tienen timeouts de 30-60 segundos)
# O reiniciar los servicios
docker-compose restart
```

### Problema: Puerto ya en uso

**Síntomas**:
```
Error: Bind for 0.0.0.0:9200 failed: port is already allocated
```

**Solución**:
```bash
# Encontrar qué proceso usa el puerto
lsof -i :9200  # En Linux/Mac
netstat -ano | findstr :9200  # En Windows

# Detener el proceso o cambiar el puerto en docker-compose.yml
# Por ejemplo: "9201:9200" en lugar de "9200:9200"
```

### Problema: Datos no se ven en Kibana

**Solución**:
1. Ir a Stack Management → Index Patterns
2. Crear nuevo Index Pattern: `product_reviews`
3. Seleccionar campo de tiempo: `date`
4. Ir a Discover

---

## ✅ Lista de Verificación Final

Antes de la presentación, verifica:

- [ ] Todos los contenedores están corriendo
- [ ] ElasticSearch responde en http://localhost:9200
- [ ] Kibana carga en http://localhost:5601
- [ ] PgAdmin carga en http://localhost:5050
- [ ] Datos cargados en ElasticSearch (1000 documentos)
- [ ] Datos cargados en PostgreSQL (1000 registros)
- [ ] `search_comparison.py` se ejecuta sin errores
- [ ] Consultas de ejemplo funcionan en Kibana
- [ ] Consultas de ejemplo funcionan en PgAdmin
- [ ] `sample_reviews.json` existe y tiene datos

---

## 📊 Métricas Esperadas

Con 1000 reseñas:

| Métrica | ElasticSearch | PostgreSQL |
|---------|---------------|------------|
| Tamaño en disco | ~1-2 MB | ~2-3 MB |
| Tiempo de indexación | 2-5 segundos | 5-10 segundos |
| Búsqueda simple | 5-20 ms | 15-50 ms |
| Búsqueda compleja | 10-30 ms | 30-100 ms |
| Agregaciones | 10-40 ms | 40-150 ms |

**Nota**: Los tiempos pueden variar según el hardware.

---

## 🔄 Reiniciar Todo (Clean Slate)

Si necesitas empezar desde cero:

```bash
# Detener y eliminar todo (incluyendo datos)
docker-compose down -v

# Eliminar archivo de datos generados
rm -f sample_reviews.json

# Reiniciar desde el principio
docker-compose up -d
sleep 60
python3 generate_data.py
python3 load_elasticsearch.py
python3 load_postgresql.py
```

---

¡Todo listo para la demostración! 🚀
