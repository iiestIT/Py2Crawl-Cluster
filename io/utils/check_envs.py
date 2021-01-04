from config import ENVs
from exceptions import MissingEnvironmentVariable
import os


async def check_envs():
    for i in ENVs:
        await _raise_if_null(os.environ.get(i), i)


async def _raise_if_null(env, value):
    if not env or len(env) == 0:
        raise MissingEnvironmentVariable(value)
