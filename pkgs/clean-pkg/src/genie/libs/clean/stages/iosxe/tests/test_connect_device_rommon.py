
import unittest
from textwrap import dedent

from pyats.topology import loader
from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed

from genie.libs.clean.stages.stages import Connect

from unicon.plugins.tests.mock.mock_device_iosxe_cat9k import MockDeviceTcpWrapperIOSXECat9k


class TestRommonConnect(unittest.TestCase):

    def test_connect_cat9k_rommon_init_commands(self):
        steps = Steps()

        md = MockDeviceTcpWrapperIOSXECat9k(port=0, state='cat9k_rommon', hostname='R1')
        md.start()

        testbed = dedent("""
        devices:
            R1:
                os: iosxe
                platform: cat9k
                credentials:
                    default:
                        password: cisco
                connections:
                    cli:
                        command: 'telnet 127.0.0.1 {}'
                        settings:
                            POST_DISCONNECT_WAIT_SEC: 0
                            GRACEFUL_DISCONNECT_WAIT_SEC: 0.2
                            FIND_BOOT_IMAGE: False,
                            ROMMON_INIT_COMMANDS:
                                - set
                                - ping 1.1.1.1
                        arguments:
                            image_to_boot: tftp://1.1.1.1/cat9k_iosxe.SSA.bin
                            log_buffer: True
            """.format(md.ports[0]))
        tb = loader.load(testbed)
        device = tb.devices.R1

        cls = Connect()

        try:
            cls.connect(steps=steps, device=device)
        except Exception:
            raise
        finally:
            device.disconnect()
            md.stop()

        self.assertEqual(Passed, steps.details[0].result)
