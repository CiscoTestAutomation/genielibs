from unittest import TestCase
from genie.libs.sdk.apis.iosxe.platform.execute import execute_setup
from unittest.mock import Mock


class TestExecuteSetup(TestCase):

    def test_execute_setup(self):
        self.device = Mock()
        results_map = {'setup': 
        '''
                   --- System Configuration Dialog ---
          
          Continue with configuration dialog? [yes/no]: yes
          
          At any point you may enter a question mark '?' for help.
          Use ctrl-c to abort configuration dialog at any prompt.
          Default settings are in square brackets '[]'.
          
          
          Basic management setup configures only enough connectivity
          for management of the system, extended setup will ask you
          to configure each interface on the system
          
          Would you like to enter basic management setup? [yes/no]: no
          
          First, would you like to see the current interface summary? [yes]: no
          
          Configuring global parameters:
          
            Enter host name [charon_03_8140]:
          
            The enable secret is a password used to protect
            access to privileged EXEC and configuration modes.
            This password, after entered, becomes encrypted in
            the configuration.
            -------------------------------------------------
            secret should be of minimum 10 characters and maximum 32 characters with
            at least 1 upper case, 1 lower case, 1 digit and
            should not be [cisco]
            -------------------------------------------------
            Enter enable secret: **********
            Confirm enable secret: **********
          
            The enable password is used when you do not specify an
            enable secret password, with some older software versions, and
            some boot images.
            Enter enable password: ***
          
            The virtual terminal password is used to protect
            access to the router over a network interface.
            Enter virtual terminal password: ***
          Setup account for accessing HTTP server? [yes]: no
              HTTP server cannot be accessed without a user account. Please remember to setup a privilege 15 user account to access Wireless WebUI
            Configure SNMP Network Management? [no]: no
            Configure LAT? [yes]: no
            Configure IP? [yes]: no
            Configure bridging? [no]: no
            Configure DECnet? [no]: no
            Configure CLNS? [no]: no
            Configure AppleTalk? [no]: no
            Configure Vines? [no]: no
            Configure XNS? [no]: no
            Configure Apollo? [no]: no
          
          Configuring interface parameters:
          
          Do you want to configure GigabitEthernet0/0/0  interface? [no]: no
          
          Do you want to configure GigabitEthernet0/0/1  interface? [no]: no
          
          Do you want to configure GigabitEthernet0/1/0  interface? [yes]: no
          
          Do you want to configure GigabitEthernet0/1/1  interface? [yes]: no
          
          Do you want to configure GigabitEthernet0/1/2  interface? [yes]: no
          
          Do you want to configure GigabitEthernet0/1/3  interface? [yes]: no
          
          Do you want to configure GigabitEthernet0/1/4  interface? [yes]: no
          
          Do you want to configure GigabitEthernet0/1/5  interface? [yes]: no
          
          Do you want to configure GigabitEthernet0/1/6  interface? [yes]: no
          
          Do you want to configure GigabitEthernet0/1/7  interface? [yes]: no
          
          Do you want to configure Vlan1  interface? [yes]: no
          
          Do you want to configure Vlan2  interface? [yes]: no
          
          Would you like to go through AutoSecure configuration? [yes]: no
          AutoSecure dialog can be started later using "auto secure" CLI
          
          The following configuration command script was created:
          
          hostname charon_03_8140
          enable secret 9 $9$K2NklosDYjeR2E$TGoYqZ2FLBpfiiHkNPlYqSvZMibj8UyKptc2M.UlEzs
          enable password lab
          line vty 0 14
          password lab
          no snmp-server
          !
          no ip routing
          no bridge 1
          no decnet routing
          no clns routing
          no appletalk routing
          no vines routing
          no xns routing
          no apollo routing
          !
          interface GigabitEthernet0/0/0
          shutdown
          no ip address
          !
          interface GigabitEthernet0/0/1
          shutdown
          no ip address
          !
          interface GigabitEthernet0/1/0
          !
          interface GigabitEthernet0/1/1
          !
          interface GigabitEthernet0/1/2
          !
          interface GigabitEthernet0/1/3
          !
          interface GigabitEthernet0/1/4
          !
          interface GigabitEthernet0/1/5
          !
          interface GigabitEthernet0/1/6
          !
          interface GigabitEthernet0/1/7
          !
          interface Vlan1
          shutdown
          no ip address
          !
          interface Vlan2
          shutdown
          no ip address
          !
          end
          
          
          [0] Go to the IOS command prompt without saving this config.
          [1] Return back to the setup without saving this config.
          [2] Save this configuration to nvram and exit.
          
          Enter your selection [2]: 2
           WARNING: Configured enable password CLI with weak encryption type 0 will be deprecated in future. Hence please migrate to enable secret CLI which accomplishes same functionality as enable password CLI and which also supports strong irreversible encryption type 9
           SECURITY WARNING - Module: AAA, Command: enable password *, Reason: Configuration employs an Insecure method for password storage, Description: Enable password configured with weak encryption instead of secure type 6 or 9 encryption, Remediation: Please consider migrating to a secure alternative such as Type-6 or Type-9
          Platform cannot disable ip route-cache on GigabitEthernet0/0/0 interface
          
          Platform cannot disable ip route-cache on GigabitEthernet0/0/1 interface
          
          Platform cannot disable ip route-cache on GigabitEthernet0/1/0 interface
          
          Platform cannot disable ip route-cache on GigabitEthernet0/1/1 interface
          
          Platform cannot disable ip route-cache on GigabitEthernet0/1/2 interface
          
          Platform cannot disable ip route-cache on GigabitEthernet0/1/3 interface
          
          Platform cannot disable ip route-cache on GigabitEthernet0/1/4 interface
          
          Platform cannot disable ip route-cache on GigabitEthernet0/1/5 interface
          
          Platform cannot disable ip route-cache on GigabitEthernet0/1/6 interface
          
          Platform cannot disable ip route-cache on GigabitEthernet0/1/7 interface
          
          Platform cannot disable ip route-cache on LIIN0 interface
          
          Platform cannot disable ip route-cache on LI-Null0 interface
          
          Platform cannot disable ip route-cache on Port-channel1 interface
          
          Platform cannot disable ip route-cache on Vlan1 interface
          
          Platform cannot disable ip route-cache on Vlan2 interface
          
          Platform cannot disable ip route-cache on VoIP-Null0 interface
          
          Building configuration...
          [OK]
          Use the enabled mode 'configure' command to modify this configuration.''',
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        
        result = execute_setup(self.device, 'Crdc12345!', 'lab', 'lab', None, 600)
        self.assertIn(
            'setup',
            self.device.execute.call_args_list[0][0]
        )
        expected_output = None
        self.assertEqual(result, expected_output)
