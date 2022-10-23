from typing import Any, Dict, Optional

from loguru import logger
from requests import Response, Session, get


def get_request(
    url: str,
    params: Dict[str, Any],
    request_params: Dict[str, Any],
    session: Optional[Session],
) -> Optional[Response]:
    """A helper method which returns the raw API response.

    Parameters
    ----------
    url : str
        The API url.
    params : Dict[str, Any]
        The parameters for the API request.
    request_params : Dict[str, Any]
        The parameters for the request.
    session : Optional[Session]
        If a session is provided, the request will be made using the session.

    Returns
    -------
    Optional[Response]
        Depending on the success of the request, a Response object or None is returned.
    """
    try:
        if session:
            req = session.get(url, **request_params, params=params)
        else:
            req = get(url, **request_params, params=params)

        if req.status_code != 200:
            logger.error("The API request returned a non 200 status code.")
            logger.debug(f"Request returned: {req.status_code}, {req.text}")

            return None
    except ConnectionError:
        logger.error("Connection error")
        logger.debug(f"url: {url}, params: {params}, request_params: {request_params}")
        return None

    return req
