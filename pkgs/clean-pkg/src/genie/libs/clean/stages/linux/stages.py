"""
Linux specific clean stages
"""

# Logger
import logging
log = logging.getLogger(__name__)

# Genie
from genie.libs.clean.stages.stages import ConfigureInterfaces as BaseConfigureInterfaces


class ConfigureInterfaces(BaseConfigureInterfaces):
    """Linux-specific ConfigureInterfaces stage.

    Linux devices do not have a 'configure terminal' mode, so configuration
    lines are sent one at a time via execute() (shell commands via iproute2).
    """

    def _apply_configuration_lines(self, device, configuration_lines):
        for line in configuration_lines:
            device.execute(line)
