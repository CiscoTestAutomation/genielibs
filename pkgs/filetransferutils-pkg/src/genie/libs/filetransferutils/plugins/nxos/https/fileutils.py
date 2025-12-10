""" File utils base class for SCP on NXOS devices. """

from ..fileutils import FileUtils as FileUtilsNXBase

from genie.libs.filetransferutils.plugins.fileutils import HTTPFileUtilsBase

class FileUtils(HTTPFileUtilsBase, FileUtilsNXBase):
    ...
