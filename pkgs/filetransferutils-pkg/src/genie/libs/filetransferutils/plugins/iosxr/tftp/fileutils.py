""" File utils base class for TFTP on IOSXR devices. """

from ..fileutils import FileUtils as FileUtilsXRBase


class FileUtils(FileUtilsXRBase):
    COPY_CONFIG_TEMPLATE = ['tftp client source-interface {interface}']

    COPY_CONFIG_VRF_TEMPLATE = [
        'tftp client vrf {vrf} source-interface {interface}'
    ]
