# super class
from genie.libs.ops.msdp.msdp import Msdp as SuperMsdp

from genie.libs.parser.nxos.show_msdp import ShowIpMsdpSaCacheDetailVrf,\
                                             ShowIpMsdpPeerVrf, \
                                             ShowIpMsdpPolicyStatisticsSaPolicyIn, \
                                             ShowIpMsdpPolicyStatisticsSaPolicyOut, \
                                             ShowIpMsdpSummary

class Msdp(SuperMsdp):
    '''Msdp Ops Object'''

    def learn(self):
        '''Learn msdp object'''
        # Place holder to make it more readable

        #  group
        #  source_addr
        #    origin_rp
        #         rp_address
        #            rp_address
        #            is_local_rp        N/A
        #            sa_adv_expire      N/A
        #  up_time
        #  expire
        #  holddown_interval            N/A
        #  peer_learned_from
        #  rpf_peer                     N/A
        src_cache = '[vrf][(?P<vrf_name>.*)][sa_cache][(?P<sa_cache>.*)]'
        dest_cache = 'info' + src_cache

        req_key = ['group', 'source_addr', 'up_time', 'expire', 'peer_learned_from']
        for key in req_key:
            self.add_leaf(cmd=ShowIpMsdpSaCacheDetailVrf,
                          src=src_cache + '[{}]'.format(key),
                          dest=dest_cache + '[{}]'.format(key),
                          vrf='all')

        src_cache_origin = src_cache + '[origin_rp][(?P<rp_address>.*)]'
        dest_cache_origin = 'info' + src_cache_origin


        self.add_leaf(cmd=ShowIpMsdpSaCacheDetailVrf,
                      src=src_cache_origin + '[rp_address]',
                      dest=dest_cache_origin + '[rp_address]',
                      vrf='all')

        # peer
        #    address
        #         connect_source
        #         peer_as
        #         authentication
        #             password
        #                 key
        #         enable
        #         description
        #         mesh_group
        #         sa_filter
        #             in
        #             out
        #         sa_limit
        #         timer
        #             connect_retry_interval
        #             keepalive_interval
        #             holdtime_interval
        #         ttl_threshold                  N/A
        #         session_state
        #         elapsed_time
        #         is_default_peer                 N/A
        #         statistics
        #             discontinuity_time
        #             error
        #                 rpf_failure
        #             queue                        N/A
        #                 size_in                  N/A
        #                 size_out                 N/A
        #             received
        #                 keepalive
        #                 notification
        #                 sa_message
        #                 sa_response
        #                 sa_request
        #                 total
        #             sent
        #                 keepalive
        #                 notification
        #                 sa_message
        #                 sa_response
        #                 sa_request
        #                 total

        src_peer = '[vrf][(?P<vrf_name>.*)][peer][(?P<address>.*)]'
        dest_peer = 'info' + src_peer

        req_key = ['connect_source', 'peer_as', 'enable', 'description', 'mesh_group', 'sa_limit',\
                   'session_state', 'elapsed_time']
        for key in req_key:
            self.add_leaf(cmd=ShowIpMsdpPeerVrf,
                          src=src_peer + '[{}]'.format(key),
                          dest=dest_peer + '[{}]'.format(key),
                          vrf='all')

        src_authentication = src_peer + '[authentication][password]'
        dest_authentication = 'info' + src_authentication
        self.add_leaf(cmd=ShowIpMsdpPeerVrf,
                          src=src_authentication + '[key]',
                          dest=dest_authentication + '[key]',
                          vrf='all')

        src_filter = src_peer + '[sa_filter]'
        dest_filter = 'info' + src_filter

        req_key = ['in', 'out']
        for key in req_key:
            self.add_leaf(cmd=ShowIpMsdpPeerVrf,
                          src=src_filter + '[{}]'.format(key),
                          dest=dest_filter + '[{}]'.format(key),
                          vrf='all')

        src_timer = src_peer + '[timer]'
        dest_timer = 'info' + src_timer

        req_key = ['connect_retry_interval', 'keepalive_interval', 'holdtime_interval']
        for key in req_key:
            self.add_leaf(cmd=ShowIpMsdpPeerVrf,
                          src=src_timer + '[{}]'.format(key),
                          dest=dest_timer + '[{}]'.format(key),
                          vrf='all')

        src_statistic = src_peer + '[statistics]'
        dest_statistic = 'info' + src_statistic
        self.add_leaf(cmd=ShowIpMsdpPeerVrf,
                      src=src_statistic + '[discontinuity_time]',
                      dest=dest_statistic + '[discontinuity_time]',
                      vrf='all')

        src_error = src_statistic +'[error][rpf_failure]'
        dest_error = 'info'+ src_error
        self.add_leaf(cmd=ShowIpMsdpPeerVrf,
                      src=src_error,
                      dest=dest_error,
                      vrf='all')

        src_received = src_statistic + '[received]'
        dest_received = 'info' + src_received

        req_key = ['keepalive', 'notification', 'sa_message', 'sa_response', 'sa_request', 'total']
        for key in req_key:
            self.add_leaf(cmd=ShowIpMsdpPeerVrf,
                          src=src_received + '[{}]'.format(key),
                          dest=dest_received+ '[{}]'.format(key),
                          vrf='all')

        src_sent = src_statistic + '[sent]'
        dest_sent = 'info' + src_sent

        req_key = ['keepalive', 'notification', 'sa_message', 'sa_response', 'sa_request', 'total']
        for key in req_key:
            self.add_leaf(cmd=ShowIpMsdpPeerVrf,
                          src=src_sent + '[{}]'.format(key),
                          dest=dest_sent + '[{}]'.format(key),
                          vrf='all')

        self.make()

        for vrf in getattr(self, 'info', {}).get('vrf', {}):
            # local_as, originator_id, statistics
            for key in ['local_as', 'originator_id', 'statistics']:
                self.add_leaf(cmd=ShowIpMsdpSummary,
                              src='[vrf][%s][%s]' % (vrf, key),
                              dest='info[vrf][%s][global][%s]' %  (vrf, key),
                              vrf=vrf)

            # last_message_received, num_of_sg_received
            for key in ['last_message_received', 'num_of_sg_received']:
                self.add_leaf(cmd=ShowIpMsdpSummary,
                              src='[vrf][%s][peer][(?P<peer>.*)][statistics][%s]' %  (vrf, key),
                              dest='info[vrf][%s][peer][(?P<peer>.*)][statistics][%s]' %  (vrf, key),
                              vrf=vrf)

            for peer in self.info['vrf'][vrf].get('peer', {}):
                in_src = '[vrf][%s][peer][%s][in]' % (vrf, peer)
                in_dest = 'info[vrf][%s][peer][%s][statistics][sa_policy][in]' % (vrf, peer)

                out_src = '[vrf][%s][peer][%s][out]' % (vrf, peer)
                out_dest = 'info[vrf][%s][peer][%s][statistics][sa_policy][out]' % (vrf, peer)

                # total_accept_count, total_reject_count
                for key in ['total_accept_count', 'total_reject_count']:

                    self.add_leaf(cmd=ShowIpMsdpPolicyStatisticsSaPolicyIn,
                                  src=in_src + '[%s]' % key,
                                  dest=in_dest + '[%s]' % key,
                                  vrf=vrf, peer=peer)

                    self.add_leaf(cmd=ShowIpMsdpPolicyStatisticsSaPolicyOut,
                                  src=out_src + '[%s]' % key,
                                  dest=out_dest + '[%s]' % key,
                                  vrf=vrf, peer=peer)

                # in - num_of_comparison, num_of_matches
                # out - num_of_comparison, num_of_matches
                for key in ['num_of_comparison', 'num_of_matches']:

                    self.add_leaf(cmd=ShowIpMsdpPolicyStatisticsSaPolicyIn,
                                  src=in_src + '[(?P<sa>.*)][(?P<match>.*)][%s]' % key,
                                  dest=in_dest + '[(?P<sa>.*)][(?P<match>.*)][%s]' % key,
                                  vrf=vrf, peer=peer)

                    self.add_leaf(cmd=ShowIpMsdpPolicyStatisticsSaPolicyOut,
                                  src=out_src + '[(?P<sa>.*)][(?P<match>.*)][%s]' % key,
                                  dest=out_dest + '[(?P<sa>.*)][(?P<match>.*)][%s]' % key,
                                  vrf=vrf, peer=peer)
        self.make(final_call=True)