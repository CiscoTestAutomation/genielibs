import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.cheetah.ap.execute import execute_erase_ap


class TestExecuteEraseAp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          APCC16.7EDB.4168:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os cheetah --mock_data_dir mock_data --state connect
                protocol: unknown
            os: cheetah
            platform: ap
            type: AP
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['APCC16.7EDB.4168']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_erase_ap(self):
        result = execute_erase_ap(self.device)
        expected_output = True
        self.assertEqual(result, expected_output)
