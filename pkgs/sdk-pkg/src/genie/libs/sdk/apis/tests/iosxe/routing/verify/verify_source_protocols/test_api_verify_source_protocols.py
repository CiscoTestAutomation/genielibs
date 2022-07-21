import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.routing.verify import verify_source_protocols


class TestVerifySourceProtocols(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          rtr1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: iol
            type: iol
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['rtr1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_verify_source_protocols(self):
        result = verify_source_protocols(self.device, ['141.1.1.0', '1.1.1.1', '141.1.4.0'], 'C')
        expected_output = True
        self.assertEqual(result, expected_output)
