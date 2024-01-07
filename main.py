import contextlib
from aiogram import Bot, Dispatcher, F
from core.middleware.middleware import DbSession
from aiogram.filters import Command
import asyncpg
import asyncio
import logging


async def create_pool():
    return await asyncpg.create_pool(user='postgres', password='password', database='database', host='127.0.0.1',
                                     port=5432,
                                     command_timeout=60)


async def start_bot():
    bot = Bot(token='token')

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%('
                                                   'funcName)s(%(lineno)d) - %(message)s')

    dp = Dispatcher()
    pool_connect = await create_pool()

    dp.update.middleware.register(DbSession(pool_connect))

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as ex:
        logging.error(f"[!!! Exception] - {ex}", exc_info=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(start_bot())
