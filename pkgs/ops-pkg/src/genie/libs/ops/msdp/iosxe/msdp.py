# super class
from genie.libs.ops.msdp.msdp import Msdp as SuperMsdp

# iosxe show msdp
from genie.libs.parser.iosxe.show_msdp import ShowIpMsdpPeer,\
                                              ShowIpMsdpSaCache


class Msdp(SuperMsdp):
    '''
        Msdp Ops Object
    '''

    def get_session_state(self, item):

        session_state_mapping_dict = {
            '(N/A)': 'disabled',
            'Down': 'inactive',
            'Listen': 'listen',
            'Connect': 'connecting',
            'Up': 'established',
            'shutdown': 'admin-shutdown'
        }

        return session_state_mapping_dict[item]

    def learn(self):
        '''
            Learn Msdp object
        '''        
        # N/A -> Keys not supported by this OS
        # vrf
        #   global N/A
        #   peer
        #       connect_source
        #       peer_as
        #       authentication              N/A
        #       enable                      N/A
        #       description                 N/A
        #       mesh_group                  N/A
        #       sa_filter                   N/A
        #       sa_limit                    N/A
        #       timer                       N/A
        #       ttl_threshold
        #       session_state
        #       elapsed_time
        #       is_default_peer             N/A
        #       statistics
        #           last_message_received   N/A
        #           num_of_sg_received      N/A
        #           discontinuity_time      N/A
        #           error
        #               rpf_failure
        #           queue
        #               size_in
        #               size_out
        #           received
        #               keepalive           N/A
        #               notification        N/A
        #               sa_message
        #               sa_response         N/A
        #               sa_request
        #               total               N/A
        #           sent
        #               keepalive           N/A
        #               notification        N/A
        #               sa_message
        #               sa_response
        #               sa_request          N/A
        #               total               N/A
        #           sa_policy               N/A
        #   sa_cache
        #       [sa_group sa_source_addr]
        #           group
        #           source_addr
        #           origin_rp
        #               rp_address
        #           up_time
        #           expire
        #           holddown_interval       N/A
        #           peer_learned_from 
        #           rpf_peer

        # vrf
        #   peer                
        info_src = '[vrf][(?P<vrf>.*)][peer][(?P<peer>.*)]'
        info_dest = 'info' + info_src

        # ShowIpMsdpPeer

        for key in ['elapsed_time', 'peer_as', 
                    'connect_source' , 'ttl_threshold']:

            self.add_leaf(cmd=ShowIpMsdpPeer,
                          src=info_src+'[{key}]'.format(key=key),
                          dest=info_dest+'[{key}]'.format(key=key))

        self.add_leaf(cmd=ShowIpMsdpPeer,
                          src=info_src+'[session_state]',
                          dest=info_dest+'[session_state]',
                          action=self.get_session_state)

        # statistics
        #   received
        #       sa_message
        #       sa_request
        for key in ['sa_message', 'sa_request',]:

            self.add_leaf(cmd=ShowIpMsdpPeer,
                          src=info_src+'[statistics][received][{key}]'\
                            .format(key=key),
                          dest=info_dest+'[statistics][received][{key}]'\
                            .format(key=key))

        # statistics
        #   queue
        #       size_in
        #       size_out
        for key in ['size_in', 'size_out']:
            self.add_leaf(cmd=ShowIpMsdpPeer,
                          src=info_src+'[statistics][queue][{key}]'.format(key=key),
                          dest=info_dest+'[statistics][queue][{key}]'.format(key=key))         

        # statistics
        #   sent
        #       sa_message
        #       sa_response
        for key in ['sa_message', 'sa_response']:
            self.add_leaf(cmd=ShowIpMsdpPeer,
                          src=info_src+'[statistics][sent][{key}]'.format(key=key),
                          dest=info_dest+'[statistics][sent][{key}]'.format(key=key))

        # statistics
        #   error
        #       rpf_failure
        self.add_leaf(cmd=ShowIpMsdpPeer,
                          src=info_src+'[statistics][error][rpf_failure]',
                          dest=info_dest+'[statistics][error][rpf_failure]')

        # ShowIpMsdpSaCache

        # vrf
        #   sa_cache
        info_src = '[vrf][(?P<vrf>.*)][sa_cache][(?P<sa_cache>.*)]'
        info_dest = 'info' + info_src

        for key in ['group', 'source_addr', 'peer_learned_from', 'rpf_peer',
                    'up_time', 'expire',]:

            self.add_leaf(cmd=ShowIpMsdpSaCache,
                          src=info_src+'[{key}]'.format(key=key),
                          dest=info_dest+'[{key}]'.format(key=key))

        # origin_rp
        #   rp_address
        self.add_leaf(cmd=ShowIpMsdpSaCache,
                      src=info_src+'[origin_rp][(?P<rp_address>.*)][rp_address]',
                      dest=info_dest+'[origin_rp][(?P<rp_address>.*)][rp_address]')

        # Make final Ops structure
        self.make(final_call=True)
