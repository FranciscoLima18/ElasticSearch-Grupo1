# Guía Rápida de Referencia

## 🚀 Inicio Rápido (Quick Start)

```bash
# 1. Instalar dependencias
pip3 install -r requirements.txt

# 2. Iniciar servicios
docker-compose up -d

# 3. Esperar 60 segundos, luego ejecutar
python3 generate_data.py
python3 load_elasticsearch.py
python3 load_postgresql.py

# 4. Probar la comparación
python3 search_comparison.py
```

---

## 📍 URLs de Acceso

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| ElasticSearch | http://localhost:9200 | - |
| Kibana | http://localhost:5601 | - |
| Kibana Dev Tools | http://localhost:5601/app/dev_tools#/console | - |
| PgAdmin | http://localhost:5050 | admin@admin.com / admin123 |
| PostgreSQL | localhost:5432 | admin / admin123 |

---

## 🐳 Comandos Docker Compose

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver estado de los servicios
docker-compose ps

# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f elasticsearch
docker-compose logs -f kibana

# Reiniciar un servicio
docker-compose restart elasticsearch

# Detener todos los servicios
docker-compose down

# Detener y eliminar datos
docker-compose down -v
```

---

## 🔍 Comandos de Verificación Rápida

### ElasticSearch
```bash
# Verificar conexión
curl http://localhost:9200

# Ver índices
curl http://localhost:9200/_cat/indices?v

# Contar documentos
curl http://localhost:9200/product_reviews/_count?pretty

# Ver un documento
curl http://localhost:9200/product_reviews/_search?size=1&pretty
```

### PostgreSQL
```bash
# Conectar a la base de datos
docker exec -it postgres psql -U admin -d products_db

# Contar registros
docker exec -it postgres psql -U admin -d products_db -c "SELECT COUNT(*) FROM product_reviews;"

# Ver estructura de tabla
docker exec -it postgres psql -U admin -d products_db -c "\d product_reviews"
```

---

## 📝 Scripts del Proyecto

| Script | Propósito | Uso |
|--------|-----------|-----|
| `generate_data.py` | Genera 1000 reseñas de ejemplo | `python3 generate_data.py` |
| `load_elasticsearch.py` | Carga datos en ElasticSearch | `python3 load_elasticsearch.py` |
| `load_postgresql.py` | Carga datos en PostgreSQL | `python3 load_postgresql.py` |
| `search_comparison.py` | Compara rendimiento de búsquedas | `python3 search_comparison.py` |
| `setup.sh` | Instalación automática completa | `./setup.sh` |

---

## 🔎 Consultas de Ejemplo

### ElasticSearch (Kibana Dev Tools)

**Búsqueda simple:**
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

**Búsqueda con filtros:**
```json
GET product_reviews/_search
{
  "query": {
    "bool": {
      "must": [
        {"match": {"review_text": "buena"}},
        {"term": {"category": "Electrónica"}},
        {"range": {"rating": {"gte": 4}}}
      ]
    }
  }
}
```

**Agregación:**
```json
GET product_reviews/_search
{
  "size": 0,
  "aggs": {
    "avg_by_category": {
      "terms": {"field": "category"},
      "aggs": {
        "avg_rating": {"avg": {"field": "rating"}}
      }
    }
  }
}
```

### PostgreSQL (PgAdmin o psql)

**Búsqueda simple:**
```sql
SELECT * FROM product_reviews
WHERE review_text ILIKE '%excelente%'
LIMIT 10;
```

**Búsqueda de texto completo:**
```sql
SELECT * FROM product_reviews
WHERE to_tsvector('spanish', review_text) @@ plainto_tsquery('spanish', 'excelente calidad')
LIMIT 10;
```

**Agregación:**
```sql
SELECT category, AVG(rating) as avg_rating
FROM product_reviews
GROUP BY category
ORDER BY avg_rating DESC;
```

---

## 🎯 Estructura de Datos

### Documento de Reseña
```json
{
  "id": "uuid",
  "product_name": "Laptop",
  "category": "Electrónica",
  "rating": 5,
  "review_text": "Excelente producto...",
  "reviewer_name": "Juan Pérez",
  "reviewer_email": "juan@email.com",
  "date": "2024-03-15T10:30:00",
  "verified_purchase": true,
  "helpful_count": 45
}
```

### Categorías Disponibles
- Electrónica
- Libros
- Ropa
- Hogar
- Deportes
- Juguetes
- Alimentos
- Belleza

---

## ⚡ Comparación Rápida

| Característica | ElasticSearch | PostgreSQL |
|----------------|---------------|------------|
| Tipo | NoSQL (Documentos) | SQL (Relacional) |
| Optimizado para | Búsqueda de texto | Transacciones ACID |
| Velocidad búsqueda texto | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Escalabilidad | Horizontal | Vertical/Horizontal |
| Consistencia | Eventual | ACID |
| Búsqueda difusa | ✅ Nativa | ⚠️ Limitada |
| Análisis morfológico | ✅ Avanzado | ⚠️ Básico |
| Relevancia | ✅ Scoring | ❌ No |

---

## 🐛 Soluciones Rápidas

### ElasticSearch no responde
```bash
docker-compose restart elasticsearch
sleep 30
curl http://localhost:9200
```

### Kibana no carga
```bash
docker-compose restart kibana
# Esperar 1-2 minutos
```

### Puerto ocupado
Editar `docker-compose.yml`:
```yaml
ports:
  - "9201:9200"  # Cambiar primer número
```

### Reiniciar todo desde cero
```bash
docker-compose down -v
rm -f sample_reviews.json
docker-compose up -d
sleep 60
python3 generate_data.py
python3 load_elasticsearch.py
python3 load_postgresql.py
```

---

## 📚 Archivos del Proyecto

```
ElasticSearch-Grupo1/
├── README.md                    # Documentación principal
├── PRESENTATION_GUIDE.md        # Guía de presentación
├── TESTING_GUIDE.md             # Guía de pruebas
├── QUICK_REFERENCE.md           # Esta guía
├── docker-compose.yml           # Configuración Docker
├── requirements.txt             # Dependencias Python
├── .gitignore                   # Archivos ignorados
├── setup.sh                     # Script de instalación
├── generate_data.py             # Generador de datos
├── load_elasticsearch.py        # Cargador ES
├── load_postgresql.py           # Cargador PG
├── search_comparison.py         # Comparador
├── elasticsearch_queries.md     # Consultas ES de ejemplo
└── postgresql_queries.sql       # Consultas PG de ejemplo
```

---

## 💡 Tips Útiles

### Kibana Dev Tools
- `Ctrl + Enter`: Ejecutar consulta
- `Ctrl + I`: Auto-formatear JSON
- `Ctrl + /`: Comentar/descomentar

### Ver logs en tiempo real
```bash
docker-compose logs -f --tail=100 elasticsearch
```

### Exportar datos de ElasticSearch
```bash
curl -X GET "localhost:9200/product_reviews/_search?pretty&size=1000" > export.json
```

### Backup de PostgreSQL
```bash
docker exec postgres pg_dump -U admin products_db > backup.sql
```

### Restaurar PostgreSQL
```bash
docker exec -i postgres psql -U admin products_db < backup.sql
```

---

## 🎓 Conceptos Clave

### ElasticSearch
- **Índice**: Similar a una base de datos
- **Documento**: Similar a una fila/registro
- **Mapping**: Similar a un schema
- **Query DSL**: Lenguaje de consulta JSON
- **Analyzer**: Procesa texto antes de indexar
- **Inverted Index**: Estructura de datos para búsqueda rápida

### Búsqueda
- **Match**: Búsqueda de texto con análisis
- **Term**: Búsqueda exacta (sin análisis)
- **Range**: Búsqueda por rango
- **Bool**: Combina múltiples consultas (must, should, must_not)
- **Fuzzy**: Tolera errores tipográficos
- **Aggregation**: Análisis y estadísticas

---

## 📞 Recursos Adicionales

- **Documentación ElasticSearch**: https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html
- **Kibana Guide**: https://www.elastic.co/guide/en/kibana/current/index.html
- **ElasticSearch Python Client**: https://elasticsearch-py.readthedocs.io/
- **PostgreSQL Full Text Search**: https://www.postgresql.org/docs/current/textsearch.html

---

## ✅ Checklist Pre-Demo

- [ ] `docker-compose ps` muestra 4 servicios "Up"
- [ ] http://localhost:9200 responde
- [ ] http://localhost:5601 carga Kibana
- [ ] http://localhost:5050 carga PgAdmin
- [ ] `sample_reviews.json` existe
- [ ] ElasticSearch tiene 1000 documentos
- [ ] PostgreSQL tiene 1000 registros
- [ ] `search_comparison.py` se ejecuta sin errores

---

¿Preguntas? Revisa el `README.md` o `TESTING_GUIDE.md` para más detalles.
