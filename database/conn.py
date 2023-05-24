import asyncpg

async def run():
    con = await asyncpg.connect(
        user='postgres',
        password='postgres',
        database='p12tgbot',
        host='localhost'
    )
    return con
