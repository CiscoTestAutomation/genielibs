""" File utils base class for SCP on IOSXE devices. """

from ..fileutils import FileUtils as FileUtilsXEBase


class FileUtils(FileUtilsXEBase):
    COPY_CONFIG_TEMPLATE = ['ip scp source-interface {interface}']

    COPY_CONFIG_VRF_TEMPLATE = ['ip scp source-interface {interface}']
