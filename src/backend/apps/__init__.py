import contextlib
from time import time

import structlog
from structlog.contextvars import bind_contextvars, clear_contextvars


logger = structlog.getLogger(__name__)


def bind_process_id_to_log(process_id: str) -> None:
    clear_contextvars()
    bind_contextvars(process_id=process_id)


@contextlib.contextmanager
def duration_context(message: str, **kwargs):
    start = time()
    yield start
    logger.info(message, duration=(time() - start) * 1000, **kwargs)
