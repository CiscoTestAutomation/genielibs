"""Common configure functions for OSPF"""

# Python
import logging

# Genie
from genie.libs.parser.utils.common import Common

# Unicon
from unicon.core.errors import SubCommandFailure

# Ospf
from genie.libs.sdk.apis.iosxe.ospf.get import (
    get_router_ospf_section_running_config,
)

from genie.libs.sdk.apis.utils import has_configuration

log = logging.getLogger(__name__)


def configure_ospf_max_metric_router_lsa_on_startup(
    device, ospf_process_id, metric_value
):
    """Configure max-metric router-lsa on start-up

        Args:
            device (`obj`): Device object
            ospf_process_id (`int`): OSPF process id
            metric_value (`int`): Metric value to be configured

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    cfg_cmd = [
        "router ospf {}".format(ospf_process_id),
        "max-metric router-lsa on-startup {}".format(metric_value),
    ]

    try:
        device.configure(cfg_cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring max-metric {metric_value}"
            " on device {device}, Error: {error}".format(
                metric_value=metric_value, device=device, error=e
            )
        ) from e


def configure_shut_ospf(device, ospf_process_id):
    """ Configure shut on ospf process

        Args:
            device (`obj`): device to execute on
            ospf_process_id (`int`): ospf process number

        Return:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        'Configuring "shutdown" on "router ospf {}"'.format(ospf_process_id)
    )
    try:
        device.configure("router ospf {}\n" "shutdown".format(ospf_process_id))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Failed in configuring "shutdown" with '
            "ospf process {ospf_process} on device {device}, "
            "Error: {error}".format(
                ospf_process=ospf_process_id, device=device, error=e
            )
        ) from e


def configure_no_shut_ospf(device, ospf_process_id):
    """ Configure no shut on ospf process

        Args:
            device (`obj`): device to execute on
            ospf_process_id (`int`): ospf process number

        Return:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        'Configuring "no shutdown" on "router ospf {}"'.format(ospf_process_id)
    )
    try:
        device.configure(
            "router ospf {}\n" "no shutdown".format(ospf_process_id)
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Failed in configuring "no shutdown" with '
            "ospf process {ospf_process} on device {device}, "
            "Error: {error}".format(
                ospf_process=ospf_process_id, device=device, error=e
            )
        ) from e


def remove_ospf_max_metric_configuration(device, ospf_process_id):
    """ Remove max-metric from running-config under ospf

        Args:
            device (`obj`): Device object 
            ospf_process_id (`str`): Router OSPF id

        Return:
            None
            
        Raises:
            SubCommandFailure
    """

    section_dict = get_router_ospf_section_running_config(
        device=device, ospf_process_id=ospf_process_id
    )
    if section_dict:
        if has_configuration(
            configuration_dict=section_dict,
            configuration="max-metric router-lsa",
        ):
            try:
                device.configure(
                    [
                        "router ospf {ospf_process_id}".format(
                            ospf_process_id=ospf_process_id
                        ),
                        "no max-metric router-lsa",
                    ]
                )
            except SubCommandFailure as e:
                raise SubCommandFailure(
                    "Failed in removing max-metric from "
                    "running-config under ospf {ospf_process_id} on device {device}, "
                    "Error: {e}".format(
                        ospf_process_id=ospf_process_id,
                        device=device.name,
                        e=str(e),
                    )
                ) from e
    else:
        raise Exception(
            "Router OSPD id {ospf_process_id} is not "
            "configured in device {device}".format(
                ospf_process_id=ospf_process_id, device=device.name
            )
        )


def configure_ospf_passive_interface(device, interface, ospf_process_id):
    """Configure passive interface

        Args:
            device (`obj`): Device object
            ospf_process_id (`int`): ospf process id
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'

        Return:
            None
            
        Raises:
            SubCommandFailure
    """

    config = []
    config.append("router ospf {}".format(ospf_process_id))
    config.append(
        "passive-interface {}".format(Common.convert_intf_name(interface))
    )
    try:
        device.configure("\n".join(config))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in configuring passive interface {interface} "
            "with OSPF process id {ospf_process_id} on device {device}, "
            "Error: {e}".format(
                interface=interface,
                ospf_process_id=ospf_process_id,
                device=device.name,
                e=str(e),
            )
        ) from e


def remove_ospf_passive_interface(device, interface, ospf_process_id):
    """Remove passive interface

        Args:
            device (`obj`): Device object
            ospf_process_id (`int`): OSPF process id
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'

        Return:
            None
            
        Raises:
            SubCommandFailure
    """

    config = []
    config.append("router ospf {}".format(ospf_process_id))
    config.append(
        "no passive-interface {}".format(Common.convert_intf_name(interface))
    )
    try:
        device.configure("\n".join(config))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed in removing passive interface {interface}"
            "with OSPF process id {ospf_process_id}"
            " on device {device}, Error: {e}".format(
                interface=interface,
                ospf_process_id=ospf_process_id,
                device=device.name,
                e=str(e),
            )
        ) from e


def configure_ospf_cost(device, interface, ospf_cost):
    """configure ospf cost

        Args:
            device (`obj`): Device object
            ospf_cost (`int`): Ospf cost value
            interface (`str`): interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'

        Return:
            None
            
        Raises:
            SubCommandFailure
    """
    config = []
    config.append("interface {}".format(interface))
    config.append("ip ospf cost {}".format(ospf_cost))
    try:
        device.configure("\n".join(config))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Ospf cost {ospf_cost} is not configured on device"
            " {device} for interface {interface}".format(
                ospf_cost=ospf_cost, device=device, interface=interface
            )
        ) from e
