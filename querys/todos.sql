CREATE TABLE IF NOT EXISTS todos(
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            item VARCHAR(255) NOT NULL
        )

INSERT INTO todos(item)
VALUES ('learn SQL'), ('한글'), ('서울시');

SELECT id, todos item 
FROM todos
WHERE id = '1e53cd80-c89f-4795-940f-3a4ef36853cb';
SELECT id, todos item FROM todos;

UPDATE todos
SET item ='learn adavanced sql'
WHERE id = '1e53cd80-c89f-4795-940f-3a4ef36853cb';

DELETE FROM todos
WHERE id = '1e53cd80-c89f-4795-940f-3a4ef36853cb';



