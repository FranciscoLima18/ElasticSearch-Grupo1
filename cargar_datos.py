#!/usr/bin/env python3
"""
Script para cargar datos de productos en ElasticSearch y realizar consultas de ejemplo.
Proyecto: ElasticSearch Grupo 1 - Bases de Datos NoSQL
"""

import json
import time
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, NotFoundError

# Configuración de ElasticSearch
ES_HOST = "localhost"
ES_PORT = 9200
INDEX_NAME = "productos"

def conectar_elasticsearch():
    """Establece conexión con ElasticSearch"""
    try:
        es = Elasticsearch([f"http://{ES_HOST}:{ES_PORT}"])
        
        # Verificar que ElasticSearch esté disponible
        if not es.ping():
            print("❌ Error: No se puede conectar a ElasticSearch")
            return None
            
        info = es.info()
        print(f"✅ Conectado a ElasticSearch {info['version']['number']}")
        return es
        
    except ConnectionError:
        print("❌ Error: ElasticSearch no está disponible. Asegúrate de que Docker esté ejecutándose.")
        return None

def crear_indice(es):
    """Crea el índice con mapping personalizado"""
    mapping = {
        "mappings": {
            "properties": {
                "id": {"type": "integer"},
                "nombre": {
                    "type": "text",
                    "analyzer": "spanish",
                    "fields": {
                        "keyword": {"type": "keyword"}
                    }
                },
                "categoria": {"type": "keyword"},
                "descripcion": {
                    "type": "text",
                    "analyzer": "spanish"
                },
                "precio": {"type": "float"},
                "marca": {"type": "keyword"},
                "stock": {"type": "integer"},
                "calificacion": {"type": "float"},
                "fecha_lanzamiento": {"type": "date"}
            }
        },
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    }
    
    try:
        # Eliminar índice si existe
        if es.indices.exists(index=INDEX_NAME):
            es.indices.delete(index=INDEX_NAME)
            print(f"🗑️  Índice '{INDEX_NAME}' eliminado")
        
        # Crear nuevo índice
        es.indices.create(index=INDEX_NAME, body=mapping)
        print(f"🎯 Índice '{INDEX_NAME}' creado con mapping personalizado")
        
    except Exception as e:
        print(f"❌ Error al crear el índice: {e}")
        return False
    
    return True

def cargar_datos(es):
    """Carga los datos desde el archivo JSON"""
    try:
        with open('productos.json', 'r', encoding='utf-8') as file:
            productos = json.load(file)
        
        print(f"📂 Cargando {len(productos)} productos...")
        
        # Indexar cada producto
        for producto in productos:
            response = es.index(
                index=INDEX_NAME,
                id=producto['id'],
                body=producto
            )
            
        # Refrescar el índice para que los datos estén disponibles inmediatamente
        es.indices.refresh(index=INDEX_NAME)
        
        print(f"✅ {len(productos)} productos cargados exitosamente")
        return True
        
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo 'productos.json'")
        return False
    except Exception as e:
        print(f"❌ Error al cargar datos: {e}")
        return False

def mostrar_estadisticas(es):
    """Muestra estadísticas básicas del índice"""
    try:
        stats = es.indices.stats(index=INDEX_NAME)
        count = es.count(index=INDEX_NAME)
        
        print(f"\n📊 ESTADÍSTICAS DEL ÍNDICE '{INDEX_NAME}':")
        print(f"   • Total documentos: {count['count']}")
        print(f"   • Tamaño del índice: {stats['indices'][INDEX_NAME]['total']['store']['size_in_bytes']} bytes")
        print(f"   • Shards: {stats['indices'][INDEX_NAME]['total']['segments']['count']}")
        
    except Exception as e:
        print(f"❌ Error al obtener estadísticas: {e}")

def buscar_por_nombre(es, termino):
    """Búsqueda por nombre del producto"""
    query = {
        "query": {
            "match": {
                "nombre": termino
            }
        },
        "highlight": {
            "fields": {
                "nombre": {}
            }
        }
    }
    
    try:
        response = es.search(index=INDEX_NAME, body=query)
        print(f"\n🔍 BÚSQUEDA POR NOMBRE: '{termino}'")
        print(f"   Resultados encontrados: {response['hits']['total']['value']}")
        
        for hit in response['hits']['hits']:
            producto = hit['_source']
            score = hit['_score']
            print(f"   • {producto['nombre']} - ${producto['precio']} (Score: {score:.2f})")
            
    except Exception as e:
        print(f"❌ Error en búsqueda por nombre: {e}")

def buscar_por_rango_precio(es, precio_min, precio_max):
    """Búsqueda por rango de precios"""
    query = {
        "query": {
            "range": {
                "precio": {
                    "gte": precio_min,
                    "lte": precio_max
                }
            }
        },
        "sort": [
            {"precio": {"order": "asc"}}
        ]
    }
    
    try:
        response = es.search(index=INDEX_NAME, body=query)
        print(f"\n💰 BÚSQUEDA POR RANGO DE PRECIO: ${precio_min} - ${precio_max}")
        print(f"   Resultados encontrados: {response['hits']['total']['value']}")
        
        for hit in response['hits']['hits']:
            producto = hit['_source']
            print(f"   • {producto['nombre']} - ${producto['precio']} ({producto['categoria']})")
            
    except Exception as e:
        print(f"❌ Error en búsqueda por rango de precio: {e}")

def buscar_por_categoria(es, categoria):
    """Búsqueda por categoría"""
    query = {
        "query": {
            "term": {
                "categoria": categoria
            }
        }
    }
    
    try:
        response = es.search(index=INDEX_NAME, body=query)
        print(f"\n📁 BÚSQUEDA POR CATEGORÍA: '{categoria}'")
        print(f"   Resultados encontrados: {response['hits']['total']['value']}")
        
        for hit in response['hits']['hits']:
            producto = hit['_source']
            print(f"   • {producto['nombre']} - ${producto['precio']}")
            
    except Exception as e:
        print(f"❌ Error en búsqueda por categoría: {e}")

def busqueda_combinada(es):
    """Búsqueda combinada con múltiples filtros"""
    query = {
        "query": {
            "bool": {
                "must": [
                    {"range": {"precio": {"gte": 100, "lte": 300}}},
                    {"range": {"calificacion": {"gte": 4.0}}}
                ],
                "should": [
                    {"match": {"descripcion": "inalámbrico"}},
                    {"match": {"categoria": "Accesorios"}}
                ],
                "minimum_should_match": 1
            }
        },
        "sort": [
            {"calificacion": {"order": "desc"}},
            {"precio": {"order": "asc"}}
        ]
    }
    
    try:
        response = es.search(index=INDEX_NAME, body=query)
        print(f"\n🎯 BÚSQUEDA COMBINADA:")
        print(f"   Filtros: Precio $100-$300, Calificación ≥4.0, Con 'inalámbrico' o categoría 'Accesorios'")
        print(f"   Resultados encontrados: {response['hits']['total']['value']}")
        
        for hit in response['hits']['hits']:
            producto = hit['_source']
            print(f"   • {producto['nombre']} - ${producto['precio']} (⭐{producto['calificacion']})")
            
    except Exception as e:
        print(f"❌ Error en búsqueda combinada: {e}")

def agregaciones_ejemplo(es):
    """Ejemplo de agregaciones para análisis de datos"""
    query = {
        "size": 0,  # No queremos los documentos, solo las agregaciones
        "aggs": {
            "productos_por_categoria": {
                "terms": {
                    "field": "categoria",
                    "size": 10
                }
            },
            "productos_por_marca": {
                "terms": {
                    "field": "marca",
                    "size": 5
                }
            },
            "estadisticas_precio": {
                "stats": {
                    "field": "precio"
                }
            },
            "rango_precios": {
                "range": {
                    "field": "precio",
                    "ranges": [
                        {"to": 100},
                        {"from": 100, "to": 300},
                        {"from": 300}
                    ]
                }
            }
        }
    }
    
    try:
        response = es.search(index=INDEX_NAME, body=query)
        aggs = response['aggregations']
        
        print(f"\n📈 ANÁLISIS Y AGREGACIONES:")
        
        # Productos por categoría
        print(f"   📁 Productos por categoría:")
        for bucket in aggs['productos_por_categoria']['buckets']:
            print(f"      • {bucket['key']}: {bucket['doc_count']} productos")
        
        # Productos por marca
        print(f"   🏷️  Top marcas:")
        for bucket in aggs['productos_por_marca']['buckets']:
            print(f"      • {bucket['key']}: {bucket['doc_count']} productos")
        
        # Estadísticas de precios
        stats = aggs['estadisticas_precio']
        print(f"   💰 Estadísticas de precios:")
        print(f"      • Precio promedio: ${stats['avg']:.2f}")
        print(f"      • Precio mínimo: ${stats['min']:.2f}")
        print(f"      • Precio máximo: ${stats['max']:.2f}")
        
        # Rangos de precios
        print(f"   📊 Distribución por rangos de precio:")
        for bucket in aggs['rango_precios']['buckets']:
            if 'from' in bucket and 'to' in bucket:
                rango = f"${bucket['from']:.0f} - ${bucket['to']:.0f}"
            elif 'to' in bucket:
                rango = f"Menos de ${bucket['to']:.0f}"
            else:
                rango = f"Más de ${bucket['from']:.0f}"
            print(f"      • {rango}: {bucket['doc_count']} productos")
            
    except Exception as e:
        print(f"❌ Error en agregaciones: {e}")

def main():
    """Función principal"""
    print("🚀 INICIANDO SCRIPT DE ELASTICSEARCH - GRUPO 1")
    print("=" * 50)
    
    # Conectar a ElasticSearch
    es = conectar_elasticsearch()
    if not es:
        return
    
    # Crear índice
    if not crear_indice(es):
        return
    
    # Cargar datos
    if not cargar_datos(es):
        return
    
    # Mostrar estadísticas
    mostrar_estadisticas(es)
    
    # Esperar un momento para que los datos se indexen completamente
    time.sleep(2)
    
    print("\n" + "=" * 50)
    print("🔍 EJECUTANDO CONSULTAS DE EJEMPLO")
    print("=" * 50)
    
    # Ejecutar consultas de ejemplo
    buscar_por_nombre(es, "Logitech")
    buscar_por_rango_precio(es, 100, 300)
    buscar_por_categoria(es, "Accesorios")
    busqueda_combinada(es)
    agregaciones_ejemplo(es)
    
    print("\n" + "=" * 50)
    print("✅ SCRIPT COMPLETADO EXITOSAMENTE")
    print("💡 Puedes acceder a Kibana en: http://localhost:5601")
    print("🔗 ElasticSearch API disponible en: http://localhost:9200")
    print("=" * 50)

if __name__ == "__main__":
    main()