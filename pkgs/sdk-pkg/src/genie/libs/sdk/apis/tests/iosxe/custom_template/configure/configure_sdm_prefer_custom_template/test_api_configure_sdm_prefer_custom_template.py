import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.custom_template.configure import configure_sdm_prefer_custom_template


class TestConfigureSdmPreferCustomTemplate(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          prom_SVL:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: '9500'
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['prom_SVL']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_configure_sdm_prefer_custom_template(self):
        result = configure_sdm_prefer_custom_template(self.device, 'commit')
        expected_output = None
        self.assertEqual(result, expected_output)
