import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.flow.configure import configure_fnf_flow_record_match_flow


class TestConfigureFnfFlowRecordMatchFlow(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          javelin-morph-bgl16-full-tb2-dut1:
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
        self.device = self.testbed.devices['javelin-morph-bgl16-full-tb2-dut1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_fnf_flow_record_match_flow(self):
        result = configure_fnf_flow_record_match_flow(self.device, 'map1', 'observation', None)
        expected_output = None
        self.assertEqual(result, expected_output)

    def test_configure_fnf_flow_record_match_flow_1(self):
        result = configure_fnf_flow_record_match_flow(self.device, 'map2', 'cts', 'destination')
        expected_output = None
        self.assertEqual(result, expected_output)
