# Consultas de Ejemplo para ElasticSearch (Kibana Dev Tools)

## 1. Ver información del índice
GET product_reviews

## 2. Contar documentos
GET product_reviews/_count

## 3. Buscar todos los documentos (primeros 10)
GET product_reviews/_search
{
  "size": 10
}

## 4. Búsqueda de texto simple
GET product_reviews/_search
{
  "query": {
    "match": {
      "review_text": "excelente"
    }
  }
}

## 5. Búsqueda de texto con fuzziness (tolera errores)
GET product_reviews/_search
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

## 6. Búsqueda por categoría específica
GET product_reviews/_search
{
  "query": {
    "term": {
      "category": "Electrónica"
    }
  }
}

## 7. Búsqueda con filtro de rating
GET product_reviews/_search
{
  "query": {
    "range": {
      "rating": {
        "gte": 4
      }
    }
  }
}

## 8. Búsqueda combinada (texto + categoría + rating)
GET product_reviews/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "review_text": "buena calidad"
          }
        },
        {
          "term": {
            "category": "Ropa"
          }
        },
        {
          "range": {
            "rating": {
              "gte": 4
            }
          }
        }
      ]
    }
  }
}

## 9. Búsqueda con highlighting (resaltar coincidencias)
GET product_reviews/_search
{
  "query": {
    "match": {
      "review_text": "excelente producto"
    }
  },
  "highlight": {
    "fields": {
      "review_text": {}
    }
  }
}

## 10. Búsqueda con ordenamiento
GET product_reviews/_search
{
  "query": {
    "term": {
      "category": "Electrónica"
    }
  },
  "sort": [
    {
      "rating": {
        "order": "desc"
      }
    },
    {
      "helpful_count": {
        "order": "desc"
      }
    }
  ]
}

## 11. Agregación: Rating promedio por categoría
GET product_reviews/_search
{
  "size": 0,
  "aggs": {
    "categories": {
      "terms": {
        "field": "category",
        "size": 10
      },
      "aggs": {
        "avg_rating": {
          "avg": {
            "field": "rating"
          }
        }
      }
    }
  }
}

## 12. Agregación: Distribución de ratings
GET product_reviews/_search
{
  "size": 0,
  "aggs": {
    "rating_distribution": {
      "terms": {
        "field": "rating",
        "order": {
          "_key": "desc"
        }
      }
    }
  }
}

## 13. Agregación: Top 10 productos con más reseñas
GET product_reviews/_search
{
  "size": 0,
  "aggs": {
    "top_products": {
      "terms": {
        "field": "product_name.keyword",
        "size": 10,
        "order": {
          "_count": "desc"
        }
      }
    }
  }
}

## 14. Agregación: Estadísticas de helpful_count
GET product_reviews/_search
{
  "size": 0,
  "aggs": {
    "helpful_stats": {
      "stats": {
        "field": "helpful_count"
      }
    }
  }
}

## 15. Búsqueda con múltiples campos
GET product_reviews/_search
{
  "query": {
    "multi_match": {
      "query": "smartphone",
      "fields": ["product_name", "review_text"]
    }
  }
}

## 16. Búsqueda de reseñas verificadas de 5 estrellas
GET product_reviews/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "rating": 5
          }
        },
        {
          "term": {
            "verified_purchase": true
          }
        }
      ]
    }
  }
}

## 17. Búsqueda con filtro de fecha (últimos 6 meses)
GET product_reviews/_search
{
  "query": {
    "range": {
      "date": {
        "gte": "now-6M/M"
      }
    }
  }
}

## 18. Agregación: Reseñas por mes
GET product_reviews/_search
{
  "size": 0,
  "aggs": {
    "reviews_over_time": {
      "date_histogram": {
        "field": "date",
        "calendar_interval": "month"
      }
    }
  }
}

## 19. Búsqueda de frases exactas
GET product_reviews/_search
{
  "query": {
    "match_phrase": {
      "review_text": "excelente calidad"
    }
  }
}

## 20. Búsqueda con boost (dar más peso a un campo)
GET product_reviews/_search
{
  "query": {
    "multi_match": {
      "query": "calidad",
      "fields": ["product_name^3", "review_text"]
    }
  }
}

## 21. Búsqueda con should (OR lógico)
GET product_reviews/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "match": {
            "review_text": "excelente"
          }
        },
        {
          "match": {
            "review_text": "perfecto"
          }
        }
      ],
      "minimum_should_match": 1
    }
  }
}

## 22. Búsqueda con must_not (excluir resultados)
GET product_reviews/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "category": "Electrónica"
          }
        }
      ],
      "must_not": [
        {
          "range": {
            "rating": {
              "lt": 3
            }
          }
        }
      ]
    }
  }
}

## 23. Agregación compleja: Categorías con rating promedio > 3.5
GET product_reviews/_search
{
  "size": 0,
  "aggs": {
    "categories": {
      "terms": {
        "field": "category"
      },
      "aggs": {
        "avg_rating": {
          "avg": {
            "field": "rating"
          }
        },
        "high_rated": {
          "bucket_selector": {
            "buckets_path": {
              "avgRating": "avg_rating"
            },
            "script": "params.avgRating > 3.5"
          }
        }
      }
    }
  }
}

## 24. Sugerir texto (búsqueda de sugerencias)
GET product_reviews/_search
{
  "suggest": {
    "text": "exelente",
    "simple_suggestion": {
      "term": {
        "field": "review_text"
      }
    }
  }
}

## 25. Ver estadísticas del índice
GET product_reviews/_stats

## 26. Ver el mapping del índice
GET product_reviews/_mapping

## 27. Búsqueda con paginación
GET product_reviews/_search
{
  "from": 0,
  "size": 10,
  "query": {
    "match_all": {}
  }
}
