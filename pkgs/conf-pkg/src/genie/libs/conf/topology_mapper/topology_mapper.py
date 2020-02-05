
__all__ = (
    'TopologyMapper',
)

from copy import copy
import collections
import contextlib
import functools
import itertools
import logging
import os
import re
import time
import types
import gc

import pyats.topology
from pyats.easypy import runtime

from genie.utils.cisco_collections import OrderedSet

from genie.decorator import managedattribute
from genie.conf import Genie
import genie.conf.base

from .device import Device
from .interface import Interface
from .link import Link
from .exceptions import AllSubsetsRejectedError
from .exceptions import FailedToResolveException

# module level logger
logger = logging.getLogger(__name__)


class JumpException(Exception):

    def __init__(self, label):
        self.label = label
        super().__init__(label)


@contextlib.contextmanager
def JumpContext(label):
    try:
        yield
    except JumpException as exc:
        # logger.debug('JumpContext(%s) caught J->%s', label, exc.label)
        if exc.label != label:
            raise


class AccessCountingDict(collections.UserDict):

    read_counts_enabled = True
    read_counts_map = None

    def __init__(self, *args):
        self.read_counts = collections.Counter()
        self.read_counts_map = {}
        super().__init__(*args)

    def __getitem__(self, item):
        value = super().__getitem__(item)
        if self.read_counts_enabled:
            mapped_item = self.read_counts_map.get(item, item)
            self.read_counts[mapped_item] += 1
        return value


class _traceAccessCountingDict(AccessCountingDict):

    def __getitem__(self, item):
        value = super().__getitem__(item)
        if self.read_counts_enabled:
            mapped_item = self.read_counts_map.get(item, item)
            logger.debug('Read %s [%s] <= %d', item, mapped_item, self.read_counts[mapped_item])
        return value


def copy_map_depth(map, depth):
    assert depth >= 1
    map = copy(map)
    if depth > 1:
        for key in list(map.keys()):
            map[key] = copy_map_depth(map[key], depth-1)
    return map


class TopologySubset(object):

    def __init__(self,
            topology,
            name,
            subset_required_objects):

        self.topology = topology
        self.name = name
        self.subset_required_objects = set(subset_required_objects)

        self.device_names = self.topology.device_names & self.subset_required_objects
        self.link_names = self.topology.link_names & self.subset_required_objects
        self.interface_names = self.topology.interface_names & self.subset_required_objects


def test_list_intersect(list1, list2):
    return not set(list1).isdisjoint(list2)


class TopologyCache(object):

    class ComputeCacheDict(collections.defaultdict):

        def __missing__(self, key):
            default_factory = self.default_factory
            if default_factory is None:
                return super().__missing__(key)
            return default_factory(key)

    def __init__(self, topology):
        self.topology = topology
        self.link = self.ComputeCacheDict(self.compute_link)
        self.link_device_names = \
            self.ComputeCacheDict(self.compute_link_device_names)
        self.link_interface_names = \
            self.ComputeCacheDict(self.compute_link_interface_names)

    def compute_link(self, link_name):
        return self.topology.constraints.get_link_by_name(link_name)

    def compute_link_device_names(self, link_name):
        return tuple(self.link[link_name].device_names)

    def compute_link_interface_names(self, link_name):
        return tuple(self.link[link_name].interface_names)


class Resolver(object):

    class ConstraintGroupsState(object):

        groups = None  # {}
        reducing_choices = None  # []
        cur_weight = None

        def __init__(self):
            self.groups = {}
            self.reducing_choices = []

        def copy(self):
            c = self.__class__()
            # Copy 1 level deep
            c.__dict__.update({k: copy(v) for k, v in self.__dict__.items()})
            return c

        __copy__ = copy

    def __init__(self,
            topology,
            subset,
            dynobj_mappings,
            dynobj_mappings_link_parts,
            _trace,
            _find_all,
            ):

        self.topology = topology
        self.cache = TopologyCache(topology)
        self.subset = subset
        self.dynobj_mappings = copy_map_depth(dynobj_mappings, 3)
        self.dynobj_mappings_link_parts = copy_map_depth(dynobj_mappings_link_parts, 4)
        self._trace = _trace
        self._find_all = _find_all

        self.objects = (_traceAccessCountingDict if self._trace.read else AccessCountingDict)({object_name: None for object_name in self.topology.object_names})
        self.object_tests = {}

        self.cg_info = types.SimpleNamespace()
        self.cg_info.groups = {}
        self.cg_state = Resolver.ConstraintGroupsState()

        self.device_decision_order = list(self.subset.device_names)
        self.link_decision_order_by_device = {device_name: [] for device_name in self.device_decision_order}
        for link_name in self.subset.link_names:
            link_device_names = self.cache.link_device_names[link_name]
            for device_name in reversed(self.device_decision_order):
                if device_name in link_device_names:
                    break
            else:
                raise Exception('No device in link %r match!' % (link_name,))
            # XXXJST TODO OPTIMIZE link_decision_order_by_device to have shorter locality of "previous" device
            self.link_decision_order_by_device[device_name].append(link_name)
            for interface_name in self.cache.link_interface_names[link_name]:
                self.objects.read_counts_map[interface_name] = link_name

        self.xos_link_devices_by_link = {}
        self.xos_link_parts_by_link = {}

    def __repr__(self):
        return '<%s(%s,%s)>' % (self.__class__.__name__, self.topology.uid, self.subset.name)

    @contextlib.contextmanager
    def ImpliedReadContext(self):
        orig_decision_read_counts_enabled = self.objects.read_counts_enabled
        self.objects.read_counts_enabled = False
        try:
            yield
        finally:
            self.objects.read_counts_enabled = orig_decision_read_counts_enabled

    def _implied_read(self, object_name):
        #with self.ImpliedReadContext():
        return self.objects.data[object_name]

    @contextlib.contextmanager
    def SaveRestoreCurrentObjectContext(self, object_name):
        '''
            Update and restore Resolver cur_object_choice.
        '''
        prev_object_choice = self.cur_object_choice
        self.cur_object_choice = object_name
        try:
            yield
        finally:
            self.cur_object_choice = prev_object_choice

    @contextlib.contextmanager
    def Pass1ChooseObjectContext(self, object_name):
        with self.SaveRestoreCurrentObjectContext(object_name):
            yield

    @contextlib.contextmanager
    def JumpToLastDecisionContext(self, object_name):
        '''
            When done with context, calls _jump_to_last_decision
        '''
        prev_decision_read_counts = copy(self.objects.read_counts)
        yield
        self._jump_to_last_decision(object_name, prev_decision_read_counts)

    @contextlib.contextmanager
    def Pass2ChooseObjectContext(self, object_type, object_name):
        # _incr_object_stat choice object_type $device_name
        with self.JumpToLastDecisionContext(object_name):
            with self.SaveRestoreCurrentObjectContext(object_name):
                yield

    def resolve(self):
        self.best_objects = None
        self.cur_object_choice = None
        self.reject_link = self._reject_link
        self.reject_device = self._reject_device
        try:
            self.decision_order = ['RESOLVE']
            self.objects['RESOLVE'] = None  # dummy for read/jump-counting
            self.objects['SOLUTION'] = None  # dummy for read/jump-counting
            if self._trace.step:
                logger.debug('pass 1...')
            self.walk_decisions(
                    device_decision_order=self.device_decision_order,
                    link_decision_order=None,
                    walker=self.pass1_walker)
            with JumpContext('RESOLVE'):
                if self._trace.step:
                    logger.debug('pass 2...')
                self.walk_decisions(
                        device_decision_order=self.device_decision_order,
                        link_decision_order=None,
                        walker=self.pass2_walker)
        finally:
            del self.cur_object_choice

    #@trace(ptraceback=False)
    def walk_decisions(self, device_decision_order, link_decision_order, walker):
        if link_decision_order:
            link_name = link_decision_order[0]
            for decision in walker(object_type='link', object_name=link_name):
                with JumpContext(link_name):
                    self.walk_decisions(device_decision_order, link_decision_order[1:], walker)
        elif device_decision_order:
            device_name = device_decision_order[0]
            for decision in walker(object_type='device', object_name=device_name):
                with JumpContext(device_name):
                    self.walk_decisions(device_decision_order[1:], self.link_decision_order_by_device[device_name], walker)
        else:
            for decision in walker(object_type='solution', object_name='SOLUTION'):
                pass

    def _solution(self):

        bBest = not self.cg_info.groups or self.cg_state.cur_weight > self.best_weight
        bAccept = bBest or self._find_all
        if bAccept:
            # incr stats(solution)
            if self.cg_info.groups:
                logger.debug('Solution accepted with weight %r', self.cg_state.cur_weight)
                if bBest:
                    self.best_weight = self.cg_state.cur_weight
            else:
                logger.debug('Solution accepted')
            # Although all choices were acceptable, allowing all to
            # be touched would break jumping to the last
            # weight-reducing choice below
            if bBest:
                # with self.ImpliedReadContext():
                self.best_objects = copy(self.objects.data)

        if not self._find_all and self.cg_info.groups and self.best_weight < self.max_weight and self.cg_state.reducing_choices:
            if self._trace.reject_cg:
                logger.debug('Touch and jump to the last weight-reducing choice: %r', self.cg_state.reducing_choices[-1])
            # It is important to touch the last weight-reducing choice as
            # everything chosen since is acceptable and not to be rejected
            # on the basis of this jump.
            _force_read = self.objects[self.cg_state.reducing_choices[-1]]
            self._jump(self.cg_state.reducing_choices[-1], 'SOLUTION')

        # All acceptable choices! Touching only the first (RESOLVE) has the
        # same effect as touching all of them. It is also not necessary to
        # touch anything if breaking out of "RESOLVE", but doing it avoids
        # any confusion caused by falsely pruning when going back up the
        # decision tree.
        _force_read = self.objects['RESOLVE']

        if not self._find_all:
            self.reject_device = self.noop
            self.reject_link = self.noop
            raise JumpException('RESOLVE')

    def _test_constraint(self, object_name, avoid_body, test_body):
        # [%stat%] upvar #[%info level%] stats stats decision_read_counts_idx decision_read_counts_idx
        # [%stat%] t1 = time.perf_counter()
        if avoid_body is not None and avoid_body():
            # [%stat%] t2 = time.perf_counter()
            # [%stat%] ::xscale::tclBench::var_add_stat stats(constraint-avoid) 1 $t1 $t2
            # [%stat%] ::xscale::mmt_add_one stats(constraint-avoid-depth-mmt) $decision_read_counts_idx($object_name)
            return True
        bExpr = test_body()
        # [%stat%] t2 = time.perf_counter()
        if not bExpr and self._trace.constraint:
            logger.debug('Fail constraint of %s: %r', object_name, test_body)
        # [%stat%] ::xscale::tclBench::var_add_stat stats(constraint) 1 $t1 $t2
        # [%stat%] ::xscale::mmt_add_one stats(constraint-depth-mmt) $decision_read_counts_idx($object_name)
        return bExpr

    def _create_group_constraint(self, group_name, test):
        if group_name is None or self.topology.constraint_groups[group_name].weight == 'mandatory':
            return test
        # TODO reduce the number of cg-dependent tests if no different cg-specific constraints exist
        return functools.partial(self._test_cg_constraint_wrapper,
                group_name=group_name,
                test=test)

    def _test_cg_constraint_wrapper(self, group_name, test, *args, **kwargs):
        if self.cg_state.groups[group_name].ratio and test(*args, **kwargs):
            self.cg_state.groups[group_name].ratio = 0
            self._update_cur_weight()
        return True  # always

    #@trace(tgenerator=True)
    def pass1_walker(self, object_type, object_name):
        self.decision_order.append(object_name)

        if object_type == 'device':
            device_name = object_name
            with self.Pass1ChooseObjectContext(device_name):
                self.object_tests[device_name] = []

                # TODO if { ![llength $dynobj_mappings($device_name)] } { error "No possible mapping for $device_name" {} [list BC_FAIL] }

                # Device intersection constraints {{{
                for device_name2 in reversed(self.device_decision_order[:self.device_decision_order.index(device_name)]):
                    if not self.dynobj_mappings[None][device_name].isdisjoint(self.dynobj_mappings[None][device_name2]):
                        self.object_tests[device_name].append(
                                functools.partial(self._test_device_collision,
                                    device_name=device_name,
                                    device_name2=device_name2))
                # }}}

                for group_name in [None] + list(self.cg_info.groups.keys()):
                    if group_name is not None:
                        # Device selection constraints {{{
                        if self.dynobj_mappings[group_name][device_name] < self.dynobj_mappings[None][device_name]:
                            test = functools.partial(self._test_device_in_mapping,
                                    device_name=device_name,
                                    dynobj_mapping=self.dynobj_mappings[group_name][device_name])
                            self.object_tests[device_name].append(
                                    self._create_group_constraint(
                                        group_name=group_name,
                                        test=test))
                        # }}}
                    # Device expr constraints {{{
                    # foreach expr [if { [keylget kltopo ${kpfxgroup}objects.$device_name.constraints.exprs v] } { set v }] {
                    #     _body_resolve_add_group_constrain $device_name $expr
                    # }
                    # }}}

                # _object_choice_done $device_name

                yield

        elif object_type == 'link':
            link_name = object_name
            with self.Pass1ChooseObjectContext(link_name):
                self.object_tests[link_name] = []

                # TODO if { ![llength $dynobj_mappings($link_name)] } { error "No possible mapping for $link_name" {} [list BC_FAIL] }

                link_device_names = self.cache.link_device_names[link_name]
                link_interface_names = self.cache.link_interface_names[link_name]

                # Link parts intersection constraints {{{
                for link_name2 in reversed([link_name2 for link_name2 in self.decision_order[:self.decision_order.index(link_name)] if link_name2 in self.subset.link_names]):
                    link_device_names2 = self.cache.link_device_names[link_name2]
                    link_device_names_intersect = set(link_device_names) & set(link_device_names2)
                    if (
                            len(link_device_names_intersect) == min(len(link_device_names), len(link_device_names2)) and
                            not self.dynobj_mappings[None][link_name].isdisjoint(self.dynobj_mappings[None][link_name2])):
                        # There is a possible intersection of link devices...
                        #   eg.: link_device_names = { R2 R4 }, link_device_names2 { R3 R2 R4 }, link_device_names_intersect = { R2 R4 }
                        link_interface_names2 = self.cache.link_interface_names[link_name2]
                        for device_name2 in link_device_names_intersect:
                            interface_name1 = link_interface_names[link_device_names.index(device_name2)]
                            interface_name2 = link_interface_names2[link_device_names2.index(device_name2)]
                            if self.dynobj_mappings[None][interface_name1].isdisjoint(self.dynobj_mappings[None][interface_name2]):
                                break
                        else:
                            # Compare intersection of link parts
                            self.object_tests[link_name].append(
                                functools.partial(self._test_link_parts_intersect,
                                    link_name=link_name,
                                    link_name2=link_name2))
                            # if 0 {
                            #     # TODO
                            #     set exprs {}
                            #     foreach device_name2 $link_devices_intersect {
                            #         set In1 [expr { [lsearch -exact $link_devices  $device_name2] + 1 }]
                            #         set In2 [expr { [lsearch -exact $link_devices2 $device_name2] + 1 }]
                            #         lappend exprs "\$${link_name2}I$In2 eq \$${link_name}I$In1"
                            #     }
                            #     # XXXJST TODO what about links with more than 2 devices/interfaces?
                            #     # XXXJST TODO what about physical meshes used by 2 different links in a discrete or disjoint fashion?
                            #     append body_resolve $indent "if { !\[_test_constraint $link_name { \[lsearch -sorted -exact \$dynobj_mappings($link_name2) \$$link_name\] == -1 } { [join $exprs " || "] }\] } { continue }\n"
                            # }
                # }}}

                for group_name in [None] + list(self.cg_info.groups.keys()):
                    if group_name is not None:
                        # Link parts intersection constraints {{{
                        if len(self.dynobj_mappings_link_parts[group_name][link_name]) != len(self.dynobj_mappings_link_parts[None][link_name]):
                            test = functools.partial(self._test_link_parts_in_mapping,
                                    link_name=link_name,
                                    dynobj_mapping_link_parts=self.dynobj_mappings_link_parts[group_name][link_name])
                            self.object_tests[link_name].append(
                                    self._create_group_constraint(
                                        group_name=group_name,
                                        test=test))
                        # }}}

                # Interface diff-slot / same-slot constraints {{{
                # for interface_name in link_interface_names:
                #     foreach intf_name2 [lsort -unique -decreasing -dictionary [if { [keylget kltopo ${kpfxgroup}objects.$intf_name.constraints.diff-slot v] } { set v }]] {
                #         if { ![lcontain $chosen_objects $intf_name2] && ![lcontain $intf_names $intf_name2] } {
                #             xscale_keyllappend kltopo ${kpfxgroup}objects.$intf_name2.constraints.diff-slot $intf_name
                #         } else {
                #             # TODO first check for intersection/disjonction of possibilities!
                #             _body_resolve_add_group_constrain $intf_name2 "\$$intf_name eq \"\" || \$$intf_name2 eq \"\" || \[enaTbGetInterfaceParam \$$intf_name2 -slot\] ne \[enaTbGetInterfaceParam \$$intf_name -slot\]"
                #         }
                #     }
                #     foreach intf_name2 [lsort -unique -decreasing -dictionary [if { [keylget kltopo ${kpfxgroup}objects.$intf_name.constraints.same-slot v] } { set v }]] {
                #         if { ![lcontain $chosen_objects $intf_name2] && ![lcontain $intf_names $intf_name2] } {
                #             xscale_keyllappend kltopo ${kpfxgroup}objects.$intf_name2.constraints.same-slot $intf_name
                #         } else {
                #             # TODO first check for intersection/disjonction of possibilities!
                #             _body_resolve_add_group_constrain $intf_name2 "\$$intf_name eq \"\" || \$$intf_name2 eq \"\" || \[enaTbGetInterfaceParam \$$intf_name2 -slot\] eq \[enaTbGetInterfaceParam \$$intf_name -slot\]"
                #         }
                #     }
                # }}}

                # Link expr constraints {{{
                # foreach expr [if { [keylget kltopo ${kpfxgroup}objects.$link_name.constraints.exprs v] } { set v }] {
                #     _body_resolve_add_group_constrain $link_name $expr
                # }
                # }}}

                # foreach intf_name $intf_names {
                #     # Interface expr constraints {{{
                #     foreach expr [if { [keylget kltopo ${kpfxgroup}objects.$intf_name.constraints.exprs v] } { set v }] {
                #         _body_resolve_add_group_constrain $intf_name $expr
                #     }
                #     # }}}
                # }

                # _object_choice_done [linsert $intf_names 0 $link_name]

                yield

        elif object_type == 'solution':
            pass
        else:
            raise ValueError(object_type)

    def _test_device_collision(self, xos_device, device_name, device_name2):
        return self._test_constraint(device_name,
                lambda: xos_device not in self.dynobj_mappings[None][device_name2],
                lambda: xos_device != self.objects[device_name2])

    def _test_device_in_mapping(self, xos_device, device_name, dynobj_mapping):
        return self._test_constraint(device_name,
                None,
                lambda: xos_device in dynobj_mapping)

    def _test_link_parts_intersect(self, xos_link, link_name, link_name2):
        return self._test_constraint(link_name,
                lambda: not self._test_possible_link_parts_intersect(
                    self.dynobj_mappings_link_parts[None][link_name2][self.xos_link_devices_by_link[link_name2]],
                    self.xos_link_parts_by_link[link_name]),
                lambda: (
                    self.objects[link_name2],  # _force_read
                    not test_list_intersect(self.xos_link_parts_by_link[link_name2], self.xos_link_parts_by_link[link_name]),
                    )[-1])

    def _test_link_parts_in_mapping(self, xos_link, link_name, dynobj_mapping_link_parts):
        return self._test_constraint(link_name,
                None,
                lambda: self.xos_link_parts_by_link[link_name] in dynobj_mapping_link_parts)

    def _test_possible_link_parts_intersect(self, l_link_parts1, link_parts2):
        link_parts2 = set(link_parts2)
        for link_parts1 in l_link_parts1:
            if not link_parts2.isdisjoint(link_parts1):
                return True
        return False

    def ChooseDeviceGenerator(self, device_name, xos_devices):
        try:
            for xos_device in list(xos_devices):
                with JumpContext(device_name):
                    # incr stats(try-device)
                    saved_cg_state = copy(self.cg_state)
                    try:
                        self.objects[device_name] = xos_device
                        prev_read_counts = copy(self.objects.read_counts)
                        try:
                            if self._trace._try:
                                logger.debug('Try %s = %r', device_name, self._implied_read(device_name))
                            yield xos_device
                        finally:
                            self.reject_device(device_name, xos_devices, prev_read_counts)
                    finally:
                        self.cg_state = saved_cg_state
        finally:
            self.objects[device_name] = None

    def ChooseLinkGenerator(self, link_name, xos_link_parts_list):
        link_interface_names = self.cache.link_interface_names[link_name]
        try:
            for xos_link_parts in list(xos_link_parts_list):
                with JumpContext(link_name):
                    self.xos_link_parts_by_link[link_name] = xos_link_parts
                    # incr stats(try-link)
                    saved_cg_state = copy(self.cg_state)
                    try:
                        self.objects.update(zip((link_name,) + link_interface_names, xos_link_parts))
                        prev_read_counts = copy(self.objects.read_counts)
                        try:
                            if self._trace._try:
                                logger.debug('Try %s = %r', link_name, xos_link_parts)
                            yield xos_link_parts
                        finally:
                            self.reject_link(link_name, xos_link_parts, xos_link_parts_list, prev_read_counts)
                    finally:
                        self.cg_state = saved_cg_state
        finally:
            self.xos_link_parts_by_link.pop(link_name, None)
            self.objects[link_name] = None
            for part_name in link_interface_names:
                self.objects[part_name] = None

    def _test_read_counts_prune(self, object_name, prev_read_counts):
        # return False  # comment-out to benchmark prune/jump optimizations
        for other_object in self.decision_order:
            if other_object == object_name:
                break
            old_read_count = prev_read_counts[other_object]
            new_read_count = self.objects.read_counts[other_object]
            if new_read_count != old_read_count:
                return False
        return True

    def _jump(self, to_object_name, from_object_name):
        # incr stats(jump) ; ::xscale::mmt_add_one stats(jump-length-mmt) [expr { $decision_read_counts_idx($from_object_name) - $decision_read_counts_idx($to_object_name) }]
        raise JumpException(to_object_name)

    def _jump_to_last_decision(self, object_name, prev_decision_read_counts):
        # return  # comment-out to benchmark prune/jump optimizations
        # Exhausted all possibilities, jump to last relevant decision...
        jump_decision = 'RESOLVE'
        for other_object in self.decision_order:
            if other_object == object_name:
                break
            old_read_count = prev_decision_read_counts[other_object]
            new_read_count = self.objects.read_counts[other_object]
            if new_read_count != old_read_count:
                jump_decision = other_object
        if self._trace.jump:
            logger.debug('Ran out of options for %s; Continue at %r: %s', object_name, jump_decision, self._explain_read_counts_diff(object_name, prev_decision_read_counts))
        self._jump(jump_decision, object_name)

    #@trace(tgenerator=True)
    def pass2_walker(self, object_type, object_name):
        if object_type == 'device':
            device_name = object_name
            with self.Pass2ChooseObjectContext('device', device_name):
                for xos_device in self.ChooseDeviceGenerator(device_name, self.dynobj_mappings[None][device_name]):
                    with JumpContext(device_name):
                        if not all(test(xos_device) for test in self.object_tests[device_name]):
                            continue
                        yield xos_device

        elif object_type == 'link':
            link_name = object_name
            with self.Pass2ChooseObjectContext('link', link_name):
                link_device_names = self.cache.link_device_names[link_name]
                xos_link_devices = tuple(self.objects[link_device_name] for link_device_name in link_device_names)
                self.xos_link_devices_by_link[link_name] = xos_link_devices
                try:
                    for xos_link_parts in self.ChooseLinkGenerator(link_name, self.dynobj_mappings_link_parts[None][link_name][xos_link_devices]):
                        with JumpContext(link_name):
                            xos_link = xos_link_parts[0]
                            if not all(test(xos_link) for test in self.object_tests[link_name]):
                                continue
                            yield xos_link_parts
                finally:
                    del self.xos_link_devices_by_link[link_name]

        elif object_type == 'solution':
            self._solution()
            pass
        else:
            raise ValueError(object_type)

    def _update_cur_weight(self):
        new_weight = 0
        for group_name, cg_state in self.cg_state.groups.items():
            if cg_state.ratio and cg_state.accounted:
                group_weight = self.cg_info.groups[group_name].weight
                if group_weight >= float('inf'):
                    new_weight = float('inf')
                elif group_weight <= - float('inf'):
                    new_weight = - float('inf')
                    break
                elif new_weight < float('inf'):
                    new_weight = new_weight + cg_state.ratio * group_weight
        if new_weight != self.cg_state.cur_weight:
            if not self._find_all and new_weight < self.best_weight:
                # Not a "jump", just forcing rejection...
                raise JumpException(self.cur_object_choice)
            self.cg_state.reducing_choices.append(self.cur_object_choice)
            self.cg_state.cur_weight = new_weight

    def _reject_device(self, device_name, xos_devices, prev_read_counts):
        # _incr_object_stat reject device $device_name
        if self._trace.reject:
            logger.debug('Reject %s = %r', device_name, self._implied_read(device_name))
        if self._test_read_counts_prune(device_name, prev_read_counts):
            # _incr_object_stat prune device $device_name
            #with self.ImpliedReadContext():
            prune_value = self.objects.data[device_name]
            if self._trace.prune:
                logger.debug('Prune %s = %r', device_name, prune_value)
            xos_devices.remove(prune_value)
        else:
            if self._trace.preserve:
                logger.debug('Preserve %s: %r', device_name, self._explain_read_counts_diff(device_name, prev_read_counts))
            pass

    def _reject_link(self, link_name, xos_link_parts, xos_link_parts_list, prev_read_counts):
        # _incr_object_stat reject link $link_name
        if self._trace.reject:
            logger.debug('Reject %s = %r', link_name, xos_link_parts)
        if self._test_read_counts_prune(link_name, prev_read_counts):
            # _incr_object_stat prune link $link_name
            if self._trace.prune:
                logger.debug('Prune %s = %r', link_name, xos_link_parts_list)
            xos_link_parts_list.remove(xos_link_parts)
        else:
            if self._trace.preserve:
                logger.debug('Preserve %s: %r', link_name, self._explain_read_counts_diff(link_name, prev_read_counts))
            pass

    def noop(self, *args):
        pass

    def _explain_read_counts_diff(self, object_name, prev_decision_read_counts):
        l_explain = []
        for other_object in self.decision_order:
            if other_object == object_name:
                break
            old_read_count = prev_decision_read_counts[other_object]
            new_read_count = self.objects.read_counts[other_object]
            if new_read_count != old_read_count:
                l_explain.append((other_object, new_read_count - old_read_count))
            else:
                l_explain.append(other_object)
        return tuple(l_explain)


class Constraints(pyats.topology.Testbed):

    subsets = None

    def __init__(self):
        self.subsets = collections.OrderedDict()
        super().__init__(name='_TopologyMapper_Constraints')

    @property
    def device_names(self):
        '''OrderedSet of device names (R#).'''
        try:
            from pyats.tcl.internal import DictionaryCompare
            sRs = [topo_dev.device_name
                   for topo_dev in self.devices.values()]
            sRs = OrderedSet(sorted(sRs, key=functools.cmp_to_key(DictionaryCompare)))
            return sRs
        except ImportError:
            # Considering users with no sourced tcl environment
            pass
        except Exception:
            return

    @property
    def link_names(self):
        '''OrderedSet of link names (L#).'''
        try:
            from pyats.tcl.internal import DictionaryCompare
            topo_devices = list(self.devices.values())
            topo_links = set()
            for topo_dev in topo_devices:
                topo_links |= set(topo_dev.links)
            sLs = [topo_link.link_name for topo_link in topo_links]
            sLs = OrderedSet(sorted(sLs, key=functools.cmp_to_key(DictionaryCompare)))
            return sLs
        except ImportError:
            # Considering users with no sourced tcl environment
            pass
        except Exception:
            return

    @property
    def interface_names(self):
        '''OrderedSet of Interface names (R#I#) in dictionnary order.'''
        try:
            from pyats.tcl.internal import DictionaryCompare
            sRIs = []
            for topo_dev in self.devices.values():
                sRIs.extend(topo_dev.interface_names)
            sRIs = OrderedSet(sorted(sRIs, key=functools.cmp_to_key(DictionaryCompare)))
            return sRIs  # R#I#
        except ImportError:
            # Considering users with no sourced tcl environment
            pass
        except Exception:
            return

    @property
    def object_names(self):
        '''Generator of object names, first devices, then links, then
        interfaces, each in their respective dictionnary order.
        '''
        yield from self.device_names
        yield from self.link_names
        yield from self.interface_names

    def get_device_by_name(self, device_name):
        return self.devices[device_name]

    def get_link_by_name(self, link_name):
        for topo_link in self.links:
            if topo_link.name == link_name:
                return topo_link
        raise KeyError(link_name)

    def get_interface_by_name(self, interface_name):
        for topo_dev in self.devices.values():
            try:
                return topo_dev.interfaces[interface_name]
            except KeyError:
                pass
        raise KeyError(interface_name)

    def link_device_names(self, link_name):
        '''List of Device names (R#) in dictionnary order.

        The order is consistent with devices corresponding to
        self.link_interface_names but may contain duplicates.
        '''
        topo_link = self.get_link_by_name(link_name)
        return topo_link.device_names  # R#

    def link_interface_names(self, link_name):
        '''OrderedSet of Interface names (R#I#) of the link in dictionnary
        order.

        The order is consistent with devices corresponding to
        self.link_device_names.
        '''
        topo_link = self.get_link_by_name(link_name)
        return topo_link.interface_names  # R#I#


class TopologyMapper(object):

    assignments = None
    constraints = None
    constraint_groups = None  # {}
    resolved_subset = None

    def __init__(self, topology_file=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.constraint_groups = {}  # TODO
        self.constraints = Constraints()

        if topology_file:
            self.load(topology_file)

    def create_bundle(self, link_name, member_links, bundle_name='#'):
        raise NotImplementedError  # TODO
        # dyntopo = self.xoo_dyntopo
        # member_link_names = dyntopo.ReverseQuery(member_links)
        # sL = str(link_name)
        # dyntopo.CreateBundle(sL, bundle_name, member_link_names)
        # xoo_link = getattr(dyntopo, sL)
        # self.assignments[sL] = xoo_link
        # In = 0
        # while True:
        #     In += 1
        #     sLI = '%sI%d' % (sL, In)
        #     xoo_intf = getattr(dyntopo, sLI)
        #     if not xoo_intf:
        #         break
        #     self.assignments[sLI] = xoo_intf

    def create_emulated_device(self, dev_name, link_name, tgen_port, *args, **kwargs):
        raise NotImplementedError  # TODO
        # TODO
        # global xscale
        # from xscale import xoo
        # dyntopo_dev_args = []
        # for ain, aout in [
        #         ('draw_rank', '-draw-rank'),
        #         ('draw_cluster', '-draw-cluster'),
        #         ]:
        #     v = kwargs.pop(ain, None)
        #     if v is not None:
        #         dyntopo_dev_args += [aout, v]
        # dyntopo = self.xoo_dyntopo
        # sR = str(dev_name)
        # xoo_tgen_port = tgen_port if isinstance(tgen_port, xoo.Interface) else getattr(dyntopo, tgen_port)
        # tgen_name = xoo_tgen_port.device.name
        # xoo_dev = xoo.Device.NewEmulated(dev_name, xoo_tgen_port, *args, **kwargs)
        # dyntopo.AddDevice(sR, *dyntopo_dev_args)
        # self.assign(sR, xoo_dev)
        # xoo_emul_link = xoo.Link.Find('-from-router', xoo_dev.name, '-linktype', 'emulated')
        # xoo_interfaces = xoo_emul_link.interfaces
        # xoo_interfaces2 = pyats.tcl.tk.call('::enaTbGetLinkParam', tclstr(xoo_emul_link), '-interfaces')
        # from xscale.tcl import cast_identity
        # xoo_emul_intf = xoo.Interface.Find('-router', xoo_dev.name, '-iftype', 'physical', '-free-list', xoo_emul_link.interfaces)
        # xoo_peer_intf = next((intf for intf in xoo_emul_link.interfaces if intf is not xoo_emul_intf))
        # if link_name is not None:
        #     self.create_link(link_name, intfs=[xoo_emul_intf, xoo_peer_intf], link=xoo_emul_link)

    def create_link(self, link_name, intfs=None, link=None):
        assert intfs is not None or link is not None
        xos_intfs = intfs
        del intfs
        xos_link = link
        del link
        link_name = str(link_name)
        if xos_link is None:
            xos_intfs = list(xos_intfs)
            xos_link = genie.conf.base.Link(
                    testbed=Genie.testbed,
                    name=link_name,
                    interfaces=xos_intfs)
        if xos_intfs is None:
            xos_intfs = list(xos_link.interfaces)
        sL = link_name
        topo_link = Link(name=sL)
        for xos_intf in xos_intfs:
            xos_device = xos_intf.device
            sR = self.reverse_query(xos_device)
            assert sR is not None
            topo_device = self.constraints.get_device_by_name(sR)
            topo_intf = Interface(
                    name=topo_device.next_interface_name,  # R#I#
                    link=sL)
            topo_device.add_interface(topo_intf)
            self.assign(sL, xos_intf)

    def remove_device(self, device_name, gc_collect=True):
        assert device_name in self.device_names
        device = self.query_constraints(device_name)
        for interface_name in list(device.interfaces.keys()):
            self.remove_interface(interface_name, gc_collect=False)
        del self.constraints.devices[device_name]
        if self.assignments:
            self.assignments.pop(device_name, None)
        if gc_collect:
            del device
            gc.collect()

    def remove_link(self, link_name, remove_interfaces=True, gc_collect=True):
        assert link_name in self.link_names
        link = self.query_constraints(link_name)
        interface = None  # for GC
        link_interfaces = set(link.interfaces)
        for interface in link_interfaces:
            link.disconnect_interface(interface)
        if self.assignments:
            self.assignments.pop(link_name, None)
        if remove_interfaces:
            for interface in link_interfaces:
                self.remove_interface(interface.name, gc_collect=False)
        if gc_collect:
            del link
            del interface
            del link_interfaces
            gc.collect()

    def remove_interface(self, interface_name, gc_collect=True):
        assert interface_name in self.interface_names
        interface = self.query_constraints(interface_name)
        link = interface.link
        if link and len(link.interfaces) <= 2:
            self.remove_link(link.name, remove_interfaces=True, gc_collect=False)
        else:
            if link:
                link.disconnect_interface(interface)
            interface.device.remove_interface(interface)
            if self.assignments:
                self.assignments.pop(interface_name, None)
        if gc_collect:
            del interface
            del link
            gc.collect()

    def query_constraints(self, obj_name):
        assert type(obj_name) is str
        try:
            return self.constraints.get_device_by_name(obj_name)
        except KeyError:
            pass
        try:
            return self.constraints.get_link_by_name(obj_name)
        except KeyError:
            pass
        try:
            return self.constraints.get_interface_by_name(obj_name)
        except KeyError:
            pass
        raise KeyError(obj_name)

    def reverse_query(self, obj):
        '''Query the constraint name assigned to the given object.'''
        assignments = self.assignments
        for s, assigned_obj in self.assignments.items():
            if assigned_obj is obj:
                return s
        raise ValueError(obj)

    def query(self, obj_name):
        '''Query the object assigned to the given constraint name.'''
        assert type(obj_name) is str
        return self.assignments[obj_name]

    def assign(self, obj_name, obj):
        assert type(obj_name) is str
        if isinstance(obj, genie.conf.base.Device):
            if obj_name not in self.device_names:
                raise KeyError(obj_name)
        elif isinstance(obj, genie.conf.base.Link):
            if obj_name not in self.link_names:
                raise KeyError(obj_name)
        elif isinstance(obj, genie.conf.base.Interface):
            if obj_name not in self.interface_names:
                raise KeyError(obj_name)
        else:
            raise ValueError(obj)
        self.assignments[obj_name] = obj

    def load(self, obj):
        from . import loader
        for device in list(self.constraints.devices.keys()):
            self.constraints.remove_device(device)
        loader.load(obj, in_place=self)

    @property
    def device_names(self):
        '''OrderedSet of device names (R#).'''
        return self.constraints.device_names

    @property
    def link_names(self):
        '''OrderedSet of link names (L#).'''
        return self.constraints.link_names

    def link_device_names(self, link_name):
        '''List of Device names (R#) in dictionnary order.

        The order is consistent with devices corresponding to
        self.link_interface_names but may contain duplicates.
        '''
        return self.constraints.link_device_names(link_name)

    def link_interface_names(self, link_name):
        '''OrderedSet of Interface names (R#I#) of the link in dictionnary
        order.

        The order is consistent with devices corresponding to
        self.link_device_names.
        '''
        return self.constraints.link_interface_names(link_name)

    @property
    def interface_names(self):
        '''OrderedSet of Interface names (R#I#) in dictionnary order.'''
        return self.constraints.interface_names

    @property
    def object_names(self):
        '''Generator of object names, first devices, then links, then
        interfaces, each in their respective dictionnary order.
        '''
        return self.constraints.object_names

    @property
    def devices(self):
        '''Generator of assigned device objects in dictionnary order of their
        name.
        '''
        assignments = self.assignments
        if assignments:
            for sR in self.device_names:
                if sR in assignments:
                    yield assignments[sR]

    @property
    def links(self):
        '''Generator of assigned link objects in dictionnary order of their
        name.
        '''
        assignments = self.assignments
        if assignments:
            for sL in self.link_names:
                if sL in assignments:
                    yield assignments[sL]

    @property
    def interfaces(self):
        '''Generator of assigned interface objects in dictionnary order of
        their name.
        '''
        assignments = self.assignments
        if assignments:
            for sRI in self.interface_names:
                if sRI in assignments:
                    yield assignments[sRI]

    def __getattr__(self, name):
        '''Provide access to assigned objects as attributes.'''
        if not name.startswith('_'):
            if name != 'assignments':
                assignments = self.assignments
                if assignments is not None:
                    try:
                        return assignments[name]
                    except KeyError:
                        pass
        sup = getattr(super(), '__getattr__', None)
        if sup:
            return sup(name)
        raise AttributeError(name)

    def resolve(self, *, log_diagram=True, **kwargs):

        self.forget()

        self.do_resolve(**kwargs)

        if log_diagram:
            self.log_diagram()

    def do_resolve(self, subset=None, required_objects=None):

        debug_level = 5
        log_traces = False  # TODO
        optimize = True  # TODO

        _find_all = False  # TODO For debugging/benchmarking

        _trace = types.SimpleNamespace()
        # {{{
        # true/1:
        d = bool(debug_level)
        _trace.step = d          # general step logs
        _trace._try = d          # log choices "try"
        _trace.dump_env = d      # dump env
        _trace.trace_best = d    # trace best_weight, best_objects
        _trace.trace_cg = d      # trace cg_state, cg_info
        _trace.dump_fail = d     # dump kl_topo and testbed diagram on failure
        _trace.stats = d         # dump stats

        # 2:
        d = debug_level >= 2
        _trace.dump_body = d     # dump body_resolve

        # 3:
        d = debug_level >= 3
        _trace.constraint = d    # log constraint test failures

        # 4:
        d = debug_level >= 4
        _trace.reject = d        # log choices "reject"
        _trace.reject_cg = d     # log choices "reject cg"

        # 5:
        d = debug_level >= 5
        _trace.prune = d          # log choices "prune"
        _trace.jump = d           # log choices "jump"

        # 6:
        d = debug_level >= 6
        _trace.read = d           # trace read counts
        _trace.preserve = d       # log choices "preserve"

        # 7:
        d = debug_level >= 7
        _trace.find_cmd = d       # dynobj_mappings find commands
        _trace.dump_mappings = d  # dump dynobjs_by_type, dynobj_mappings

        # 8:
        d = debug_level >= 8

        # 9:
        d = debug_level >= 9
        _trace.trace_stats = d    # trace stats
        # }}}

        required_objects = set(required_objects or ())

        if subset is None:
            subset = 'master'
        subset_names = [subset] if isinstance(subset, str) else list(subset)
        del subset

        self.assignments = {}
        all_objects = set(self.object_names)

        all_used_objects = set()
        absolutely_required_objects = None
        for subset_name in list(subset_names):
            subset_required_objects = all_objects if subset_name == 'master' else self.constraints.subsets[subset_name]
            if required_objects > subset_required_objects:
                logger.info('Missing required objects: Reject subset %s', subset_name)
                subset_names.remove(subset_name)
                continue
            all_used_objects |= subset_required_objects
            if absolutely_required_objects is not None:
                absolutely_required_objects &= subset_required_objects
            else:
                absolutely_required_objects = set(subset_required_objects)
        if not subset_names:
            raise AllSubsetsRejectedError(self)

        # TODO bringup
        # if { [enaTbFindTestDevice -objState * -no-error] eq "" } {
        #     # No testbed/devices available. On-the-fly spawning?
        #     package require X-Scale::EnXR
        #     if { [info exists ::env(XRUT_ROOT)] } {
        #         set bFoundSubset false
        #         foreach subset_name $subset_names {
        #             if { $subset_name eq "master" } {
        #                 set subset_required_objects $all_objects
        #             } else {
        #                 set subset_required_objects [keylget kltopo subsets.$subset_name.required_objects]
        #             }
        #             if { [lcontain $subset_required_objects "TGEN"] } {
        #                 set tgen_platform "pagent"
        #                 # Handle TBTOPO_TGEN_PLATFORM like enaTbResetAllObjects {{{
        #                 if {
        #                     [info exists ::env(TBTOPO_TGEN_PLATFORM)] &&
        #                     ![string match [string tolower $::env(TBTOPO_TGEN_PLATFORM)] $tgen_platform]
        #                 } {
        #                     enaLogVerify -skip "Skipping subset '$subset_name': TGEN platform '$tgen_platform' does not match '$::env(TBTOPO_TGEN_PLATFORM)' specified by ::env(TBTOPO_TGEN_PLATFORM)." -fail false -log terse
        #                     continue
        #                 }
        #                 # }}}
        #             }
        #             set enxr_count 0
        #             foreach device_name [lsearch -regexp -all -inline $subset_required_objects {^[RS]\d+$}] {
        #                 incr enxr_count
        #                 if {
        #                     [string is true -strict [keylget data topos.$current_dyntopo_name.objects.$device_name.constraints.redundancy]] ||
        #                     [lcontain [keylget data topos.$current_dyntopo_name.objects.$device_name.constraints.prereqs] "xscale_prereq_router_has_redundancy"]
        #                 } {
        #                     incr enxr_count
        #                 }
        #             }
        #             if { $enxr_count > $::env(XSCALE_MAX_ENXR_DEVICES) } {
        #                 enaLogVerify -skip "Skipping subset '$subset_name': Number of EnXR devices/RPs greater than ::env(XSCALE_MAX_ENXR_DEVICES) \[$enxr_count > $::env(XSCALE_MAX_ENXR_DEVICES)\]" -fail false -log terse
        #                 continue
        #             }
        #             set bFoundSubset true
        #             break
        #         }
        #         if { $bFoundSubset } {
        #             set enxr_topology_script [format -subset $subset_name -format xrut.py]
        #             xscale_spawn_enxr_topology -script $enxr_topology_script -step -diagram false
        #             # Pagent's hltapi::conect doesn't care about the value of
        #             # -reset, only that it exists or not.
        #             # Since we may have spawned a fresh pagent, we want to make
        #             # sure that any leftover backup configs won't be used now or
        #             # later and cause issues, such as IP address conflicts.
        #             foreach router [enaTbFindTestDevice -name {"*pagent*"} -type tgen -all -no-error -- -name] {
        #                 foreach file [glob -nocomplain -directory /tmp -types f ${router} ${router}_*] {
        #                     catch {file delete -force $file}
        #                 }
        #             }
        #             xscale_connect_routers
        #             enaDestructor -id on_resolve_fail [list xscale_forget_enxr_topology]
        #         } else {
        #             enaLogVerify -skip "No subset applicable to EnXR" -fail false
        #         }
        #     }
        # }
        mappings_start_time = time.perf_counter()
        # {{{

        dynobj_mappings = {}  # [group_name][object_name] = set([xos_obj, ...])
        dynobj_mappings_link_parts = {}  # [group_name][link_name][tuple(xos_link_devices)] = set([xos_link_parts, ...])
        dynobjs_by_type = {
            'device': self.device_names & all_used_objects,
            'interface': self.interface_names & all_used_objects,
            'link': self.link_names & all_used_objects,
        }
        # Determine useable constraint_groups {{{
        weighted_constraint_groups_list = []
        mandatory_constraint_groups_list = []
        for group_name, constraint_group in self.constraint_groups.items():
            constraint_group_objects = set(constraint_group.objects.keys())
            if constraint_group_objects and constraint_group_objects <= all_used_objects:
                if constraint_group.weight == 'mandatory':
                    mandatory_constraint_groups_list.append(group_name)
                else:
                    weighted_constraint_groups_list.append(group_name)
        # }}}
        for group_name in [None] + mandatory_constraint_groups_list + weighted_constraint_groups_list:
            dynobj_mappings[group_name] = {}
            dynobj_mappings_link_parts[group_name] = {}
            # enaVerifyGroup {{{
            if group_name is None:
                constraint_group = self
                group_weight = 'mandatory'
                # TODO set ipfxgroup ""
                # TODO set kpfxgroup ""
            else:
                # TODO lappend _enaVerify_defaults -prefix "($group_name group) "
                constraint_group = self.constraint_groups[group_name]
                # TODO set ipfxgroup $group_name,
                # TODO set kpfxgroup constraint_groups.$group_name.
                group_weight = constraint_group.weight
            for type in ('device', 'interface', 'link'):
                for object_name in dynobjs_by_type[type]:
                    object_constraints = constraint_group.query_constraints(object_name)
                    # enaVerifyGroup {{{
                    # TODO lappend _enaVerify_defaults -append-prefix "$object_name"
                    if group_name is not None:
                        pass  # TODO
                        #     if { ![keylexists kltopo ${kpfxgroup}objects.$object_name.constraints] } {
                        #         if { $type eq "device" } {
                        #             set dynobj_mappings($ipfxgroup$object_name) $dynobj_mappings($object_name)
                        #             continue
                        #         } else {
                        #             keylset kltopo ${kpfxgroup}objects.$object_name.constraints [set [namespace current]::kl_default_constraints_$type]
                        #         }
                        #     }
                    if type == 'device':
                        # {{{
                        if group_name is None:
                            # TODO
                            # if { [info exists ::test_params(rtrLabelList)] } {
                            #     set lbls [lsearch -glob -all -inline [keylkeys ::test_params(rtrLabelList)] [keylget kltopo ${kpfxgroup}objects.$object_name.constraints.labels]]
                            #     if { [llength $lbls] } {
                            #         keylset kltopo objects.$object_name.constraints.name [struct::list map $lbls {keylget ::test_params(rtrLabelList)}]
                            #     }
                            # }
                            # XXXJST TODO support constraint-group environment overrides
                            for constraint, envsfx in (
                                    ('type', 'TYPE'),
                                    ('match_name', 'NAME'),
                                    ('platform', 'PLATFORM'),
                                    ('tgen_platform', 'TGEN_PLATFORM'),
                                    ('os', 'OS'),
                                    ('multinode_requested', 'MULTINODE'),
                                    ):
                                for role in [object_name] + list(object_constraints.label) + list(object_constraints.role):
                                    env = os.environ.get('DYNTOPO_%s_%s' % (role, envsfx), None)
                                    if env is not None:
                                        if constraint == 'multinode_requested':
                                            env = bool(env)
                                        setattr(object_constraints, constraint, env.split())
                                        break
                        find_kwargs = {}
                        if object_constraints.type is not None:
                            find_kwargs['type'] = object_constraints.type.__contains__
                        name_constraint = None
                        if object_constraints.match_name is not None:
                            v = set(object_constraints.match_name)
                            if name_constraint is None:
                                name_constraint = v
                            else:
                                name_constraint &= v
                        if group_name is not None:
                            v = set(o.name for o in dynobj_mappings[object_name])
                            if name_constraint is None:
                                name_constraint = v
                            else:
                                name_constraint &= v
                        if name_constraint is not None:
                            find_kwargs['name'] = name_constraint.__contains__
                        if object_constraints.platform is not None:
                            find_kwargs['platform'] = object_constraints.platform.__contains__
                        if object_constraints.tgen_platform is not None:
                            find_kwargs['tgen_platform'] = object_constraints.tgen_platform.__contains__
                        if object_constraints.os is not None:
                            find_kwargs['os'] = object_constraints.os.__contains__
                        if object_constraints.multinode_requested is not None:
                            find_kwargs['multinode'] = object_constraints.multinode_requested
                        if _trace.find_cmd:
                            logger.debug('group_name=%r, object_name=%r, find_kwargs=%r', group_name, object_name, find_kwargs)
                        xos_devices = Genie.testbed.find_devices(**find_kwargs)
                        if _trace.find_cmd:
                            logger.debug('found xos_devices=%r', xos_devices)
                        for predicate in (object_constraints.predicates or []):
                            xos_devices = filter(predicate, xos_devices)
                        xos_devices = OrderedSet(sorted(xos_devices))
                        dynobj_mappings[group_name][object_name] = xos_devices
                        if group_name is not None and group_weight == 'mandatory':
                            dynobj_mappings[None][object_name] = dynobj_mappings[group_name][object_name]
                        # }}}
                    elif type == 'interface':
                        # {{{
                        m = re.search(r'^(?P<device_name>R\d+|TGEN)I(?P<link_intf_num>\d+)(?:\.(?P<intf_sub>\d+))?$', object_name)
                        if not m:
                            raise KeyError('Invalid interface object name %r' % (object_name,))
                        device_name = m.group('device_name')
                        # link_intf_num = int(m.group('link_intf_num'))
                        # intf_sub = m.group('intf_sub')
                        if group_name is None:
                            for constraint, envsfx in (
                                    #('device', 'DEVICE'),
                                    ('match_name', 'NAME'),
                                    ('type', 'TYPE'),
                                    #('engine', 'ENGINE'),
                                    ('product_id', 'PRODUCT_ID'),
                                    #('diff_slot', 'DIFF_SLOT'),
                                    #('same_slot', 'SAME_SLOT'),
                                    ):
                                for role in [object_name] + list(object_constraints.label):
                                    env = os.environ.get('DYNTOPO_%s_%s' % (role, envsfx), None)
                                    if env is not None:
                                        setattr(object_constraints, constraint, env.split())
                                        break
                        find_kwargs = {}
                        find_kwargs['device'] = dynobj_mappings[group_name][device_name].__contains__
                        # if object_constraints.device_name is not None:
                        #     find_kwargs['name', object_constraints.device_name.__contains__]
                        if object_constraints.match_name is not None:
                            find_kwargs['name'] = object_constraints.match_name.__contains__
                        if object_constraints.type is not None:
                            find_kwargs['type'] = object_constraints.type.__contains__
                        # if object_constraints.engine is not None:
                        #     find_kwargs['engine'] = object_constraints.engine.__contains__
                        if object_constraints.product_id is not None:
                            find_kwargs['product_id'] = object_constraints.product_id.__contains__
                        # if object_constraints.diff_slot is not None:
                        #     find_kwargs['diff_slot'] = object_constraints.diff_slot.__contains__
                        # if object_constraints.same_slot is not None:
                        #     find_kwargs['same_slot'] = object_constraints.same_slot.__contains__
                        if group_name is not None:
                            find_kwargs['iterable'] = dynobj_mappings[None][object_name]
                        if _trace.find_cmd:
                            logger.debug('group_name=%r, object_name=%r, device_name=%r, find_kwargs=%r', group_name, object_name, device_name, find_kwargs)
                        # diff_slot & same_slot handled later
                        xos_interfaces = Genie.testbed.find_interfaces(**find_kwargs)
                        if _trace.find_cmd:
                            logger.debug('found xos_interfaces=%r', xos_interfaces)
                        for predicate in (object_constraints.predicates or []):
                            xos_interfaces = filter(predicate, xos_interfaces)
                        xos_interfaces = OrderedSet(sorted(xos_interfaces))
                        dynobj_mappings[group_name][object_name] = xos_interfaces
                        if group_name is not None and group_weight == 'mandatory':
                            dynobj_mappings[None][object_name] = dynobj_mappings[group_name][object_name]
                        # }}}
                    elif type == 'link':
                        # {{{
                        if group_name is None:
                            for constraint, envsfx in (
                                    ('match_name', 'NAME'),
                                    ('type', 'TYPE'),
                                    ('interface', 'INTERFACE'),
                                    ):
                                for role in [object_name] + list(object_constraints.label):
                                    env = os.environ.get('DYNTOPO_%s_%s' % (role, envsfx), None)
                                    if env is not None:
                                        setattr(object_constraints, constraint, env.split())
                                        break
                        # TODO from and to constraints, including exact names
                        link_device_names = self.link_device_names(object_name)
                        link_interface_names = self.link_interface_names(object_name)
                        # XXXJST TODO Support Mesh objects
                        device_name1 = link_device_names[0]
                        device_name2 = link_device_names[1]
                        find_kwargs = {}
                        if object_constraints.match_name is not None:
                            find_kwargs['name'] = object_constraints.match_name.__contains__
                        if object_constraints.type is not None:
                            find_kwargs['type'] = object_constraints.type.__contains__
                        if group_name is not None:
                            find_kwargs['iterable'] = dynobj_mappings[None][object_name]
                        if _trace.find_cmd:
                            logger.debug('group_name=%r, object_name=%r, find_kwargs=%r', group_name, object_name, find_kwargs)
                        xos_links = []
                        if _trace.find_cmd:
                            logger.debug('found xos_links=%r', xos_links)
                        xos_links = Genie.testbed.find_links(**find_kwargs)
                        # Could add this as find_kwargs['interfaces'] but it is
                        # very slow compared to other constraint checks,do
                        # last.
                        def test_link_interface_mappings(interfaces):
                            for iintf1, intf1 in enumerate(interfaces):
                                if intf1 not in dynobj_mappings[group_name][link_interface_names[0]]:
                                    continue
                                if intf1.device not in dynobj_mappings[group_name][device_name1]:
                                    continue
                                if object_constraints.interface is not None:
                                    if intf1.name not in object_constraints.interface:
                                        continue
                                # intf1 matches
                                for iintf2, intf2 in enumerate(interfaces):
                                    if iintf1 == iintf2:
                                        continue
                                    if intf2 not in dynobj_mappings[group_name][link_interface_names[1]]:
                                        continue
                                    if intf2.device not in dynobj_mappings[group_name][device_name2]:
                                        continue
                                    if object_constraints.interface is not None:
                                        if intf2.name not in object_constraints.interface:
                                            continue
                                    break  # intf2 matches
                                else:
                                    continue  # no intf2 matches
                                return True  # intf1 and intf2 match
                            else:
                                return False  # no intf1 and intf2 match
                        xos_links = filter(
                            (lambda xos_link: test_link_interface_mappings(xos_link.interfaces)),
                            xos_links)  # generator
                        # Filter predicates last so users can proceed based on
                        # the assumption that all other constraints are
                        # asserted first.
                        for predicate in (object_constraints.predicates or []):
                            xos_links = filter(predicate, xos_links)  # generator
                        xos_links = sorted(xos_links)

                        new_xos_links = set()
                        new_xos_link_parts = set()  # [xos_link, xos_intf1, xos_intf2, ...]
                        arr_new_xos_devices = {device_name: set() for device_name in link_device_names}
                        arr_new_link_parts = {}
                        for xos_link in xos_links:
                            xos_link_intfs = xos_link.interfaces  # WeakList
                            if len(xos_link_intfs) < len(link_device_names):
                                # XXXJST TODO != 2 devices!
                                continue
                            xos_link_intfs = sorted(xos_link_intfs)  # WeakList -> sorted list
                            link_predicates = object_constraints.predicates or []
                            for xos_link_intfs in itertools.permutations(xos_link_intfs, len(link_device_names)):
                                # xos_link_intfs is a tuple... keep it as such because lists are not hashable
                                bAccept = True
                                for i, xos_intf in enumerate(xos_link_intfs):
                                    if xos_intf not in dynobj_mappings[group_name][link_interface_names[i]]:
                                        bAccept = False
                                        break
                                    if i >= 2:
                                        # find_links above only matches I1 & I2...
                                        # complete constraint matching for I3+
                                        if object_constraints.interface is not None:
                                            if xos_intf.name not in object_constraints.interface:
                                                # bAccept = False
                                                continue
                                if not bAccept:
                                    continue
                                if not all(predicate(xos_link) for predicate in link_predicates):
                                    # bAccept = False
                                    break  # NOT continue
                                link_predicates = []  # Only needs to be tested once per link
                                xos_link_devices = tuple(xos_intf.device for xos_intf in xos_link_intfs)
                                for xos_device, device_name in zip(xos_link_devices, link_device_names):
                                    arr_new_xos_devices[device_name].add(xos_device)
                                xos_link_parts = (xos_link,) + xos_link_intfs
                                new_xos_links.add(xos_link)
                                new_xos_link_parts.add(xos_link_parts)
                                arr_new_link_parts.setdefault(xos_link_devices, set())
                                arr_new_link_parts[xos_link_devices].add(xos_link_parts)
                        dynobj_mappings[group_name][object_name] = OrderedSet(sorted(new_xos_links))
                        dynobj_mappings_link_parts[group_name][object_name] = collections.defaultdict(set)
                        dynobj_mappings_link_parts[group_name][object_name][None] = new_xos_link_parts
                        for xos_link_devices, xos_link_parts_set in arr_new_link_parts.items():
                            dynobj_mappings_link_parts[group_name][object_name][xos_link_devices] = xos_link_parts_set
                        if group_name is not None and group_weight == 'mandatory':
                            dynobj_mappings[None][object_name] = dynobj_mappings[group_name][object_name]
                            dynobj_mappings_link_parts[None][object_name] = dynobj_mappings_link_parts[group_name][object_name]
                            arr_old_link_parts = copy(dynobj_mappings_link_parts[None][object_name])
                            dynobj_mappings_link_parts[None][object_name] = collections.defaultdict(set)
                            dynobj_mappings_link_parts[None][object_name][None] = arr_old_link_parts.pop(None)
                            for xos_link_devices in arr_new_link_parts.keys():
                                dynobj_mappings_link_parts[None][object_name][xos_link_devices] = \
                                        arr_old_link_parts.getdefault(xos_link_devices, set()) & dynobj_mappings_link_parts[group_name][object_name][xos_link_devices]
                        if object_name in absolutely_required_objects:
                            for device_name, new_xos_devices in arr_new_xos_devices.items():
                                dynobj_mappings[group_name][device_name] &= new_xos_devices
                            if group_name is not None and group_weight == 'mandatory':
                                for device_name in link_device_names:
                                    dynobj_mappings[None][device_name] = dynobj_mappings[group_name][device_name]
                        # XXXJST TODO -- optimize based on list of accepted xos_link_parts {{{
                        # if { $optimize && [lcontain $absolutely_required_objects $object_name] } {
                        #     set dynobj_mappings($ipfxgroup$device_name1) [intersect $dynobj_mappings($ipfxgroup$device_name1) [enaObjGetParam -list true $lvIntfs1 -router -self]]
                        #     set dynobj_mappings($ipfxgroup$device_name2) [intersect $dynobj_mappings($ipfxgroup$device_name2) [enaObjGetParam -list true $lvIntfs2 -router -self]]
                        #     set dynobj_mappings($ipfxgroup${object_name}I1) [intersect $dynobj_mappings($ipfxgroup${object_name}I1) $lvIntfs1]
                        #     set dynobj_mappings($ipfxgroup${object_name}I2) [intersect $dynobj_mappings($ipfxgroup${object_name}I2) $lvIntfs2]
                        #     if { $group_name ne "" && $group_weight eq "mandatory" } {
                        #         set dynobj_mappings($device_name1) $dynobj_mappings($ipfxgroup$device_name1)
                        #         set dynobj_mappings($device_name2) $dynobj_mappings($ipfxgroup$device_name2)
                        #         set dynobj_mappings(${object_name}I1) $dynobj_mappings($ipfxgroup${object_name}I1)
                        #         set dynobj_mappings(${object_name}I2) $dynobj_mappings($ipfxgroup${object_name}I2)
                        #     }
                        # }
                        # }}}
                        # }}}
                    else:
                        raise ValueError('Invalid dynamic topology object type %r.' % (type,))
                    # }}}
            # }}}

        # }}}
        # Having all values in dynobj_mappings sorted and unique is mandatory; This is already covered above.

        mappings_end_time = time.perf_counter()

        # if _trace['dump_env']:
        #     logger.debug('env:\n  %s', '\n  '.join(['%s = %s' % (env, val) for env, val in os.environ.items() if env.startswith('DYNTOPO_')]))
        if _trace.dump_mappings:
            logger.debug('dynobjs_by_type=%r', dynobjs_by_type)
            logger.debug('dynobj_mappings=%r', dynobj_mappings)
            logger.debug('dynobj_mappings_link_parts=%r', dynobj_mappings_link_parts)
        for subset_name in subset_names:

            # if { $_trace(trace_cg) } {
            #     foreach v { cg_state cg_info } {
            #         unset -nocomplain $v ; enaTraceVar $v
            #     }
            # }
            # if { $_trace(trace_best) } {
            #     foreach v { best_weight best_objects } {
            #         unset -nocomplain $v ; enaTraceVar $v
            #     }
            # }

            # # Stats {{{
            #
            # stats = {
            #         'choice-device': 0,
            #         'choice-link': 0,
            #         'try-device': 0,
            #         'try-link': 0,
            #         'reject-device': 0,
            #         'reject-link': 0,
            #         'prune-device': 0,
            #         'prune-link': 0,
            #         'read-device': 0,
            #         'read-link': 0,
            #         'jump': 0,
            #         'solution': 0,
            #         }
            # set stats(choice-depth-mmt)           [::xscale::mmt_init]
            # set stats(reject-depth-mmt)           [::xscale::mmt_init]
            # set stats(prune-depth-mmt)            [::xscale::mmt_init]
            # set stats(read-depth-mmt)             [::xscale::mmt_init]
            # set stats(jump-length-mmt)            [::xscale::mmt_init]
            # set stats(constraint-depth-mmt)       [::xscale::mmt_init]
            # set stats(constraint-avoid-depth-mmt) [::xscale::mmt_init]
            # ::xscale::tclBench::var_reset_stats stats(constraint)
            # ::xscale::tclBench::var_reset_stats stats(constraint-avoid)
            #
            # if { $_trace(trace_stats) } { foreach a [array names stats] { enaTraceVar -ops write stats($a) } } ;# enaTraceVar stats would not work with upvars
            #
            # # proc _dump_stats {{{
            #
            # proc _dump_stats {} [string map [list {[%info level%]} [info level]] {
            #         upvar #[%info level%] \
            #             stats stats \
            #             subset_name subset_name \
            #             decision_order decision_order \
            #             mappings_start_time mappings_start_time \
            #             mappings_end_time mappings_end_time
            #         variable current_dyntopo_name
            #         set out {}
            #         append out "X-Scale Dynamic Topology Resolution Statistics:"
            #         append out [::format "\n dyntopo:     %s, subset: %s" $current_dyntopo_name $subset_name]
            #         append out [::format "\n solutions:   %i in %.6fs" $stats(solution) [expr { $stats(end_time) - $stats(start_time) }]]
            #         set stats(object-device) [llength [lsearch -all -regexp $decision_order {^[RVS]\d+$|^TGEN$}]]
            #         set stats(object-link)   [llength [lsearch -all -regexp $decision_order {^L\d+$}]]
            #         set stats(object) [expr { $stats(object-device) + $stats(object-link) }]
            #         append out [::format "\n objects:     %i (%i devices, %i links), mapped in %.6fs" $stats(object) $stats(object-device) $stats(object-link) [expr { $mappings_end_time - $mappings_start_time }]]
            #         set stats(choice) [expr { $stats(choice-device) + $stats(choice-link) }]
            #         append out [::format "\n choices:     %i (%i devices, %i links)" $stats(choice) $stats(choice-device) $stats(choice-link)]
            #         if { $stats(choice) } {
            #             append out [::format ", depth: %s \[min/max/avg\]" [::xscale::mmt_fmt_mma $stats(choice-depth-mmt) $stats(choice)]]
            #         } else {
            #             append out [::format ", depth: n/a"]
            #         }
            #         if 0 {
            #             set stats(try) [expr { $stats(try-device) + $stats(try-link) }]
            #             append out [::format "\n tries:       %i (%i devices, %i links)" $stats(try) $stats(try-device) $stats(try-link)]
            #         }
            #         set stats(reject) [expr { $stats(reject-device) + $stats(reject-link) }]
            #         append out [::format "\n rejects:     %i (%i devices, %i links)" $stats(reject) $stats(reject-device) $stats(reject-link)]
            #         if { $stats(reject) } {
            #             append out [::format ", depth: %s \[min/max/avg\]" [::xscale::mmt_fmt_mma $stats(reject-depth-mmt) $stats(reject)]]
            #         } else {
            #             append out [::format ", depth: n/a"]
            #         }
            #         set stats(prune) [expr { $stats(prune-device) + $stats(prune-link) }]
            #         append out [::format "\n prunes:      %i (%i devices, %i links)" $stats(prune) $stats(prune-device) $stats(prune-link)]
            #         if { $stats(prune) } {
            #             append out [::format ", depth: %s \[min/max/avg\]" [::xscale::mmt_fmt_mma $stats(prune-depth-mmt) $stats(prune)]]
            #         } else {
            #             append out [::format ", depth: n/a"]
            #         }
            #         set stats(read) [expr { $stats(read-device) + $stats(read-link) }]
            #         append out [::format "\n reads:       %i (%i devices, %i links)" $stats(read) $stats(read-device) $stats(read-link)]
            #         if { $stats(read) } {
            #             append out [::format ", depth: %s \[min/max/avg\]" [::xscale::mmt_fmt_mma $stats(read-depth-mmt) $stats(read)]]
            #         } else {
            #             append out [::format ", depth: n/a"]
            #         }
            #         append out [::format "\n jumps:       %i" $stats(jump)]
            #         if { $stats(jump) } {
            #             append out [::format ", length: %s \[min/max/avg\]" [::xscale::mmt_fmt_mma $stats(jump-length-mmt) $stats(jump)]]
            #         } else {
            #             append out [::format ", length: n/a"]
            #         }
            #         append out [::format "\n constraints: %s" [::xscale::tclBench::var_get_stats_string stats(constraint) "tests"]]
            #         if { [set n [lindex [::xscale::tclBench::var_get_stats stats(constraint)] 0]] } {
            #             append out [::format ", depth: %s \[min/max/avg\]" [::xscale::mmt_fmt_mma $stats(constraint-depth-mmt) $n]]
            #         } else {
            #             append out [::format ", depth: n/a"]
            #         }
            #         append out [::format "\n  avoided:    %s" [::xscale::tclBench::var_get_stats_string stats(constraint-avoid) "tests"]]
            #         if { [set n [lindex [::xscale::tclBench::var_get_stats stats(constraint-avoid)] 0]] } {
            #             append out [::format ", depth: %s \[min/max/avg\]" [::xscale::mmt_fmt_mma $stats(constraint-avoid-depth-mmt) $n]]
            #         } else {
            #             append out [::format ", depth: n/a"]
            #         }
            #         enaLogVerify -info $out
            # }]
            #
            # # }}}
            # # proc _incr_object_stat {{{
            #
            # proc _incr_object_stat { stat_type object_type object_name } [string map [list {[%info level%]} [info level]] {
            #         upvar #[%info level%] \
            #             stats stats \
            #         if { $object_type eq "" } {
            #             incr stats($stat_type)
            #         } else {
            #             # incr stats($stat_type) ;# summed-up in _dump_stats, if needed.
            #             incr stats($stat_type-$object_type)
            #         }
            #         ::xscale::mmt_add_one stats($stat_type-depth-mmt) $decision_read_counts_idx($object_name)
            # }]
            # if { !$_trace(stats) && !$_trace(trace_stats) } { proc _incr_object_stat { args } {} }
            #
            # # }}}
            #
            # # }}}

            if _trace.step:
                logger.debug('Resolving topology... subset_name=%r', subset_name)
            subset = TopologySubset(
                    topology=self,
                    name=subset_name,
                    subset_required_objects=all_objects if subset_name == 'master' else self.constraints.subsets[subset_name],
                    )

            r = Resolver(
                    topology=self,
                    subset=subset,
                    dynobj_mappings=dynobj_mappings,
                    dynobj_mappings_link_parts=dynobj_mappings_link_parts,
                    _trace=_trace,
                    _find_all=_find_all,
                    )

            # Define states {{{

            # TODO limit weighted_constraint_groups_list to applicable ones
            if weighted_constraint_groups_list:
                r.max_weight = 0
                for group_name in weighted_constraint_groups_list:
                    constraint_group = self.constraint_groups[group_name]
                    group_weight = constraint_group.weight
                    r.cg_info.groups[group_name] = types.SimpleNamespace()
                    r.cg_info.groups[group_name].weight = group_weight
                    r.cg_info.groups[group_name].ratio = 1
                    r.cg_info.groups[group_name].object_names = set(constraint_group.object_names)
                    r.cg_state.groups[group_name] = types.SimpleNamespace()
                    if group_weight < 0:
                        # Do not include in max_weight
                        r.cg_state.groups[group_name].accounted = False
                    else:
                        r.cg_state.groups[group_name].accounted = True
                        if group_weight >= float('inf') or r.max_weight >= float('inf'):
                            r.max_weight = float('inf')
                        else:
                            r.max_weight += group_weight
                r.best_weight = - float('inf')
                r.cg_state.cur_weight = r.max_weight

            # }}}

            # if _trace.step:
            #     enaTraceProc -leave false -max-args 1 _choose_device
            #     enaTraceProc -leave false -max-args 2 _choose_link
            # stats['start_time'] time.perf_counter()
            r.resolve()
            # stats['end_time'] time.perf_counter()

            # if { $_trace(stats) } { _dump_stats }

            if (
                    not r.best_objects or
                    (weighted_constraint_groups_list and r.best_weight < 0)):
                logger.debug('Failed to resolve X-Scale dynamic topology, subset %r', subset_name)
                continue
            if weighted_constraint_groups_list:
                logger.info('Resolved X-Scale dynamic topology, subset %r, weight %r.', subset_name, r.best_weight)
            else:
                logger.info('Resolved X-Scale dynamic topology, subset %r.', subset_name)
            # enaDestructor -id on_resolve_fail -cancel
            active_xos_interfaces = []
            # enaTbSetDefaultTopologyLayer [keylget kltopo params.topolayer]
            for object_name, object_value in r.best_objects.items():
                if object_name in ('RESOLVE', 'SOLUTION'):
                    continue
                if object_value is None:
                    continue
                self.assign(object_name, object_value)
                if isinstance(object_value, genie.conf.base.Device):
                    # if { [enaTbGetTestDeviceParam $object_value -type] eq "router" } {
                    #     lappend lvActiveIntfs [enaTbFindInterface -router $object_value -interface "Loopback0" -create]
                    # }
                    # enaTbSetTestDevice $object_value -label [linsert [keylget kltopo objects.$object_name.params.labels] 0 $object_name]
                    pass
                elif isinstance(object_value, genie.conf.base.Interface):
                    active_xos_interfaces.append(object_value)
                    # enaTbSetInterface $object_value -topolayer [keylget kltopo params.topolayer]
                elif isinstance(object_value, genie.conf.base.Link):
                    # enaTbSetLink $object_value -topolayer [keylget kltopo params.topolayer]
                    pass
                else:
                    raise ValueError(object_value)
            Genie.testbed.set_active_interfaces(active_xos_interfaces)
            # enaTbSetDefaultTopologyLayer test
            self.resolved_subset = subset
            return

        # if { $_trace(dump_fail) } {
        #     xscale::dyntopo dump
        #     if { ![lcontain [xscale::dyntopo names] $::env(TESTBED)] } {
        #         set orig_current_dyntopo_name $current_dyntopo_name
        #         xscale::dyntopo new $::env(TESTBED)
        #         xscale::dyntopo load-testbed
        #         xscale::dyntopo log -suffix $::env(TESTBED)
        #         xscale::dyntopo forget
        #         xscale::dyntopo select $orig_current_dyntopo_name
        #     }
        # }
        # enaDestructor -id dyntopo_debug_restore -eval
        raise FailedToResolveException(self)

    def log_diagram(self):
        legend = []
        legend.append('Topology assignments:')
        assigned_object_names = set(self.assignments.keys())
        assigned_device_names = self.device_names & assigned_object_names
        assigned_link_names = self.link_names & assigned_object_names
        assigned_interface_names = self.interface_names & assigned_object_names
        done_interface_names = set()

        if assigned_device_names:
            legend.append('--- Devices ---')
            for device_obj_name in assigned_device_names:
                legend.append('    {}: {}'.format(
                    device_obj_name,
                    self.assignments[device_obj_name].name))
        if assigned_link_names:
            legend.append('--- Links ---')
            for link_obj_name in assigned_link_names:
                legend.append('    {}:'.format(
                    link_obj_name))
                link_constraints = self.constraints.get_link_by_name(link_obj_name)
                for interface_obj_name in link_constraints.interface_names & assigned_interface_names:
                    legend.append('        {}: {} {}'.format(
                        interface_obj_name,
                        self.assignments[interface_obj_name].device.name,
                        self.assignments[interface_obj_name].name))
                    assigned_interface_names.remove(interface_obj_name)
        if assigned_interface_names:
            legend.append('--- Interfaces ---')
            for interface_obj_name in assigned_interface_names:
                legend.append('    {}: {} {}'.format(
                    interface_obj_name,
                    self.assignments[interface_obj_name].device.name,
                    self.assignments[interface_obj_name].name))
        logger.info('\n'.join(legend))

    def forget(self):

        self.assignments = None
        self.resolved_subset = None

        if pyats.easypy.runtime.testbed:
            # Reset testbed from scratch
            Genie.init(testbed=pyats.easypy.runtime.testbed)
        elif Genie.testbed:
            # Reset object states
            for xos_device in Genie.testbed.devices:
                xos_device.obj_state = 'active'
                for xos_link in xos_device.interfaces:
                    xos_link.obj_state = 'active'
            for link in Genie.testbed.links:
                link.obj_state = 'active'
            # TODO remove features?

# vim: ft=python ts=8 sw=4 et
