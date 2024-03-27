'''
Interface Genie Ops Object for Cheetah - CLI.
'''


# super class
from genie.libs.ops.interface.interface import Interface as SuperInterface


class Interface(SuperInterface):
    '''Interface Genie Ops Object'''

    def learn(self, custom=None, interface=None, vrf=None, address_family=None):
        '''Learn Interface Ops'''
        ########################################################################
        #                               info
        ########################################################################
        # Global source

        src = '[interface][(?P<interface>.*)]'
        dest = 'info' + src
        wired_key_map = {
            'type': 'type',
            'status': 'oper_status',
            'mac_address': 'phys_address',
            'status': 'enabled',
            'speed': 'bandwidth',
            'mac_address': 'mac_address',
            'duplex': 'duplex_mode'
        }

        # show interfaces wired
        #   <0-3>  wired interface number
        for x in range(4):
            for src_key, dest_key in wired_key_map.items():
                self.add_leaf(cmd=f'show interfaces wired {x}',
                              src=src + f'[{src_key}]',
                              dest=dest + f'[{dest_key}]',
                              ifnum=x)

        self.make()

        # keys from parser schema
        src = '[interface][(?P<interface>.*)][statistics]'
        # keys from ops schema
        dest = 'info[interface][(?P<interface>.*)][counters]'

        counter_map = {
            'rx_pkts_cumulative_total' : 'in_pkts',
            'rx_octets_cumulative_total' : 'in_octets',
            'rx_err_cumulative_total' : 'in_errors',
            'rx_drops_cumulative_total' : 'in_discards',
            'tx_pkts_cumulative_total' : 'out_pkts',
            'tx_octets_cumulative_total' : 'out_octets',
            'tx_err_cumulative_total' : 'out_errors',
        }

        for x in range(4):
            for src_key, dest_key in counter_map.items():
                self.add_leaf(cmd=f'show interfaces wired {x}',
                              src=src + f'[{src_key}]',
                              dest=dest + f'[{dest_key}]',
                              ifnum=x)

            self.make()

        src = '[interface][(?P<interface>.*)]'
        dest = 'info[interface][(?P<interface>.*)][counters][rate]'

        counter_rate_map = {
            'load_interval' : 'input_load_interval',
            'input_rate_bps' : 'in_rate',
            'input_pps' : 'in_rate_pkts',
            'output_rate_bps' : 'out_rate',
            'output_pps' : 'out_rate_pkts'
        }

        for x in range(4):
            for src_key, dest_key in counter_rate_map.items():
                self.add_leaf(cmd=f'show interfaces wired {x}',
                              src=src + f'[{src_key}]',
                              dest=dest + f'[{dest_key}]',
                              ifnum=x)

            self.make()

        src = '[interface][(?P<interface>.*)]'
        dest = 'info' + src

        dot11radio_key_map = {
            'hardware': 'type',
            'protocol_state': 'oper_status',
            'mac_address': 'phys_address',
            'admin_state': 'enabled',
            'mac_address': 'mac_address',
        }

        # show interface dot11Radio
        #   <0-2>  Dot11Radio interface number
        for x in range(3):
            for src_key, dest_key in dot11radio_key_map.items():
                self.add_leaf(cmd=f'show interfaces dot11radio {x}',
                              src=src + f'[{src_key}]',
                              dest=dest + f'[{dest_key}]',
                              ifnum=x)

            self.make()

        # keys from parser schema
        src = '[interface][(?P<interface>.*)][rx]'
        # keys from ops schema
        dest = 'info[interface][(?P<interface>.*)][counters][rate]'

        counter_rx_map = {
            'packets' : 'in_rate_pkts'
        }

        for x in range(3):
            for src_key, dest_key in counter_rx_map.items():
                self.add_leaf(cmd=f'show interfaces dot11radio {x}',
                              src=src + f'[{src_key}]',
                              dest=dest + f'[{dest_key}]',
                              ifnum=x)

            self.make()

        counter_tx_map = {
            'packets' : 'out_rate_pkts',
        }

        for x in range(3):
            for src_key, dest_key in counter_tx_map.items():
                self.add_leaf(cmd=f'show interfaces dot11radio {x}',
                              src=src + f'[{src_key}]',
                              dest=dest + f'[{dest_key}]',
                              ifnum=x)

            self.make()

        # keys from parser schema
        src = '[interface][(?P<interface>.*)]'
        # keys from ops schema
        dest = 'info[interface][(?P<interface>.*)][counters][rate]'

        counter_rx_map = {
            'rx_bytes' : 'in_pkts'
        }

        for x in range(3):
            for src_key, dest_key in counter_rx_map.items():
                self.add_leaf(cmd=f'show interfaces dot11radio {x}',
                              src=src + f'[{src_key}]',
                              dest=dest + f'[{dest_key}]',
                              ifnum=x)

            self.make()

        counter_tx_map = {
            'tx_bytes' : 'out_pkts',
        }

        for x in range(3):
            for src_key, dest_key in counter_tx_map.items():
                self.add_leaf(cmd=f'show interfaces dot11radio {x}',
                              src=src + f'[{src_key}]',
                              dest=dest + f'[{dest_key}]',
                              ifnum=x)

            self.make()

        # keys from parser schema
        # Interface is a wildcard key whereas ml_type and statistics aren't
        # hence explicitly hardcoded it
        # from the available options (ml/non-ml , cumulative_total/last_5_secs)
        src = '[interface][(?P<interface>.*)][ml_type][ml][statistics][cumulative_total]'
        # keys from ops schema
        dest = 'info[interface][(?P<interface>.*)][counters]'

        counter_map = {
            'unicast_rx' : 'in_unicast_pkts',
            'broadcasts_rx' : 'in_broadcast_pkts',
            'multicast_rx' : 'in_multicast_pkts',
            'ctrl_frame_rx' : 'in_mac_control_frames',
            'unicast_tx' : 'out_unicast_pkts',
            'broadcasts_tx' : 'out_broadcast_pkts',
            'multicast_tx' : 'out_multicast_pkts',
            'ctrl_frame_tx' : 'out_mac_control_frames',
        }

        for x in range(3):
            for src_key, dest_key in counter_map.items():
                self.add_leaf(cmd=f'show interfaces dot11radio {x}',
                              src=src + f'[{src_key}]',
                              dest=dest + f'[{dest_key}]',
                              ifnum=x)

            self.make()

        self.make(final_call=True)