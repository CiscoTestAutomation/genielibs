import logging
import unittest

from unittest.mock import Mock

from genie.libs.clean.stages.iosxe.c9800.stages import VerifyInstallationMode
from genie.libs.clean.stages.tests.utils import create_test_device

from pyats.aetest.steps import Steps
from pyats.results import Passed, Failed
from pyats.aetest.signals import TerminateStepSignal

# Disable logging. It may be useful to comment this out when developing tests.
logging.disable(logging.CRITICAL)


class TestInstallationMode(unittest.TestCase):

    def setUp(self):
        # Instantiate class object
        self.cls = VerifyInstallationMode()

        # Instantiate device object. This also sets up commonly needed
        # attributes and Mock objects associated with the device.
        self.device = create_test_device('PE1', os='iosxe', platform='c9800')

    def test_pass(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        data= {'show version': '''
        Cisco IOS XE Software, Version BLD_V179_THROTTLE_LATEST_20220506_192009
        Cisco IOS Software [Cupertino], C9800-CL Software (C9800-CL-K9_IOSXE), Experimental Version 17.9.20220506:200143 [BLD_V179_THROTTLE_LATEST_20220506_192009:/nobackup/mcpre/s2c-build-ws 101]
        Copyright (c) 1986-2022 by Cisco Systems, Inc.
        Compiled Fri 06-May-22 13:01 by mcpre
        
        
        Cisco IOS-XE software, Copyright (c) 2005-2022 by cisco Systems, Inc.
        All rights reserved.  Certain components of Cisco IOS-XE software are
        licensed under the GNU General Public License ("GPL") Version 2.0.  The
        software code licensed under GPL Version 2.0 is free software that comes
        with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
        GPL code under the terms of GPL Version 2.0.  For more details, see the
        documentation or "License Notice" file accompanying the IOS-XE software,
        or the applicable URL provided on the flyer accompanying the IOS-XE
        software.
        
        
        ROM: IOS-XE ROMMON
        
        vidya-ewlc-5 uptime is 3 weeks, 6 days, 13 hours, 26 minutes
        Uptime for this control processor is 3 weeks, 6 days, 13 hours, 30 minutes
        System returned to ROM by reload
        System restarted at 13:54:07 UTC Thu May 12 2022
        System image file is "bootflash:packages.conf"
        Last reload reason: Install 
        
        
        
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
        
        AIR License Level: AIR DNA Advantage
        Next reload AIR license Level: AIR DNA Advantage
        
        Smart Licensing Status: Smart Licensing Using Policy
        
        cisco C9800-CL (VXE) processor (revision VXE) with 12266721K/3075K bytes of memory.
        Processor board ID 9SV9FR9MWP9
        Router operating mode: Autonomous
        5 Virtual Ethernet interfaces
        3 Gigabit Ethernet interfaces
        32768K bytes of non-volatile configuration memory.
        16332132K bytes of physical memory.
        6201343K bytes of virtual hard disk at bootflash:.
        Installation mode is INSTALL
        
        
        Configuration register is 0x102
        '''}

        # And we want the verify_installation_mode api to be mocked.
        # This simulates the pass case.
        self.device.execute = Mock(side_effect=lambda x: data[x])

        # Call the method to be tested (clean step inside class)
        self.cls.verify_installation_mode(device=self.device, steps=steps, installation_mode="INSTALL")

        # Check that the result is expected
        self.assertEqual(Passed, steps.details[0].result)

    def test_fail_installation_mode(self):
        # Make sure we have a unique Steps() object for result verification
        steps = Steps()
        data = {'show version': '''
                Cisco IOS XE Software, Version BLD_V179_THROTTLE_LATEST_20220506_192009
                Cisco IOS Software [Cupertino], C9800-CL Software (C9800-CL-K9_IOSXE), Experimental Version 17.9.20220506:200143 [BLD_V179_THROTTLE_LATEST_20220506_192009:/nobackup/mcpre/s2c-build-ws 101]
                Copyright (c) 1986-2022 by Cisco Systems, Inc.
                Compiled Fri 06-May-22 13:01 by mcpre


                Cisco IOS-XE software, Copyright (c) 2005-2022 by cisco Systems, Inc.
                All rights reserved.  Certain components of Cisco IOS-XE software are
                licensed under the GNU General Public License ("GPL") Version 2.0.  The
                software code licensed under GPL Version 2.0 is free software that comes
                with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
                GPL code under the terms of GPL Version 2.0.  For more details, see the
                documentation or "License Notice" file accompanying the IOS-XE software,
                or the applicable URL provided on the flyer accompanying the IOS-XE
                software.


                ROM: IOS-XE ROMMON

                vidya-ewlc-5 uptime is 3 weeks, 6 days, 13 hours, 26 minutes
                Uptime for this control processor is 3 weeks, 6 days, 13 hours, 30 minutes
                System returned to ROM by reload
                System restarted at 13:54:07 UTC Thu May 12 2022
                System image file is "bootflash:packages.conf"
                Last reload reason: Install 



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

                AIR License Level: AIR DNA Advantage
                Next reload AIR license Level: AIR DNA Advantage

                Smart Licensing Status: Smart Licensing Using Policy

                cisco C9800-CL (VXE) processor (revision VXE) with 12266721K/3075K bytes of memory.
                Processor board ID 9SV9FR9MWP9
                Router operating mode: Autonomous
                5 Virtual Ethernet interfaces
                3 Gigabit Ethernet interfaces
                32768K bytes of non-volatile configuration memory.
                16332132K bytes of physical memory.
                6201343K bytes of virtual hard disk at bootflash:.
                Installation mode is INSTALL


                Configuration register is 0x102
                '''}

        # And we want the verify_installation_mode api to be mocked to raise an
        # exception when called. This simulates the fail case.
        self.device.execute = Mock(side_effect=lambda x: data[x])

        # We expect this step to fail so make sure it raises the signal
        with self.assertRaises(TerminateStepSignal):
            self.cls.verify_installation_mode(device=self.device, steps=steps, installation_mode="BUNDLE")

        # Check the overall result is as expected
        self.assertEqual(Failed, steps.details[0].result)
