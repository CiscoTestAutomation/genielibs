import os
from pyats.topology import loader
from unittest import TestCase
from genie.libs.sdk.apis.nxos.platform.get import get_standby_systemcontroller_slot


class TestGetStandbySystemcontrollerSlot(TestCase):
    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Reg22-EX-EOR1:
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
        self.device = self.testbed.devices['Reg22-EX-EOR1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_standby_systemcontroller_slot(self):
        result = get_standby_systemcontroller_slot(self.device)
        expected_output = ['29']
        self.assertEqual(result, expected_output)
