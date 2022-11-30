import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.dot1x.configure import configure_service_template_with_access_group


class TestConfigureServiceTemplateWithAccessGroup(unittest.TestCase):

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

    def test_configure_service_template_with_access_group(self):
        result = configure_service_template_with_access_group(self.device, 'DefaultCriticalAccess_SRV_TEMPLATE', 'IPV4_CRITICAL_AUTH_ACL')
        expected_output = None
        self.assertEqual(result, expected_output)
