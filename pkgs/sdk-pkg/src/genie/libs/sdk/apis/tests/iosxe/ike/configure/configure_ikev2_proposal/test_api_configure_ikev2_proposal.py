import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ike.configure import configure_ikev2_proposal


class TestConfigureIkev2Proposal(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          TLS_Mad2:
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
        self.device = self.testbed.devices['TLS_Mad2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_ikev2_proposal(self):
        result = configure_ikev2_proposal(self.device, 'IKEv2_PROPOSAL', 'aes-gcm-256', 19, 'sha512', 'sha512')
        expected_output = None
        self.assertEqual(result, expected_output)
