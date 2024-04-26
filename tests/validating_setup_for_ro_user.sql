--- Creating table
CREATE TABLE todos (id SERIAL PRIMARY KEY, title VARCHAR(255) NOT NULL);

--- Testing write operation
INSERT INTO todos (title) VALUES ('Learn basic SQL syntax');

--- Updating table
ALTER TABLE public.todos ADD COLUMN completed BOOLEAN NOT NULL DEFAULT false;


--- Updating a record
UPDATE todos SET completed = true;

--- Testing write operation
INSERT INTO todos (title,completed) VALUES ('Practice writing SELECT queries', false);


ALTER TABLE todos OWNER TO test_ro_user;
