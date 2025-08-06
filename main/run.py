from main import dp
from main import bot
import asyncio
from database import init_db


async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
