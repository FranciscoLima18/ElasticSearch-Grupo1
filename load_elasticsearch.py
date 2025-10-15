"""
Script para cargar datos en ElasticSearch
"""
from elasticsearch import Elasticsearch
import json
import time

# Conectar a ElasticSearch
es = Elasticsearch(['http://localhost:9200'])

def wait_for_elasticsearch(max_retries=30):
    """Espera a que ElasticSearch esté disponible"""
    for i in range(max_retries):
        try:
            if es.ping():
                print("✓ Conexión exitosa con ElasticSearch")
                return True
        except:
            pass
        print(f"Esperando a ElasticSearch... ({i+1}/{max_retries})")
        time.sleep(2)
    return False

def create_index():
    """Crea el índice con el mapping apropiado"""
    index_name = 'product_reviews'
    
    # Eliminar índice si existe
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
        print(f"✓ Índice '{index_name}' eliminado")
    
    # Definir el mapping
    mapping = {
        "mappings": {
            "properties": {
                "id": {"type": "keyword"},
                "product_name": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    }
                },
                "category": {"type": "keyword"},
                "rating": {"type": "integer"},
                "review_text": {
                    "type": "text",
                    "analyzer": "spanish"
                },
                "reviewer_name": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    }
                },
                "reviewer_email": {"type": "keyword"},
                "date": {"type": "date"},
                "verified_purchase": {"type": "boolean"},
                "helpful_count": {"type": "integer"}
            }
        },
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    }
    
    es.indices.create(index=index_name, body=mapping)
    print(f"✓ Índice '{index_name}' creado con éxito")

def load_data(filename='sample_reviews.json'):
    """Carga los datos desde el archivo JSON a ElasticSearch"""
    index_name = 'product_reviews'
    
    with open(filename, 'r', encoding='utf-8') as f:
        reviews = json.load(f)
    
    print(f"\nCargando {len(reviews)} reseñas a ElasticSearch...")
    
    # Cargar datos usando bulk API para mejor rendimiento
    from elasticsearch.helpers import bulk
    
    actions = [
        {
            "_index": index_name,
            "_id": review['id'],
            "_source": review
        }
        for review in reviews
    ]
    
    success, failed = bulk(es, actions, raise_on_error=False)
    
    print(f"✓ Documentos indexados exitosamente: {success}")
    if failed:
        print(f"✗ Documentos fallidos: {failed}")
    
    # Refrescar el índice para que los datos estén disponibles inmediatamente
    es.indices.refresh(index=index_name)
    
    # Mostrar información del índice
    count = es.count(index=index_name)['count']
    print(f"✓ Total de documentos en el índice: {count}")

def show_index_info():
    """Muestra información sobre el índice"""
    index_name = 'product_reviews'
    
    # Estadísticas del índice
    stats = es.indices.stats(index=index_name)
    size_in_bytes = stats['indices'][index_name]['total']['store']['size_in_bytes']
    size_mb = size_in_bytes / (1024 * 1024)
    
    print(f"\n📊 Información del índice:")
    print(f"  Tamaño: {size_mb:.2f} MB")
    print(f"  Documentos: {es.count(index=index_name)['count']}")

if __name__ == "__main__":
    print("=== Carga de datos en ElasticSearch ===\n")
    
    # Esperar a que ElasticSearch esté disponible
    if not wait_for_elasticsearch():
        print("✗ No se pudo conectar a ElasticSearch")
        print("Asegúrate de que Docker Compose esté ejecutándose:")
        print("  docker-compose up -d")
        exit(1)
    
    # Crear índice
    create_index()
    
    # Cargar datos
    load_data()
    
    # Mostrar información
    show_index_info()
    
    print("\n✓ Proceso completado exitosamente")
    print("\nPuedes visualizar los datos en Kibana:")
    print("  http://localhost:5601")
