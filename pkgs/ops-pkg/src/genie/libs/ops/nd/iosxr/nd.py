# Genie package
from genie.ops.base import Base
from genie.utils.config import Config

# genie.libs
from genie.libs.parser.iosxr.show_interface import ShowIpv6VrfAllInterface
from genie.libs.parser.iosxr.show_ipv6 import ShowIpv6NeighborsDetail, ShowIpv6Neighbors


class Nd(Base):
    '''Nd Ops Object'''

    def learn(self, vrf='all', interface=''):
        '''Learn Nd object'''

        # new Nd structure
        # Place holder to make it more readable
        #  interfaces
        #     interface
        #     router_advertisement
        #         interval
        #         lifetime
        #         suppress
        #     neighbors
        #         neighbor
        #             ip
        #             link_layer_address
        #             neighbor_state
        #             age
        #             origin
        #             is_router             N/A

        if interface:
            src_nd = '[interfaces][{}]'.format(interface)
        else:
            src_nd = '[interfaces][(?P<interface>.*)]'

        dest_nd = 'info' + src_nd
        
        self.add_leaf(cmd=ShowIpv6Neighbors,
                      src=src_nd + '[interface]',
                      dest=dest_nd + '[interface]',
                      interface=interface, vrf=vrf)
        self.make()

        if interface:
            src_rd = '[{}][ipv6]'.format(interface)
        else:
            src_rd = '[(?P<interface>.*)][ipv6]'
        
        dest_rd = dest_nd +'[router_advertisement]'
        req_dict = {'nd_adv_duration':'interval', 
                    'nd_router_adv':'lifetime'}

        for src, dest in req_dict.items():
            self.add_leaf(cmd=ShowIpv6VrfAllInterface,
                          src=src_rd + '[{}]'.format(src),
                          dest=dest_rd + '[{}]'.format(dest),
                          interface=interface, vrf=vrf)

        src_nd_neighbor = src_nd +'[neighbors][(?P<neighbor>.*)]'
        dest_nd_neighbor = 'info' + src_nd_neighbor
        req_key =['ip','link_layer_address','neighbor_state','age','origin']
        for key in req_key:
            self.add_leaf(cmd=ShowIpv6NeighborsDetail,
                          src=src_nd_neighbor + '[{}]'.format(key),
                          dest=dest_nd_neighbor + '[{}]'.format(key))
        self.make()

        # Get nd suppress by executing 'show running-config interface'
        if interface:
            show_run_cmd = 'show running-config interface {}'.format(interface)
        else:
            show_run_cmd = 'show running-config interface'

        show_run = self.device.execute(show_run_cmd)
        cfg = Config(show_run)
        cfg.tree()
        config_dict = cfg.config

        if config_dict and hasattr(self, 'info'):
            for intf, intf_dict in self.info['interfaces'].items():
                key = 'interface {}'.format(intf)
                if key in config_dict and 'ipv6 nd suppress-ra' in config_dict[key]:
                    intf_dict.setdefault('router_advertisement', {}).update({'suppress': True})

        self.make(final_call=True)
