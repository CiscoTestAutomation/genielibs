"""Implementation for HTTP file utilities."""

import logging

import requests
from requests.exceptions import RequestException
from pyats.datastructures import AttrDict
from genie.libs.filetransferutils.bases.fileutils import (
    redact_url_credentials,
)
from genie.libs.filetransferutils.fileutils import FileUtils as FileUtilsLinuxBase

logger = logging.getLogger(__name__)


def _response_details(response):
    """Return useful, credential-safe details for an HTTP response."""
    if response is None:
        return "no response received"

    headers = {}
    for name in (
        "Content-Length",
        "Content-Range",
        "Content-Type",
        "Location",
        "Server",
        "WWW-Authenticate",
    ):
        value = response.headers.get(name)
        if value is not None:
            headers[name] = redact_url_credentials(str(value))

    details = [
        "status={}".format(response.status_code),
        "reason={!r}".format(response.reason),
        "url={}".format(redact_url_credentials(response.url)),
    ]
    if headers:
        details.append("headers={!r}".format(headers))
    return ", ".join(details)


class FileUtils(FileUtilsLinuxBase):
    """ 
    FileUtils http implementation.
    """

    def stat(self, target, timeout_seconds, *args, **kwargs):
        """ Retrieve file size.

        Parameters
        ----------
            target : `str`
                The URL of the file whose details are to be retrieved.

            timeout_seconds : `int`
                The number of seconds to wait before aborting the operation.

        Returns
        -------
            `os.stat_result` : Filename details including size.
        """
        file_size = None
        response = None
        get_response = None
        get_error = None

        try:
            response = requests.head(
                url=target,
                timeout=timeout_seconds,
                allow_redirects=True,
                verify=False  # ignore ssl errors
            )
            response.raise_for_status()
            file_size = response.headers.get('Content-Length')
        except RequestException as exc:
            details = _response_details(response)
            logger.error(
                "HTTP HEAD request failed while getting file size: %s; "
                "error=%s",
                details,
                redact_url_credentials(str(exc)),
            )
            raise Exception(
                "Failed to get the file size from http server for "
                f"{redact_url_credentials(target)}. Error: "
                f"{redact_url_credentials(str(exc))}. Response: {details}"
            ) from None

        # Some HTTP servers respond to HEAD (especially after redirects) with
        # Content-Length: 0. As a fallback, do a ranged GET to retrieve the
        # total size via Content-Range, without downloading the whole file.
        if not file_size or str(file_size) == '0':
            try:
                get_response = requests.get(
                    url=target,
                    timeout=timeout_seconds,
                    stream=True,
                    allow_redirects=True,
                    headers={'Range': 'bytes=0-0'},
                    verify=False  # ignore ssl errors
                )
                get_response.raise_for_status()

                content_range = get_response.headers.get('Content-Range')
                if content_range and '/' in content_range:
                    maybe_total = content_range.split('/')[-1].strip()
                    if maybe_total.isdigit():
                        file_size = maybe_total
                if not file_size or str(file_size) == '0':
                    file_size = get_response.headers.get('Content-Length')
            except RequestException as exc:
                get_error = exc
                details = _response_details(get_response)
                logger.warning(
                    "HTTP range GET request failed while getting file size: "
                    "%s; error=%s",
                    details,
                    redact_url_credentials(str(exc)),
                )
            finally:
                if get_response is not None:
                    get_response.close()

        if (not file_size or str(file_size) == '0' or
                not str(file_size).isdigit()):
            details = _response_details(get_response)
            head_details = _response_details(response)
            error_details = " HEAD response: {}".format(head_details)
            log_error_details = ""
            if get_error is not None:
                error_details += " Range GET error: {}. Response: {}".format(
                    redact_url_credentials(str(get_error)), details)
                log_error_details = " Range GET error: {}. Response: {}".format(
                    redact_url_credentials(str(get_error)), details)
            logger.error(
                "Unable to determine HTTP file size for %s. HEAD response: %s.%s",
                redact_url_credentials(target),
                head_details,
                log_error_details,
            )
            raise Exception(
                "Unable to determine file size from http server for "
                f"{redact_url_credentials(target)}."
                f"{error_details}"
            )

        result = AttrDict()
        # Construct st_size
        result.st_size = int(file_size)

        return result
