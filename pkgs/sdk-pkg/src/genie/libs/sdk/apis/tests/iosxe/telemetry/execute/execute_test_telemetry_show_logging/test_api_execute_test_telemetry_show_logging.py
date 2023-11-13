import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.telemetry.execute import execute_test_telemetry_show_logging
from genie.libs.sdk.apis.utils import sanitize

class TestExecuteTestTelemetryShowLogging(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          Switch:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: cat9k
            type: c9300
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['Switch']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_execute_test_telemetry_show_logging(self):
        result = execute_test_telemetry_show_logging(self.device)
        expected_output = ('Syslog logging: enabled (0 messages dropped, 2 messages rate-limited, 0 '
 'flushes, 0 overruns, xml disabled, filtering disabled)\r\n'
 '\r\n'
 'No Active Message Discriminator.\r\n'
 '\r\n'
 '\r\n'
 '\r\n'
 'No Inactive Message Discriminator.\r\n'
 '\r\n'
 '\r\n'
 '    Console logging: disabled\r\n'
 '    Monitor logging: disabled\r\n'
 '    Buffer logging:  level debugging, 423 messages logged, xml disabled,\r\n'
 '                    filtering disabled\r\n'
 '    Exception Logging: size (4096 bytes)\r\n'
 '    Count and timestamp logging messages: disabled\r\n'
 '    File logging: disabled\r\n'
 '    Persistent logging: disabled\r\n'
 '\r\n'
 'No active filter modules.\r\n'
 '\r\n'
 '    Trap logging: level informational, 414 message lines logged\r\n'
 '        Logging Source-Interface:       VRF Name:\r\n'
 '    TLS Profiles: \r\n'
 '\r\n'
 'Log Buffer (1000000 bytes):\r\n'
 '\r\n'
 '*Nov 13 15:53:49.926 PDT: %PAE_CORE_TEST-6-REPORT_ID: Switch 2 R0/0: paed: '
 'Created report id: 1668380029\r\n'
 '*Nov 13 15:54:46.371 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 15:54:47.458 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 15:54:47.875 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 15:55:13.959 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 15:55:14.391 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 15:55:21.206 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 15:55:22.027 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 15:56:52.287 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 15:56:52.892 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 15:58:01.254 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 15:58:01.677 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 15:58:33.192 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 15:58:34.304 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 15:58:34.463 PDT: %SMAN-5-CRFT_COLLECT_REQUEST_SUCCESS: Switch 2 '
 'R0/0: smand: CRFT collection completed successfully.\r\n'
 '*Nov 13 15:58:37.597 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 15:59:09.273 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 15:59:13.111 PDT: %SELINUX-5-MISMATCH: Switch 2 R0/0: audispd: '
 'type=AVC msg=audit(1668380353.109:123): avc:  denied  { read write } for  '
 'pid=14256 comm="dmesg" path="/dev/pts/1" dev="devpts" ino=4 '
 'scontext=system_u:system_r:dmesg_t:s0 '
 'tcontext=system_u:object_r:telnetd_devpts_t:s0 tclass=chr_file '
 'permissive=1\r\n'
 '*Nov 13 15:59:13.111 PDT: %SELINUX-5-MISMATCH: Switch 2 R0/0: audispd: '
 'type=AVC msg=audit(1668380353.109:123): avc:  denied  { append } for  '
 'pid=14256 comm="dmesg" path="/dev/pts/1" dev="devpts" ino=4 '
 'scontext=system_u:system_r:dmesg_t:s0 '
 'tcontext=system_u:object_r:telnetd_devpts_t:s0 tclass=chr_file '
 'permissive=1\r\n'
 '*Nov 13 15:59:14.475 PDT: %SELINUX-5-MISMATCH: Switch 8 R0/0: audispd: '
 'type=AVC msg=audit(1668380354.473:126): avc:  denied  { read write } for  '
 'pid=8018 comm="dmesg" path="/dev/pts/0" dev="devpts" ino=3 '
 'scontext=system_u:system_r:dmesg_t:s0 '
 'tcontext=system_u:object_r:telnetd_devpts_t:s0 tclass=chr_file '
 'permissive=1\r\n'
 '*Nov 13 15:59:14.475 PDT: %SELINUX-5-MISMATCH: Switch 8 R0/0: audispd: '
 'type=AVC msg=audit(1668380354.473:126): avc:  denied  { append } for  '
 'pid=8018 comm="dmesg" path="/dev/pts/0" dev="devpts" ino=3 '
 'scontext=system_u:system_r:dmesg_t:s0 '
 'tcontext=system_u:object_r:telnetd_devpts_t:s0 tclass=chr_file '
 'permissive=1\r\n'
 '*Nov 13 15:59:48.216 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 17:19:47.008 PDT: %PLATFORM-4-ELEMENT_WARNING: Switch 2 R0/0: smand: '
 '8/RP/0: limited space - copy corefiles/switch-reports out of flash:core & '
 'crashinfo: directories. crashinfo: value 100% (1612 MB) exceeds warning '
 'level 80% (1290 MB).\r\n'
 '*Nov 13 17:22:49.302 PDT: %PLATFORM-4-ELEMENT_WARNING: Switch 2 R0/0: smand: '
 '2/RP/0: limited space - copy files out of flash: directory. flash: value 75% '
 '(8276 MB) exceeds warning level 70% (7760 MB).\r\n'
 '*Nov 13 17:22:49.301 PDT: %PLATFORM-4-ELEMENT_WARNING: Switch 8 R0/0: smand: '
 '2/RP/0: limited space - copy files out of flash: directory. flash: value 75% '
 '(8276 MB) exceeds warning level 70% (7760 MB).\r\n'
 '*Nov 13 17:23:07.009 PDT: %PLATFORM-4-ELEMENT_WARNING: Switch 8 R0/0: smand: '
 '8/RP/0: limited space - copy corefiles/switch-reports out of flash:core & '
 'crashinfo: directories. crashinfo: value 100% (1612 MB) exceeds warning '
 'level 80% (1290 MB).\r\n'
 '*Nov 13 21:42:42.992 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 21:44:57.204 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 22:01:11.255 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 22:02:01.075 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 22:08:32.698 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 22:08:49.630 PDT: %PAE_CORE_TEST-6-REPORT_ID: Switch 2 R0/0: paed: '
 'Created report id: 1668402529\r\n'
 '*Nov 13 22:09:10.831 PDT: %PAE_CORE_TEST-6-REPORT_ID: Switch 2 R0/0: paed: '
 'Created report id: 1668402550\r\n'
 '*Nov 13 22:13:51.244 PDT: %PAE_CORE_TEST-6-REPORT_ID: Switch 2 R0/0: paed: '
 'Created report id: 1668402831\r\n'
 '*Nov 13 22:14:22.327 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 22:15:03.853 PDT: %PAE_CORE_TEST-6-REPORT_ID: Switch 2 R0/0: paed: '
 'Created report id: 1668402903\r\n'
 '*Nov 13 22:16:33.091 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console\r\n'
 '*Nov 13 22:16:51.503 PDT: %PAE_CORE_TEST-6-REPORT_ID: Switch 2 R0/0: paed: '
 'Created report id: 1668403011\r\n'
 '*Nov 13 22:17:28.120 PDT: %SYS-5-CONFIG_I: Configured from console by '
 'console')
        self.assertEqual(sanitize(result), sanitize(expected_output))
