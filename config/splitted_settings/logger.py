from loguru import logger

logger.add(
    "logs/app.log",
    format="{time:YYYY-MM-DD HH:mm:ss} {level} [{name}:{line}] {message}",
    # serialize=True,
)

