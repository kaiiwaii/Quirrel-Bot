import asyncpg

class Database:
    def __init__(self, config):
        self.config = config
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(**self.config)
        schema = open("schema/schema.sql", "r").read()
        async with self.pool.acquire() as con:
            #await con.execute("DROP table market")
            #await con.execute("drop table users")
            #await con.execute("drop table warns")
            await con.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
            #await con.execute("DROP EXTENSION fuzzystrmatch")
            await con.execute(schema)
            await con.execute("INSERT INTO market (name, price, description) VALUES ('Brújula caprichosa', '50', 'Te guiará en el camino')")