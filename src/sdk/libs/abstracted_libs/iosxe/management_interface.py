'''IOSXE implementation of ManagemntInterface class'''

# parser
from genie.libs.parser.iosxe.show_interface import ShowInterfaces

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

        # Calling parser
        parser_obj = ShowInterfaces(device=device)
        parsed_output = parser_obj.parse()

        # Get the corresponding interface name
        interface_name = self.parse_the_name(ipaddress, parsed_output)

        return interface_name
