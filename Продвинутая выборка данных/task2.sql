-- 1. Самый длинный трек
SELECT title, duration_seconds
FROM tracks
ORDER BY duration_seconds DESC
LIMIT 1;

-- 2. Треки >= 3.5 минут (210 сек)
SELECT title
FROM tracks
WHERE duration_seconds >= 210;

-- 3. Сборники 2018–2020
SELECT title
FROM compilations
WHERE release_year BETWEEN 2018 AND 2020;

-- 4. Исполнители с одним словом
SELECT name
FROM artists
WHERE name NOT LIKE '% %';

-- 5. Треки со словом "my"
SELECT title
FROM tracks
WHERE LOWER(title) LIKE '%my%'
   OR LOWER(title) LIKE '%мой%';
