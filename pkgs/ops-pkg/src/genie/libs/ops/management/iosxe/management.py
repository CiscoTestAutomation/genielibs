"""
Platform Genie Ops Object for IOSXE.
"""

import logging

# super class
from genie.libs.ops.management.management import Management as SuperManagement

logger = logging.getLogger(__name__)


class Management(SuperManagement):
    """Management Genie Ops Object"""

    def learn(self):

        self.add_leaf(
            cmd="show ip route 0.0.0.0",
            src="[entry][0.0.0.0/0][paths][(?P<idx>.*)][nexthop]",
            dest="info[management][ipv4_gateway]",
            route='0.0.0.0'
        )

        self.add_leaf(
            cmd="show ip route 0.0.0.0",
            src="[vrf][default][address_family][ipv4][routes][0.0.0.0/0][next_hop][next_hop_list][(?P<idx>.*)][next_hop]",
            dest="info[management][ipv4_gateway]",
            route='0.0.0.0'
        )

        self.make()

        try:
            next_hop = self.info["management"]["ipv4_gateway"]
        except Exception:
            pass
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
            pass
        else:
            self.add_leaf(
                cmd=f"show ip interface {interface}",
                src=f"[{interface}][ipv4]",
                dest="info[management][ipv4_address]",
                interface=interface
            )

            self.make()

        try:
            ip = self.info['management']['ipv4_address']
            gw = self.info['management']['ipv4_gateway']
            iface = self.info['management']['interface']
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

        self.add_leaf(
            cmd="show vrf",
            src="[vrf][(?P<vrf>.*)]",
            dest="info[vrf][(?P<vrf>.*)]"
        )

        self.make()

        for vrf in self.info['vrf']:
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

        for vrf in self.info['vrf']:
            if self.info['vrf'][vrf]['networks']['total'] < 10:
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

                    self.add_leaf(
                        cmd=f"show ip route vrf {vrf} {next_hop}",
                        src="[entry][(?P<route>.*)][paths][(?P<idx>.*)][interface]",
                        dest="info[management][interface]",
                        vrf=vrf,
                        route=next_hop
                    )

                    self.make()

                    interface = self.info["management"]["interface"]

                    self.add_leaf(
                        cmd=f"show ip interface {interface}",
                        src=f"[{interface}][ipv4]",
                        dest="info[management][ipv4_address]",
                        interface=interface
                    )

                    self.make()

                    break

        self.info.pop('vrf', None)

        try:
            self.info['management']['ipv4_address'] = list(self.info['management']['ipv4_address'].keys())[0]
        except Exception:
            pass

        # Make Ops object
        self.make(final_call=True)