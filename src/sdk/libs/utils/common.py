'''Those are normalized functions that could be used in all platforms'''

# Python
import re
import random
import logging
from enum import Enum
from copy import deepcopy
from ipaddress import _BaseAddress
from collections import defaultdict, Iterable

# import genie
from genie.utils.diff import Diff
from genie.conf.base.attributes import SubAttributesDict

# import ats
from ats.utils.objects import find, R, Operator

# Genie Libs
from genie.libs.conf.base.neighbor import Neighbor

# module logger
log = logging.getLogger(__name__)


class UpdateLearntDatabase(object):
    """Class to update local/global verifications and PTS"""

    def __init__(self, obj, device):
        """built-in __init__

        instantiates each update actions.

        Arguments
        ---------
            device (`obj`): Device object
        """
        self.device = device
        self.obj = obj

    def update_verification(self, abstract, update_ver_list):
        '''Learn the verifications from the given list and
        overwrite it into local and global verifications.

       Args:
          Mandatory:
            abstract (`obj`): Abstract object
            update_ver_list (`list`) : Verifications that want to be updatd

       Returns:
           None

       Raises:
           None

       Example:
           >>> update_obj = UpdateLearntDatabase(object)
           >>> update_obj.update_verification(
                   abstract=abstract,
                   update_ver_list=['Verify_Module', 'Verify_RedundancyStatus'])
        '''
        if self.obj.parent.verifications:
            for ver in update_ver_list:
                # skip updating verification for the ones
                # not in the previous learned list
                if ver not in self.obj.parent.verifications:
                    log.warning('Verification {} was not supported'
                            .format(ver))
                    continue

                # Check if verificaiton is parser, callable or Ops
                if 'cmd' in self.obj.parent.verifications[ver]:
                    # compose the command object
                    execute_obj = abstract.parser
                    for item in self.obj.parent.verifications[ver]['cmd']['class'].split('.'):
                        execute_obj = getattr(execute_obj, item)
                    execute_obj = execute_obj(self.device)
                elif 'source' in self.obj.parent.verifications[ver]:
                    # compose the source object
                    execute_obj = abstract
                    for item in self.obj.parent.verifications[ver]['source']['class'].split('.'):
                        execute_obj = getattr(execute_obj, item)
                    execute_obj = execute_obj(self.device)
                else:
                    # no source execute command valid
                    continue

                # parser update
                if hasattr(execute_obj, 'parse'):
                    # check if has parameters
                    if 'parameters' in self.obj.parent.verifications[ver]:
                        para = self.obj.parent.verifications[ver]['parameters']
                    else:
                        para = {}
                    try:
                        parser_output = execute_obj.parse(**para)
                    except Exception as e:
                        log.warning(
                            'Local verification "{}" cannot be updated'.format(ver))
                        log.warning(str(e))
                        continue
                else:
                    # initial parser_output
                    parser_output = None

                # Ops update
                if hasattr(execute_obj, 'learn'):
                    try:
                        execute_obj.learn()
                    except Exception as e:
                        # ignore when the output is empty
                        log.warning(
                            'Local verification "{}" cannot be updated'.format(ver))
                        log.warning(str(e))
                        continue

                # Callable update
                # TODO
                    
                # update local verififations
                if self.obj.verf and self.device.name in self.obj.verf and \
                   self.obj.verf[self.device.name] and \
                   ver in self.obj.verf[self.device.name]:
                    if parser_output:
                        self.obj.verf[self.device.name][ver].name = parser_output
                    elif isinstance(execute_obj, object):
                        self.obj.verf[self.device.name][ver] = execute_obj
                else:
                    log.warning('Local verification "{v}" is '
                        'not learned before on device {d}, Skip updating local'
                        .format(v=ver, d=self.device.name))

                # update global verififations
                if self.device.name in self.obj.parent.verf and \
                   self.obj.parent.verf[self.device.name] and \
                   ver in self.obj.parent.verf[self.device.name]:
                    if parser_output:
                        self.obj.parent.verf[self.device.name][ver].name = parser_output
                    elif isinstance(execute_obj, object):
                        self.obj.parent.verf[self.device.name][ver] = execute_obj
                else:
                    log.warning('Global verification "{v}" is '
                        'not learned before on device {d}, Skip updating global'
                        .format(v=ver, d=self.device.name))


    def update_pts(self, abstract, update_feature_list, update_attributes=None):
        '''Learn the verifications from the given list and
        overwrite it into local and global verifications.

       Args:
          Mandatory:
            abstract (`obj`): Abstract object
            update_feature_list (`list`) : Features of the PTSs
                                           that want to be updatd
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
           >>> update_obj = UpdateLearntDatabase(object)
           >>> update_obj.update_verification(
                   abstract=abstract,
                   update_feature_list=['platform', 'bgp'],
                   update_attributes={'bgp': ['info'],
                                      'platform': ['chassis_sn', 'slot']})
        '''
        # update pts
        if 'pts' in self.obj.parent.parameters:
            for feature in update_feature_list:
                if feature not in self.obj.parent.parameters['pts']:
                    log.warning(
                        'Feature {} was not learned before, Skip updating'
                        .format(feature))
                    continue
                   
                log.info("Update {f} pts on {d}".format(f=feature, d=self.device))

                # check if pts runs on this device before
                if self.device.alias in self.obj.parent.parameters['pts'][feature]:

                    # learn the ops again
                    try:
                        module = self.obj.parent.parameters['pts'][feature][self.device.alias]\
                            .__class__(self.device)
                        module.learn()
                    except Exception as e:
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
                            pass
                else:
                    log.warning(
                        'Feature {f} was not learned on {d} before, Skip updating'
                        .format(f=feature, d=self.device))

        else:
            log.info('There is no PTS learned previously, Skip updating the PTS')


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
