import logging
from typing import Any, Dict, Optional

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
    url : Optional[str]
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
            logging.error("The API request returned a non 200 status code.")
            logging.debug("Request returned: %s, %s", req.status_code, req.text)

            return None
    except ConnectionError:
        logging.error("Connection error")
        logging.debug("url: %s, params: %s, request_params: %s", url, params, request_params)
        return None

    return req
