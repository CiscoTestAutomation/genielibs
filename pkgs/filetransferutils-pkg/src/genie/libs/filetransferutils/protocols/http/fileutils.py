""" 
Implementation for http File Utilities. 
"""

import requests
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
        try:
            data = requests.head(url=target, timeout=timeout_seconds)
            file_size = data.headers.get('Content-Length')
        except Exception as e:
            raise Exception("Failed to get the file size from http server. Error: {e}")

        result = AttrDict()
        # Construct st_size
        result.st_size = int(file_size)

        return result

