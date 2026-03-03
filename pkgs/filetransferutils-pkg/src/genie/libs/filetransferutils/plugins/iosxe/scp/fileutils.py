""" File utils base class for SCP on IOSXE devices. """

from ..fileutils import FileUtils as FileUtilsXEBase


class FileUtils(FileUtilsXEBase):
    COPY_CONFIG_TEMPLATE = ['ip ssh source-interface {interface}', 'no ip ssh stricthostkeycheck']

    COPY_CONFIG_VRF_TEMPLATE = ['ip ssh source-interface {interface}', 'no ip ssh stricthostkeycheck']
