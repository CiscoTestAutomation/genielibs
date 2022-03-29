import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.cheetah.ap.execute import execute_prime_ap


class TestExecutePrimeAp(unittest.TestCase):

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

    def test_execute_prime_ap(self):
        result = execute_prime_ap(self.device, '9.4.62.51', 'vidya-ewlc-5')
        expected_output = True
        self.assertEqual(result, expected_output)
