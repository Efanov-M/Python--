-- 1. Количество исполнителей в каждом жанре
SELECT g.name, COUNT(ag.artist_id)
FROM genres g
JOIN artist_genres ag ON g.id = ag.genre_id
GROUP BY g.name;

-- 2. Количество треков в альбомах 2019–2020
SELECT COUNT(t.id)
FROM tracks t
JOIN albums a ON t.album_id = a.id
WHERE a.release_year BETWEEN 2019 AND 2020;

-- 3. Средняя длительность треков по альбомам
SELECT a.title, AVG(t.duration_seconds)
FROM albums a
JOIN tracks t ON a.id = t.album_id
GROUP BY a.title;

-- 4. Исполнители без альбомов в 2020
SELECT name
FROM artists
WHERE id NOT IN (
    SELECT aa.artist_id
    FROM artist_albums aa
    JOIN albums a ON aa.album_id = a.id
    WHERE a.release_year = 2020
);

-- 5. Сборники с конкретным исполнителем (например Eminem)
SELECT DISTINCT c.title
FROM compilations c
JOIN compilation_tracks ct ON c.id = ct.compilation_id
JOIN tracks t ON ct.track_id = t.id
JOIN albums a ON t.album_id = a.id
JOIN artist_albums aa ON a.id = aa.album_id
JOIN artists ar ON aa.artist_id = ar.id
WHERE ar.name = 'Eminem';
