from aiogram import Bot
from Settings import settings


async def start_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, 'Бот запущен')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, 'Бот остановлен')
