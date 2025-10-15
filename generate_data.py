"""
Script para generar datos de ejemplo: reseñas de productos
"""
from faker import Faker
import json
import random

fake = Faker(['es_ES', 'es_MX'])

# Categorías de productos
CATEGORIES = [
    'Electrónica',
    'Libros',
    'Ropa',
    'Hogar',
    'Deportes',
    'Juguetes',
    'Alimentos',
    'Belleza'
]

# Productos de ejemplo por categoría
PRODUCTS = {
    'Electrónica': ['Laptop', 'Smartphone', 'Auriculares', 'Tablet', 'Smart TV', 'Cámara Digital'],
    'Libros': ['Novela Fantástica', 'Libro de Cocina', 'Biografía', 'Ciencia Ficción', 'Historia'],
    'Ropa': ['Camiseta', 'Pantalón', 'Vestido', 'Chaqueta', 'Zapatos', 'Gorra'],
    'Hogar': ['Sartén', 'Lámpara', 'Cojín', 'Cortinas', 'Reloj de Pared', 'Florero'],
    'Deportes': ['Pelota de Fútbol', 'Raqueta de Tenis', 'Bicicleta', 'Pesas', 'Yoga Mat'],
    'Juguetes': ['Muñeca', 'Coche de Juguete', 'Puzzle', 'Peluche', 'Juego de Mesa'],
    'Alimentos': ['Café Orgánico', 'Chocolate', 'Aceite de Oliva', 'Miel', 'Té Verde'],
    'Belleza': ['Crema Facial', 'Shampoo', 'Perfume', 'Maquillaje', 'Protector Solar']
}

def generate_review():
    """Genera una reseña de producto aleatoria"""
    category = random.choice(CATEGORIES)
    product = random.choice(PRODUCTS[category])
    rating = random.randint(1, 5)
    
    # Generar texto de reseña basado en la calificación
    if rating >= 4:
        review_templates = [
            f"Excelente {product.lower()}, superó mis expectativas. {fake.sentence()}",
            f"Muy contento con la compra de este {product.lower()}. {fake.sentence()}",
            f"Producto de alta calidad. El {product.lower()} es perfecto. {fake.sentence()}",
            f"Recomendado 100%. {fake.sentence()} El {product.lower()} es increíble.",
        ]
    elif rating == 3:
        review_templates = [
            f"El {product.lower()} cumple con lo esperado. {fake.sentence()}",
            f"Producto correcto, nada extraordinario. {fake.sentence()}",
            f"Está bien por el precio. {fake.sentence()}",
        ]
    else:
        review_templates = [
            f"Decepcionado con el {product.lower()}. {fake.sentence()}",
            f"No lo recomiendo. {fake.sentence()} El {product.lower()} no es bueno.",
            f"Mala calidad. {fake.sentence()}",
        ]
    
    review = {
        'id': fake.uuid4(),
        'product_name': product,
        'category': category,
        'rating': rating,
        'review_text': random.choice(review_templates) + " " + fake.text(max_nb_chars=200),
        'reviewer_name': fake.name(),
        'reviewer_email': fake.email(),
        'date': fake.date_time_between(start_date='-2y', end_date='now').isoformat(),
        'verified_purchase': random.choice([True, False]),
        'helpful_count': random.randint(0, 100)
    }
    
    return review

def generate_dataset(num_reviews=1000):
    """Genera un conjunto de datos con reseñas"""
    reviews = []
    for _ in range(num_reviews):
        reviews.append(generate_review())
    return reviews

if __name__ == "__main__":
    # Generar 1000 reseñas
    print("Generando datos de ejemplo...")
    reviews = generate_dataset(1000)
    
    # Guardar en archivo JSON
    with open('sample_reviews.json', 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Se generaron {len(reviews)} reseñas")
    print("✓ Datos guardados en: sample_reviews.json")
    
    # Mostrar estadísticas
    categories_count = {}
    ratings_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    
    for review in reviews:
        category = review['category']
        rating = review['rating']
        categories_count[category] = categories_count.get(category, 0) + 1
        ratings_count[rating] += 1
    
    print("\n📊 Estadísticas:")
    print("\nReseñas por categoría:")
    for category, count in sorted(categories_count.items()):
        print(f"  {category}: {count}")
    
    print("\nReseñas por calificación:")
    for rating, count in sorted(ratings_count.items()):
        print(f"  {'⭐' * rating}: {count}")
