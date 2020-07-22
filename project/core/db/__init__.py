from gino_starlette import Gino

from core.settings import settings

db = Gino(
    dsn=settings.DB_DSN,
    pool_min_size=settings.DB_POOL_MIN_SIZE,
    pool_max_size=settings.DB_POOL_MAX_SIZE,
    echo=settings.DB_ECHO,
    ssl=settings.DB_SSL,
    use_connection_for_request=settings.DB_USE_CONNECTION_FOR_REQUEST,
    retry_limit=settings.DB_RETRY_LIMIT,
    retry_interval=settings.DB_RETRY_INTERVAL,
)
