'''IOSXE Specific implementation of checkcommands'''

import time
import logging

# import ats
from ats.utils.objects import find, R

# genie.libs
from genie.libs.sdk.libs.utils.normalize import GroupKeys


# from genie.utils.timeout import TempResult

log = logging.getLogger(__name__)


def get_requirements(requirements, output):
    '''get values which match the requirements from the output,
    and return them into dictonary

    Args:
      Mandatory:
        requirements (`dict`) : Dictionary which contains the list of requirements.
        output (`dict`) : Parser output.

    Returns:
        Dictionary contains the matched vavlues.


    Raises:
        None

    Example:
        >>> get_requirements(
            requirements = {
                'active': 
                   [['switch', 'stack', '(?P<stack>.*)','role', 'active'],
                    ['switch', 'stack', '(?P<stack>.*)','state', 'ready']],
                  'standby': 
                   [['switch', 'stack', '(?P<stack>.*)','role', 'standby'],
                    ['switch', 'stack', '(?P<stack>.*)','state', 'ready']],
                  'member': 
                   [['switch', 'stack', '(?P<stack>.*)','role', 'member'],
                    ['switch', 'stack', '(?P<stack>.*)','state', 'ready']]
            },
            output = {'switch': {
                'mac_persistency_wait_time': 'indefinite',
                'mac_address': '0057.d228.1a00',
                'stack': {'4': {'state': 'ready', 'role': 'member',
                                'ports': {'2': {'stack_port_status': 'ok',
                                               'neighbors_num': 2},
                                          '1': {'stack_port_status': 'ok',
                                                'neighbors_num': 3}},
                                'mac_address': '0057.d268.df80',
                                'hw_ver': 'V04', 'priority': '1'},
                          '5': {'state': 'ready', 'role': 'standby',
                                'ports': {'2': {'stack_port_status': 'ok',
                                                'neighbors_num': 1},
                                          '1': {'stack_port_status': 'ok',
                                                'neighbors_num': 2}},
                                'mac_address': '0057.d21b.cd80',
                                'hw_ver': 'V04', 'priority': '1'},
                          '2': {'state': 'ready', 'role': 'member',
                                'ports': {'2': {'stack_port_status': 'ok',
                                                'neighbors_num': 5},
                                          '1': {'stack_port_status': 'ok',
                                                'neighbors_num': 4}},
                                'mac_address': '0057.d283.8a00',
                                'hw_ver': 'V04', 'priority': '1'},
                          '1': {'state': 'ready', 'role': 'member',
                                'ports': {'2': {'stack_port_status': 'ok',
                                                'neighbors_num': 3},
                                          '1': {'stack_port_status': 'ok',
                                                'neighbors_num': 5}},
                                'mac_address': '0057.d228.1a00',
                                'hw_ver': 'V01', 'priority': '3'},
                          '3': {'state': 'ready', 'role': 'active',
                                'ports': {'2': {'stack_port_status': 'ok',
                                                'neighbors_num': 4},
                                          '1': {'stack_port_status': 'ok',
                                                'neighbors_num': 1}},
                                'mac_address': '0057.d21b.c800',
                                'hw_ver': 'V04', 'priority': '1'}}}})
        >>> {'active': [{'stack': '3'}],
             'standby': [{'stack': '5'}],
             'member': [{'stack': '1'}, {'stack': '2'}, {'stack': '4'}]}
    '''
    ret_dict = {}
    for key, item in requirements.items():
        rs = [R(path) for path in item]
        ret = find([output], *rs, filter_=False, all_keys=True)
        if ret:
            values = GroupKeys.group_keys(reqs=item,
                                          ret_num={},
                                          source=ret,
                                          all_keys=True)
        else:
            raise Exception('Cannot learn requirement: {}'.format(requirements))
        ret_dict.update({key: values}) if values else None
    return ret_dict

def verify_requirements(keys_dict, reqs, full_stack='', raise_exception=True):
    '''Verify if values from keys_dict match the requirements 
    for each number from full_stack

    Args:
      Mandatory:
        keys_dict (`dict`): dict of values which get from get_requirements.
        reqs (`dict`) : Dictionary which contains the list of requirements.
        full_stack (`list`) : List of switch members
        raise_exception (`bool`) : True if neeed to raise the Exception
                                   when values are not exsits or not matching
                                   False if Not need to raise the Exception
                                   when values are not exsits or not matching
                                   Default: True

    Returns:
        None


    Raises:
        KeyError: Lack of required values

    Example:
        >>> verify_requirements(
            requirements = {
                'active': 
                   [['switch', 'stack', '(?P<stack>.*)','role', 'active'],
                    ['switch', 'stack', '(?P<stack>.*)','state', 'ready']],
                  'standby': 
                   [['switch', 'stack', '(?P<stack>.*)','role', 'standby'],
                    ['switch', 'stack', '(?P<stack>.*)','state', 'ready']],
                  'member': 
                   [['switch', 'stack', '(?P<stack>.*)','role', 'member'],
                    ['switch', 'stack', '(?P<stack>.*)','state', 'ready']]
            },
            keys_dict = {'active': [{'stack': '3'}],
             'standby': [{'stack': '5'}],
             'member': [{'stack': '1'}, {'stack': '2'}, {'stack': '4'}]},
            full_stack = ['1', '2', '3', '4', '5'])
    '''
    if full_stack:
        for switch in full_stack:
            for key in reqs.keys():
                key_dict = keys_dict.get(key, {})
                if not key_dict:
                    raise KeyError('{} info is not exists in any Models'.format(key)) \
                        if raise_exception else None
                for item in key_dict:
                    if switch not in item['stack']:
                        continue
                    # compose the message
                    msg = 'switch {}'.format(switch)
                    for msg_key in item:
                        if msg_key not in ['stack', key]:
                            msg += ' {k} {v}'.format(k=msg_key, v=item[msg_key])
                    try:
                        log.info('    {m}: {k} is {v}'.format(m=msg, v=item[key], k=key))
                    except Exception:
                        raise KeyError('{m} does not have "{k}" '
                            'values'.format(m=msg, k=key)) \
                                if raise_exception else None
    else:            
        for key in reqs.keys():
            key_dict = keys_dict.get(key, {})
            if not key_dict:
                raise KeyError('{k} status is not up and ready'
                    '\nrequirements: {r}'.format(kkey, r=reqs)) \
                        if raise_exception else None
            for item in key_dict:
                try:
                    log.info('    System {k}: {v}'.format(k=key, v=item[key]))
                except Exception:
                    raise KeyError('{k} status is not up and ready'
                        '\nrequirements: {r}'.format(kkey, r=reqs)) \
                            if raise_exception else None

def verify_switches(keys_dict, full_stack):
    '''Verify if all switches from full_stack is Ready

    Args:
      Mandatory:
        keys_dict (`dict`): dict of values which get from get_requirements.
        full_stack (`list`) : List of switch members

    Returns:
        None


    Raises:
        KeyError: Lack of required values

    Example:
        >>> verify_switches(
            keys_dict = {'active': [{'stack': '3'}],
             'standby': [{'stack': '5'}],
             'member': [{'stack': '1'}, {'stack': '2'}, {'stack': '4'}]},
            full_stack = ['1', '2', '3', '4', '5'])
    '''
    # get full stacks number
    get_stacks = []
    info = []

    # check active
    if 'active' in keys_dict:
        actives = [item.get('stack') for item in keys_dict['active']]
        if len(actives) > 1:
            raise KeyError('Two Active RPs found')
        get_stacks.extend(actives)
        info.extend(['node{} is in Active mode'.format(i) for i in actives])
    else:
        raise KeyError('Active switch is not existed')

    # check standby
    if 'standby' in keys_dict:
        standbys = [item.get('stack') for item in keys_dict['standby']]
        if len(standbys) > 1:
            raise KeyError('Two standby RPs found')
        get_stacks.extend(standbys)
        info.extend(['node{} is in Standby mode'.format(i) for i in standbys])
    else:
        log.warning('Standby switch is not existed')

    # check member
    if 'member' in keys_dict:
        members = [item.get('stack') for item in keys_dict['member']]
        get_stacks.extend(members)
        info.extend(['node{} is in Member mode'.format(i) for i in members])
    else:
        log.warning('Member switch is not existed')

    # Check if all stacks are up and ready
    get_stacks = sorted(get_stacks)
    mismatched = [i for i in full_stack if i not in get_stacks]
    if mismatched:
        raise KeyError('Switches {} are Not Ready'.format(mismatched))
    else:
        info.extend(['Expected full "Ready" stack is {}'.format(full_stack),
            'Get real full "Ready" stack is {}'.format(get_stacks)])
        log.info('\n'.join(info))
