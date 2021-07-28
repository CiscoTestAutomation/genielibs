""" File utils base class for HTTP on IOSXE devices. """

from ..fileutils import FileUtils as FileUtilsXEBase


class FileUtils(FileUtilsXEBase):
    COPY_CONFIG_TEMPLATE = ['ip http client source-interface {interface}']

    COPY_CONFIG_VRF_TEMPLATE = ['ip http client source-interface {interface}']
