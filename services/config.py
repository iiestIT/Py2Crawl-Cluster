import os

ENVs = [
    "REDIS_HOSTNAME", "REDIS_PORT", "REDIS_PASSWORD"
]


class BaseConfig:
    REDIS_HOSTNAME = os.environ.get("REDIS_HOSTNAME")
    REDIS_PORT = int(os.environ.get("REDIS_PORT"))
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")
