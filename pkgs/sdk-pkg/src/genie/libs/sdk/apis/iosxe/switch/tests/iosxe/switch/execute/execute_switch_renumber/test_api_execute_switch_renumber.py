import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.switch.execute import execute_switch_renumber


class TestExecuteSwitchRenumber(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          intrepid-2:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: INTREPID
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['intrepid-2']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_switch_renumber(self):
        result = execute_switch_renumber(self.device, '1', '2')
        expected_output = None
        self.assertEqual(result, expected_output)
