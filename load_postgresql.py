"""
Script para cargar datos en PostgreSQL
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json
import time

def wait_for_postgres(max_retries=30):
    """Espera a que PostgreSQL esté disponible"""
    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                host="localhost",
                port="5432",
                user="admin",
                password="admin123",
                database="products_db"
            )
            conn.close()
            print("✓ Conexión exitosa con PostgreSQL")
            return True
        except:
            print(f"Esperando a PostgreSQL... ({i+1}/{max_retries})")
            time.sleep(2)
    return False

def create_table():
    """Crea la tabla de reseñas"""
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        user="admin",
        password="admin123",
        database="products_db"
    )
    
    cursor = conn.cursor()
    
    # Eliminar tabla si existe
    cursor.execute("DROP TABLE IF EXISTS product_reviews")
    print("✓ Tabla eliminada (si existía)")
    
    # Crear tabla
    cursor.execute("""
        CREATE TABLE product_reviews (
            id VARCHAR(255) PRIMARY KEY,
            product_name VARCHAR(255),
            category VARCHAR(100),
            rating INTEGER,
            review_text TEXT,
            reviewer_name VARCHAR(255),
            reviewer_email VARCHAR(255),
            date TIMESTAMP,
            verified_purchase BOOLEAN,
            helpful_count INTEGER
        )
    """)
    
    print("✓ Tabla 'product_reviews' creada")
    
    # Crear índices para búsquedas
    cursor.execute("CREATE INDEX idx_product_name ON product_reviews(product_name)")
    cursor.execute("CREATE INDEX idx_category ON product_reviews(category)")
    cursor.execute("CREATE INDEX idx_rating ON product_reviews(rating)")
    
    # Crear índice de texto completo (para búsquedas de texto)
    cursor.execute("""
        CREATE INDEX idx_review_text_gin ON product_reviews 
        USING gin(to_tsvector('spanish', review_text))
    """)
    
    print("✓ Índices creados")
    
    conn.commit()
    cursor.close()
    conn.close()

def load_data(filename='sample_reviews.json'):
    """Carga los datos desde el archivo JSON a PostgreSQL"""
    with open(filename, 'r', encoding='utf-8') as f:
        reviews = json.load(f)
    
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        user="admin",
        password="admin123",
        database="products_db"
    )
    
    cursor = conn.cursor()
    
    print(f"\nCargando {len(reviews)} reseñas a PostgreSQL...")
    
    # Insertar datos
    for review in reviews:
        cursor.execute("""
            INSERT INTO product_reviews 
            (id, product_name, category, rating, review_text, reviewer_name, 
             reviewer_email, date, verified_purchase, helpful_count)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            review['id'],
            review['product_name'],
            review['category'],
            review['rating'],
            review['review_text'],
            review['reviewer_name'],
            review['reviewer_email'],
            review['date'],
            review['verified_purchase'],
            review['helpful_count']
        ))
    
    conn.commit()
    
    # Contar registros
    cursor.execute("SELECT COUNT(*) FROM product_reviews")
    count = cursor.fetchone()[0]
    
    print(f"✓ Registros insertados exitosamente: {count}")
    
    cursor.close()
    conn.close()

def show_table_info():
    """Muestra información sobre la tabla"""
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        user="admin",
        password="admin123",
        database="products_db"
    )
    
    cursor = conn.cursor()
    
    # Tamaño de la tabla
    cursor.execute("""
        SELECT pg_size_pretty(pg_total_relation_size('product_reviews'))
    """)
    size = cursor.fetchone()[0]
    
    # Número de registros
    cursor.execute("SELECT COUNT(*) FROM product_reviews")
    count = cursor.fetchone()[0]
    
    print(f"\n📊 Información de la tabla:")
    print(f"  Tamaño: {size}")
    print(f"  Registros: {count}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    print("=== Carga de datos en PostgreSQL ===\n")
    
    # Esperar a que PostgreSQL esté disponible
    if not wait_for_postgres():
        print("✗ No se pudo conectar a PostgreSQL")
        print("Asegúrate de que Docker Compose esté ejecutándose:")
        print("  docker-compose up -d")
        exit(1)
    
    # Crear tabla
    create_table()
    
    # Cargar datos
    load_data()
    
    # Mostrar información
    show_table_info()
    
    print("\n✓ Proceso completado exitosamente")
    print("\nPuedes visualizar los datos en PgAdmin:")
    print("  http://localhost:5050")
    print("  Email: admin@admin.com")
    print("  Password: admin123")
