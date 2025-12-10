""" File utils base class for HTTPS on IOSXR devices. """

from ..fileutils import FileUtils as FileUtilsXRBase

from genie.libs.filetransferutils.plugins.fileutils import HTTPFileUtilsBase


class FileUtils(HTTPFileUtilsBase, FileUtilsXRBase):
    COPY_CONFIG_TEMPLATE = ['http client source-interface ipv4 {interface}']

    COPY_CONFIG_VRF_TEMPLATE = ['http client vrf {vrf}', 'http client source-interface ipv4 {interface}']
