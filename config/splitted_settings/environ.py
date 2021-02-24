"""Read .env file"""
import environ

env = environ.Env(
    DEBUG=(bool, False),
    CI=(bool, False),
)

environ.Env.read_env('./.env')                  # reading .env file

__all__ = [
    env,
]
