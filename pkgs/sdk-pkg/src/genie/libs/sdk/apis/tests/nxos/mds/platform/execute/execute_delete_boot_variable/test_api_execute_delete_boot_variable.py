import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.nxos.mds.platform.execute import execute_delete_boot_variable


class TestExecuteDeleteBootVariable(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          II23-FCCORE:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os nxos --mock_data_dir mock_data --state connect
                protocol: unknown
            os: nxos
            platform: MDS
            type: MDS
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['II23-FCCORE']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_delete_boot_variable(self):
        result = execute_delete_boot_variable(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
