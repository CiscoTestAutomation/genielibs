'''Junos implementation of ManagementInterface class'''

# parser
from genie.libs.parser.junos.show_interface import ShowInterfacesTerse

# ManagementInterface
from ..management_interface import ManagementInterface as ManagementInterface_main


class ManagementInterface(ManagementInterface_main):
    """ManagementInterface class

    `ManagementInterface` class the functionality to retrieve the given ip
    address corresponding interface name.

    Args:
            `None`

    Returns:
            an `interafce_name` string

    Examples:
        # Creating an instnace of ManagementInterface
        managment_interface_instance = lookup.sdk.libs.abstracted_libs.\
            management_interface.ManagementInterface()

        >>> managment_interface_instance = lookup.sdk.libs.\
            abstracted_libs.management_interface.ManagementInterface()
            <genie.libs.sdk.libs.abstracted_libs.nxos.management_interface.\
            ManagementInterface object at 0xf5a73a2c>

    """

    def get_interface_name(self, device, ipaddress):
        """Method to return the ip address corresponding interface name

        Args:
            device (`Device`): Genie device object
            ipaddress (`str`): connection ip address

        Returns:
            `str`: a `str` of the interface name

        Examples:
            >>> managment_interface_instance.\
                get_interface_name(device, ipaddress)

        """

        # Create parser object
        parser_obj = ShowInterfacesTerse(device=device)
        try:
            parsed_output = parser_obj.parse(interface='fxp0')
        except SchemaEmptyParserError:
            # We are looping over all the ips provided in the testbed yaml file
            # Show command output will be empty in some cases.
            return None

        # Get the corresponding interface name
        for intf in parsed_output.keys():
            # Parser structure only has one interface
            if parsed_output.get(intf, {}).get('protocol', {}).get('inet', {}).keys() or \
               parsed_output.get(intf, {}).get('protocol', {}).get('inet6', {}).keys():
                return intf
