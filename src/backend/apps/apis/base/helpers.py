import datetime
import decimal
import json
from typing import Optional
from uuid import UUID

import dateutil.parser
import structlog

logger = structlog.get_logger(__name__)


def parse_datetime_from_dict(body: dict, field_name: str) -> Optional[datetime.datetime]:
    dt = body.get(field_name)
    if dt is not None:
        try:
            return dateutil.parser.isoparse(dt).replace(tzinfo=None)
        except (TypeError, ValueError) as e:
            logger.exception(
                f'Failed to convert "{field_name}" field into datetime: {type(e).__name__} {e}, data={body}'
            )
    return None


class CupJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        if isinstance(o, datetime.date):
            return o.isoformat()
        if isinstance(o, UUID):
            return str(o)
        return super(CupJsonEncoder, self).default(o)


def serialize_for_cup(data: dict) -> str:
    return json.dumps(data, cls=CupJsonEncoder)
