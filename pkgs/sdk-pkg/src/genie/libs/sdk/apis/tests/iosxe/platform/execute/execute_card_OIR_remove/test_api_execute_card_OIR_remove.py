import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.platform.execute import execute_card_OIR_remove


class TestExecuteCardOirRemove(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          intrepid-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: INTERPID
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['intrepid-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_card_OIR_remove(self):
        result = execute_card_OIR_remove(self.device, '1/0', '1', 60)
        expected_output = None
        self.assertEqual(result, expected_output)
