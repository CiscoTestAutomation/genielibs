""" File utils base class for HTTP on IOSXR devices. """

from ..fileutils import FileUtils as FileUtilsXRBase


class FileUtils(FileUtilsXRBase):
    COPY_CONFIG_TEMPLATE = ['http client source-interface ipv4 {interface}']

    COPY_CONFIG_VRF_TEMPLATE = ['http client vrf {vrf}', 'http client source-interface ipv4 {interface}']
