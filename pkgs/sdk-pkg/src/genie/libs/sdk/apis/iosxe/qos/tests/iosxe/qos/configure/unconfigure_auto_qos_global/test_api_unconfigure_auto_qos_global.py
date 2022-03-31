import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.qos.configure import unconfigure_auto_qos_global


class TestUnconfigureAutoQosGlobal(unittest.TestCase):

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

    def test_unconfigure_auto_qos_global(self):
        result = unconfigure_auto_qos_global(self.device, 'compact')
        expected_output = None
        self.assertEqual(result, expected_output)
