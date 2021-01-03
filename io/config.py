import os

ENVs = [
    "REDIS_HOSTNAME", "REDIS_PORT", "REDIS_PASSWORD", "CONTROLLER_PORT"
]


class BaseConfig:
    REDIS_HOSTNAME = os.environ.get("REDIS_HOSTNAME", "localhost")
    REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

    CONTROLLER_PORT = int(os.environ.get("CONTROLLER_PORT", "8080"))
