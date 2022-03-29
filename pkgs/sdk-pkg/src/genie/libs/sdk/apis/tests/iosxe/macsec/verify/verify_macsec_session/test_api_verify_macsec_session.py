import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.macsec.verify import verify_macsec_session


class TestVerifyMacsecSession(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          FE3:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['FE3']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_macsec_session(self):
        result = verify_macsec_session(self.device, 'TwentyFiveGigE 1/0/2', 'TwentyFiveGigE 1/0/2', 'GCM-AES-128', '10', 'must secure', 0, 5)
        expected_output = True
        self.assertEqual(result, expected_output)
