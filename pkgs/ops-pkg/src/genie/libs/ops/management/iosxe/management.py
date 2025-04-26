"""
Management Genie Ops Object for IOSXE.
"""

import logging

# super class
from genie.libs.ops.management.management import Management as SuperManagement

logger = logging.getLogger(__name__)


class Management(SuperManagement):
    """Management Genie Ops Object

    Try to discovery management connectivity:

    * management interface
    * management VRF (if used)
    * management address (IPv4 only)
    * default gateway (IPv4 only)

    This model assumes the default route (0.0.0.0) will point to the management interface.

    """
    def learn(self, **kwargs):

        self.add_leaf(
            cmd="show ip route 0.0.0.0",
            src="[entry][0.0.0.0/0][paths][(?P<idx>.*)][nexthop]",
            dest="info[management][ipv4_gateway]",
            route="0.0.0.0"
        )

        self.add_leaf(
            cmd="show ip route 0.0.0.0",
            src="[vrf][default][address_family][ipv4][routes][0.0.0.0/0][next_hop][next_hop_list][(?P<idx>.*)][next_hop]",
            dest="info[management][ipv4_gateway]",
            route="0.0.0.0"
        )

        # Updated parser may return default gateway if "ip default-gateway" is configured
        self.add_leaf(
            cmd="show ip route 0.0.0.0",
            src="[default_gateway]",
            dest="info[management][ipv4_gateway]",
            route="0.0.0.0"
        )

        self.make()

        try:
            next_hop = self.info["management"]["ipv4_gateway"]
        except Exception:
            next_hop = None
        else:
            self.add_leaf(
                cmd=f"show ip route {next_hop}",
                src="[entry][(?P<route>.*)][paths][(?P<idx>.*)][interface]",
                dest="info[management][interface]",
                route=next_hop
            )

            self.add_leaf(
                cmd=f"show ip route {next_hop}",
                src="[vrf][default][address_family][ipv4][routes][(?P<route>.*)][next_hop][outgoing_interface][(?P<iface>.*)][outgoing_interface]",
                dest="info[management][interface]",
                route=next_hop
            )

            self.make()

        try:
            interface = self.info["management"]["interface"]
        except Exception:

            if next_hop:

                # If we don't have an interface, try to find it via arp entry
                self.add_leaf(
                    cmd=f"show ip arp {next_hop}",
                    src="[interfaces]",
                    dest="info[management][interface]",
                    intf_or_ip=next_hop
                )

                self.make()

                # ARP entry will return a dict, need to normalize to the interface name
                try:
                    self.info["management"]["interface"] = list(self.info['management']['interface'].keys())[0]
                except Exception:
                    pass

        # Check again if we have an interface
        try:
            interface = self.info["management"]["interface"]
        except Exception:
            pass
        else:
            # If we have an interface, find the IP address
            self.add_leaf(
                cmd=f"show ip interface {interface}",
                src=f"[{interface}][ipv4]",
                dest="info[management][ipv4_address]",
                interface=interface
            )

            self.make()

        # If we have all data, management is using global routing table
        # Return info as-is.
        try:
            ip = self.info['management']['ipv4_address']
            gw = self.info['management']['ipv4_gateway']
            interface = self.info['management']['interface']
            if ip and gw and interface:
                try:
                    self.info['management']['ipv4_address'] = list(self.info['management']['ipv4_address'].keys())[0]
                except Exception:
                    pass

                # Make Ops object
                self.make(final_call=True)
                return
        except Exception:
            pass

        # If we are not using global routing, check for VRFs
        self.add_leaf(
            cmd="show vrf",
            src="[vrf][(?P<vrf>.*)]",
            dest="info[vrf][(?P<vrf>.*)]"
        )

        self.make()

        # Get the VRF route summary to find out the number of routes
        for vrf in self.info.get('vrf', {}):
            self.add_leaf(
                cmd="show ip route vrf {vrf} summary",
                src="[vrf][(?P<vrf>.*)][total_route_source][networks]",
                dest="info[vrf][(?P<vrf>.*)][networks][total]",
                vrf=vrf
            )

            self.add_leaf(
                cmd="show ip route vrf {vrf} summary",
                src="[vrf][(?P<vrf>.*)][route_source][connected][networks]",
                dest="info[vrf][(?P<vrf>.*)][networks][connected]",
                vrf=vrf
            )

        self.make()

        # Check for VRFs with less than 10 routes, assume its the management VRF
        for vrf in self.info.get('vrf', {}):
            if self.info['vrf'][vrf]['networks']['total'] < 10:

                # Find connected interfaces with less than 3 entries,
                # assume its the management interfae
                if self.info['vrf'][vrf]['networks']['connected'] < 3:
                    self.add_leaf(
                        cmd=f"show ip route vrf {vrf} 0.0.0.0",
                        src="entry[0.0.0.0/0][paths][(?P<idx>.*)][nexthop]",
                        dest="info[management][ipv4_gateway]",
                        vrf=vrf,
                        route='0.0.0.0'
                    )
                    self.add_leaf(
                        cmd=f"show ip route vrf {vrf} 0.0.0.0",
                        src="routing_table",
                        dest="info[management][vrf]",
                        vrf=vrf,
                        route='0.0.0.0'
                    )
                    self.make()

                    next_hop = self.info["management"]["ipv4_gateway"]

                    # Find the interface using the routing entry for the next hop
                    self.add_leaf(
                        cmd=f"show ip route vrf {vrf} {next_hop}",
                        src="[entry][(?P<route>.*)][paths][(?P<idx>.*)][interface]",
                        dest="info[management][interface]",
                        vrf=vrf,
                        route=next_hop
                    )

                    self.make()

                    interface = self.info["management"]["interface"]

                    # Find the address using the interface
                    self.add_leaf(
                        cmd=f"show ip interface {interface}",
                        src=f"[{interface}][ipv4]",
                        dest="info[management][ipv4_address]",
                        interface=interface
                    )

                    self.make()

                    break

        # Remove VRF data from the returned data
        self.info.pop('vrf', None)

        # Normalize the ipv4 address, it may be a dict structure
        try:
            self.info['management']['ipv4_address'] = list(self.info['management']['ipv4_address'].keys())[0]
        except Exception:
            pass

        # Make Ops object
        self.make(final_call=True)
