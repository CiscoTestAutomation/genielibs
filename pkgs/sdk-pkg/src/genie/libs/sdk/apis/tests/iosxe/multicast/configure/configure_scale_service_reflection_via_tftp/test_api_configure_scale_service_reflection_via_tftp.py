import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.multicast.configure import configure_scale_service_reflection_via_tftp


class TestConfigureScaleServiceReflectionViaTftp(unittest.TestCase):

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

    def test_configure_scale_service_reflection_via_tftp(self):
        result = configure_scale_service_reflection_via_tftp(self.device, {'myftpserver': {'custom': {'scale_config_path': '/auto/tftp-sjc-users4/siwwu/'},
                 'dynamic': True,
                 'protocol': 'ftp'}}, 'vif1', 'GigabitEthernet5', '66.0.0.0', '0.0.1.0', '235.0.0.0', '0.0.0.0', 24, '10.1.1.1', '0.0.0.1', 10, False, False)
        expected_output = ('\n'
 '        interface vif1\n'
 '             ip service reflect GigabitEthernet5 destination 66.0.0.0 to '
 '235.0.0.0 mask-len 24 source 10.1.1.1\n'
 '        \n'
 '        interface vif1\n'
 '             ip service reflect GigabitEthernet5 destination 66.0.1.0 to '
 '235.0.0.0 mask-len 24 source 10.1.1.2\n'
 '        \n'
 '        interface vif1\n'
 '             ip service reflect GigabitEthernet5 destination 66.0.2.0 to '
 '235.0.0.0 mask-len 24 source 10.1.1.3\n'
 '        \n'
 '        interface vif1\n'
 '             ip service reflect GigabitEthernet5 destination 66.0.3.0 to '
 '235.0.0.0 mask-len 24 source 10.1.1.4\n'
 '        \n'
 '        interface vif1\n'
 '             ip service reflect GigabitEthernet5 destination 66.0.4.0 to '
 '235.0.0.0 mask-len 24 source 10.1.1.5\n'
 '        \n'
 '        interface vif1\n'
 '             ip service reflect GigabitEthernet5 destination 66.0.5.0 to '
 '235.0.0.0 mask-len 24 source 10.1.1.6\n'
 '        \n'
 '        interface vif1\n'
 '             ip service reflect GigabitEthernet5 destination 66.0.6.0 to '
 '235.0.0.0 mask-len 24 source 10.1.1.7\n'
 '        \n'
 '        interface vif1\n'
 '             ip service reflect GigabitEthernet5 destination 66.0.7.0 to '
 '235.0.0.0 mask-len 24 source 10.1.1.8\n'
 '        \n'
 '        interface vif1\n'
 '             ip service reflect GigabitEthernet5 destination 66.0.8.0 to '
 '235.0.0.0 mask-len 24 source 10.1.1.9\n'
 '        \n'
 '        interface vif1\n'
 '             ip service reflect GigabitEthernet5 destination 66.0.9.0 to '
 '235.0.0.0 mask-len 24 source 10.1.1.10\n'
 '        ')
        self.assertEqual(result, expected_output)
