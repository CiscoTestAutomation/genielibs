import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_service_policy


class TestConfigureInterfaceServicePolicy(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          ASR1002-HX:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['ASR1002-HX']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_interface_service_policy(self):
        result = configure_interface_service_policy(self.device, 'Te0/1/0', 'grandparent', 'out')
        expected_output = 'interface Te0/1/0\r\ninterface Te0/1/0\r\nservice-policy out grandparent\r\nservice-policy out grandparent\r\n'
        self.assertEqual(result, expected_output)
