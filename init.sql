DROP TABLE IF EXISTS news;

CREATE TABLE news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title TEXT NOT NULL,
    href TEXT,
    content TEXT,
    scraped_at DATETIME NOT NULL
);
