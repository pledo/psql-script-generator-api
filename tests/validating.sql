--- Creating table
CREATE TABLE todos (id SERIAL PRIMARY KEY, title VARCHAR(255) NOT NULL);

--- Testing write operation
INSERT INTO todos (title) VALUES ('Learn basic SQL syntax');

--- Reading data operation
SELECT * FROM todos;

--- Updating table
ALTER TABLE public.todos ADD COLUMN completed BOOLEAN NOT NULL DEFAULT false;


--- Updating a record
UPDATE todos SET completed = true;

--- Testing read operation
SELECT * FROM todos;

--- Testing write operation
INSERT INTO todos (title,completed) VALUES ('Practice writing SELECT queries', false);


--- Testing delete operation
DELETE from todos where completed = false ;

--- Testing read operation
SELECT * FROM todos;

--- Drop table
DROP TABLE todos;
