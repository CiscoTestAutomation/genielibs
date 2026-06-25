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


class test_platform_rev2_members_svl(unittest.TestCase):
    """Verify that the normalized `members` collection is populated for a
    multi-chassis IOS XE SVL pair. The rev2 Platform Ops carries the same
    `members` learning logic as rev1, so it has to expose the same contract.
    """

    def setUp(self):
        self.device = Device(name='svl')
        self.device.os = 'iosxe'
        self.device.mapping = {'cli': 'cli'}
        self.device_connection = Mock(device=self.device)
        self.device.connectionmgr.connections['cli'] = self.device_connection

    @staticmethod
    def _svl_show_version():
        return {
            'version': {
                'chassis': 'C9550-48L4CD',
                'chassis_sn': 'FDO29250F16',
                'rtr_type': 'C9550-48L4CD',
                'os': 'IOS-XE',
                'version': '26.02',
                'platform': 'Cisco L3 Switch',
                'image_id': 'CISCO9K_IOSXE',
                'system_image': 'bootflash:packages.conf',
                'switch_num': {
                    '1': {
                        'mac_address': 'f0:03:bc:82:f0:00',
                        'mb_assembly_num': '57FE',
                        'mb_sn': 'FDO29250F16',
                        'model_rev_num': 'V02',
                        'mb_rev_num': '2',
                        'model_num': 'C9550-48L4CD',
                        'system_sn': 'FDO29250F16',
                    },
                    '2': {
                        'mac_address': 'f4:33:92:a1:30:00',
                        'mb_assembly_num': '57FE',
                        'mb_sn': 'FDO29250E66',
                        'model_rev_num': 'V02',
                        'mb_rev_num': '2',
                        'model_num': 'C9550-48L4CD',
                        'system_sn': 'FDO29250E66',
                    },
                },
            }
        }

    @staticmethod
    def _svl_show_module():
        return {
            'switches': {
                1: {
                    'module': {
                        1: {
                            'ports': 54,
                            'card_type': 'Cisco 9550-48L4CD Switch',
                            'model': 'C9550-48L4CD',
                            'serial': 'FDO29250F16',
                            'mac_address': 'F003.BC82.F000 to F003.BC82.F035',
                            'hw': '0.3',
                            'fw': '26.0.0.B[REL]',
                            'sw': 'BLD_V262_1_EA1_THR',
                            'status': 'ok',
                            'redundancy_role': 'active',
                            'operating_redundancy_mode': 'sso',
                            'configured_redundancy_mode': 'sso',
                        },
                    },
                },
                2: {
                    'module': {
                        1: {
                            'ports': 54,
                            'card_type': 'Cisco 9550-48L4CD Switch',
                            'model': 'C9550-48L4CD',
                            'serial': 'FDO29250E66',
                            'mac_address': 'F433.92A1.3000 to F433.92A1.3035',
                            'hw': '0.3',
                            'fw': '26.0.0.B[REL]',
                            'sw': 'BLD_V262_1_EA1_THR',
                            'status': 'ok',
                            'redundancy_role': 'standby',
                            'operating_redundancy_mode': 'sso',
                            'configured_redundancy_mode': 'sso',
                        },
                    },
                },
            },
        }

    def _build_platform(self, show_version=None, show_module=None):
        f = Platform(device=self.device)
        f.maker.outputs[ShowVersion] = {
            '': show_version if show_version is not None else self._svl_show_version()
        }
        f.maker.outputs[ShowModule] = {
            '': show_module if show_module is not None else self._svl_show_module()
        }
        # Stub the remaining parsers rev2 Platform.learn() touches; they
        # are irrelevant to this test (we only assert on `members`) but
        # they need *some* parseable output so the maker doesn't try to
        # execute against the mock connection.
        f.maker.outputs[Dir] = {'': {'dir': {'dir': '/'}}}
        f.maker.outputs[ShowRedundancy] = {'': {}}
        f.maker.outputs[ShowInventoryRev2] = {'': {}}
        f.maker.outputs[ShowPlatformRev1] = {'': {}}
        return f

    def test_members_populated_for_svl(self):
        self.maxDiff = None
        f = self._build_platform()
        f.learn()

        self.assertTrue(hasattr(f, 'members'),
                        "rev2 Platform Ops did not expose `members` collection")
        self.assertEqual(set(f.members.keys()), {'1', '2'})
        self.assertEqual(f.members['1']['serial'], 'FDO29250F16')
        self.assertEqual(f.members['2']['serial'], 'FDO29250E66')
        self.assertEqual(f.members['1']['pid'], 'C9550-48L4CD')
        self.assertEqual(f.members['2']['pid'], 'C9550-48L4CD')
        self.assertEqual(f.members['1']['role'], 'active')
        self.assertEqual(f.members['2']['role'], 'standby')

    def test_members_absent_for_non_stack(self):
        """Single-chassis IOS XE devices have no switch_num; members must
        not appear (or be empty) so consumers can guard with hasattr / empty
        checks without crashing."""
        sv = self._svl_show_version()
        sv['version'].pop('switch_num')
        f = self._build_platform(show_version=sv, show_module={})
        f.learn()

        self.assertFalse(getattr(f, 'members', None),
                         "members should be empty/absent without switch_num")


if __name__ == '__main__':
    unittest.main()
