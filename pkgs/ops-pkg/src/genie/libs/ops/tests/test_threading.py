from __future__ import annotations

import logging
import unittest
from typing import Any

from genie.conf.base.utils import QDict
from genie.libs.conf.device import Device as GenieDevice

from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)


class Device(GenieDevice):  # type: ignore[misc] # Class cannot subclass "GenieDevice" (has type "Any")

    def __init__(
        self,
        device: str,
        os: str | None = None,
        exec_timeout: int | None = None,
        **kwargs: Any,
    ) -> None:
        if os is None:
            raise ValueError(
                f"{device} is missing 'os' information, can't instantiate Device"
            )
        else:
            device_os = os

        # instantiate Genie Device object
        custom = {"abstraction": {"order": ["os"]}}
        super().__init__(device, os=device_os, custom=custom, **kwargs)

    def connect(self, *args: Any, **kwargs: Any) -> None:
        pass

    def disconnect(self, *args: Any, **kwargs: Any) -> None:
        pass

    # Overload the execute() method to return device command output
    # back to genie. This is needed for genie learn which interactively
    # collects device command output
    def execute(self, command: str, **kwargs: Any) -> str:
        logger.info(f'executing {command}')
        data = {
            'show version': """
Cisco IOS XE Software, Version BLD_POLARIS_DEV_LATEST_20230827_101613_V17_13_0_38
Cisco IOS Software [IOSXE], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Experimental Version 17.14.20230827:110032 [BLD_POLARIS_DEV_LATEST_20230827_101613:/nobackup/mcpre/s2c-build-ws 101]
Copyright (c) 1986-2023 by Cisco Systems, Inc.
Compiled Sun 27-Aug-23 04:01 by mcpre


Cisco IOS-XE software, Copyright (c) 2005-2023 by cisco Systems, Inc.
All rights reserved.  Certain components of Cisco IOS-XE software are
licensed under the GNU General Public License ("GPL") Version 2.0.  The
software code licensed under GPL Version 2.0 is free software that comes
with ABSOLUTELY NO WARRANTY.  You can redistribute and/or modify such
GPL code under the terms of GPL Version 2.0.  For more details, see the
documentation or "License Notice" file accompanying the IOS-XE software,
or the applicable URL provided on the flyer accompanying the IOS-XE
software.


ROM: IOS-XE ROMMON
CSR104 uptime is 1 day, 23 hours, 32 minutes
Uptime for this control processor is 1 day, 23 hours, 34 minutes
System returned to ROM by reload
System image file is "bootflash:c8kv.bin"
Last reload reason: reload



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

License Level: network-advantage
License Type: Perpetual
Next reload license Level: network-advantage

Addon License Level: dna-advantage
Addon License Type: Subscription
Next reload addon license Level: dna-advantage

The current throughput level is 20000 kbps 


Smart Licensing Status: Smart Licensing Using Policy

cisco C8000V (VXE) processor (revision VXE) with 2251787K/3075K bytes of memory.
Processor board ID 9BKQ6ZRKD0C
Router operating mode: Autonomous
4 Gigabit Ethernet interfaces
32768K bytes of non-volatile configuration memory.
8083304K bytes of physical memory.
11530240K bytes of virtual hard disk at bootflash:.

Configuration register is 0x2102
"""
        }
        return data.get(command, "% Unknown command")


def _task_learn(
    device: str,
    models: list[str],
    os: str | None = None,
    exec_timeout: int | None = None,
) -> tuple[str, QDict]:
    results = {}

    dev = Device(device, os=os, exec_timeout=exec_timeout)

    for model in models:
        try:
            result = dev.learn(model)
        except Exception as e:
            logger.exception(e)
            results[model] = {
                'data': None,
                'status': False,
                'status_message': f"Exception occurred during learning: {e}",
            }
            continue

        output = QDict(result.to_dict())

        results[model] = {
            'data': output,
            'status': True,
            'status_message': "learnt successfully",
        }

    return device, results


def _learn(
    devices: list[str],
    models: str | list[str],
    os: str | None = None,
    exec_timeout: int | None = None,
    num_threads: int | None = None,
):

    if isinstance(models, str):
        models = [models]

    results = {}
    with ThreadPoolExecutor(
        max_workers=num_threads,
    ) as executor:
        tasks = []
        for device in devices:
            tasks.append(
                executor.submit(
                    _task_learn,
                    device,
                    models,
                    os,
                    exec_timeout,
                )
            )

        for task in as_completed(tasks):
            name, result = task.result()
            results[name] = result

    return results


class TestThreading(unittest.TestCase):

    def test_threaded_learn(self):
        results = _learn(
            devices=['r1', 'r2'],
            models=['platform'],
            os='iosxe',
            num_threads=2
        )
        expected_results = {
                'platform': {
                    'data': {
                        'context_manager': {},
                        'attributes': None,
                        'commands': None,
                        'connections': None,
                        'raw_data': False,
                        'chassis': 'C8000V',
                        'chassis_sn': '9BKQ6ZRKD0C',
                        'rtr_type': 'C8000V',
                        'os': 'IOS-XE',
                        'version': '17.14.20230827:110032',
                        'image': 'bootflash:c8kv.bin',
                        'label': 'BLD_POLARIS_DEV_LATEST_20230827_101613',
                        'config_register': '0x2102',
                        'main_mem': '2251787'
                    },
                    'status': True,
                    'status_message': 'learnt successfully'
                }
            }

        self.assertEqual(results, {'r1': expected_results, 'r2': expected_results})
