import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.configure import config_portchannel_range


class TestConfigPortchannelRange(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          mac-gen2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: single_rp
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['mac-gen2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_config_portchannel_range(self):
        result = config_portchannel_range(device=self.device, portchannel_start='10', portchannel_end='20')
        expected_output = None
        self.assertEqual(result, expected_output)
