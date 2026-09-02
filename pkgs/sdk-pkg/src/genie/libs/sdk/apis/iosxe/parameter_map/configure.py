"""Common configure functions for parameter-map type inspect"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_parameter_map_type_inspect(
        device,
        name,
        log_dropped_packets=True):
    """ Configure 'parameter-map type inspect' (ZBFW)

        Args:
            device ('obj'): Device object
            name ('str'): Parameter-map name (e.g. 'global', 'log_param')
            log_dropped_packets ('bool', optional): Enable 'log
                dropped-packets'. Defaults to True
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"parameter-map type inspect {name}"]
    if log_dropped_packets:
        cmd.append("log dropped-packets")
    log.debug(f"Configuring parameter-map type inspect {name}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure parameter-map type inspect "
            f"{name}. Error:\n{e}"
        )


def unconfigure_parameter_map_type_inspect(
        device,
        name,
        log_dropped_packets=None,
        remove_parameter_map=True):
    """ Unconfigure 'parameter-map type inspect' (ZBFW)

        Args:
            device ('obj'): Device object
            name ('str'): Parameter-map name (e.g. 'global', 'log_param')
            log_dropped_packets ('bool', optional): Remove only the 'log
                dropped-packets' setting when True. Defaults to None
            remove_parameter_map ('bool', optional): Also delete the
                parameter-map with 'no parameter-map type inspect ...'.
                Defaults to True
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = []
    if log_dropped_packets:
        cmd.extend([
            f"parameter-map type inspect {name}",
            "no log dropped-packets",
            "exit",
        ])
    if remove_parameter_map:
        cmd.append(f"no parameter-map type inspect {name}")
    log.debug(f"Unconfiguring parameter-map type inspect {name}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure parameter-map type inspect "
            f"{name}. Error:\n{e}"
        )
