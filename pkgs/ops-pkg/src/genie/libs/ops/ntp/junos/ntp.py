''' 
NTP Genie Ops Object for Junos - CLI.
'''
# super class
from genie.libs.ops.ntp.ntp import Ntp as SuperNtp

# Parser
from genie.libs.parser.junos.show_ntp import ShowNtpAssociations, \
                                             ShowNtpStatus, \
                                             ShowConfigurationSystemNtpSet


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
        self.add_leaf(cmd=ShowNtpAssociations,
                      src='[clock_state]',
                      dest='info[clock_state]')

        # 'associations_address', 'associations_local_mode',
        # 'clock_state', clock_stratum', 'root_delay'
        for src_key, dest_key in {'frequency': 'actual_freq',
                                  'precision': 'clock_precision',
                                  'reftime': 'reference_time',
                                  'rootdispersion': 'root_dispersion'}.items():            
            self.add_leaf(cmd=ShowNtpStatus,
                          src='[clock_state][system_status][%s]' % src_key,
                          dest='info[clock_state][system_status][%s]' % dest_key)

        # unicast_configuration
        self.add_leaf(cmd=ShowConfigurationSystemNtpSet,
                      src='[vrf][(?P<vrf>.*)][address][(?P<address>.*)][type][(?P<type>.*)]',
                      dest='info[vrf][(?P<vrf>.*)][unicast_configuration][address]'
                           '[(?P<address>.*)][type][(?P<type>.*)]')

        # associations
        self.add_leaf(cmd=ShowConfigurationSystemNtpSet,
                      src='[vrf][(?P<vrf>.*)][address][(?P<address>.*)][isconfigured][(?P<isconfigured>.*)]',
                      dest='info[vrf][(?P<vrf>.*)][associations][address][(?P<address>.*)]'
                           '[isconfigured][(?P<isconfigured>.*)]')

        # associations
        asso_keys = ['address', 'local_mode', 'stratum', 'refid', 'reach', 'poll',
                     'offset', 'delay', 'receive_time']
        for key in asso_keys:
            self.add_leaf(cmd=ShowNtpAssociations,
                          src='[peer][(?P<address>.*)][local_mode][(?P<local_mode>.*)][%s]' % key,
                          dest='info[associations][address][(?P<address>.*)]'
                               '[local_mode][(?P<local_mode>.*)][%s]' % key)


        # make to write in cache
        self.make(final_call=True)

        # needs combine structures from ShowConfigurationSystemNtpSet and ShowNtpAssociations
        if hasattr(self, 'info') and 'associations' in self.info :

            peers = list(self.info['associations']['address'].keys()).copy()

            for peer in peers:
                for vrf in self.info['vrf']:
                    if not self.info['vrf'][vrf]['associations']['address'].get(peer):
                        continue

                    for local_mode in self.info['associations']['address'][peer]['local_mode'].keys():
                        mode_dict = self.info['vrf'][vrf]['associations']['address'][peer].setdefault('local_mode', {}).setdefault(local_mode, {})
                        mode_dict.setdefault('isconfigured', {}).update(self.info['vrf'][vrf]['associations']['address'][peer]['isconfigured'])
                        for configured in mode_dict['isconfigured']:
                            mode_dict['isconfigured'][configured].update(self.info['associations']['address'][peer]['local_mode'][local_mode])
                            mode_dict['isconfigured'][configured]['vrf'] = vrf
                            mode_dict['isconfigured'][configured]['local_mode'] = local_mode
                   
                    try:
                        del(self.info['vrf'][vrf]['associations']['address'][peer]['isconfigured'])
                    except Exception:
                        pass

            # remove the non-combined key
            try:
                del(self.info['associations'])
            except Exception:
                pass
