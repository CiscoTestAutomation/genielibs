# super class
from genie.libs.ops.msdp.msdp import Msdp as SuperMsdp

# iosxr show msdp
from genie.libs.parser.iosxr.show_vrf import ShowVrfAllDetail
from genie.libs.parser.iosxr.show_msdp import ShowMsdpPeer,\
                                              ShowMsdpContext, \
                                              ShowMsdpSummary, \
                                              ShowMsdpSaCache, \
                                              ShowMsdpStatisticsPeer


class Msdp(SuperMsdp):
    """
        Msdp Ops Object
    """
    def get_session_state(self, item):
        session_state_mapping_dict = {
            'Inactive': 'inactive',
            'Listen': 'listen',
            'Connect': 'established',
        }
        return session_state_mapping_dict[item]

    def keys(self, item):
        """return only the key as list from the item"""
        if isinstance(item, dict):
            return list(item.keys())

    def learn(self, vrf='', peer='', group=''):

        if vrf == 'default':
            vrf_list = ['default']
        elif vrf:
            vrf_list = [vrf]
        else:
            vrf_list = ['default']
            self.add_leaf(cmd=ShowVrfAllDetail,
                          src='',
                          dest='list_of_vrfs',
                          action=self.keys)
            self.make()
            vrf_list.extend(self.list_of_vrfs)

        # loop for vrfs
        for v in sorted(vrf_list):
            
            # create kwargs
            vrf = '' if v == 'default' else v
            
            """ Learn msdp object """
            # vrf
            #   peer
            #     address
            info_src = '[vrf][(?P<vrf>.*)][peer][(?P<address>.*)]'
            info_dest = 'info' + info_src
    
            # ShowMsdpPeer
            # ShowMsdpStatisticsPeer
    
            #       connect_source              N/A
            #       peer_as
            #       authentication              N/A
            #       enable                      N/A
            #       description
            #       mesh_group                  N/A
            #       sa_filter
            #           in
            #           out
            #       sa_limit                    N/A
            #       timer
            #           connect_retry_interval  N/A
            #           keepalive_interval
            #           holdtime_interval
            #       ttl_threshold
            #       session_state
            #       elapsed_time
            #       is_default_peer             N/A
    
            for key in ['peer_as', 'description', 'ttl_threshold', 'elapsed_time']:
                self.add_leaf(cmd=ShowMsdpPeer,
                              src=info_src+'[{key}]'.format(key=key),
                              dest=info_dest+'[{key}]'.format(key=key),
                              vrf=vrf, peer=peer)
    
            self.add_leaf(cmd=ShowMsdpStatisticsPeer,
                          src=info_src + '[as]',
                          dest=info_dest + '[peer_as]',
                          vrf=vrf, peer=peer)
    
            self.add_leaf(cmd=ShowMsdpPeer,
                          src=info_src+'[session_state]',
                          dest=info_dest+'[session_state]',
                          action=self.get_session_state,
                          vrf=vrf, peer=peer)
    
            self.add_leaf(cmd=ShowMsdpStatisticsPeer,
                          src=info_src + '[state]',
                          dest=info_dest + '[session_state]',
                          action=self.get_session_state,
                          vrf=vrf, peer=peer)
    
            #       sa_filter
            #           in
            #           out
            for key in ['in', 'out']:
                self.add_leaf(cmd=ShowMsdpPeer,
                              src=info_src+'[sa_filter][{key}][(?P<filter_in>\(\S+\))][filter]'.format(key=key),
                              dest=info_dest+'[sa_filter][{key}]'.format(key=key),
                              vrf=vrf, peer=peer)
    
            #       timer
            #           connect_retry_interval  N/A
            #           keepalive_interval
            #           holdtime_interval
            for key in ['keepalive_interval', 'peer_timeout_interval']:
                if key == 'peer_timeout_interval':
                    dest_key = 'holdtime_interval'
                else:
                    dest_key = key
                self.add_leaf(cmd=ShowMsdpPeer,
                              src=info_src + '[timer][{key}]'.format(key=key),
                              dest=info_dest + '[timer][{key}]'.format(key=dest_key),
                              vrf=vrf, peer=peer)
    
            #       statistics
            #           last_message_received   N/A
            #           num_of_sg_received      N/A
            #           discontinuity_time      N/A
            #           error                   N/A
            #               rpf_failure         N/A
            #           queue
            #               size_in
            #               size_out
            #           received
            #               keepalive           N/A
            #               notification        N/A
            #               sa_message
            #               sa_response         N/A
            #               sa_request          N/A
            #               total
            #           sent
            #               keepalive           N/A
            #               notification        N/A
            #               sa_message
            #               sa_response
            #               sa_request          N/A
            #               total               N/A
            #           sa_policy               N/A
    
            for key in ['size_input', 'size_output']:
                dest_key = key[:-3]
                self.add_leaf(cmd=ShowMsdpPeer,
                              src=info_src + '[statistics][queue][{key}]'.format(key=key),
                              dest=info_dest + '[statistics][queue][{dest_key}]'.format(dest_key=dest_key),
                              vrf=vrf, peer=peer)
    
            counts = 0
            for key in ['total', 'keepalive', 'notification', 'sa_response']:
                if counts == 0:
                    tlv_act = 'tlv_rcvd'
                    ops_act = 'received'
                else:
                    tlv_act = 'tlv_sent'
                    ops_act = 'sent'
                self.add_leaf(cmd=ShowMsdpStatisticsPeer,
                              src=info_src + '[{tlv_act}][{key}]'.format(tlv_act=tlv_act, key=key),
                              dest=info_dest + '[statistics][{ops_act}][{key}]'.format(ops_act=ops_act, key=key),
                              vrf=vrf, peer=peer)
                counts += 1

            for key in ['received', 'sent']:
                self.add_leaf(cmd=ShowMsdpStatisticsPeer,
                              src=info_src + '[sa_msgs][{key}]'.format(key=key),
                              dest=info_dest + '[statistics][{key}][sa_message]'.format(key=key),
                              vrf=vrf, peer=peer)
    
            #  global
            #      connect_source
            #      default_peer
            #          peer_addr
            #          prefix_policy        N/A
            #      originating_rp
            #      local_as                 N/A
            #      originator_id            N/A
            #      statistics               N/A
            #          num_of_configured_peers  N/A
            #          num_of_established_peers N/A
            #          num_of_shutdown_peers    N/A
            #      sa_filter
            #          in
            #          out
            #      sa_limit
            #      ttl_threshold
            #      timer                        N/A
            #          connect_retry_interval   N/A
    
            # ShowMsdpContext
            global_src = '[vrf][(?P<vrf>.*)]'
            global_dest = 'info'+global_src+'[global]'
    
            for key in ['connect_source', 'ttl']:
                if key == 'ttl':
                    dest_key = 'ttl_threshold'
                else:
                    dest_key = key
                self.add_leaf(cmd=ShowMsdpContext,
                              src=global_src+'[inheritable_config][{key}]'.format(key=key),
                              dest=global_dest+'[{key}]'.format(key=dest_key),
                              vrf=vrf)
    
            self.add_leaf(cmd=ShowMsdpContext,
                          src=global_src+'[config][default_peer_address]',
                          dest=global_dest+'[default_peer][peer_addr]',
                          vrf=vrf)
    
            self.add_leaf(cmd=ShowMsdpContext,
                          src=global_src+'[config][originator_interface]',
                          dest=global_dest+'[originating_rp]',
                          vrf=vrf)
    
            for key in ['in', 'out']:
                self.add_leaf(cmd=ShowMsdpContext,
                              src=global_src + '[inheritable_config][sa_filter][{key}]'.format(key=key),
                              dest=global_dest + '[sa_filter][{key}]'.format(key=key),
                              vrf=vrf)
    
            self.make()
    
            # ShowMsdpSummary
            self.add_leaf(cmd=ShowMsdpSummary,
                          src=global_src+'[maximum_external_sa_global]',
                          dest=global_dest+'[sa_limit]',
                          vrf=vrf)
    
            self.make()
    
            # ShowMsdpSaCache
    
            #   sa_cache
            #       [sa_group sa_source_addr]
            #           group
            #           source_addr
            #           origin_rp
            #               rp_address
            #               is_local_rp         N/A
            #               sa_adv_expire       N/A
            #           up_time
            #           expire
            #           holddown_interval       N/A
            #           peer_learned_from
            #           rpf_peer
            info_src = '[vrf][(?P<vrf>.*)][sa_cache][(?P<sa_cache>.*)]'
            info_dest = 'info' + info_src
    
            for key in ['group', 'source_addr', 'up_time', 'expire','peer_learned_from', 'rpf_peer']:
                self.add_leaf(cmd=ShowMsdpSaCache,
                              src=info_src+'[{key}]'.format(key=key),
                              dest=info_dest+'[{key}]'.format(key=key),
                              vrf=vrf, group=group)
    
            self.add_leaf(cmd=ShowMsdpSaCache,
                          src=info_src+'[origin_rp][(?P<rp_address>.*)][rp_address]',
                          dest=info_dest+'[origin_rp][(?P<rp_address>.*)][rp_address]',
                          vrf=vrf, group=group)

        self.make(final_call=True)