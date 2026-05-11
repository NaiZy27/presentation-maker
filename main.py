import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from core.config import config
from core.logger import setup_logging, get_logger
from bot.handlers import router

logger = get_logger(__name__)


async def main() -> None:
    setup_logging()
    logger.info("Starting bot...")

    redis = Redis.from_url(str(config.redis_url))
    storage = RedisStorage(redis)
    bot = Bot(token=config.tg_bot_token.get_secret_value())
    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    logger.info("Bot started, polling...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
