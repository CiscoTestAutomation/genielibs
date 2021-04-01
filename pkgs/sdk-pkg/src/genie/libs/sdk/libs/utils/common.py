'''Those are normalized functions that could be used in all platforms'''

# Python
import re
import random
import logging
from enum import Enum
from copy import deepcopy
from ipaddress import _BaseAddress
from collections import defaultdict
from collections.abc import Iterable
from prettytable import PrettyTable as ptable

# import genie
from genie.ops.utils import get_ops
from genie.utils.diff import Diff
from genie.conf.base.attributes import SubAttributesDict
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.libs.conf.base import IPv4Network
from genie.libs import parser
from genie.utils.summary import Summary

# abstract
from genie.abstract import Lookup

# import pyats
from pyats.log.utils import banner
from pyats.utils.objects import find, R, Operator

# Genie Libs
from genie.libs.conf.base.neighbor import Neighbor
from genie.libs.sdk.libs.utils.mapping import Mapping

# module logger
log = logging.getLogger(__name__)


class UpdateLearntDatabase(object):
    """Class to update local/global verifications and PTS"""

    def __init__(self, obj, device, update_ver_list=None, update_feature_list=None):
        """built-in __init__

        instantiates each update actions.

        Arguments
        ---------
            device (`obj`): Device object
            obj (`obj`): Genie Trigger Object
            update_ver_list (`list`): List of verifications names
            update_feature_list(`list`): List of pts features names
        """
        self.device = device
        self.obj = obj
        # update verifications list
        self.update_ver_list = update_ver_list
        # update pts features list
        self.update_feature_list = update_feature_list
        # build up abstract object based on the os of device
        self.abstract = Lookup.from_device(device)

    @property
    def is_local_ver_enabled(self):
        '''To check if local verifications need to be udpated.'''

        # create summary instnace for local verification
        self.local_summary = Summary(title='Local Verifications', width=150)

        if not self.obj.parent.verifications:
            self.local_summary.add_message(
              '* No verifications imported')
            self.local_summary.add_subtitle_line()
            log.info('No verifications imported')
            return False

        if not self.obj.verf:
            self.local_summary.add_message(
              '* No local verifications executed')
            self.local_summary.add_subtitle_line()
            log.info('No local verifications executed')
            return False

        if not self.update_ver_list:
            self.local_summary.add_message(
              '* No verifications defined to be updated')
            self.local_summary.add_subtitle_line()
            log.info('No verifications defined to be updated')
            return False

        for ver in self.update_ver_list:
            if self.obj.verf and self.device.name in self.obj.verf and \
               self.obj.verf[self.device.name] and \
               ver in self.obj.verf[self.device.name]:
                return True

        # add seperate line
        self.local_summary.add_sep_line()

        # compose the summary message
        self.local_summary.add_message(
          '* Skipped Update\n')
        msgs = ''
        for ver in self.update_ver_list:
            msgs += '%s: Not learned before on device %s\n' % \
                (self.local_summary.add_indent(ver), self.device.name)
        self.local_summary.add_message(msgs)
        self.local_summary.add_subtitle_line()

        log.info('Required Local verification "{v}" is '
                'not learned before on device {d}, Skip updating local'
                .format(v=self.update_ver_list, d=self.device.name))
        return False
    
    @property
    def is_global_ver_enabled(self):
        '''To check if global verifications need to be udpated.'''

        # create summary instnace for Global verification
        self.global_summary = Summary(title='Global Verifications', width=150)

        if not self.obj.parent.verifications:
            self.global_summary.add_message(
              '* No verifications imported')
            self.global_summary.add_subtitle_line()
            log.info('No verifications imported')
            return False

        if hasattr('self.obj.parent', 'verf'):
            if not self.obj.parent.verf:
                self.global_summary.add_message(
                '* No global verifications executed')
                self.global_summary.add_subtitle_line()
                log.info('No global verifications executed')
                return False
           
        if not self.update_ver_list:
            self.global_summary.add_message(
              '* No verifications defined to be updated')
            self.global_summary.add_subtitle_line()
            log.info('No verifications require to be updated')
            return False

        for ver in self.update_ver_list:
            if hasattr('self.obj.parent', 'verf'):
                if self.device.name in self.obj.parent.verf and \
                self.obj.parent.verf[self.device.name] and \
                ver in self.obj.parent.verf[self.device.name]:
                    return True

        # add seperate line
        self.global_summary.add_sep_line()

        # compose the summary message
        self.global_summary.add_message(
          '* Skipped Update\n')
        msgs = ''
        for ver in self.update_ver_list:
            msgs += '%s: Not learned before on device %s\n' % \
                (self.global_summary.add_indent(ver), self.device.name)
        self.global_summary.add_message(msgs)
        self.global_summary.add_subtitle_line()

        log.info('Required Global verification "{v}" is '
                'not learned before on device {d}, Skip updating global'
                .format(v=self.update_ver_list, d=self.device.name))
        return False

    @property
    def is_pts_enabled(self):
        '''To check if PTS need to be udpated.'''
        # create summary instnace for PTS
        self.pts_summary = Summary(title='PTS', width=150)

        if 'pts' not in self.obj.parent.parameters:
            self.pts_summary.add_message('* No PTS executed')
            log.info('No PTS executed')
            self.pts_summary.add_subtitle_line()
            return False

        if not self.update_feature_list:
            self.pts_summary.add_message(
              '* No PTS features require to be updated')
            self.pts_summary.add_subtitle_line()
            log.info('No PTS features require to be updated')
            return False

        for feature in self.update_feature_list:
            if feature in self.obj.parent.parameters['pts']:
                return True

        # add seperate line
        self.pts_summary.add_sep_line()
        
        # compose the summary message
        self.pts_summary.add_message(
          '* Skipped Update')
        msgs = ''
        for fe in self.update_feature_list:
            msgs += '%s: Not learned before on device %s\n' % \
                (self.pts_summary.add_indent(fe), self.device.name)
        self.pts_summary.add_message(msgs)
        self.pts_summary.add_subtitle_line()

        log.info('Required features "{v}" is '
                'not learned before on device {d}, Skip updating PTS'
                .format(v=self.update_feature_list, d=self.device.name))
        return False

    def _get_command_output(self, ver):
        '''Extract the Verification output.
           Args:
              Mandatory:
                ver (`str`) : verification name.

           Returns:
               str: parser output
               ops object: ops object after learn

           Raises:
               Metaparser errors
        '''

        # Check if verificaiton is parser, callable or Ops
        if 'cmd' in self.obj.parent.verifications[ver]:
            # compose the command object
            execute_obj = self.abstract.parser
            for item in self.obj.parent.verifications[ver]['cmd']['class'].split('.'):
                execute_obj = getattr(execute_obj, item)
            execute_obj = execute_obj(self.device)
        elif 'source' in self.obj.parent.verifications[ver]:
            # compose the source object
            execute_obj = self.abstract
            for item in self.obj.parent.verifications[ver]['source']['class'].split('.'):
                execute_obj = getattr(execute_obj, item)
            execute_obj = execute_obj(self.device)
        
        # parser update
        if hasattr(execute_obj, 'parse'):
            # check if has parameters
            if 'parameters' in self.obj.parent.verifications[ver]:
                para = self.obj.parent.verifications[ver]['parameters']
            else:
                para = {}
            output = execute_obj.parse(**para)
            return output

        # Ops update
        if hasattr(execute_obj, 'learn'):
            execute_obj.learn()
            return execute_obj

        # Callable update
        # TODO

    def _update_msg_summary(self, summary, successes, skips):
        if successes:
            summary.add_message(
              '* Successfully Updated')
            for ver in successes:
                msg = summary.add_indent(ver)
                summary.add_message(msg)

        if skips:
            summary.add_message(
              '* Skipped Update')
            for ver, msg in skips.items():
                msgs = '%s: %s\n' % \
                    (summary.add_indent(ver), msg)
                summary.add_message(msgs)

    def update_verification(self):
        '''Learn the verifications from the given list and
        overwrite it into local and global verifications.

       Args:
          None

       Returns:
           None

       Raises:
           None

       Example:
           >>> update_obj = UpdateLearntDatabase(object, device, 
                 update_ver_list=['Verify_Module', 'Verify_RedundancyStatus'])
           >>> update_obj.update_verification()
        '''
        # Check if neede to update
        if not self.is_local_ver_enabled:
            # no combining the logic is to let it run each function
            # to initial the summary object
            if not self.is_global_ver_enabled:
                return
        else:
            # inital the global summary object
            self.is_global_ver_enabled

        # Initial lists for updating local/global vers
        tmp_list_local = []
        tmp_list_global = []
        # initial for message print
        skip_dict_local = {}
        skip_dict_global = {}
        success_list_local = []
        success_list_global = []

        # get same commands for local/global to avoid the duplicated show commands
        for ver in self.update_ver_list:
            # local verififations
            if self.obj.verf and self.device.name in self.obj.verf and \
               self.obj.verf[self.device.name] and \
               ver in self.obj.verf[self.device.name]:
                tmp_list_local.append(ver)
            else:
                skip_dict_local.update(
                  {ver: 'Not learned before on device %s' % self.device.name})

            # global verififations
            if self.device.name in self.obj.parent.verf and \
               self.obj.parent.verf[self.device.name] and \
               ver in self.obj.parent.verf[self.device.name]:
                tmp_list_global.append(ver)
            else:
                skip_dict_global.update(
                  {ver: 'Not learned before on device %s' % self.device.name})

        # get same list
        same_list = list(set(tmp_list_local).intersection(tmp_list_global))

        # get diff list
        [tmp_list_local.remove(i) for i in same_list]
        [tmp_list_global.remove(i) for i in same_list]

        # update same commands for local and global
        for ver in same_list:
            try:
                output = self._get_command_output(ver)
            except Exception as e:
                skip_dict_local.update(
                  {ver: '%s' % e.__class__.__name__})
                skip_dict_global.update(
                  {ver: '%s' % e.__class__.__name__})
                # ignore when the output is empty
                log.warning(
                    'Local verification "{}" cannot be updated'.format(ver))
                log.warning(str(e))
                continue
            else:
                success_list_local.append(ver)
                success_list_global.append(ver)

            if isinstance(output, dict):
                self.obj.verf[self.device.name][ver].name = output
                self.obj.parent.verf[self.device.name][ver].name = output
            elif isinstance(output, object):
                self.obj.verf[self.device.name][ver] = output
                self.obj.parent.verf[self.device.name][ver] = output
        
        # update local specific
        for ver in tmp_list_local:
            try:
                output = self._get_command_output(ver)
            except Exception as e:
                skip_dict_local.update(
                  {ver: '%s' % e.__class__.__name__})
                # ignore when the output is empty
                log.warning(
                    'Local verification "{}" cannot be updated'.format(ver))
                log.warning(str(e))
                continue
            else:
                success_list_local.append(ver)

            if isinstance(output, dict):
                self.obj.verf[self.device.name][ver].name = output
            elif isinstance(output, object):
                self.obj.verf[self.device.name][ver] = output
        
        # update global  specific
        for ver in tmp_list_global:
            try:
                output = self._get_command_output(ver)
            except Exception as e:
                skip_dict_global.update(
                  {ver: '%s' % e.__class__.__name__})
                # ignore when the output is empty
                log.warning(
                    'Global verification "{}" cannot be updated'.format(ver))
                log.warning(str(e))
                continue
            else:
                success_list_global.append(ver)

            if isinstance(output, dict):
                self.obj.parent.verf[self.device.name][ver].name = output
            elif isinstance(output, object):
                self.obj.parent.verf[self.device.name][ver] = output

        # print out messages
        # - LOCAL
        self._update_msg_summary(self.local_summary, 
                                 success_list_local,
                                 skip_dict_local)
      
        # - Global
        self._update_msg_summary(self.global_summary, 
                                 success_list_global,
                                 skip_dict_global)
     
    def update_pts(self, update_attributes=None):
        '''Learn the PTS from the given list and
        overwrite it.

       Args:
          Mandatory:
          Optional:
            update_attributes (`dict`) : 
                Attributes from the PTSs that want to be updatd,
                should be {'feature': ['key1_path', 'key2_path']}.
                Default: None (will update the whole PTS)

       Returns:
           None

       Raises:
           None

       Example:
           >>> update_obj = UpdateLearntDatabase(object, device, 
                   update_feature_list=['platform', 'bgp'])
           >>> update_obj.update_verification(
                   update_attributes={'bgp': ['info'],
                                      'platform': ['chassis_sn', 'slot']})
        '''
        if not self.is_pts_enabled:
            return

        # initial skip list for pring message
        skip_dict_pts = {}
        success_list_pts = []

        # update pts
        for feature in self.update_feature_list:
               
            log.info("Update {f} pts on {d}".format(f=feature, d=self.device))

            # check if pts runs on this device before
            if self.device.alias in self.obj.parent.parameters['pts'][feature]:

                # learn the ops again
                try:
                    module = self.obj.parent.parameters['pts'][feature][self.device.alias]\
                        .__class__(self.device)
                    module.learn()
                except Exception as e:
                    skip_dict_pts.update({feature: e.__class__.__name__})
                    log.warning('Feature {} cannot be learned, Skip updating'
                                 .format(feature))
                    log.warning(str(e))
                    continue

                # update the given keys
                for attr in update_attributes[feature]:
                    try:
                        setattr(self.obj.parent.parameters['pts'][feature][self.device.alias],
                                   attr, (getattr(module, attr)))
                    except Exception as e:
                        skip_dict_pts.update({feature: e.__class__.__name__})
                        
                success_list_pts.append(feature)
            else:
                skip_dict_pts.update({feature: 
                  'Feature {f} was not learned on {d} before, Skip updating'
                    .format(f=feature, d=self.device)})
                log.warning(
                    'Feature {f} was not learned on {d} before, Skip updating'
                    .format(f=feature, d=self.device))
        # print out messages
        # - PTS
        self._update_msg_summary(self.pts_summary, 
                                 success_list_pts,
                                 skip_dict_pts)        
        self.pts_summary.add_subtitle_line()


class LearnPollDiff():

    @classmethod
    def ops_diff(self, ops_learn, ops_compare, exclude=None, ops_modified=None,
                  conf_argument=None):
        '''Diff two ops object with ignoring the keys from the exclude list

           Args:
              Mandatory:
                ops_learn (`obj`) : Ops object.
                ops_compare (`obj`) : Ops object.
              Optional:
                exclude (`list`) : Keys/attributs to ignore in the diff.
                mock (`list`) : List of items, which contain a list of keys
                               strucure of dict, and the value
                               needs to be mocked.

           Returns:
               None

           Raises:
               AssertionError: When diff is found

           Example:
               >>> ops_diff(ops_learn = <bgp_ops_obj>,
                            ops_compare = <bgp_ops_obj>,
                            exclude = ['up_time', 'keepalive', 'maker'],
                            mock = [['info', 'instance', '{}', 'vrf', '{}',
                                    'neighbor', '{}', 'remote_as', '900']])
        '''
        if ops_modified and conf_argument:
            # Some section of ops_learn needs to be
            # modified as its value was modified.

            # First verify the R requirement to make sure they are valid.
            for r in ops_modified:
                # Modify r to only verify that one which were modified.
                for argument, value in conf_argument.items():
                    if argument in r.args[0]:
                        loc = r.args[0].index(argument)
                        r.args[0][loc+1] = value

                ret = find([ops_learn], r, filter_=False)
                if not ret:
                    raise Exception("'{r} does not exists in new "
                                    "snapshot".format(r=r))

                # Good this exists, but it will fail the comparaison with the
                # next snapshot, even though its valid. So let's take the value
                # of the snap and use it for this snapshot comparaison as we've
                # already verified it was valid
                osnap = ops_compare
                learn = ops_learn
                for item in r.args[0][:-2]:
                    # item could be either attr or dit
                    try:
                        osnap = osnap[item]
                        learn = learn[item]
                    except (KeyError, TypeError) as e:
                        try:
                            osnap = getattr(osnap, item)
                            learn = getattr(learn, item)
                        except AttributeError:
                            raise KeyError("'{item}' does not exists in the "
                                           "snapshots".format(item=item))
                else:
                    learn[r.args[0][-2]] = osnap[r.args[0][-2]]
                    pass


        diff = Diff(ops_compare, ops_learn, exclude=exclude)
        diff.findDiff()

        if str(diff):
            log.info("The output is not same with diff\n{}".format(str(diff)))
            raise AssertionError("The output is not same with diff\n{}"
                                 .format(str(diff)))


def learn_ops(feature, device, attributes=None, **kwargs):
    '''function to get ops class and create object then learn the features.
    It can be the child process from pcall as well'''
    # print the messages
    log.info(banner('Sending the corresponding clis to learn {} \n'
        'Operational status on device {}'
        .format(feature, device.name), align='left'))
    # get uut os corresponding feature ops class by genie provided function
    try:
        ops = get_ops(feature, device)
    except Exception as e:
        raise Exception('Cannot get the {f} corresponding '
            'abstracted class on {d}\n{m}'
              .format(m=str(e), f=feature, d=device.name))
    
    ops_obj = ops(device, attributes=attributes)
    # learn the ops
    ops_obj.learn_poll(**kwargs)

    return ops_obj


def get_ops_diff(new, original, exclude=None, modified_path=None, keys=None):
    '''Diff two ops object with ignoring the keys from the exclude list

       Args:
          Mandatory:
            new (`obj`) : Ops object.
            original (`obj`) : Ops object.
          Optional:
            exclude (`list`) : Keys/attributs to ignore in the diff.
            modified_path (`list`) : List of items that needs to be checked.
                                     The item is following the ops attributes path
                                     in a list.
            keys (`list`) : List of items that contains the key values for the
                            'modified_path' regexp items.

       Returns:
           None

       Raises:
           AssertionError: When diff is found
           ValueError: When required attributes are not in the ops

       Example:
           >>> ops_diff(new = <bgp_ops_obj>,
                        original = <bgp_ops_obj>,
                        exclude = ['up_time', 'keepalive', 'maker'],
                        modified_path = [['info', 'instance', '(?P<instance>.*)',
                                          'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                          'remote_as', '900']],
                        keys = [{'instance': '1', 'vrf': 'default', 'neighbor': '10.4.1.1'},
                                {'instance': '1', 'vrf': 'VRF1', 'neighbor': '10.16.2.2'},])
    '''

    def _modify_ops_snapshot(original, current, path):
        # First does path exists in original, except the value
        r = R(path[:-1] + ['(.*)'])
        ret = find([original], r, filter_=False)
        if not ret:
            raise ValueError("'{p}' does not exist on original snapshot "
                "as per the original trigger requirement".format(p=path))
        _modify_value(current, path[:-1], ret[0][0])

    def _modify_value(snapshot, path, value):
        for p in path[:-1]:
            try:
                snapshot = snapshot[p]
            except (TypeError):
                snapshot = getattr(snapshot, p)
        if isinstance(snapshot, dict):
            snapshot[path[-1]] = value
        else:
            setattr(snapshot, path[-1], value)
    
    if modified_path and keys:
        mapping = Mapping()
        for req in modified_path:

            # use mapping internal function to populate the path with learned values
            req = mapping._populate_path([req], new.device, keys=keys)
            rs = [R(requirement) for requirement in req]

            # want to print one by one
            for rs_item in rs:
                ret = find([new], rs_item, filter_=False, all_keys=True)
                if not ret:
                    # return rs_item.args
                    raise ValueError("'{req}' does not exists in "
                                    "'{o}'".format(req=rs_item.args, o=new))

            # Let's modify the ops value to be equal to the original
            # snapshot. This will allow for comparing the other keys
            for require in req:
                try:
                    _modify_ops_snapshot(original=original,
                                         current=new, path=require)
                except Exception as e:
                    return

    diff = Diff(original, new, exclude= (exclude or []) + ['maker', 'callables', 'device', 'diff_ignore'])
    diff.findDiff()
    if diff.diffs:
        log.error("Current ops is not equal to the initial Snapshot "
                  "taken on device {d}.\n{e}".format(e=str(diff),
                                                    d=getattr(new, 'device', 'name')))
        raise AssertionError("Current ops is not equal to the initial Snapshot "
                        "taken on device {d}.\n{e}".format(e=str(diff),
                                                          d=getattr(new, 'device', 'name')))


def get_duplicated_interface_ip(ops):
    '''Get interface A which has ipv4 address, and find another interface B'''
    # initial return values
    duplicated_ip = None
    duplicated_iprefix_length = None
    ip_intf = None
    duplicated_intf = None
    network_addr = None

    intfs = list(ops.info.keys())
    # find any 'up' interface
    for intf in ops.info:
        for ipv4, item in ops.info[intf].get('ipv4', {}).items():
            # choose one different interfaces
            diff_intfs = intfs.copy()
            diff_intfs.remove(intf)
            if not diff_intfs:
                # no diff_intf found, find the next item
                continue

            # store the ip and interface lists for next section
            duplicated_ip = item['ip']
            duplicated_iprefix_length = item['prefix_length']

            if duplicated_iprefix_length == '32':
                # looks for loopback interfaces
                duplicated_intfs = [i for i in diff_intfs if 'Loopback' in i]
                if not duplicated_intfs:
                    continue
            else:
                # choose one non-loopback interface
                duplicated_intfs = [i for i in diff_intfs if 'Loopback' not in i]
                if not duplicated_intfs:
                    continue

            # get interface from same vrf
            for interface in duplicated_intfs:
                try:
                    assert ops.info[intf].get('vrf') == ops.info[interface].get('vrf')
                except Exception:
                    continue
                else:
                    duplicated_intf = interface
                    break

            # store interface to accurate the error message
            ip_intf = intf
            # store network address to accurate the error message
            network_addr = IPv4Network(ipv4, False).network_address
            # print out the message
            log.info(banner("The ip address {ip} is collected from {o_intf}".format(
                        ip=ipv4, o_intf=intf), align='left'))
        if duplicated_intf:
            break

    # return the values
    return duplicated_ip, duplicated_iprefix_length, ip_intf, duplicated_intf, network_addr

def get_ospf_router_id(ops):
    '''Get OSPF router-id from ospf ops'''
    # Create R object to contain the required interface ops attributes path
    # find router_id
    rs_rd_helper = R(['info', 'vrf', '(?P<vrf>.*)', 'address_family', '(?P<af>.*)',
                      'instance', '(?P<instance>.*)', 'router_id', '(?P<router_id>.*)'])

    # use find object to find required interfaces and ip address
    # returned value is like
    # [('10.2.2.2', ['info', 'vrf', 'default', 'address_family', 'ipv4', 'instance', '1', 'router_id'])]
    ret_rd_helper = find([ops], rs_rd_helper, filter_=False)

    if not ret_rd_helper:
        return None

    # call function to get dict of {key: value}
    ret = GroupKeys.group_keys(ret_num={}, source=ret_rd_helper,
                               reqs=rs_rd_helper.args)
    # return the values
    return ret

def get_ospf_interfaces_with_neighbor(ops, neighbor):
    '''Get OSPF interfaces by given neighbor'''
    
    # find the neighbors on uut connected to the helper device
    reqs = [['info', 'vrf', '(?P<vrf>.*)', 'address_family', '(?P<af>.*)',
            'instance', '(?P<instance>.*)', 'areas', '(?P<areas>.*)', 'interfaces',
            '(?P<interfaces>.*)', 'neighbors', neighbor, '(?P<neighbors_info>.*)']]
    rs_uut = [R(i) for i in reqs]
    ret_uut = find([ops], *rs_uut, filter_=False)

    return GroupKeys.group_keys(ret_num={}, source=ret_uut, reqs=reqs)

def get_ospf_interfaces(ops):
    '''Get OSPF interfaces by given neighbor'''
    
    # Create R object to contain the required interface ops attributes path
    # find any ospf 'up' interface
    reqs = [['info', 'vrf', '(?P<vrf>.*)', 'address_family', '(?P<af>.*)',
            'instance', '(?P<instance>.*)', 'areas', '(?P<areas>.*)', 'interfaces',
            '(?P<interfaces>.*)','state', '(?P<state>(dr|bdr|dr_other|point_to_point))'],
            ['info', 'vrf', '(?P<vrf>.*)', 'address_family', '(?P<af>.*)',
             'instance', '(?P<instance>.*)', 'areas', '(?P<areas>.*)', 'interfaces',
             '(?P<interfaces>.*)', 'cost', '(?P<cost>.*)']]

    rs = [R(i) for i in reqs]
    ret = find([ops], *rs, filter_=False, all_keys=True)

    return GroupKeys.group_keys(ret_num={}, source=ret, reqs=reqs, all_keys=True)

def get_ready_rps_lcs(ops):
    '''Get ready RPs/LCs from platform ops'''
    
    reqs = [['slot', 'rp', '(?P<rp>.*)',
             'state', '(?P<state>ok, active|ok, standby|Ready)'],
            # ['slot', 'lc', '(?P<lc>.*)','state', 'ok'],
            ['slot', 'oc', '(?P<oc>.*)', 'state',
             '(?P<oc_state>ok, active|ok, standby|ok|ps, fail)']]

    rs = [R(i) for i in reqs]
    ret = find([ops], *rs, filter_=False, all_keys=True)
    return GroupKeys.group_keys(ret_num={}, source=ret,
                                reqs=reqs, all_keys=True)

def check_regexp_uptime(log_output, expect_uptime, pre_time, tolerance=0.5):
    '''Get the uptime by given regexp from the routers show logging, 
    and compare them with the given expected uptime.'''

    # create table info for Neighbors
    log.info(banner('Calculate Method for "tolerance check" is below:\n'
        '|a - b| <= 0.5 * (a + b) * tolerance'))

    # create table headers
    table = ptable(['log pattern', 'expected time', 'actual time', 'tolerance check', 'result'])

    # initial
    flag = True

    # check feature uptime
    # setup the regexp pattern
    p = r'.+ +(?P<uptime>\d+\:\d+\:\d+).\d+.+{}.+'

    for item in (expect_uptime or []):
        for regexp, expect_up in item.items():

            # *Dec  6 11:51:37.043: %OSPF-5-ADJCHG: Process 1, Nbr 10.2.2.2 on GigabitEthernet3 from LOADING to FULL, Loading Done
            pattern = re.compile(p.format(regexp))

            # find all the matched value
            uptimes = pattern.findall(log_output)

            # find the lastest one
            try:
                assert uptimes
            except Exception as e:
                raise AssertionError('Cannot find log message for {}'.format(regexp)) from e
            else:
                latest_uptime = list(uptimes)[-1]

            # calculate the time slot it takes to reach ready
            start = pre_time.split(':')
            start = int(start[0]) * 3600 + int(start[1]) * 60 + int(start[2])
            end = latest_uptime.split(':')
            end = int(end[0]) * 3600 + int(end[1]) * 60 + int(end[2])

            # get real uptime
            time_consume = end - start
            
            # calculate the Equation left and right sides
            equal_left = abs(time_consume - expect_up)
            equal_right = 0.5 * tolerance * (time_consume + expect_up)

            # check uptime
            try:
                # calculate to see if the real time consuming is clased to the expect number
                assert equal_left <= equal_right
            except Exception:
                flag = False
                table.add_row([regexp, expect_up, time_consume, '{} <= {}'.format(equal_left, equal_right), 'Failed' ] )
            else:
                table.add_row([regexp, expect_up, time_consume, '{} <= {}'.format(equal_left, equal_right), 'Passed' ]  )

    table_str = table.get_string()
    log.info('\n{}'.format(banner('Overall Information', width=len(table._hrule))))
    log.info(table_str)

    if not flag:
      raise Exception('Not all the regexps uptime are closed to the ones given from trigger yaml file. \n'
        'Please refer the table to see if anything needs to be adjusted from trigger yaml file')

def set_filetransfer_attributes(self, device, fileutil):
    """ Used for certain triggers like TriggerIssu when ran from run_genie_sdk
    as some setup for that trigger is normally done in the configure subsection.
    """

    testbed = device.testbed

    if (hasattr(self, 'parent') and
            hasattr(self.parent, 'filetransfer_protocol') and
            self.parent.filetransfer_protocol):
        protocol = self.parent.filetransfer_protocol
    else:
        protocol = None

    if not hasattr(testbed, 'servers'):
        raise Exception("No servers have been defined in the testbed yaml")

    address = None

    if protocol:
        if protocol not in testbed.servers:
            raise Exception("The protocol '{}' is not provided in the "
                            "testbed.servers block".format(protocol))

        if not hasattr(testbed.servers[protocol], 'address'):
            raise Exception("There was no 'address' provided under the '{}' "
                            "server in the testbed.servers block".format(protocol))

        address = testbed.servers[protocol].address
    else:
        # no user provided protocol provided. Grab any suitable one.
        for server in testbed.servers:
            if not hasattr(testbed.servers[server], 'address'):
                continue

            address = testbed.servers[server].address
            protocol = server
            break

    device.filetransfer = fileutil
    device.filetransfer_attributes = {}
    device.filetransfer_attributes['server_address'] = address
    device.filetransfer_attributes['protocol'] = protocol
    device.filetransfer_attributes['path'] = \
        testbed.servers[protocol].get('path')
    device.filetransfer_attributes['credentials'] = \
        testbed.servers[protocol].get('credentials')