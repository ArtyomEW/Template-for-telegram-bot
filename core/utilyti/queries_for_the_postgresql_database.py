import asyncpg


class Request:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def add_data(self, user_id, first_name, last_name, user_name, statuse):
        query = f"INSERT INTO datausers (user_id, first_name,last_name,user_name,statuse) " \
                f"VALUES ({user_id}, '{first_name}', '{last_name}','{user_name}', '{statuse}') ON CONFLICT (" \
                f"user_id) " \
                f"DO UPDATE SET first_name= '{first_name}' , last_name='{last_name}', user_name='{user_name}', " \
                f"statuse='{statuse}' "
        await self.connector.execute(query)

    """Проверяем есть ли такая таблица"""

    async def check_table(self, name_table):
        query = f"SELECT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = '{name_table}');"
        return await self.connector.fetchval(query)

    """Создаём таблицу"""

    async def create_table(self, name_table):
        query = f"CREATE TABLE {name_table} (user_id bigint NOT NULL,status text,description text," \
                "PRIMARY KEY (user_id)); "
        await self.connector.execute(query)
        query = f"INSERT INTO {name_table} (user_id, status, description) SELECT user_id, 'waiting', null FROM " \
                f"datausers WHERE statuse='member' "
        await self.connector.execute(query)

    """Удаляем таблицу"""

    async def delete_table(self, name_table):
        query = f"DROP TABLE {name_table};"
        await self.connector.execute(query)
