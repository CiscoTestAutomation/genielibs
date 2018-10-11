'''ManagementInterface class'''

# metaparser
from genie.metaparser.util.exceptions import SchemaEmptyParserError


class ManagementInterface(object):
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

    def get_interface_name(self, ipaddress, parser_obj):
        """Method to return the ip address corresponding interface name

        Args:
            ipaddress (`str`): connection ip address
            parser_obj (`obj`): Os specific parser object

        Returns:
            `str`: a `str` of the interface name

        Examples:
            >>> managment_interface_instance.\
                get_interface_name(ipaddress, parser_obj)

        """

        # Calling parser
        try:
            parsed_output = parser_obj.parse(ip=ipaddress)
        except SchemaEmptyParserError:
            # We are looping over all the ips provided in the testbed yaml file
            # Show command output will be empty in some cases.
            return None

        # Get the corresponding interface name
        for intf in parsed_output['interface'].keys():
            # Parser structure only has one interface
            interface_name = intf

        return interface_name