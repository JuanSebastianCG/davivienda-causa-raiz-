import logging
from logging.config import dictConfig

from dotenv import find_dotenv
from pydantic_settings import BaseSettings

from .logger import LogConfig


class Config(BaseSettings):
    BASES: dict = {
        "empresas": "Empresas 2da Línea",
        "no_fraude": "No Fraude",
    }

    class Config:
        extra = "allow"
        env_file = find_dotenv()


config = Config()

dictConfig(LogConfig().model_dump())
logger = logging.getLogger("Intention")

logger.info("Configuration finished")
