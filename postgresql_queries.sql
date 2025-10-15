-- Consultas de Ejemplo para PostgreSQL

-- 1. Contar todos los registros
SELECT COUNT(*) FROM product_reviews;

-- 2. Ver todos los registros (primeros 10)
SELECT * FROM product_reviews LIMIT 10;

-- 3. Búsqueda de texto simple
SELECT id, product_name, category, rating, 
       LEFT(review_text, 100) as review_preview
FROM product_reviews
WHERE review_text ILIKE '%excelente%';

-- 4. Búsqueda de texto completo (con índice GIN)
SELECT id, product_name, category, rating,
       LEFT(review_text, 100) as review_preview
FROM product_reviews
WHERE to_tsvector('spanish', review_text) @@ plainto_tsquery('spanish', 'excelente calidad')
LIMIT 10;

-- 5. Búsqueda por categoría específica
SELECT id, product_name, rating, reviewer_name
FROM product_reviews
WHERE category = 'Electrónica'
LIMIT 10;

-- 6. Búsqueda con filtro de rating
SELECT id, product_name, category, rating
FROM product_reviews
WHERE rating >= 4
LIMIT 10;

-- 7. Búsqueda combinada (texto + categoría + rating)
SELECT id, product_name, category, rating,
       LEFT(review_text, 100) as review_preview
FROM product_reviews
WHERE to_tsvector('spanish', review_text) @@ plainto_tsquery('spanish', 'buena calidad')
AND category = 'Ropa'
AND rating >= 4
LIMIT 10;

-- 8. Búsqueda con ordenamiento
SELECT id, product_name, category, rating, helpful_count
FROM product_reviews
WHERE category = 'Electrónica'
ORDER BY rating DESC, helpful_count DESC
LIMIT 10;

-- 9. Rating promedio por categoría
SELECT category, 
       AVG(rating) as avg_rating,
       COUNT(*) as total_reviews
FROM product_reviews
GROUP BY category
ORDER BY avg_rating DESC;

-- 10. Distribución de ratings
SELECT rating, 
       COUNT(*) as count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM product_reviews), 2) as percentage
FROM product_reviews
GROUP BY rating
ORDER BY rating DESC;

-- 11. Top 10 productos con más reseñas
SELECT product_name, 
       COUNT(*) as review_count,
       AVG(rating) as avg_rating
FROM product_reviews
GROUP BY product_name
ORDER BY review_count DESC
LIMIT 10;

-- 12. Estadísticas de helpful_count
SELECT 
    MIN(helpful_count) as min,
    MAX(helpful_count) as max,
    AVG(helpful_count) as avg,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY helpful_count) as median
FROM product_reviews;

-- 13. Búsqueda en múltiples campos
SELECT id, product_name, category, rating,
       LEFT(review_text, 100) as review_preview
FROM product_reviews
WHERE product_name ILIKE '%smartphone%'
OR review_text ILIKE '%smartphone%'
LIMIT 10;

-- 14. Reseñas verificadas de 5 estrellas
SELECT id, product_name, reviewer_name, 
       LEFT(review_text, 100) as review_preview
FROM product_reviews
WHERE rating = 5
AND verified_purchase = true
LIMIT 10;

-- 15. Búsqueda con filtro de fecha (últimos 6 meses)
SELECT id, product_name, category, rating, date
FROM product_reviews
WHERE date >= NOW() - INTERVAL '6 months'
ORDER BY date DESC
LIMIT 10;

-- 16. Reseñas por mes
SELECT 
    DATE_TRUNC('month', date) as month,
    COUNT(*) as review_count
FROM product_reviews
GROUP BY DATE_TRUNC('month', date)
ORDER BY month DESC;

-- 17. Búsqueda de frase exacta (menos eficiente)
SELECT id, product_name, category, rating,
       LEFT(review_text, 100) as review_preview
FROM product_reviews
WHERE review_text ILIKE '%excelente calidad%'
LIMIT 10;

-- 18. Productos por categoría con rating promedio
SELECT category, product_name,
       COUNT(*) as review_count,
       AVG(rating) as avg_rating
FROM product_reviews
GROUP BY category, product_name
HAVING COUNT(*) >= 2
ORDER BY category, avg_rating DESC;

-- 19. Reseñas con rating alto y muchos votos útiles
SELECT id, product_name, category, rating, helpful_count,
       LEFT(review_text, 100) as review_preview
FROM product_reviews
WHERE rating >= 4
AND helpful_count >= 50
ORDER BY helpful_count DESC
LIMIT 10;

-- 20. Excluir reseñas con rating bajo
SELECT id, product_name, category, rating
FROM product_reviews
WHERE category = 'Electrónica'
AND rating >= 3
ORDER BY rating DESC
LIMIT 10;

-- 21. Categorías con rating promedio mayor a 3.5
SELECT category, 
       AVG(rating) as avg_rating,
       COUNT(*) as total_reviews
FROM product_reviews
GROUP BY category
HAVING AVG(rating) > 3.5
ORDER BY avg_rating DESC;

-- 22. Búsqueda con paginación (página 1, 10 resultados)
SELECT id, product_name, category, rating
FROM product_reviews
ORDER BY id
LIMIT 10 OFFSET 0;

-- 23. Búsqueda con paginación (página 2, 10 resultados)
SELECT id, product_name, category, rating
FROM product_reviews
ORDER BY id
LIMIT 10 OFFSET 10;

-- 24. Revisar el tamaño de la tabla
SELECT 
    pg_size_pretty(pg_total_relation_size('product_reviews')) as total_size,
    pg_size_pretty(pg_relation_size('product_reviews')) as table_size,
    pg_size_pretty(pg_indexes_size('product_reviews')) as indexes_size;

-- 25. Ver información de los índices
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'product_reviews';

-- 26. Análisis de rendimiento de una consulta (con EXPLAIN ANALYZE)
EXPLAIN ANALYZE
SELECT id, product_name, category, rating
FROM product_reviews
WHERE to_tsvector('spanish', review_text) @@ plainto_tsquery('spanish', 'excelente calidad')
LIMIT 10;

-- 27. Buscar reseñas de un revisor específico
SELECT id, product_name, category, rating, date,
       LEFT(review_text, 100) as review_preview
FROM product_reviews
WHERE reviewer_name ILIKE '%García%'
ORDER BY date DESC;

-- 28. Reseñas más útiles por categoría
SELECT category, product_name, rating, helpful_count,
       LEFT(review_text, 100) as review_preview
FROM product_reviews
WHERE helpful_count > 70
ORDER BY category, helpful_count DESC;

-- 29. Comparar reseñas verificadas vs no verificadas
SELECT 
    verified_purchase,
    COUNT(*) as review_count,
    AVG(rating) as avg_rating
FROM product_reviews
GROUP BY verified_purchase;

-- 30. Búsqueda por email de revisor
SELECT id, product_name, category, rating, reviewer_name
FROM product_reviews
WHERE reviewer_email LIKE '%@gmail.com'
LIMIT 10;
