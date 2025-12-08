""" File utils base class for HTTPS on IOSXE devices. """

from ..fileutils import FileUtils as FileUtilsXEBase

from genie.libs.filetransferutils.plugins.fileutils import HTTPFileUtilsBase

class FileUtils(HTTPFileUtilsBase, FileUtilsXEBase):
    COPY_CONFIG_TEMPLATE = ['ip http client source-interface {interface}']

    COPY_CONFIG_VRF_TEMPLATE = ['ip http client source-interface {interface}']

