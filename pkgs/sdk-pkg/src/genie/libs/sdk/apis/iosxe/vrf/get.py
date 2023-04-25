"""Common get info functions for vrf"""

# Python
import logging

# genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def get_vrf_vrfs(device):
    """ Get all vrfs from device

        Args:
            device ('obj'): Device object

        Returns:
            out ('dict'): Vrf dictionary

        Raises:
            None
    """
    log.info(
        "Getting all vrfs on '{dev_name}'".format(dev_name=device.hostname)
    )
    cmd = "show vrf detail"

    try:
        out = device.parse(cmd)
    except SchemaEmptyParserError:
        return False

    return out


def get_vrf_route_distinguisher(device, vrf):
    """ Get default route distinguisher from show command

        Args:
            device ('obj')  : Device object
            vrf ('str')     : VRF value

        Returns:
            route_distinguisher ('str'): Route distinguisher value
            False

        Raises:
            Exception
    """

    log.info(
        "Getting the route distinguisher value for {vrf} on device "
        "{device}".format(vrf=vrf, device=device.name)
    )

    command = "show vrf {vrf}".format(vrf=vrf)

    try:
        output = device.parse(command)
    except SchemaEmptyParserError:
        return False
    except Exception:
        raise Exception(
            "Could not execute parser command " "'{cmd}'".format(cmd=command)
        )

    route_distinguisher = output["vrf"][vrf].get("route_distinguisher")

    log.info(
        "Found route distinguisher {rd} on device {device}".format(
            device=device.name, rd=route_distinguisher
        )
    )

    return route_distinguisher


def get_vrf_interface(device, vrf):
    """ Gets the subinterfaces for vrf

        Args:
            device ('obj'): device to run on
            vrf ('str'): vrf to search under

        Returns:
            interfaces('list'): List of interfaces under specified vrf
            None

        Raises:
            None
    """
    log.info("Getting the interfaces under vrf {vrf}".format(vrf=vrf))

    try:
        out = device.parse("show vrf {vrf}".format(vrf=vrf))
    except SchemaEmptyParserError:
        return None

    if out and "vrf" in out and vrf in out["vrf"]:
        return out["vrf"][vrf].get("interfaces", None)


def get_vrf_route_targets(
    device, address_family, rt_type, vrf=None, route_distinguisher=None
):
    """ Get route target value from a device

        Args:
            address_family ('str'): address family value
            rt_type ('str'): route target type
                ex.) rt_type = 'import' OR
                     rt_type = 'export' OR
                     rt_type = 'both'
            vrf('str'): vrf name
            route_distinguisher ('str'): route distinguisher value

        Returns:
            Route target value
            None

        Raises:
            None
    """

    log.info(
        "Getting route target of type {rt_type} for device {dev_name}".format(
            rt_type=rt_type, dev_name=device.name
        )
    )

    cli_command = ["show vrf detail {vrf}", "show vrf detail"]
    if vrf:
        cmd = cli_command[0].format(vrf=vrf)
    else:
        cmd = cli_command[1]

    try:
        raw_out = device.execute(cmd)
        out = device.parse(cmd, output=raw_out)
    except SchemaEmptyParserError:
        return None

    if not vrf:
        vrf = "default"

    try:
        if not route_distinguisher:
            route_distinguisher = out[vrf]["route_distinguisher"]
        if "multicast" not in raw_out:
            address_family = address_family.split()[0]
        route_targets = out[vrf]["address_family"][address_family][
            "route_targets"
        ][route_distinguisher]

        if (
            route_targets["rt_type"] == rt_type
            or route_targets["rt_type"] == "both"
        ):
            return route_targets["route_target"]

    except KeyError as e:
        return None

    return None
