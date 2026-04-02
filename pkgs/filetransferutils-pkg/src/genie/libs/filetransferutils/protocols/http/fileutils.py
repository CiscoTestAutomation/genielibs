""" 
Implementation for http File Utilities. 
"""

import requests
from requests.exceptions import RequestException
from pyats.datastructures import AttrDict
from genie.libs.filetransferutils.fileutils import FileUtils as FileUtilsLinuxBase

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

        try:
            response = requests.head(
                url=target,
                timeout=timeout_seconds,
                allow_redirects=True,
            )
            response.raise_for_status()
            file_size = response.headers.get('Content-Length')
        except RequestException as exc:
            raise Exception(
                f"Failed to get the file size from http server for {target}. Error: {exc}"
            ) from exc

        # Some HTTP servers respond to HEAD (especially after redirects) with
        # Content-Length: 0. As a fallback, do a ranged GET to retrieve the
        # total size via Content-Range, without downloading the whole file.
        if not file_size or str(file_size) == '0':
            get_response = None
            try:
                get_response = requests.get(
                    url=target,
                    timeout=timeout_seconds,
                    stream=True,
                    allow_redirects=True,
                    headers={'Range': 'bytes=0-0'},
                )
                get_response.raise_for_status()

                content_range = get_response.headers.get('Content-Range')
                if content_range and '/' in content_range:
                    maybe_total = content_range.split('/')[-1].strip()
                    if maybe_total.isdigit():
                        file_size = maybe_total
                if not file_size or str(file_size) == '0':
                    file_size = get_response.headers.get('Content-Length')
            except RequestException:
                # Best-effort fallback only; if it fails, we use what we already have.
                pass
            finally:
                if get_response is not None:
                    get_response.close()

        if not file_size or not str(file_size).isdigit():
            raise Exception(f"Unable to determine file size from http server for {target}.")

        result = AttrDict()
        # Construct st_size
        result.st_size = int(file_size)

        return result

