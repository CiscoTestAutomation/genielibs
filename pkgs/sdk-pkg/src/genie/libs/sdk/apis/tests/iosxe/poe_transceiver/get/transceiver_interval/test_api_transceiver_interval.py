import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.poe_transceiver.get import transceiver_interval


class TestTransceiverInterval(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          A2-9300-3M:
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
        self.device = self.testbed.devices['A2-9300-3M']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_transceiver_interval(self):
        result = transceiver_interval(self.device)
        expected_output = {'interval': [30], 'transceiver': ['TenGigabitEthernet3/1/1']}
        self.assertEqual(result, expected_output)
