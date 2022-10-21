from typing import Any

from loguru import logger
from requests import Session, get
from requests.models import Response


def get_request(
    url: str,
    params: dict[str, Any],
    request_params: dict[str, Any],
    session: Session | None,
) -> Response | None:
    """A helper method which returns the raw API response.

    Parameters
    ----------
    url : str
        The API url.
    params : dict[str, Any]
        The parameters for the API request.
    request_params : dict[str, Any]
        The parameters for the request.
    session : Session | None
        If a session is provided, the request will be made using the session.

    Returns
    -------
    Response | None
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
