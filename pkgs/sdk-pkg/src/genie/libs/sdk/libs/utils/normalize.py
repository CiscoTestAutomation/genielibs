'''THis is normalized functions could be used in all platforms'''

# Python
import re
import random
import logging
from enum import Enum
from copy import deepcopy
from ipaddress import _BaseAddress
from collections import defaultdict
from collections.abc import Iterable

# import genie
from genie.utils.diff import Diff
from genie.conf.base.attributes import SubAttributesDict
from genie.conf.base.base import ConfigurableBase

from genie.libs.conf.base.neighbor import Neighbor

# import pyats
from pyats.utils.objects import find, R, Operator

log = logging.getLogger(__name__)


class GroupKeys():
    ''' Compose the dict which contains the headers as keys, and values
          from the source corresponding keys
    '''

    @classmethod
    def group_keys(cls, source, reqs, ret_num=None, all_keys=False):
        ''' Compose the dict which contains the headers as keys, and values
            from the source corresponding keys

            Args:
              Mandatory:
              (At least one of source and source_func should be defined.
               Build the dict from source if both of them are defined.)
                source (`list`) : Function pyats.utils.objects.find output.
                headers (`list`) : Keys from the find output, use this as
                                   headers in the table.
                reqs (`list`) : List of requirements.

            Returns:
                dict - Dictionary with the keys from args, format will be like
                {key1: [value1, value2], key2: [value1, value2]}
                empty - Empty dict


            Raises:
                None

            Example:
                >>> group_keys(source = \
                                  [('Established', ['instance', 'default',
                                    'vrf', 'default', 'neighbor',
                                    '192.168.4.1', 'session_state']),
                                    ('Established', ['instance', 'default',
                                     'vrf', 'default', 'neighbor',
                                     '2001:db8:4:1::1:1', 'session_state'])],
                               headers = ['neighbor', 'vrf', 'instance'])

                >>> {'vrf': ['default', 'default'],
                     'instance': ['default', 'default'],
                     'neighbor': ['192.168.4.1', '2001:db8:4:1::1:1']}

        '''

        temp_ret = []
        counter = {}
        # Get the source output ready
        # nest one level deeper for not all_keys find result
        # TODO: Not great, to be removed
        if not all_keys or not isinstance(source[0], list):
            source = [source]
        # Place value as part of the list
        # [(5, [x,y,w])] -> [[x,y,w,5]]

        # all_keys=True returns matching values to all
        # requirements in the following format:
        # [[('a', ['info','instance','vrf','100','neighbor']),
        #   ('b', ['info','instance','vrf','100','neighbor'])]]
        # [['info','instance','vrf','10','neighbor','a'],
        #  ['info','instance','vrf','10','neighbor','b']]

        # all_keys=False returns value of initial requirement in
        # the following format:
        # [('a', ['info','instance','vrf','100','neighbor'])]
        # [['info','instance','vrf','10','neighbor','a']]
        sources = []
        for item in source:
            temp_source = []
            for i in item:
                temp_source.extend([i[1] + [i[0]]])
            sources.append(temp_source)

        # For each requirement, will have different source
        if not all_keys:
            for source, found_req in zip(sources, reqs):
                # Each req can have multiple path 
                for found_path in source:
                    # pairing found path with its requirement path
                    ret_source = {}
                    # Go for each item on the path and see if it match with req
                    for item, req in zip(found_path, found_req):
                        # find operator has overrided __eq__, have to check type
                        is_find_operator = isinstance(req, Operator) and req.regex
                        # continue if source equals to any requirement path item
                        if not is_find_operator and item == req:
                            continue

                        # check if it's type of formatted regex
                        if isinstance(req, str) and req.startswith('(?P<'):
                            try:
                                com = re.compile(req)
                            except Exception as e:
                                raise ValueError("'{v}' is not a valid regex "
                                                 "expression".format(v=found_path)) from e
                        # check if it's type of find.operator
                        elif is_find_operator and req.value.startswith('(?P<'):
                            com = req.regex
                        # none of above, move on
                        else:
                            continue

                        # Get the variable name
                        var = list(com.groupindex)[0]
                        ret_source[var] = item

                    temp_ret.append(ret_source)
        else:
            for source, found_req in zip(sources, reqs):
                temp_dict = []
                for sour in sorted(source):
                    # pairing found path with its requirement path
                    ret_source = {}
                    # Go for each item on the path and see if it match with req
                    for item, req in zip(sour, found_req):
                        # find operator has overrided __eq__, have to check type
                        is_find_operator = isinstance(req, Operator) and req.regex
                        # continue if source equals to any requirement path item
                        if not is_find_operator and item == req:
                            continue

                        # check if it's type of formatted regex
                        if isinstance(req, str) and req.startswith('(?P<'):
                            try:
                                com = re.compile(req)
                            except Exception as e:
                                raise ValueError("'{v}' is not a valid regex "
                                                 "expression".format(v=sour)) from e
                        # check if it's type of find.operator
                        elif is_find_operator and req.value.startswith('(?P<'):
                            com = req.regex
                        # none of above, move on
                        else:
                            continue

                        # Get the variable name
                        # It's possible the regex has multiple group
                        matched = com.match(str(item))
                        original_type = type(item)
                        if matched:
                            origin_type = type(item)
                            for k, v in matched.groupdict().items():
                                # If issue with type, we can use ast.literal_eval. 
                                # But its not recommended, so trying with type first
                                ret_source[k] = origin_type(v)
                        else:
                            # I don't understand how it could
                            # go here; so raise an exception
                            raise Exception('{item} does not match {req}'\
                                            .format(item=item, req=req))
                    temp_dict = cls.merge_all_keys(temp_ret, temp_dict, ret_source)

                temp_ret = temp_dict.copy()

            return temp_ret

        ret = []
        for temp in temp_ret:
            for k in temp:
                # Make sure we have not reached our limit of those specific keys
                try:
                    if get_length_counter(counter[k], ret_num, k) >= \
                                      int(get_num_value(ret_num[k])) and \
                                                      temp[k] not in counter[k]:
                        break
                except ValueError:
                    # Then str > int
                    # Check if counter[k] is 'all'
                    # If so, all good
                    if get_num_value(ret_num[k]) != 'all':
                        break
                except KeyError:
                    # Either not in counter, or not in ret_num.
                    # In either case, it means its good to go
                    counter.setdefault(k, []).append(get_reduced_value(temp[k],
                                                                       ret_num,
                                                                       k))
            else:
                # reduce the value if there is any to be reduced
                ret_dict = { k: get_reduced_value(temp[k], ret_num, k) \
                                                            for k in temp }
                ret.append(ret_dict)

        return ret

    @classmethod
    def max_amount(cls, temp_ret, ret_num):
        ret = []
        counter = {}
        for temp in temp_ret:
            for k in temp:
                # Make sure we have not reached our limit of those specific keys
                try:
                    if get_length_counter(counter[k], ret_num, k) >= \
                                      int(get_num_value(ret_num[k])) and \
                                                      temp[k] not in counter[k]:
                        break
                except ValueError:
                    # Then str > int
                    # Check if counter[k] is 'all'
                    # If so, all good
                    if get_num_value(ret_num[k]) != 'all':
                        break
                except KeyError:
                    # Either not in counter, or not in ret_num.
                    # In either case, it means its good to go
                    counter.setdefault(k, []).append(get_reduced_value(temp[k],
                                                                       ret_num,
                                                                       k))
            else:
                # reduce the value if there is any to be reduced
                ret_dict = { k: get_reduced_value(temp[k], ret_num, k) \
                                                            for k in temp }
                ret.append(ret_dict)
        return ret

    @classmethod
    def merge_all_keys(cls, temp_ret, temp_dict, ret_source):
        # Merge all the keys into a group keys that make sense
        # This code...is not optimal

        temp_ret = deepcopy(temp_ret)
        #temp_dict = []
        # temp_ret = previous requirements found information
        skip = {}
        found = False
        for temp in temp_ret:
            temp_found = False
            temp_values = {}

            # Evaluate how many are needed here.
            for key, value in ret_source.items():
                # Convert obj to string
                if isinstance(value, Neighbor):
                    value = value.ip.compressed
                elif isinstance(value, Enum):
                    value = value.value
                elif isinstance(value, _BaseAddress):
                    value = value.compressed

                if key in temp:
                    if temp[key] == value or (isinstance(value, Iterable) and temp[key] in value):
                        if key in skip:
                            del skip[key]
                        continue
                    # This mean this ret_source does not respect
                    # an existing key, but it could respect from another
                    # temp_ret.
                    # So keep in memory
                    # Dict so its faster
                    skip[key] = False
                    break

                # Key does not exists
                temp_values[key] = value
                continue
            else:
                # Good found a match
                temp_found = found = True
                if temp_values:
                    if temp in temp_dict:
                        temp_dict.remove(temp)
                    temp.update(temp_values)
            if temp not in temp_dict and temp_found:
                # Temp was not found
                temp_dict.append(temp)

        # Make sure no value was still in skip.  If so, do not add
        if not skip and not found and ret_source not in temp_dict:
            temp_dict.append(ret_source)

        return temp_dict

def get_num_value(ret_num, key='num', default='all'):
    ''' get num_value information '''
    if isinstance(ret_num, str):
        return ret_num.lower()
    # if it's dictionary, go one level deeper
    if isinstance(ret_num, dict):
        return get_num_value(ret_num.get(key, default))

    return ret_num

def get_reduced_value(ret_value, ret_num, k):
    ''' get reduced value based on exclude and limit '''
    ret_num = ret_num.get(k, None)
    if isinstance(ret_num, dict) and \
             not isinstance(ret_value, str) and isinstance(ret_value, Iterable):
        # get num_values limit
        limit = ret_num.get('num', None)
        try:
            if isinstance(limit, str) and limit.lower() == 'all':
                limit = None
            else:
                limit = int(limit)
        except Exception:
            limit = None
        # remove items in excluded list
        exclude = ret_num.get('exclude', [])
        ret_value = [ v for v in ret_value if v not in exclude ]
        if limit:
            # reduced the size to limit
            ret_value = ret_value[:limit]

    return ret_value

def get_length_counter(counter_value, ret_num, k):
    ''' get reduced value based on exclude and limit '''
    ret_num = ret_num.get(k, None)
    if isinstance(ret_num, dict):
        # flat the counter list for dictionary num_value config
        flat_list = []
        for sublist in counter_value:
            if not isinstance(sublist, str) and isinstance(sublist, Iterable):
                flat_list = flat_list + sublist
                continue
            flat_list.append(sublist)
        # remove duplicates
        counter_value = set(flat_list)

    return len(counter_value)

# will move to genie.utils.cisco_collections from genie.metaparser
def merge_dict(dic_result, dic, path=None, update=False):
    """ Method merges dic into dic_result

    Args:
        dic_result: the dict will be returned.
        dic ('dict'): the dict used to merge with dict_result.
        path (`list`): internal variable for keeping track of stack.

    Examples:
        >>> merge_dict({'province': {'city': 'ottawa'}},
        ...            {'province': {'county': 'kanata'}})

    Returns: {'province': {'county': 'kanata', 'city': 'ottawa'}}
    """
    if path is None:
        path = []
    for key in dic:
        if key in dic_result:
            if isinstance(dic_result[key], dict) and isinstance(dic[key], dict):
                merge_dict(dic_result[key], dic[key], path + [str(key)], update=update)
            elif isinstance(dic_result[key], str) and isinstance(dic[key], str):
                dic_result[key] = dic[key]
            elif dic_result[key] == dic[key]:
                # same leaf value
                pass
            elif update:
                dic_result[key] = dic[key]
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            dic_result[key] = dic[key]
    return dic_result


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

def _to_dict(conf_obj, value=None):
    ret = {}
    for k, value in conf_obj.__dict__.items():
        # Disregard those, as cannot be compared between
        # run
        base = ConfigurableBase()
        k = base._convert(conf_obj, k)

        if isinstance(value, SubAttributesDict):
            # Its already a dict
            ret[k] = {}
            for k2, v2 in value.items():
                # Loop over the returned conf and substitute the objects with
                # their corresponding values
                k2 = _convert_obj_to_value(k2)
                ret[k][k2] = _to_dict(v2)
        else:
            # Loop over the returned conf and substitute the objects with their
            # corresponding values
            value = _convert_obj_to_value(value)
            ret[k] = value
    return ret

def _convert_obj_to_value(value):
    if isinstance(value, Neighbor):
        value = value.ip.compressed
    elif isinstance(value, Enum):
        value = value.value
    elif isinstance(value, _BaseAddress):
        value = value.compressed
    return value
