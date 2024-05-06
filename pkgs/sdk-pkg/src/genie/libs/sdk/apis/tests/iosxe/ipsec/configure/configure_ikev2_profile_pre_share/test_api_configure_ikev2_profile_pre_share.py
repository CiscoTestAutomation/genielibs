import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ipsec.configure import configure_ikev2_profile_pre_share


class TestConfigureIkev2ProfilePreShare(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          kparames_csr1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat8k
            model: c8000v
            type: iosxe
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['kparames_csr1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ikev2_profile_pre_share(self):
        result = configure_ikev2_profile_pre_share(self.device, 'test_ike_prof', 'pre-share', 'pre-share', '1', None, '', 'ipv4', None, '2', 'periodic', 'UNDERLAY')
        expected_output = None
        self.assertEqual(result, expected_output)
