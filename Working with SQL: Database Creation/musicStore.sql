CREATE TABLE genres (
    id INT PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE artists (
    id INT PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE albums (
    id INT PRIMARY KEY,
    title TEXT NOT NULL,
    release_year INT NOT NULL
);

CREATE TABLE tracks (
    id INT PRIMARY KEY,
    title TEXT NOT NULL,
    duration_seconds INT NOT NULL,
    album_id INT NOT NULL REFERENCES albums(id)
);

CREATE TABLE compilations (
    id INT PRIMARY KEY,
    title TEXT NOT NULL,
    release_year INT NOT NULL
);

-- связь артистов и жанров
CREATE TABLE artist_genres (
    artist_id INT REFERENCES artists(id),
    genre_id INT REFERENCES genres(id),
    PRIMARY KEY (artist_id, genre_id)
);

-- связь артистов и альбомов
CREATE TABLE artist_albums (
    artist_id INT REFERENCES artists(id),
    album_id INT REFERENCES albums(id),
    PRIMARY KEY (artist_id, album_id)
);

-- связь сборников и треков
CREATE TABLE compilation_tracks (
    compilation_id INT REFERENCES compilations(id),
    track_id INT REFERENCES tracks(id),
    PRIMARY KEY (compilation_id, track_id)
);



INSERT INTO genres VALUES
(1, 'Rock'),
(2, 'Pop'),
(3, 'Hip-Hop');

INSERT INTO artists VALUES
(1, 'Queen'),
(2, 'Michael Jackson'),
(3, 'Eminem'),
(4, 'Linkin Park');

INSERT INTO albums VALUES
(1, 'A Night at the Opera', 1975),
(2, 'Thriller', 1982),
(3, 'The Eminem Show', 2002),
(4, 'Hybrid Theory', 2000);

INSERT INTO tracks VALUES
(1, 'Bohemian Rhapsody', 355, 1),
(2, 'Beat It', 258, 2),
(3, 'Without Me', 290, 3),
(4, 'In The End', 216, 4);

INSERT INTO compilations VALUES
(1, 'Best of Rock', 2005),
(2, 'Top Hits 2000s', 2010);

INSERT INTO artist_genres VALUES
(1,1),
(2,2),
(3,3),
(4,1),
(4,3);

INSERT INTO artist_albums VALUES
(1,1),
(2,2),
(3,3),
(4,4);

INSERT INTO compilation_tracks VALUES
(1,1),
(1,4),
(2,2),
(2,3);
