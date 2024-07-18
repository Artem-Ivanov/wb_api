# Logger settings
import contextlib
import json
from time import time

import structlog
from structlog.contextvars import bind_contextvars, clear_contextvars
from structlog.threadlocal import merge_threadlocal

import settings


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "kafka": {
            "level": "ERROR",
            "handlers": ["console"],
        },
        "django.db.backends": {
            "level": "ERROR",
            "handlers": ["console"],
        },
    },
}


def json_serializer(obj, **kwargs):
    kwargs.pop("ensure_ascii", None)
    return json.dumps(obj, ensure_ascii=False, **kwargs)


def _rename_event_key(logger, method_name, event_dict):
    event_dict["message"] = event_dict.pop("event")
    return event_dict


processors = [
    merge_threadlocal,
    structlog.stdlib.filter_by_level,
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
    _rename_event_key,
]

if settings.DEBUG:
    processors.append(structlog.dev.ConsoleRenderer(event_key="message", pad_event=100))
else:
    processors.append(
        structlog.processors.JSONRenderer(sort_keys=True, serializer=json_serializer)
    )

structlog.configure(
    processors=processors,
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.getLogger(__name__)


def bind_process_id_to_log(process_id: str) -> None:
    clear_contextvars()
    bind_contextvars(process_id=process_id)


@contextlib.contextmanager
def duration_context(message: str, **kwargs):
    start = time()
    yield start
    logger.info(message, duration=(time() - start), **kwargs)
