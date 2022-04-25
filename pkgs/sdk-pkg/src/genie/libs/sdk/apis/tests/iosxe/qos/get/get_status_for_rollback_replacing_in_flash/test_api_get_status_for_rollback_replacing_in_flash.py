import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.qos.get import get_status_for_rollback_replacing_in_flash


class TestGetStatusForRollbackReplacingInFlash(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = """
        devices:
          Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: C9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_get_status_for_rollback_replacing_in_flash(self):
        result = get_status_for_rollback_replacing_in_flash(self.device)
        expected_output = None
        self.assertEqual(result, expected_output)
