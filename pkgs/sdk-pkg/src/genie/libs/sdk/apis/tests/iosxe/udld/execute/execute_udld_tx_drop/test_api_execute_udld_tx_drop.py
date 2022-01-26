import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.udld.execute import execute_udld_tx_drop


class TestExecuteUdldTxDrop(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Switch:
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
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_udld_tx_drop(self):
        result = execute_udld_tx_drop(self.device, 'GigabitEthernet3/0/1')
        expected_output = None
        self.assertEqual(result, expected_output)
