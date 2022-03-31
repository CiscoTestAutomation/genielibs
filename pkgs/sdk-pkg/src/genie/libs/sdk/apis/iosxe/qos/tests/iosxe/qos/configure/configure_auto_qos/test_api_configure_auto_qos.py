import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.qos.configure import configure_auto_qos


class TestConfigureAutoQos(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Startek:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: router
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Startek']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_auto_qos(self):
        result = configure_auto_qos(self.device, 'Hu1/0/3', 'trust', 'dscp')
        expected_output = None
        self.assertEqual(result, expected_output)
