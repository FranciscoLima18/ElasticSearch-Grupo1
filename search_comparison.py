"""
Script para realizar búsquedas en ElasticSearch y PostgreSQL y comparar el rendimiento
"""
from elasticsearch import Elasticsearch
import psycopg2
import time

# Configuración
es = Elasticsearch(['http://localhost:9200'])
ES_INDEX = 'product_reviews'

def connect_postgres():
    """Conecta a PostgreSQL"""
    return psycopg2.connect(
        host="localhost",
        port="5432",
        user="admin",
        password="admin123",
        database="products_db"
    )

# ============ BÚSQUEDAS EN ELASTICSEARCH ============

def search_elasticsearch_text(query_text):
    """Búsqueda de texto completo en ElasticSearch"""
    start_time = time.time()
    
    response = es.search(
        index=ES_INDEX,
        body={
            "query": {
                "match": {
                    "review_text": {
                        "query": query_text,
                        "fuzziness": "AUTO"
                    }
                }
            },
            "size": 10
        }
    )
    
    elapsed_time = (time.time() - start_time) * 1000  # en milisegundos
    
    return response['hits']['hits'], elapsed_time, response['hits']['total']['value']

def search_elasticsearch_category_rating(category, min_rating):
    """Búsqueda por categoría y rating en ElasticSearch"""
    start_time = time.time()
    
    response = es.search(
        index=ES_INDEX,
        body={
            "query": {
                "bool": {
                    "must": [
                        {"term": {"category": category}},
                        {"range": {"rating": {"gte": min_rating}}}
                    ]
                }
            },
            "size": 10,
            "sort": [
                {"rating": {"order": "desc"}},
                {"helpful_count": {"order": "desc"}}
            ]
        }
    )
    
    elapsed_time = (time.time() - start_time) * 1000
    
    return response['hits']['hits'], elapsed_time, response['hits']['total']['value']

def search_elasticsearch_complex(query_text, category, min_rating):
    """Búsqueda compleja en ElasticSearch"""
    start_time = time.time()
    
    response = es.search(
        index=ES_INDEX,
        body={
            "query": {
                "bool": {
                    "must": [
                        {"match": {"review_text": query_text}},
                        {"term": {"category": category}},
                        {"range": {"rating": {"gte": min_rating}}}
                    ]
                }
            },
            "size": 10,
            "highlight": {
                "fields": {
                    "review_text": {}
                }
            }
        }
    )
    
    elapsed_time = (time.time() - start_time) * 1000
    
    return response['hits']['hits'], elapsed_time, response['hits']['total']['value']

def search_elasticsearch_aggregations(category):
    """Agregaciones en ElasticSearch"""
    start_time = time.time()
    
    response = es.search(
        index=ES_INDEX,
        body={
            "query": {
                "term": {"category": category}
            },
            "size": 0,
            "aggs": {
                "avg_rating": {
                    "avg": {"field": "rating"}
                },
                "rating_distribution": {
                    "terms": {"field": "rating"}
                },
                "top_products": {
                    "terms": {
                        "field": "product_name.keyword",
                        "size": 5
                    }
                }
            }
        }
    )
    
    elapsed_time = (time.time() - start_time) * 1000
    
    return response['aggregations'], elapsed_time

# ============ BÚSQUEDAS EN POSTGRESQL ============

def search_postgresql_text(query_text):
    """Búsqueda de texto completo en PostgreSQL"""
    conn = connect_postgres()
    cursor = conn.cursor()
    
    start_time = time.time()
    
    # Usar búsqueda de texto completo con to_tsvector
    cursor.execute("""
        SELECT id, product_name, category, rating, review_text, 
               reviewer_name, date, helpful_count
        FROM product_reviews
        WHERE to_tsvector('spanish', review_text) @@ plainto_tsquery('spanish', %s)
        LIMIT 10
    """, (query_text,))
    
    results = cursor.fetchall()
    
    # Contar total de resultados
    cursor.execute("""
        SELECT COUNT(*)
        FROM product_reviews
        WHERE to_tsvector('spanish', review_text) @@ plainto_tsquery('spanish', %s)
    """, (query_text,))
    
    total = cursor.fetchone()[0]
    
    elapsed_time = (time.time() - start_time) * 1000
    
    cursor.close()
    conn.close()
    
    return results, elapsed_time, total

def search_postgresql_category_rating(category, min_rating):
    """Búsqueda por categoría y rating en PostgreSQL"""
    conn = connect_postgres()
    cursor = conn.cursor()
    
    start_time = time.time()
    
    cursor.execute("""
        SELECT id, product_name, category, rating, review_text, 
               reviewer_name, date, helpful_count
        FROM product_reviews
        WHERE category = %s AND rating >= %s
        ORDER BY rating DESC, helpful_count DESC
        LIMIT 10
    """, (category, min_rating))
    
    results = cursor.fetchall()
    
    cursor.execute("""
        SELECT COUNT(*)
        FROM product_reviews
        WHERE category = %s AND rating >= %s
    """, (category, min_rating))
    
    total = cursor.fetchone()[0]
    
    elapsed_time = (time.time() - start_time) * 1000
    
    cursor.close()
    conn.close()
    
    return results, elapsed_time, total

def search_postgresql_complex(query_text, category, min_rating):
    """Búsqueda compleja en PostgreSQL"""
    conn = connect_postgres()
    cursor = conn.cursor()
    
    start_time = time.time()
    
    cursor.execute("""
        SELECT id, product_name, category, rating, review_text, 
               reviewer_name, date, helpful_count
        FROM product_reviews
        WHERE to_tsvector('spanish', review_text) @@ plainto_tsquery('spanish', %s)
        AND category = %s
        AND rating >= %s
        LIMIT 10
    """, (query_text, category, min_rating))
    
    results = cursor.fetchall()
    
    cursor.execute("""
        SELECT COUNT(*)
        FROM product_reviews
        WHERE to_tsvector('spanish', review_text) @@ plainto_tsquery('spanish', %s)
        AND category = %s
        AND rating >= %s
    """, (query_text, category, min_rating))
    
    total = cursor.fetchone()[0]
    
    elapsed_time = (time.time() - start_time) * 1000
    
    cursor.close()
    conn.close()
    
    return results, elapsed_time, total

def search_postgresql_aggregations(category):
    """Agregaciones en PostgreSQL"""
    conn = connect_postgres()
    cursor = conn.cursor()
    
    start_time = time.time()
    
    # Promedio de rating
    cursor.execute("""
        SELECT 
            AVG(rating) as avg_rating,
            COUNT(*) as total_reviews
        FROM product_reviews
        WHERE category = %s
    """, (category,))
    
    avg_result = cursor.fetchone()
    
    # Distribución de ratings
    cursor.execute("""
        SELECT rating, COUNT(*) as count
        FROM product_reviews
        WHERE category = %s
        GROUP BY rating
        ORDER BY rating DESC
    """, (category,))
    
    rating_dist = cursor.fetchall()
    
    # Top productos
    cursor.execute("""
        SELECT product_name, COUNT(*) as count
        FROM product_reviews
        WHERE category = %s
        GROUP BY product_name
        ORDER BY count DESC
        LIMIT 5
    """, (category,))
    
    top_products = cursor.fetchall()
    
    elapsed_time = (time.time() - start_time) * 1000
    
    cursor.close()
    conn.close()
    
    return {
        'avg_rating': avg_result[0],
        'total_reviews': avg_result[1],
        'rating_distribution': rating_dist,
        'top_products': top_products
    }, elapsed_time

# ============ FUNCIONES DE DEMOSTRACIÓN ============

def print_separator():
    print("\n" + "="*80 + "\n")

def demo_text_search():
    """Demostración de búsqueda de texto"""
    print_separator()
    print("🔍 BÚSQUEDA DE TEXTO: 'excelente calidad'")
    print_separator()
    
    # ElasticSearch
    print("📊 ElasticSearch:")
    es_results, es_time, es_total = search_elasticsearch_text("excelente calidad")
    print(f"  ⏱️  Tiempo: {es_time:.2f} ms")
    print(f"  📄 Resultados encontrados: {es_total}")
    print(f"  📋 Mostrando: {len(es_results)} primeros")
    
    if es_results:
        print("\n  Ejemplo de resultado:")
        result = es_results[0]['_source']
        print(f"    Producto: {result['product_name']}")
        print(f"    Rating: {'⭐' * result['rating']}")
        print(f"    Reseña: {result['review_text'][:100]}...")
    
    # PostgreSQL
    print("\n📊 PostgreSQL:")
    pg_results, pg_time, pg_total = search_postgresql_text("excelente calidad")
    print(f"  ⏱️  Tiempo: {pg_time:.2f} ms")
    print(f"  📄 Resultados encontrados: {pg_total}")
    print(f"  📋 Mostrando: {len(pg_results)} primeros")
    
    # Comparación
    print(f"\n⚡ ElasticSearch es {pg_time/es_time:.2f}x más rápido en esta búsqueda")

def demo_category_rating_search():
    """Demostración de búsqueda por categoría y rating"""
    print_separator()
    print("🔍 BÚSQUEDA: Categoría 'Electrónica' con rating >= 4")
    print_separator()
    
    # ElasticSearch
    print("📊 ElasticSearch:")
    es_results, es_time, es_total = search_elasticsearch_category_rating("Electrónica", 4)
    print(f"  ⏱️  Tiempo: {es_time:.2f} ms")
    print(f"  📄 Resultados encontrados: {es_total}")
    
    # PostgreSQL
    print("\n📊 PostgreSQL:")
    pg_results, pg_time, pg_total = search_postgresql_category_rating("Electrónica", 4)
    print(f"  ⏱️  Tiempo: {pg_time:.2f} ms")
    print(f"  📄 Resultados encontrados: {pg_total}")
    
    # Comparación
    if es_time > 0:
        print(f"\n⚡ ElasticSearch es {pg_time/es_time:.2f}x más rápido en esta búsqueda")

def demo_complex_search():
    """Demostración de búsqueda compleja"""
    print_separator()
    print("🔍 BÚSQUEDA COMPLEJA: Texto 'buena calidad' + Categoría 'Ropa' + Rating >= 4")
    print_separator()
    
    # ElasticSearch
    print("📊 ElasticSearch:")
    es_results, es_time, es_total = search_elasticsearch_complex("buena calidad", "Ropa", 4)
    print(f"  ⏱️  Tiempo: {es_time:.2f} ms")
    print(f"  📄 Resultados encontrados: {es_total}")
    
    # PostgreSQL
    print("\n📊 PostgreSQL:")
    pg_results, pg_time, pg_total = search_postgresql_complex("buena calidad", "Ropa", 4)
    print(f"  ⏱️  Tiempo: {pg_time:.2f} ms")
    print(f"  📄 Resultados encontrados: {pg_total}")
    
    # Comparación
    if es_time > 0:
        print(f"\n⚡ ElasticSearch es {pg_time/es_time:.2f}x más rápido en esta búsqueda")

def demo_aggregations():
    """Demostración de agregaciones"""
    print_separator()
    print("🔍 AGREGACIONES: Estadísticas de categoría 'Libros'")
    print_separator()
    
    # ElasticSearch
    print("📊 ElasticSearch:")
    es_aggs, es_time = search_elasticsearch_aggregations("Libros")
    print(f"  ⏱️  Tiempo: {es_time:.2f} ms")
    print(f"  ⭐ Rating promedio: {es_aggs['avg_rating']['value']:.2f}")
    print(f"  📊 Distribución de ratings:")
    for bucket in es_aggs['rating_distribution']['buckets']:
        print(f"    {'⭐' * bucket['key']}: {bucket['doc_count']} reseñas")
    
    # PostgreSQL
    print("\n📊 PostgreSQL:")
    pg_aggs, pg_time = search_postgresql_aggregations("Libros")
    print(f"  ⏱️  Tiempo: {pg_time:.2f} ms")
    print(f"  ⭐ Rating promedio: {pg_aggs['avg_rating']:.2f}")
    print(f"  📊 Distribución de ratings:")
    for rating, count in pg_aggs['rating_distribution']:
        print(f"    {'⭐' * rating}: {count} reseñas")
    
    # Comparación
    if es_time > 0:
        print(f"\n⚡ ElasticSearch es {pg_time/es_time:.2f}x más rápido en esta agregación")

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🚀 COMPARACIÓN DE RENDIMIENTO: ElasticSearch vs PostgreSQL")
    print("="*80)
    
    try:
        # Verificar conexión a ElasticSearch
        if not es.ping():
            print("✗ No se pudo conectar a ElasticSearch")
            exit(1)
        
        # Verificar conexión a PostgreSQL
        conn = connect_postgres()
        conn.close()
        
        print("\n✓ Conexiones establecidas correctamente\n")
        
        # Ejecutar demostraciones
        demo_text_search()
        demo_category_rating_search()
        demo_complex_search()
        demo_aggregations()
        
        print_separator()
        print("✓ Demostración completada")
        print_separator()
        
        print("\n💡 Conclusiones:")
        print("  • ElasticSearch está optimizado para búsquedas de texto completo")
        print("  • ElasticSearch maneja mejor las búsquedas difusas y relevancia")
        print("  • ElasticSearch es más rápido en agregaciones complejas")
        print("  • PostgreSQL puede ser competitivo con índices apropiados")
        print("  • ElasticSearch destaca en análisis de texto y búsqueda en tiempo real")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nAsegúrate de que:")
        print("  1. Docker Compose esté ejecutándose: docker-compose up -d")
        print("  2. Los datos estén cargados: python load_elasticsearch.py && python load_postgresql.py")
