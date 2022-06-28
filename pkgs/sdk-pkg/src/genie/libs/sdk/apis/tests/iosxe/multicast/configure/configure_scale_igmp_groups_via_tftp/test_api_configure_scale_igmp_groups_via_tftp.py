import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.multicast.configure import configure_scale_igmp_groups_via_tftp


class TestConfigureScaleIgmpGroupsViaTftp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Organ:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: router
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Organ']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_scale_igmp_groups_via_tftp(self):
        result = configure_scale_igmp_groups_via_tftp(self.device, {'myftpserver': {'custom': {'scale_config_path': '/auto/tftp-sjc-users4/siwwu/'},
                 'dynamic': True,
                 'protocol': 'ftp'}}, 'GigabitEthernet3', 'join-group', '235.0.0.1', '0.0.0.1', 15, False, False)
        expected_output = ('\n'
 '        interface GigabitEthernet3\n'
 '             ip igmp join-group 235.0.0.1\n'
 '        \n'
 '        interface GigabitEthernet3\n'
 '             ip igmp join-group 235.0.0.2\n'
 '        \n'
 '        interface GigabitEthernet3\n'
 '             ip igmp join-group 235.0.0.3\n'
 '        \n'
 '        interface GigabitEthernet3\n'
 '             ip igmp join-group 235.0.0.4\n'
 '        \n'
 '        interface GigabitEthernet3\n'
 '             ip igmp join-group 235.0.0.5\n'
 '        \n'
 '        interface GigabitEthernet3\n'
 '             ip igmp join-group 235.0.0.6\n'
 '        \n'
 '        interface GigabitEthernet3\n'
 '             ip igmp join-group 235.0.0.7\n'
 '        \n'
 '        interface GigabitEthernet3\n'
 '             ip igmp join-group 235.0.0.8\n'
 '        \n'
 '        interface GigabitEthernet3\n'
 '             ip igmp join-group 235.0.0.9\n'
 '        \n'
 '        interface GigabitEthernet3\n'
 '             ip igmp join-group 235.0.0.10\n'
 '        \n'
 '        interface GigabitEthernet3\n'
 '             ip igmp join-group 235.0.0.11\n'
 '        \n'
 '        interface GigabitEthernet3\n'
 '             ip igmp join-group 235.0.0.12\n'
 '        \n'
 '        interface GigabitEthernet3\n'
 '             ip igmp join-group 235.0.0.13\n'
 '        \n'
 '        interface GigabitEthernet3\n'
 '             ip igmp join-group 235.0.0.14\n'
 '        \n'
 '        interface GigabitEthernet3\n'
 '             ip igmp join-group 235.0.0.15\n'
 '        ')
        self.assertEqual(result, expected_output)
