import os
from pyats.topology import loader
from unittest import TestCase
from genie.libs.sdk.apis.iosxe.ie3k.platform.execute import execute_reload_noverify
from unittest.mock import Mock

class TestExecuteReloadNoVerify(TestCase):

    def test_execute_reload_noverify(self):
        self.device = Mock()
        self.device.reload = Mock()
        results_map = {"""
System configuration has been modified. Save? [yes/no]: n
                       Reload command is being issued on Active unit, this will reload the whole stack
Proceed with reload? [confirm]

Chassis 1 reloading, reason - Reload command
Jun 23 06:40:00.113: %PMAN-5-EXITACTION: C0/0: pvp: Process manager is exiting: reload cc action requested
Jun 23 06:40:00.175: %PMAN-5-EXITACTION: F0/0: pvp: Process manager is exiting: reload fp action requested
Jun 23 06:40:02.272: %PMAN-5-EXITACTION: R0/0: pvp: Process manager is exiting: process exit with reload stack code


watchdog: watchdog0: watchdog did not stop!
ext2 filesystem being remounted at /run/initramfs/bootflash supports timestamps until 2038 (0x7fffffff)
ext2 filesystem being remounted at /mnt/sd3 supports timestamps until 2038 (0x7fffffff)
ext2 filesystem being remounted at /run/initramfs/bootflash supports timestamps until 2038 (0x7fffffff)
systemd-shutdown[1]: Failed to disable hardware watchdog, ignoring: Device or resource busy
watchdog: watchdog0: watchdog did not stop!
reboot: Restarting system

Initializing Hardware...
Aikido Bus encryption enabled
TAM Processing and reading the IDPROM Data

System Bootstrap, Version v17_14_1r [FC1], RELEASE SOFTWARE (P) 
Compiled Tue 01/23/2024 14:48:05 by rel

Current ROMMON image : Primary
IE-9320-26S2C platform with 4194304 Kbytes of main memory

IO-FPGA version : 176

PCIE SERDES Init for FPGA 

PCIE SERDES Init for DopplerG 2.0 
 Local  Core0 PCIe Link(0x113) - UP
 Local  Core1 PCIe Link(0x113) - UP
Validate Chip guard ... Success.
boot: attempting to boot from [sdflash:/ie9k_iosxe.BLD_POLARIS_DEV_LATEST_20250613_001658.SSA.bin]
boot: reading file /ie9k_iosxe.BLD_POLARIS_DEV_LATEST_20250613_001658.SSA.bin
################################################################################################################################################################################################
Verifying image sdflash:/ie9k_iosxe.BLD_POLARIS_DEV_LATEST_20250613_001658.SSA.bin
WARNING: DEV-Keys are installed in box
SecureBoot: DEV KEY signed image verified successfully!


Both links down, not waiting for other switches
Switch number is 1

              Restricted Rights Legend

Use, duplication, or disclosure by the Government is
subject to restrictions as set forth in subparagraph
(c) of the Commercial Computer Software - Restricted
Rights clause at FAR sec. 52.227-19 and subparagraph
(c) (1) (ii) of the Rights in Technical Data and Computer
Software clause at DFARS sec. 252.227-7013.

           Cisco Systems, Inc.
           170 West Tasman Drive
           San Jose, California 95134-1706



Cisco IOS Software [IOSXE], Catalyst L3 Switch Software (IE9K_IOSXE), Experimental Version 17.19.20250613:012620 [BLD_POLARIS_DEV_LATEST_20250613_001658:/nobackup/mcpre/s2c-build-ws 101]
Copyright (c) 1986-2025 by Cisco Systems, Inc.
Compiled Fri 13-Jun-25 01:27 by mcpre


This software version supports only Smart Licensing as the software licensing mechanism.


Please read the following carefully before proceeding. By downloading,
installing, and/or using any Cisco software product, application, feature,
license, or license key (collectively, the "Software"), you accept and
agree to the following terms. If you do not agree, do not proceed and do not
use this Software.

This Software and its use are governed by Cisco's General Terms and any 
relevant supplemental terms found at
https://www.cisco.com/site/us/en/about/legal/contract-experience/index.html.
If you have a negotiated agreement with Cisco that includes this Software, the
terms of that agreement apply as well. In the event of a conflict, the order 
of precedence stated in your negotiated agreement controls.

Cisco Software is licensed on a term and/or subscription-basis. The license to
the Software is valid only for the duration of the specified term, or in the
case of a subscription-based license, only so long as all required subscription
payments are current and fully paid-up. While Cisco may provide you
licensing-related alerts, it is your sole responsibility to monitor your usage.
Using Cisco Software without a valid license is not permitted and may result in
fees charged to your account. Cisco reserves the right to terminate access to,
or restrict the functionality of, any Cisco Software, or any features thereof,
that are being used without a valid license.



FIPS: Flash Key Check : Key Not Found, FIPS Mode Not Enabled
cisco IE-9320-26S2C (ARM64) processor with 545760K/3071K bytes of memory.
Processor board ID FDO2714JU4S
2048K bytes of non-volatile configuration memory.
4011284K bytes of physical memory.
523264K bytes of Crash Files at crashinfo:.
2650112K bytes of Flash at flash:.
3883008K bytes of SD Flash at sdflash:.

Base Ethernet MAC Address          : 90:eb:50:31:41:80
Motherboard Assembly Number        : 73-102472-05
Motherboard Serial Number          : FDO271422BX
Model Revision Number              : H0
Motherboard Revision Number        : B0
Model Number                       : IE-9320-26S2C
System Serial Number               : FDO2714JU4S




Press RETURN to get started!

        """,
        }
        
        def results_side_effect(arg, **kwargs):
            return results_map.get(arg)
        
        self.device.execute.side_effect = results_side_effect
        result = execute_reload_noverify(self.device, 10, 600)
        
        # self.assertTrue(self.device.reload.called, "Expected device.reload to be called")

        # Retrieve keyword arguments from the call
        self.assertIn(
            'reload /noverify',
            self.device.reload.call_args.kwargs.get('reload_command', '')
        )
        # Validate expected output (adjust if the function returns something else)
        expected_output = None
        self.assertEqual(result, expected_output)
