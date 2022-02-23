import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.ptp.configure import unconfigure_ptp_8275_holdover_spec_duration


class TestUnconfigurePtp8275HoldoverSpecDuration(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          centi_48TX_1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['centi_48TX_1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_unconfigure_ptp_8275_holdover_spec_duration(self):
        result = unconfigure_ptp_8275_holdover_spec_duration(device=self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
