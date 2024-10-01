import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_ikev2_profile_pre_share


class TestConfigureIkev2ProfilePreShare(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          PE-B:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['PE-B']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ikev2_profile_pre_share(self):
        result = configure_ikev2_profile_pre_share(self.device, 'scale_ikev2_profile_v4_phy', 'pre-share', 'pre-share', 'ikev2_key_v4_phy', '19.1.1.0', '255.255.255.0', 'ipv4', None, '2', 'periodic', None, None, 'TenGigabitEthernet1/0/1')
        expected_output = None
        self.assertEqual(result, expected_output)
