#!/usr/bin/env python

import unittest
from unittest.mock import Mock
import inspect

from genie.tests.conf import TestCase
from genie.libs.conf.utils import *
from genie.libs.conf.topology_mapper.cli import *


class test_round_nearest(TestCase):

    def test_init(self):

        for v, i, r, rn in (

                (2.0, 2, 2, 2),
                (2.1, 2, 2, 2),
                (2.4, 2, 2, 2),
                (2.5, 2, 2, 3),  # diff
                (2.6, 2, 3, 3),
                (2.9, 2, 3, 3),

                (1.0, 1, 1, 1),
                (1.1, 1, 1, 1),
                (1.4, 1, 1, 1),
                (1.5, 1, 2, 2),
                (1.6, 1, 2, 2),
                (1.9, 1, 2, 2),

                (0.0, 0, 0, 0),
                (0.1, 0, 0, 0),
                (0.4, 0, 0, 0),
                (0.5, 0, 0, 1),  # diff
                (0.6, 0, 1, 1),
                (0.9, 0, 1, 1),

                (-1.0, -1, -1, -1),
                (-1.1, -1, -1, -1),
                (-1.4, -1, -1, -1),
                (-1.5, -1, -2, -2),
                (-1.6, -1, -2, -2),
                (-1.9, -1, -2, -2),

                (-2.0, -2, -2, -2),
                (-2.1, -2, -2, -2),
                (-2.4, -2, -2, -2),
                (-2.5, -2, -2, -3),  # diff
                (-2.6, -2, -3, -3),
                (-2.9, -2, -3, -3),

        ):
            with self.subTest(v=v):
                self.assertEqual(int(v), i)
                self.assertEqual(round(v), r)
                self.assertEqual(round_nearest(v), rn)


class test_nth(TestCase):

    def test_nth(self):

        r = range(10)
        self.assertEqual(nth(r, 0), 0)
        self.assertEqual(nth(r, 5), 5)
        self.assertEqual(nth(r, 9), 9)
        self.assertEqual(nth(r, 10), None)

        r = range(10)
        ri = iter(r)
        self.assertEqual(nth(ri, 0), 0)
        ri = iter(r)
        self.assertEqual(nth(ri, 5), 5)
        ri = iter(r)
        self.assertEqual(nth(ri, 9), 9)
        ri = iter(r)
        self.assertEqual(nth(ri, 10), None)


class test_config_cli_to_tree(TestCase):

    def test_cli_to_tree_1(self):

        cli = inspect.cleandoc('''
            vrf irb1
             address-family ipv4 unicast
              import route-target
               100:100
              !
              export route-target
               100:100
              !
             !
            !
        ''')

        cli_tree = config_cli_to_tree(cli)
        self.assertEqual(cli_tree, (
            ('vrf irb1', (
                (' address-family ipv4 unicast', (
                    ('  import route-target', (
                        ('   100:100', None),
                    )),
                    ('  export route-target', (
                        ('   100:100', None),
                    )),
                )),
            )),
        ))

        new_cli = cli_tree_to_config(cli_tree)
        self.assertEqual(new_cli, inspect.cleandoc('''
            vrf irb1
             address-family ipv4 unicast
              import route-target
               100:100
               exit
              export route-target
               100:100
               exit
              exit
             exit
        '''))

    def test_cli_to_tree_strip(self):

        cli = inspect.cleandoc('''
            vrf irb1
             address-family ipv4 unicast
              import route-target
               100:100
              !
              export route-target
               100:100
              !
             !
            !
        ''')

        cli_tree = config_cli_to_tree(cli, strip=True)
        self.assertEqual(cli_tree, (
            ('vrf irb1', (
                ('address-family ipv4 unicast', (
                    ('import route-target', (
                        ('100:100', None),
                    )),
                    ('export route-target', (
                        ('100:100', None),
                    )),
                )),
            )),
        ))

        new_cli = cli_tree_to_config(cli_tree)
        self.assertEqual(new_cli, inspect.cleandoc('''
            vrf irb1
             address-family ipv4 unicast
              import route-target
               100:100
               exit
              export route-target
               100:100
               exit
              exit
             exit
        '''))

    def test_cli_to_tree_special(self):

        cli = inspect.cleandoc('''
            route-policy SID
              if destination in (192.0.0.4/32) then
                set label-index 100
              else
                pass
              endif
            end-policy
        ''')

        cli_tree = config_cli_to_tree(cli, strip=True)
        self.assertEqual(cli_tree, (
            ('route-policy SID', (
                ('if destination in (192.0.0.4/32) then', (
                    ('set label-index 100', None),
                )),
                ('else', (
                    ('pass', None),
                )),
                ('endif', None),
            )),
            ('end-policy', None),
        ))

        new_cli = cli_tree_to_config(cli_tree)
        self.assertEqual(new_cli, inspect.cleandoc('''
            route-policy SID
             if destination in (192.0.0.4/32) then
              set label-index 100
             else
              pass
             endif
            end-policy
        '''))

if __name__ == '__main__':
    unittest.main()

