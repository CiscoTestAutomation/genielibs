""" File utils base class for TFTP on IOSXE devices. """

from ..fileutils import FileUtils as FileUtilsXEBase


class FileUtils(FileUtilsXEBase):
    COPY_CONFIG_TEMPLATE = [
        'ip tftp source-interface {interface}', 'ip tftp blocksize {blocksize}'
    ]

    COPY_CONFIG_VRF_TEMPLATE = [
        'ip tftp source-interface {interface}', 'ip tftp blocksize {blocksize}'
    ]
