import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.interface.verify import verify_etherchannel_counter


class TestVerifyEtherchannelCounter(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          PE1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['PE1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_etherchannel_counter(self):
        result = verify_etherchannel_counter(self.device, 'Port-channel10', ['in', 'out'], 164349, 20000, 40)
        expected_output = False
        self.assertEqual(result, expected_output)
