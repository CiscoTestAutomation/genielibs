import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.flow.configure import disable_et_analytics


class TestDisableEtAnalytics(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Macallan1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9400
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Macallan1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_disable_et_analytics(self):
        result = disable_et_analytics(self.device, 'GigabitEthernet1/0/35')
        expected_output = None
        self.assertEqual(result, expected_output)
