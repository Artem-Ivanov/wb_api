import decimal
import secrets
from json import JSONDecodeError
from typing import Any, Optional

import structlog
import requests
from django.conf import settings
from requests.adapters import HTTPAdapter
from requests.auth import HTTPDigestAuth
from urllib3 import Retry

logger = structlog.get_logger(__name__)


class APIError(Exception):
    pass


class ResponseError(APIError):
    def __init__(self, message: str, resp: requests.Response):
        super().__init__(message)
        self.resp = resp


class APIStatusError(ResponseError):
    pass


class APIJsonError(ResponseError):
    pass


class HttpTransport:
    """
    Транспорт в сервисы через HTTP.
    """

    def __init__(
        self,
        connect_timeout: Optional[int] = None,
        read_timeout: Optional[int] = None,
        cert: Optional[tuple[str, str]] = None,
        verify: Optional[bool] = True,
        auth: Optional[HTTPDigestAuth] = None,
    ):
        self.connect_timeout = connect_timeout or settings.HTTP_REQUEST_CONNECT_TIMEOUT_SECONDS
        self.read_timeout = read_timeout or settings.HTTP_REQUEST_READ_TIMEOUT_SECONDS
        retry_strategy = Retry(
            total=3, status_forcelist=[500, 502, 503, 504], backoff_factor=0.2
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        self._retrying_session = session
        self._session = requests.Session()

        if cert is not None:
            self._session.cert = cert
            self._retrying_session.cert = cert

        if not verify:
            self._session.verify = verify
            self._retrying_session.verify = verify

        if auth is not None:
            self._session.auth = auth
            self._retrying_session.auth = auth

    def get_session(self, should_retry: bool) -> requests.Session:
        if should_retry:
            return self._retrying_session
        return self._session

    def get(self, url: str, token: str, params: dict = None, **kwargs) -> requests.Response:
        session = self.get_session(should_retry=kwargs.pop("should_retry", False))
        try:
            resp = session.get(
                url=url,
                headers={'Authorization': token},
                params=params,
                **kwargs,
                verify=False,
            )
        except Exception as e:
            raise APIError(f"Request to {url} failed. Params: {kwargs}, error: {e}") from e

        logger.info("HTTP_GET_RESPONSE", url=url, params=kwargs.get("params", ""), status=resp.status_code)
        if resp.status_code >= requests.codes.multiple_choices:
            logger.info(
                "HTTP_GET_RESPONSE_BODY", url=url, params=kwargs.get("params", ""), body=resp.content
            )
        return resp

    def post(self, url: str, token: str, **kwargs) -> requests.Response:
        session = self.get_session(should_retry=kwargs.pop("should_retry", False))
        http_request_id = secrets.token_hex(2)
        request_body = kwargs.get("json", kwargs.get("data", ""))
        logger.info(
            f"[HTTP>>] {http_request_id} POST url={url} "
            f"params={kwargs.get('params', '')} "
            f"body={request_body}"
        )
        try:
            resp = session.post(
                url=url,
                headers={'Authorization': token},
                **kwargs,
                verify=False,
            )
        except Exception as e:
            raise APIError(f"Request to {url} failed. Params: {kwargs}, error: {type(e).__name__}: {e}") from e

        msg = f"[HTTP<<] {http_request_id} POST url={url} status={resp.status_code}"
        if resp.status_code >= requests.codes.multiple_choices:
            logger.info(f"{msg} body={resp.content}")
        return resp

    def put(self, url: str, token: str, **kwargs) -> requests.Response:
        session = self.get_session(should_retry=kwargs.pop("should_retry", False))
        http_request_id = secrets.token_hex(2)
        request_body = kwargs.get("json", kwargs.get("data", ""))
        logger.info(
            f"[HTTP>>] {http_request_id} PUT url={url} "
            f"params={kwargs.get('params', '')} "
            f"body={request_body}"
        )
        try:
            resp = session.post(
                url=url,
                headers={'Authorization': token},
                **kwargs,
                verify=False,
            )
        except Exception as e:
            raise APIError(f"Request to {url} failed. Params: {kwargs}, error: {type(e).__name__}: {e}") from e

        msg = f"[HTTP<<] {http_request_id} POST url={url} status={resp.status_code}"
        if resp.status_code >= requests.codes.multiple_choices:
            logger.info(f"{msg} body={resp.content}")
        return resp

    def decode_json(self, resp: requests.Response) -> Any:
        """
        Декодировать ответ как json.
        """
        url = resp.url
        try:
            json_response = resp.json(parse_float=decimal.Decimal)
        except (requests.JSONDecodeError, JSONDecodeError) as e:
            raise APIJsonError(
                f"Bad json, {url=}, request={resp.request.body}, "
                f"status={resp.status_code}, content={resp.content}",
                resp,
            ) from e
        return json_response

    def check_status(self, resp: requests.Response):
        url = resp.url
        try:
            resp.raise_for_status()
        except Exception as e:
            raise APIStatusError(
                f"Request failed: {url=}, status={resp.status_code}, content={resp.content}", resp
            ) from e
