import unittest

from genie.libs.clean.templates.iosxe.templates import DEFAULT_ARGS


class TestIosxeCleanTemplateDefaults(unittest.TestCase):

    def test_install_remove_inactive_timeout(self):
        self.assertEqual(DEFAULT_ARGS["install_remove_inactive__timeout"], 300)
