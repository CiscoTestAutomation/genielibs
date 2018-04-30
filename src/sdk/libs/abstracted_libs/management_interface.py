'''ManagemntInterface class'''

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

    def parse_the_name(self, ipaddress, output):
        """Method to identify the interface name from the output dictionary
        using the given ip address

        Args:
            ipaddress (`str`): connection ip address
            output (`dict`): Dictionary of the parsed output

        Returns:
            `str`: a `str` of the interface name

        Examples:
            >>> interface_name = managment_interface_instance.\
                parse_the_name(ipaddress, parsed_output)

        """

        # Return the interface name whose ip matches the ip address
        for intf, value in output.items():
            if 'ipv4' in value.keys():
            	for val in output[intf]['ipv4'].values():
                    if 'ip' in val and val['ip'] in ipaddress:
                        return intf
