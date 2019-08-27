"""Common get functions for VIRL STD"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def get_simulations(device, connection_alias="rest"):
    """Get simulations list

        Args:
            device (`obj`): Device object
            connection_alias (`str`): connection alias

        Returns:
            list: list of simulation names
        
        Raise:
            None
    """
    try:
        device.connect(via=connection_alias)
    except Exception as e:
        log.info("Failed to connect to device {}: {}".format(device.name, e))

    try:
        out = device.get("/simengine/rest/list")
    except Exception as e:
        log.info("Failed to get simulation list: {}".format(e))

    sim_list = []
    for sim in out.get("simulations", {}).keys():
        sim_list.append(sim)

    return sim_list


def get_node_summary(device, simulation_name, connection_alias="rest"):
    """Get node summary

        Args:
            device (`obj`): Device object
            simulation_name (`str`): simulation name
            connection_alias (`str`): connection alias

        Returns:
            dict: node summary info
        
        Raise:
            None
    """
    try:
        device.connect(via=connection_alias)
    except Exception as e:
        log.info("Failed to connect to device {}: {}".format(device.name, e))

    try:
        out = device.get("/simengine/rest/nodes/{}".format(simulation_name))
    except Exception as e:
        log.info("Failed to get node summary: {}".format(e))

    nodes = out[simulation_name]
    return nodes


def get_node_list(device, simulation_name):
    """Get node list

        Args:
            device (`obj`): Device object
            simulation_name: simulation name

        Returns:
            list: node list
        
        Raise:
            None
    """
    nodes = get_node_summary(device, simulation_name)
    return nodes.keys()
