import unittest

from unittest.mock import Mock, call, ANY

from genie.libs.clean.stages.iosxe.ie3k.stages import VerifyRunningImage
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
        self.device = create_test_device('PE1', os='iosxe', platform='ie3k')

    def test_verify_running_image(self):
        class MockExecute:

            def __init__(self, *args, **kwargs):
                self.data = {
                    'show version': '''
Cisco IOS XE Software, Version BLD_POLARIS_DEV_LATEST_20241204_191609
Cisco IOS Software [IOSXE], IE31xx Switch Software (IE31xx-UNIVERSALK9-M), Experimental Version 17.17.20241204:200702 [BLD_POLARIS_DEV_LATEST_20241204_191609:/nobackup/mcpre/s2c-build-ws 101]
Copyright (c) 1986-2024 by Cisco Systems, Inc.
Compiled Wed 04-Dec-24 12:09 by mcpre


Cisco IOS-XE software, Copyright (c) 2005-2024 by cisco Systems, Inc.
All rights reserved.  Certain components of Cisco IOS-XE software are
licensed under the GNU General Public License ("GPL") Version 2.0.  The
software code licensed under GPL Version 2.0 is free software that comes
with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
GPL code under the terms of GPL Version 2.0.  For more details, see the
documentation or "License Notice" file accompanying the IOS-XE software,
or the applicable URL provided on the flyer accompanying the IOS-XE
software.


ROM: IOS-XE ROMMON
BOOTLDR: Version 1.1.8 [RELEASE SOFTWARE]
IE-3105-18T2C-uut9 uptime is 5 days, 17 hours, 4 minutes
Uptime for this control processor is 5 days, 17 hours, 7 minutes
System returned to ROM by Reload Command
System image file is "flash:/ie31xx-universalk9.BLD_POLARIS_DEV_LATEST_20241204_191609.SSA.bin"
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


Technology Package License Information:

------------------------------------------------------------------------------
Technology-package                                     Technology-package
Current                        Type                       Next reboot
------------------------------------------------------------------------------
network-essentials      Smart License                    None
None                    Subscription Smart License       None


Smart Licensing Status: Smart Licensing Using Policy

cisco IE-3105-18T2C (ARM) processor (revision V01) with 659549K/6147K bytes of memory.
Processor board ID FDO2729J0GN
5 Virtual Ethernet interfaces
20 Gigabit Ethernet interfaces
4096K bytes of non-volatile configuration memory.
3492448K bytes of physical memory.
524288K bytes of crashinfo at crashinfo:.
1945600K bytes of Flash at flash:.

Base Ethernet MAC Address          : 48:1b:a4:24:26:80
Motherboard Assembly Number        : 73-105757-05
Motherboard Serial Number          : FDO27270TDL
Model Revision Number              : V01
Motherboard Revision Number        : 5
Model Number                       : IE-3105-18T2C
System Serial Number               : FDO2729J0GN
Top Assembly Part Number           : 68-103582-04
Top Assembly Revision Number       : F0
Top Assembly SN                    : FDO2729J0GN
Top Assembly HW series             : A
Top Assembly el-mech SN code       : FDO2729J0GN
Top Assembly hw-date code          : 20230718
System FPGA version                : 0.2.27
CIP Serial Number                  : 0xFE242680
SKU Brand Name                     : Cisco


Configuration register is 0x2102

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
            images=['flash:/general_image.bin']
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
Cisco IOS XE Software, Version BLD_POLARIS_DEV_LATEST_20241204_191609
Cisco IOS Software [IOSXE], IE31xx Switch Software (IE31xx-UNIVERSALK9-M), Experimental Version 17.17.20241204:200702 [BLD_POLARIS_DEV_LATEST_20241204_191609:/nobackup/mcpre/s2c-build-ws 101]
Copyright (c) 1986-2024 by Cisco Systems, Inc.
Compiled Wed 04-Dec-24 12:09 by mcpre


Cisco IOS-XE software, Copyright (c) 2005-2024 by cisco Systems, Inc.
All rights reserved.  Certain components of Cisco IOS-XE software are
licensed under the GNU General Public License ("GPL") Version 2.0.  The
software code licensed under GPL Version 2.0 is free software that comes
with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
GPL code under the terms of GPL Version 2.0.  For more details, see the
documentation or "License Notice" file accompanying the IOS-XE software,
or the applicable URL provided on the flyer accompanying the IOS-XE
software.


ROM: IOS-XE ROMMON
BOOTLDR: Version 1.1.8 [RELEASE SOFTWARE]
IE-3105-18T2C-uut9 uptime is 5 days, 17 hours, 4 minutes
Uptime for this control processor is 5 days, 17 hours, 7 minutes
System returned to ROM by Reload Command
System image file is "flash:/ie31xx-universalk9.BLD_POLARIS_DEV_LATEST_20241204_191609.SSA.bin"
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


Technology Package License Information:

------------------------------------------------------------------------------
Technology-package                                     Technology-package
Current                        Type                       Next reboot
------------------------------------------------------------------------------
network-essentials      Smart License                    None
None                    Subscription Smart License       None


Smart Licensing Status: Smart Licensing Using Policy

cisco IE-3105-18T2C (ARM) processor (revision V01) with 659549K/6147K bytes of memory.
Processor board ID FDO2729J0GN
5 Virtual Ethernet interfaces
20 Gigabit Ethernet interfaces
4096K bytes of non-volatile configuration memory.
3492448K bytes of physical memory.
524288K bytes of crashinfo at crashinfo:.
1945600K bytes of Flash at flash:.

Base Ethernet MAC Address          : 48:1b:a4:24:26:80
Motherboard Assembly Number        : 73-105757-05
Motherboard Serial Number          : FDO27270TDL
Model Revision Number              : V01
Motherboard Revision Number        : 5
Model Number                       : IE-3105-18T2C
System Serial Number               : FDO2729J0GN
Top Assembly Part Number           : 68-103582-04
Top Assembly Revision Number       : F0
Top Assembly SN                    : FDO2729J0GN
Top Assembly HW series             : A
Top Assembly el-mech SN code       : FDO2729J0GN
Top Assembly hw-date code          : 20230718
System FPGA version                : 0.2.27
CIP Serial Number                  : 0xFE242680
SKU Brand Name                     : Cisco


Configuration register is 0x2102

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
                images=['flash:/test.bin']
            )

    def test_verify_running_image_ignore_flash_false(self):
        class MockExecute:

            def __init__(self, *args, **kwargs):
                self.data = {
                    'show version': '''
Cisco IOS XE Software, Version BLD_POLARIS_DEV_LATEST_20241204_191609
Cisco IOS Software [IOSXE], IE31xx Switch Software (IE31xx-UNIVERSALK9-M), Experimental Version 17.17.20241204:200702 [BLD_POLARIS_DEV_LATEST_20241204_191609:/nobackup/mcpre/s2c-build-ws 101]
Copyright (c) 1986-2024 by Cisco Systems, Inc.
Compiled Wed 04-Dec-24 12:09 by mcpre


Cisco IOS-XE software, Copyright (c) 2005-2024 by cisco Systems, Inc.
All rights reserved.  Certain components of Cisco IOS-XE software are
licensed under the GNU General Public License ("GPL") Version 2.0.  The
software code licensed under GPL Version 2.0 is free software that comes
with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
GPL code under the terms of GPL Version 2.0.  For more details, see the
documentation or "License Notice" file accompanying the IOS-XE software,
or the applicable URL provided on the flyer accompanying the IOS-XE
software.


ROM: IOS-XE ROMMON
BOOTLDR: Version 1.1.8 [RELEASE SOFTWARE]
IE-3105-18T2C-uut9 uptime is 5 days, 17 hours, 4 minutes
Uptime for this control processor is 5 days, 17 hours, 7 minutes
System returned to ROM by Reload Command
System image file is "flash:/ie31xx-universalk9.BLD_POLARIS_DEV_LATEST_20241204_191609.SSA.bin"
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


Technology Package License Information:

------------------------------------------------------------------------------
Technology-package                                     Technology-package
Current                        Type                       Next reboot
------------------------------------------------------------------------------
network-essentials      Smart License                    None
None                    Subscription Smart License       None


Smart Licensing Status: Smart Licensing Using Policy

cisco IE-3105-18T2C (ARM) processor (revision V01) with 659549K/6147K bytes of memory.
Processor board ID FDO2729J0GN
5 Virtual Ethernet interfaces
20 Gigabit Ethernet interfaces
4096K bytes of non-volatile configuration memory.
3492448K bytes of physical memory.
524288K bytes of crashinfo at crashinfo:.
1945600K bytes of Flash at flash:.

Base Ethernet MAC Address          : 48:1b:a4:24:26:80
Motherboard Assembly Number        : 73-105757-05
Motherboard Serial Number          : FDO27270TDL
Model Revision Number              : V01
Motherboard Revision Number        : 5
Model Number                       : IE-3105-18T2C
System Serial Number               : FDO2729J0GN
Top Assembly Part Number           : 68-103582-04
Top Assembly Revision Number       : F0
Top Assembly SN                    : FDO2729J0GN
Top Assembly HW series             : A
Top Assembly el-mech SN code       : FDO2729J0GN
Top Assembly hw-date code          : 20230718
System FPGA version                : 0.2.27
CIP Serial Number                  : 0xFE242680
SKU Brand Name                     : Cisco


Configuration register is 0x2102

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
                images=['bootflash:/test.bin'],
                ignore_flash=False
            )

    def test_verify_running_image_ignore_flash_false_negative(self):
        class MockExecute:

            def __init__(self, *args, **kwargs):
                self.data = {
                    'show version': '''
Cisco IOS XE Software, Version BLD_POLARIS_DEV_LATEST_20241204_191609
Cisco IOS Software [IOSXE], IE31xx Switch Software (IE31xx-UNIVERSALK9-M), Experimental Version 17.17.20241204:200702 [BLD_POLARIS_DEV_LATEST_20241204_191609:/nobackup/mcpre/s2c-build-ws 101]
Copyright (c) 1986-2024 by Cisco Systems, Inc.
Compiled Wed 04-Dec-24 12:09 by mcpre


Cisco IOS-XE software, Copyright (c) 2005-2024 by cisco Systems, Inc.
All rights reserved.  Certain components of Cisco IOS-XE software are
licensed under the GNU General Public License ("GPL") Version 2.0.  The
software code licensed under GPL Version 2.0 is free software that comes
with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
GPL code under the terms of GPL Version 2.0.  For more details, see the
documentation or "License Notice" file accompanying the IOS-XE software,
or the applicable URL provided on the flyer accompanying the IOS-XE
software.


ROM: IOS-XE ROMMON
BOOTLDR: Version 1.1.8 [RELEASE SOFTWARE]
IE-3105-18T2C-uut9 uptime is 5 days, 17 hours, 4 minutes
Uptime for this control processor is 5 days, 17 hours, 7 minutes
System returned to ROM by Reload Command
System image file is "flash:/ie31xx-universalk9.BLD_POLARIS_DEV_LATEST_20241204_191609.SSA.bin"
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


Technology Package License Information:

------------------------------------------------------------------------------
Technology-package                                     Technology-package
Current                        Type                       Next reboot
------------------------------------------------------------------------------
network-essentials      Smart License                    None
None                    Subscription Smart License       None


Smart Licensing Status: Smart Licensing Using Policy

cisco IE-3105-18T2C (ARM) processor (revision V01) with 659549K/6147K bytes of memory.
Processor board ID FDO2729J0GN
5 Virtual Ethernet interfaces
20 Gigabit Ethernet interfaces
4096K bytes of non-volatile configuration memory.
3492448K bytes of physical memory.
524288K bytes of crashinfo at crashinfo:.
1945600K bytes of Flash at flash:.

Base Ethernet MAC Address          : 48:1b:a4:24:26:80
Motherboard Assembly Number        : 73-105757-05
Motherboard Serial Number          : FDO27270TDL
Model Revision Number              : V01
Motherboard Revision Number        : 5
Model Number                       : IE-3105-18T2C
System Serial Number               : FDO2729J0GN
Top Assembly Part Number           : 68-103582-04
Top Assembly Revision Number       : F0
Top Assembly SN                    : FDO2729J0GN
Top Assembly HW series             : A
Top Assembly el-mech SN code       : FDO2729J0GN
Top Assembly hw-date code          : 20230718
System FPGA version                : 0.2.27
CIP Serial Number                  : 0xFE242680
SKU Brand Name                     : Cisco


Configuration register is 0x2102

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
                images=['bootflash:/test.bin'],
                ignore_flash=False
            )
