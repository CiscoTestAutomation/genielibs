import unittest

from unittest.mock import Mock, call, ANY

from genie.libs.clean.stages.stages import VerifyRunningImage
from genie.libs.clean.stages.tests.utils import create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal
from pyats.topology import Testbed
from pyats.datastructures import AttrDict


class TestVerifyRunningImage(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = VerifyRunningImage()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe')

    def test_verify_running_image(self):
        class MockExecute:

            def __init__(self, *args, **kwargs):
                self.data = {
                    'show version': '''
Cisco IOS Software, IOS-XE Software (X86_64_LINUX_IOSD-ADVENTERPRISEK9-M), Experimental Version 15.2(20110615:055721) [mcp_dev-BLD-BLD_MCP_DEV_LATEST_20110615_044519-ios 143]
Copyright (c) 1986-2011 by Cisco Systems, Inc.
Compiled Wed 15-Jun-11 08:54 by mcpre


Cisco IOS-XE software, Copyright (c) 2005-2011 by cisco Systems, Inc.
All rights reserved.  Certain components of Cisco IOS-XE software are
licensed under the GNU General Public License ("GPL") Version 2.0.  The
software code licensed under GPL Version 2.0 is free software that comes
with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
GPL code under the terms of GPL Version 2.0.  For more details, see the
documentation or "License Notice" file accompanying the IOS-XE software,
or the applicable URL provided on the flyer accompanying the IOS-XE
software.


ROM: IOS-XE ROMMON
ROM: Cisco IOS Software, IOS-XE Software (X86_64_LINUX_IOSD-ADVENTERPRISEK9-M), Experimental Version 15.2(20110615:055721) [mcp_dev-BLD-BLD_MCP_DEV_LATEST_20110615_044519-ios 143]

issu-asr-lns uptime is 1 hour, 16 minutes
Uptime for this control processor is 1 hour, 17 minutes
System returned to ROM by reload
System image file is "bootflash:/general_image.bin"
Last reload reason: Reload Command



This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.

cisco ASR1006 (RP2) processor with 4254354K/6147K bytes of memory.
3 ATM interfaces
32768K bytes of non-volatile configuration memory.
8388608K bytes of physical memory.
1826815K bytes of eUSB flash at bootflash:.
78085207K bytes of SATA hard disk at harddisk:.

Configuration register is 0x1
                    '''
                }

            def __call__(self, cmd, *args, **kwargs):
                output = self.data.get(cmd)
                return output

        mock_execute = MockExecute()

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=mock_execute)

        steps = Steps()

        # Call the method to be tested (clean step inside class)
        self.cls.verify_running_image(
            steps=steps, device=self.device,
            images=['bootflash:/general_image.bin']
        )

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)
        self.device.execute.assert_has_calls([
            call('show version'),
        ])

    def test_verify_running_image_negative(self):
        class MockExecute:

            def __init__(self, *args, **kwargs):
                self.data = {
                    'show version': '''
Cisco IOS Software, IOS-XE Software (X86_64_LINUX_IOSD-ADVENTERPRISEK9-M), Experimental Version 15.2(20110615:055721) [mcp_dev-BLD-BLD_MCP_DEV_LATEST_20110615_044519-ios 143]
Copyright (c) 1986-2011 by Cisco Systems, Inc.
Compiled Wed 15-Jun-11 08:54 by mcpre


Cisco IOS-XE software, Copyright (c) 2005-2011 by cisco Systems, Inc.
All rights reserved.  Certain components of Cisco IOS-XE software are
licensed under the GNU General Public License ("GPL") Version 2.0.  The
software code licensed under GPL Version 2.0 is free software that comes
with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
GPL code under the terms of GPL Version 2.0.  For more details, see the
documentation or "License Notice" file accompanying the IOS-XE software,
or the applicable URL provided on the flyer accompanying the IOS-XE
software.


ROM: IOS-XE ROMMON
ROM: Cisco IOS Software, IOS-XE Software (X86_64_LINUX_IOSD-ADVENTERPRISEK9-M), Experimental Version 15.2(20110615:055721) [mcp_dev-BLD-BLD_MCP_DEV_LATEST_20110615_044519-ios 143]

issu-asr-lns uptime is 1 hour, 16 minutes
Uptime for this control processor is 1 hour, 17 minutes
System returned to ROM by reload
System image file is "bootflash:/general_image.bin"
Last reload reason: Reload Command



This product contains cryptographic features and is subject to United
States and local country laws governing import, export, transfer and
use. Delivery of Cisco cryptographic products does not imply
third-party authority to import, export, distribute or use encryption.
Importers, exporters, distributors and users are responsible for
compliance with U.S. and local country laws. By using this product you
agree to comply with applicable laws and regulations. If you are unable
to comply with U.S. and local laws, return this product immediately.

A summary of U.S. laws governing Cisco cryptographic products may be found at:
http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

If you require further assistance please contact us by sending email to
export@cisco.com.

cisco ASR1006 (RP2) processor with 4254354K/6147K bytes of memory.
3 ATM interfaces
32768K bytes of non-volatile configuration memory.
8388608K bytes of physical memory.
1826815K bytes of eUSB flash at bootflash:.
78085207K bytes of SATA hard disk at harddisk:.

Configuration register is 0x1
                    '''
                }

            def __call__(self, cmd, *args, **kwargs):
                output = self.data.get(cmd)
                return output

        mock_execute = MockExecute()

        # And we want the execute method to be mocked with device console output.
        self.device.execute = Mock(side_effect=mock_execute)

        steps = Steps()

        with self.assertRaises(TerminateStepSignal):
            # Call the method to be tested (clean step inside class)
            self.cls.verify_running_image(
                steps=steps, device=self.device,
                images=['bootflash:/test.bin']
            )
