from __future__ import annotations

import logging
import unittest

from genie.libs.conf.device import Device

from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)


class TestThreading(unittest.TestCase):

    def test_api_not_supported_with_threading(self):
        custom = {"abstraction": {"order": ["os"]}}
        dev = Device('r1', os='iosxe', custom=custom)
        with ThreadPoolExecutor() as executor:
            tasks = []
            tasks.append(
                executor.submit(
                    dev.api.device_recovery_boot,
                    dev)
            )
        with self.assertRaisesRegex(Exception, 'This API is not supported with threading'):
            for task in as_completed(tasks):
                task.result()
