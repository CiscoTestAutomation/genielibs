''' 
Dot1x Genie Ops Object for IOSXE - CLI.
'''
# Genie
from genie.libs.ops.dot1x.dot1x import Dot1X as SuperDot1X
from genie.ops.base import Context


class Dot1X(SuperDot1X):
    '''Dot1x Genie Ops Object'''

    def learn(self):
        '''Learn Dot1x Ops'''
        
        ########################################################################
        #                               info
        ########################################################################
        # unsupported keys
        # credentials, critical, test, supplicant

        # version, system_auth_control
        for key in ['version', 'system_auth_control']:
            self.add_leaf(cmd='show dot1x all details',
                          src='[{}]'.format(key),
                          dest='info[{}]'.format(key))

        # sessions
        self.add_leaf(cmd='show dot1x all count',
                      src='[sessions]',
                      dest='info[sessions]')

        # --------------  interfaces -----------------
        intf_src = '[interfaces][(?P<intf>.*)]'
        intf_dst = 'info[interfaces][(?P<intf>.*)]'

        # 'max_req', 'max_reauth_req', 'pae'
        # interface, credentials, authenticator
        # supplicant, max_start
        for key in ['max_req', 'max_reauth_req', 'interface', 'pae',
            'credentials', 'authenticator', 'supplicant', 'max_start']:
            self.add_leaf(cmd='show dot1x all details',
                          src=intf_src + '[{}]'.format(key),
                          dest=intf_dst + '[{}]'.format(key))

        # timeout
        for key in ['auth_period', 'held_period', 'quiet_period', 'ratelimit_period',
            'server_timeout', 'start_period', 'supp_timeout', 'tx_period']:
            self.add_leaf(cmd='show dot1x all details',
                          src=intf_src + '[timeout][{}]'.format(key),
                          dest=intf_dst + '[timeout][{}]'.format(key))
        # statistics
        self.add_leaf(cmd='show dot1x all statistics',
                      src=intf_src + '[statistics]',
                      dest=intf_dst + '[statistics]')
        # client
        client_src = '[interfaces][(?P<intf>.*)][clients][(?P<clients>.*)]'
        client_dst = 'info[interfaces][(?P<intf>.*)][clients][(?P<clients>.*)]'
        #    client, status, pae
        for key in ['client', 'status', 'pae']:
            self.add_leaf(cmd='show dot1x all summary',
                          src=client_src + '[{}]'.format(key),
                          dest=client_dst + '[{}]'.format(key))
        # client
        #    eap_method, session
        for key in ['eap_method', 'session']:
            self.add_leaf(cmd='show dot1x all details',
                          src=client_src + '[{}]'.format(key),
                          dest=client_dst + '[{}]'.format(key))

        # make to write in cache
        self.make(final_call=True)
