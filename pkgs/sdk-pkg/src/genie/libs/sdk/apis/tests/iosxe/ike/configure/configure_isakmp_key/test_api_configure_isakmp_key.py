import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ike.configure import configure_isakmp_key


class TestConfigureIsakmpKey(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          INT1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iosxe
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['INT1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_isakmp_key(self):
        result = configure_isakmp_key(self.device, 'test123', '0', None, None, None, '2007:1::44/112', 'True')
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_isakmp_key_1(self):
        result = configure_isakmp_key(self.device, 'ash123', '0', '20.18.19.5', '255.255.255.0', None, None, False)
        expected_output = None
        self.assertEqual(result, expected_output)
