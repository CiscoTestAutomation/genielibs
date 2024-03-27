import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.nxos.platform.get import get_lc_slots


class TestGetLcSlots(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Mando-7:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os nxos --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: nxos
            platform: n9k
            type: n9k
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Mando-7']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_lc_slots(self):
        result = get_lc_slots(self.device)
        expected_output = ['4']
        self.assertEqual(result, expected_output)
