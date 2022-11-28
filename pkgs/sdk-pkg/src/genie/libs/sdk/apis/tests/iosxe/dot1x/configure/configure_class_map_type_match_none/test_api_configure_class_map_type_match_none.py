import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dot1x.configure import configure_class_map_type_match_none


class TestConfigureClassMapTypeMatchNone(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          stack-12m:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9300
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['stack-12m']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_class_map_type_match_none(self):
        result = configure_class_map_type_match_none(self.device, 'NOT_IN_CRITICAL_AUTH', 'DefaultCriticalVoice_SRV_TEMPLATE')
        expected_output = None
        self.assertEqual(result, expected_output)
