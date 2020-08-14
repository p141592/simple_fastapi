import logging
import time

from starlette.requests import Request

from core.settings import settings

logging.config.fileConfig(settings.LOGGING_CONFIG, disable_existing_loggers=False)

logger = logging.getLogger(__name__)


def middlewares(func):
    def wrap(*args, **kwargs):
        app = func(*args, **kwargs)

        @app.middleware("http")
        async def log_requests(request: Request, call_next):
            logger.info(f"start request path={request.url.path}")
            start_time = time.time()

            response = await call_next(request)

            process_time = (time.time() - start_time) * 1000
            formatted_process_time = '{0:.2f}'.format(process_time)
            logger.info(f"completed_in={formatted_process_time}ms status_code={response.status_code}")

            return response

    return wrap
