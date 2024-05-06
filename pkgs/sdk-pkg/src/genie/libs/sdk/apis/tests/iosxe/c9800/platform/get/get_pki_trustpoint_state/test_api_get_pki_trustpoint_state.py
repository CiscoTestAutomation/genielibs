import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.get import get_pki_trustpoint_state


class TestGetPkiTrustpointState(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          vidya-ewlc-5:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            model: c9800
            type: wlc
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['vidya-ewlc-5']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_pki_trustpoint_state(self):
        result = get_pki_trustpoint_state(self.device, 'vidya-ewlc-5_WLC_TP')
        expected_output = {'certificate_requests': 'yes',
 'issuing_ca_authenticated': 'yes',
 'keys_generated': 'yes'}
        self.assertEqual(result, expected_output)
