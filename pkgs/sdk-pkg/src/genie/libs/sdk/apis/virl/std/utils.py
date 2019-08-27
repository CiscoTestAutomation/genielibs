"""Common utils functions for VIRL STD"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def launch_simulation(
    device, simulation_name, simulation_data, connection_alias="rest"
):
    """launch simulation

        Args:
            device (`obj`): Device object
            simulation_name (`str`): simulation name
            simulation_data (`str`): simulation data 
            connection_alias (`str`): connection_alias

        Returns:
            result: result of launching simulation
        
        Raise:
            None
    """
    try:
        device.connect(via=connection_alias)
    except Exception as e:
        log.info("Failed to connect to device {}: {}".format(device.name, e))

    try:
        out = device.post(
            "/simengine/rest/launch?session={}".format(simulation_name),
            simulation_data,
        )
    except Exception as e:
        out = e

    return out


def stop_simulation(device, simulation_name, connection_alias="rest"):
    """Stop simulation

        Args:
            device (`obj`): Device object
            simulation_name ('str'): simulation name
            connection_alias (`str`): connection alias

        Returns:

            result: result of GET command
        
        Raise:
            None
    """
    try:
        device.connect(via=connection_alias)
    except Exception as e:
        log.info("Failed to connect to device {}: {}".format(device.name, e))

    try:
        out = device.get("/simengine/rest/stop/{}".format(simulation_name))
    except Exception as e:
        out = e

    return out
