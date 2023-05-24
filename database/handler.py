from .conn import run


async def add_user(full_name, phone, age):
    con = await run()
    await con.execute('''
        insert into users(full_name, phone, age) values 
        ($1, $2, $3)
    ''', full_name, phone, age)
