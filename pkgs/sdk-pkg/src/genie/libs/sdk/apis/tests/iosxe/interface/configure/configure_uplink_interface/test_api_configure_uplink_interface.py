import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import configure_uplink_interface


class TestConfigureUplinkInterface(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          9400-D2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            model: c9400
            type: c9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9400-D2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_uplink_interface(self):
        result = configure_uplink_interface(self.device, {'GigabitEthernet1/1/0/1': None}, '1-4093', '1222', '222')
        expected_output = None
        self.assertEqual(result, expected_output)
