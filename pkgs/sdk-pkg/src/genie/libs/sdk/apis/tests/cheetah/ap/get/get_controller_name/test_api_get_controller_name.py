import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.cheetah.ap.get import get_controller_name


class TestGetControllerName(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          AP188B.4500.5EE8:
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
        self.device = self.testbed.devices['AP188B.4500.5EE8']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_controller_name(self):
        result = get_controller_name(self.device)
        expected_output = 'vidya-ewlc-5'
        self.assertEqual(result, expected_output)
