import os
import unittest
from pyats.topology import loader
from genie.libs.sdk.apis.iosxe.utils import request_system_shell


class TestRequestSystemShell(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        testbed = f"""
        devices:
          9350-stack-1:
            connections:
              defaults:
                class: unicon.Unicon
              a:
                command: mock_device_cli --os iosxe --mock_data_dir {os.path.dirname(__file__)}/mock_data --state connect
                protocol: unknown
            os: iosxe
            platform: c9350
            type: c9350
        """
        self.testbed = loader.load(testbed)
        self.device = self.testbed.devices['9350-stack-1']
        self.device.connect(
            learn_hostname=True,
            init_config_commands=[],
            init_exec_commands=[]
        )

    def test_request_system_shell(self):
        self.maxDiff = None
        result = request_system_shell(self.device, 'active', 'R0', False, True, 'ls', 60)
        expected_output = ('Activity within this shell can jeopardize the functioning of the system.\r\n'
                           'Are you sure you want to continue? [y/n] y\r\n'
                           '2023/10/10 09:50:10 : Shell access was granted to user <anon>; Trace file: , '
                           '/crashinfo/tracelogs/system_shell_R0-0.31502_0.20231010095010.bin\r\n'
                           '********************************************************************** \r\n'
                           'Activity within this shell can jeopardize the functioning \r\n'
                           'of the system.\r\n'
                           'Use this functionality only under supervision of Cisco Support.\r\n'
                           '\r\n'
                           'Session will be logged to:\r\n'
                           '  crashinfo:tracelogs/system_shell_R0-0.31502_0.20231010095010.bin\r\n'
                           '********************************************************************** \r\n'
                           "Terminal type 'network' unknown.  Assuming vt100"
                           '3pa\t\t      dev\t      lib64\t\t sbin\r\n'
                           'POE\t\t      disk0\t      lic0\t\t sdwan-utils\r\n'
                           'app\t\t      drec0\t      lic1\t\t sys\r\n'
                           'appstore_flash\t      etc\t      lua\t\t tftp\r\n'
                           'appstore_hd\t      explode\t      misc\t\t tmp\r\n'
                           'auto\t\t      explode-common  mnt\t\t ucode0\r\n'
                           'bin\t\t      firmware\t      mount_packages.sh  umount_packages.sh\r\n'
                           'bless\t\t      flash\t      ngwc_config\t usb0\r\n'
                           'bootflash\t      guestshell      obfl0\t\t usb1\r\n'
                           'codesign.pubkey       harddisk\t      opt\t\t usr\r\n'
                           'codesign.revkey       hugepages.sh    platform-specific  var\r\n'
                           'common\t\t      init\t      proc\t\t verify_packages.sh\r\n'
                           'config\t\t      initrd.image    rmon_vars.sh\t webui\r\n'
                           'copy_act2_sr_libs.sh  install\t      rommon_to_env\r\n'
                           'cpld_util.sh\t      issu\t      root\r\n'
                           'crashinfo\t      lib\t      run')
        self.assertEqual(result, expected_output)

    def test_request_system_shell_processor_slot(self):
        self.maxDiff = None
        result = request_system_shell(self.device, None, 'F0')
        expected_output = ('Activity within this shell can jeopardize the functioning of the system.\r\n'
                           'Are you sure you want to continue? [y/n] y\r\n'
                           '2024/02/28 11:43:13 : Shell access was granted to user ; Trace file: , '
                           '/harddisk/tracelogs/system_shell_F0-0.5246_0.20240228114313.bin\r\n'
                           '** \r\n'
                           'Activity within this shell can jeopardize the functioning \r\n'
                           'of the system.\r\n'
                           'Use this functionality only under supervision of Cisco Support.\r\n'
                           'Only RP shell access is available for this platform.\r\n'
                           '\r\n'
                           'Session will be logged to:\r\n'
                           'harddisk:tracelogs/system_shell_F0-0.5246_0.20240228114313.bin\r\n'
                           '**\r\n'
                           "Terminal type 'network' unknown. Assuming vt100")
        self.assertEqual(result, expected_output)

    def test_request_system_shell_multiple_commands(self):
        self.maxDiff = None
        expected_output = ('Activity within this shell can jeopardize the functioning of the system.\r\n'
                           'Are you sure you want to continue? [y/n] y\r\n'
                           '2023/10/10 09:50:10 : Shell access was granted to user <anon>; Trace file: , '
                           '/crashinfo/tracelogs/system_shell_R0-0.31502_0.20231010095010.bin\r\n'
                           '********************************************************************** \r\n'
                           'Activity within this shell can jeopardize the functioning \r\n'
                           'of the system.\r\n'
                           'Use this functionality only under supervision of Cisco Support.\r\n'
                           '\r\n'
                           'Session will be logged to:\r\n'
                           '  crashinfo:tracelogs/system_shell_R0-0.31502_0.20231010095010.bin\r\n'
                           '********************************************************************** \r\n'
                           "Terminal type 'network' unknown.  Assuming vt100"
                           '[69318.122111] NFS: SECINFO: security flavor 390005 is not supported\r\n'
                           '[69404.497666] igb: eth1 NIC Link is Up 1000 Mbps Full Duplex, Flow Control: RX/TX\r\n'
                           '[69437.624382] RP3 CPLD: Old val 0x30003 Updated val 0x30003\r\n'
                           '[69437.625824] RP3 CPLD: Old val 0x30003 Updated val 0x30003\r\n'
                           '[69961.469516] watchdog: watchdog0: nowayout prevents watchdog being stopped!\r\n'
                           '[69961.469553] watchdog: watchdog0: nowayout prevents watchdog being stopped!\r\n'
                           '[69961.469555] watchdog: watchdog0: watchdog did not stop!\r\n'
                           '[69961.534934] systemd[1]: systemd 251 running in system mode (+PAM +AUDIT +SELINUX '
                           '-APPARMOR +IMA -SMACK -SECCOMP -GCRYPT -GNUTLS -OPENSSL +ACL +BLKID -CURL -ELFUTILS '
                           '-FIDO2 -IDN2 -IDN -IPTC +KMOD -LIBCRYPTSETUP +LIBFDISK -PCRE2 -PWQUALITY -P11KIT '
                           '-QRENCODE -TPM2 -BZIP2 -LZ4 -XZ -ZLIB +ZSTD -BPF_FRAMEWORK '
                           '-XKBCOMMON +UTMP +SYSVINIT default-hierarchy=hybrid)\r\n'
                           '[69961.535030] systemd[1]: Detected architecture x86-64.\r\n'
                           '[69966.416588] watchdog: watchdog0: watchdog did not stop!')
        cmds_list= [
            "sed -r -i 's/(RuntimeWatchdogSec=).*/\\10/' /etc/systemd/system.conf",
            "systemctl daemon-reexec",
            "echo 1 > /dev/watchdog",
            "dmesg | tail"
        ]
        result = request_system_shell(self.device, command=cmds_list)
        self.assertEqual(result, expected_output)
