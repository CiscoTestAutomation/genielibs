#!/usr/bin/env python

import unittest
from unittest.mock import Mock

from genie.tests.conf import TestCase
from genie.conf import Genie
from genie.conf.base import Testbed, Device

from genie.libs.conf.device import UnsupportedDeviceOsWarning
from genie.libs.conf.testbed import Testbed as XbuTestbed


class test_device(TestCase):

    def test_init(self):

        with self.assertNoWarnings():

            Genie.testbed = Testbed()
            self.assertIsInstance(Genie.testbed, Testbed)
            self.assertIsInstance(Genie.testbed, XbuTestbed)
            self.assertIs(type(Genie.testbed), XbuTestbed)

if __name__ == '__main__':
    unittest.main()

