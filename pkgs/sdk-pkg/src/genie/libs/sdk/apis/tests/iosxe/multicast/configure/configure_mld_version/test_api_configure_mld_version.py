import os
import unittest
from pyats.topology import loader
<<<<<<< HEAD:pkgs/sdk-pkg/src/genie/libs/sdk/apis/tests/iosxe/multicast/configure/configure_mld_version/test_api_configure_mld_version.py
from genie.libs.sdk.apis.iosxe.multicast.configure import configure_mld_version


class TestConfigureMldVersion(unittest.TestCase):
=======
from genie.libs.sdk.apis.iosxe.interface.configure import configure_monitor_erspan_source_interface


class TestConfigureMonitorErspanSourceInterface(unittest.TestCase):
>>>>>>> external/master:pkgs/sdk-pkg/src/genie/libs/sdk/apis/tests/iosxe/interface/configure/configure_monitor_erspan_source_interface/test_api_configure_monitor_erspan_source_interface.py

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          T2-9500-RA_SDG:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9500
            type: c9500
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['T2-9500-RA_SDG']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

<<<<<<< HEAD:pkgs/sdk-pkg/src/genie/libs/sdk/apis/tests/iosxe/multicast/configure/configure_mld_version/test_api_configure_mld_version.py
    def test_configure_mld_version(self):
        result = configure_mld_version(self.device, 202, 2)
=======
    def test_configure_monitor_erspan_source_interface(self):
        result = configure_monitor_erspan_source_interface(self.device, '1', 'te1/0/2', 'rx')
>>>>>>> external/master:pkgs/sdk-pkg/src/genie/libs/sdk/apis/tests/iosxe/interface/configure/configure_monitor_erspan_source_interface/test_api_configure_monitor_erspan_source_interface.py
        expected_output = None
        self.assertEqual(result, expected_output)
