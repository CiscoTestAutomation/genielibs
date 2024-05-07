import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_interface_mac_address


class TestConfigureInterfaceMacAddress(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          g24c:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat3k
            model: c3650
            type: c3650
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['g24c']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_interface_mac_address(self):
        result = configure_interface_mac_address(device=self.device, interface='ten1/0/7', mac='0000.1111.2222')
        expected_output = None
        self.assertEqual(result, expected_output)
