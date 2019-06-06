''' 
NTP Genie Ops Object for NXOS - CLI.
'''
# super class
from genie.libs.ops.ntp.ntp import Ntp as SuperNtp

# Parser
from genie.libs.parser.nxos.show_ntp import ShowNtpPeerStatus, \
                                            ShowNtpPeers


class Ntp(SuperNtp):
    '''NTP Genie Ops Object'''

    def learn(self):
        '''Learn NTP Ops'''
        
        ########################################################################
        #                               info
        ########################################################################

        # clock_state
        # 'associations_address', 'associations_local_mode',
        # 'clock_state', clock_stratum', 'root_delay'
        self.add_leaf(cmd=ShowNtpPeerStatus,
                      src='[clock_state]',
                      dest='info[clock_state]')

        # ShowNtpPeerStatus - store to a valid structure in case attribtue is used
        self.add_leaf(cmd=ShowNtpPeerStatus,
                      src='[vrf][(?P<vrf>.*)][peer][(?P<peer>.*)]',
                      dest='info[associations][(?P<peer>.*)][vrf][(?P<vrf>.*)]')

        # ShowNtpPeers - store to a valid structure in case attribtue is used
        self.add_leaf(cmd=ShowNtpPeers,
                      src='[peer][(?P<peer>.*)]',
                      dest='info[unicast_configuration][(?P<peer>.*)]')

        # make to write in cache
        self.make(final_call=True)

        # needs combine structures from ShowNtpPeerStatus and ShowNtpPeers
        if hasattr(self, 'info') and \
          ('associations' in self.info and 'unicast_configuration' in self.info):

            peers = list(self.info['associations'].keys()).copy()

            for peer in peers:
                for vrf in self.info['associations'][peer]['vrf']:

                    # get level key
                    for item in self.info['unicast_configuration'][peer]['isconfigured'].values():
                        ntp_type = item['type']
                        isconfigured = item['isconfigured']
                    local_mode = self.info['associations'][peer]['vrf'][vrf].get('mode', '')

                    # unicast_configuration
                    unicast_dict = self.info.setdefault('vrf', {}).setdefault(vrf, {})\
                        .setdefault('unicast_configuration', {})\
                          .setdefault('address', {}).setdefault(peer, {})\
                            .setdefault('type', {}).setdefault(ntp_type, {})

                    unicast_dict.update({'address': peer,
                                         'type': ntp_type,
                                         'source': self.info['associations'][peer]['vrf'][vrf]['local'],
                                         'vrf': vrf})


                    # associateions
                    if 'sync' not in local_mode:
                        associations_dict = self.info.setdefault('vrf', {}).setdefault(vrf, {})\
                            .setdefault('associations', {}).setdefault('address', {})\
                              .setdefault(peer, {}).setdefault('local_mode', {})\
                                .setdefault(local_mode, {}).setdefault('isconfigured', {})\
                                  .setdefault(str(isconfigured), {})
                        associations_dict.update({'address': peer, 'local_mode': self.info['associations'][peer]['vrf'][vrf]['mode'],
                                                  'isconfigured': isconfigured,
                                                  'stratum': self.info['associations'][peer]['vrf'][vrf]['stratum'],
                                                  'reach': self.info['associations'][peer]['vrf'][vrf]['reach'],
                                                  'poll': self.info['associations'][peer]['vrf'][vrf]['poll'],
                                                  'delay': self.info['associations'][peer]['vrf'][vrf]['delay'],
                                                  'vrf': vrf})

            # remove the non-combined key
            try:
                del(self.info['associations'])
            except Exception:
                pass
            try:
                del(self.info['unicast_configuration'])
            except Exception:
                pass
