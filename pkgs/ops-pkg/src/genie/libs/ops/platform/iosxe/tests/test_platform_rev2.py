"""Unit tests for ``genie.libs.ops.platform.iosxe.rev2.platform.Platform``.

"""
import unittest
from unittest.mock import Mock

from pyats.topology import Device

from genie.libs.ops.platform.iosxe.rev2.platform import Platform
from genie.libs.ops.platform.iosxe.tests.c9610r_platform_output import \
    PlatformOutput

from genie.libs.parser.iosxe.show_platform import ShowVersion, \
                                                  Dir, \
                                                  ShowRedundancy, \
                                                  ShowModule

from genie.libs.parser.iosxe.rv1.show_platform import \
    ShowPlatform as ShowPlatformRev1
from genie.libs.parser.iosxe.rv2.show_platform import \
    ShowInventory as ShowInventoryRev2


class test_platform_rev2_c9610r(unittest.TestCase):

    def setUp(self):
        self.device = Device(name='aDevice')
        self.device.os = 'iosxe'
        self.device.mapping = {}
        self.device.mapping['cli'] = 'cli'
        self.device_connection = Mock(device=self.device)
        self.device.connectionmgr.connections['cli'] = self.device_connection

    def _build_platform(self):
        f = Platform(device=self.device)
        f.maker.outputs[ShowVersion] = \
            {'': PlatformOutput.showVersionC9610R}
        f.maker.outputs[Dir] = \
            {'': PlatformOutput.showDirC9610R}
        f.maker.outputs[ShowRedundancy] = \
            {'': PlatformOutput.showRedundancyC9610R}
        f.maker.outputs[ShowInventoryRev2] = \
            {'': PlatformOutput.showInventoryC9610R}
        f.maker.outputs[ShowPlatformRev1] = \
            {'': PlatformOutput.showPlatformC9610R}
        f.maker.outputs[ShowModule] = \
            {'': PlatformOutput.showModuleC9610R}
        return f

    def test_learn_does_not_raise_keyerror_on_sup_slot(self):
        """Regression: KeyError: '6' on C9610R with a SUP in slot 6."""
        f = self._build_platform()
        try:
            f.learn()
        except KeyError as exc:
            self.fail(
                "Platform.learn() raised KeyError({!r}) on C9610R "
                "(SUP slot expected to land on slot['rp]).".format(exc)
            )

    def test_chassis_attributes_learned(self):
        f = self._build_platform()
        f.learn()
        self.assertEqual(f.chassis, 'C9610R')
        self.assertEqual(f.chassis_sn, 'FOX2746PQGL')
        self.assertEqual(f.os, 'iosxe')
        self.assertEqual(f.version, '26.01.01prd12')

    def test_lc_hw_revision_routed_to_lc_subtree(self):
        f = self._build_platform()
        f.learn()
        for slot, expected_hw in PlatformOutput.expected_hw_revision_C9610R['lc'].items():
            self.assertIn(slot, f.slot.get('lc', {}),
                          msg="slot['lc'][{!r}] missing".format(slot))
            self.assertEqual(
                f.slot['lc'][slot].get('hw_revision'),
                expected_hw,
                msg="slot['lc'][{!r}].hw_revision".format(slot),
            )

    def test_sup_hw_revision_routed_to_rp_subtree(self):
        f = self._build_platform()
        f.learn()
        for slot, expected_hw in PlatformOutput.expected_hw_revision_C9610R['rp'].items():
            self.assertIn(slot, f.slot.get('rp', {}),
                          msg="slot['rp'][{!r}] missing".format(slot))
            self.assertEqual(
                f.slot['rp'][slot].get('hw_revision'),
                expected_hw,
                msg="slot['rp'][{!r}].hw_revision".format(slot),
            )

    def test_sup_hw_revision_not_smuggled_into_lc(self):
        f = self._build_platform()
        f.learn()
        for sup_slot in PlatformOutput.expected_hw_revision_C9610R['rp']:
            self.assertNotIn(
                sup_slot,
                f.slot.get('lc', {}),
                msg="SUP slot {!r} should not appear in slot['lc']".format(sup_slot),
            )

    def test_mod_attribute_cleaned_up(self):
        f = self._build_platform()
        f.learn()
        self.assertFalse(
            hasattr(f, 'mod'),
            msg="`self.mod` should be deleted after Platform.learn()",
        )


if __name__ == '__main__':
    unittest.main()
