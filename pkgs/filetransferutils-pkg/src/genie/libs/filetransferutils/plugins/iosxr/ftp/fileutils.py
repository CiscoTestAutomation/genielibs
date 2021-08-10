""" File utils base class for FTP on IOSXR devices. """

from ..fileutils import FileUtils as FileUtilsXRBase


class FileUtils(FileUtilsXRBase):
    COPY_CONFIG_TEMPLATE = ['ftp client source-interface {interface}']

    COPY_CONFIG_VRF_TEMPLATE = [
        'ftp client vrf {vrf} source-interface {interface}'
    ]
