import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ike.configure import configure_ikev2_profile_advanced


class TestConfigureIkev2ProfileAdvanced(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          RAMONES:
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
        self.device = self.testbed.devices['RAMONES']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ikev2_profile_advanced(self):
        result = configure_ikev2_profile_advanced(self.device, 'IKEv2_PROFILE', None, None, None, None, None, None, None, None, None, False, None, False, None, None, None, None, None, False, False, None, False, False, False, False, None, False, None, None, None, False, None, None, None, None, None, False, None, False, None, None, None, None, None, False, None, 'client', False, False, None, None, None, False, False, None, False, False)
        expected_output = None
        self.assertEqual(result, expected_output)
