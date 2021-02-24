"""Common verification functions for OSPF"""

# Python
import logging
from netaddr import IPAddress
import re
import operator

# pyATS
from pyats.utils.objects import find, R

# Genie
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.utils import Dq


log = logging.getLogger(__name__)


def verify_ospf_interface_cost(device,
                               interface,
                               expected_cost,
                               cost_type='ospf',
                               instance=None,
                               area=None,
                               max_time=60,
                               check_interval=15):
    """ Verifies ospf cost on interface

        Args:
            device ('obj'): device to use
            interface ('str'): Interface to use
            cost_type ('str'): Cost type configured
            expected_cost ('int'): Expected configured cost
            instance ('str'): Instance to use
            area ('str'): Area to use
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check

        Returns:
            True/False

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)

    if 'ospf' in cost_type.lower():
        while timeout.iterate():
            try:
                out = device.parse(
                    'show ospf interface {interface} detail'.format(
                        interface=interface))
            except SchemaEmptyParserError:
                log.info('Parser is empty')
                timeout.sleep()
                continue

            reqs = R([
                'instance', '{}'.format(instance if instance else 'master'),
                'areas', '{}'.format(area if area else '(.*)'), 'interfaces',
                interface, 'cost', '(?P<cost>.*)'
            ])

            found = find([out], reqs, filter_=False, all_keys=True)
            if found:
                keys = GroupKeys.group_keys(
                    reqs=reqs.args, ret_num={}, source=found, all_keys=True)
                if 'cost' in keys[0] and int(expected_cost) == int(
                        keys[0]['cost']):
                    return True

            timeout.sleep()
        return False
    elif 'te' in cost_type.lower():
        while timeout.iterate():
            try:
                out = device.parse('show interfaces {interface} terse'.format(
                    interface=interface))
            except SchemaEmptyParserError:
                log.info('Parser is empty')
                timeout.sleep()
                continue

            reqs = R([
                interface, 'protocol', 'inet', '(.*)', 'local', '(?P<local>.*)'
            ])

            found = find([out], reqs, filter_=False, all_keys=True)
            if found:
                keys = GroupKeys.group_keys(
                    reqs=reqs.args, ret_num={}, source=found, all_keys=True)
                local_address = keys[0].get('local')

                try:
                    out = device.parse('show ted database extensive')
                except SchemaEmptyParserError:
                    log.info('Parser is empty')
                    timeout.sleep()
                    continue

                reqs = R([
                    'node', '(.*)', 'protocol', '(.*)', 'to', '(.*)', 'local',
                    local_address.split('/')[0], 'remote', '(.*)', 'metric',
                    '(?P<metric>.*)'
                ])
                found = find([out], reqs, filter_=False, all_keys=True)
                if found:
                    keys = GroupKeys.group_keys(
                        reqs=reqs.args,
                        ret_num={},
                        source=found,
                        all_keys=True)
                    if 'metric' in keys[0] and int(expected_cost) == int(
                            keys[0]['metric']):
                        return True

            timeout.sleep()
        return False

    log.info('This api does not support cost type {}'.format(cost_type))


def verify_ospf_neighbor_state(device,
                               expected_state,
                               interface,
                               neighbor_address=None,
                               extensive=False,
                               max_time=60,
                               check_interval=10):
    """ Verifies state of ospf neighbor

        Args:
            device ('obj'): device to use
            expected_state ('str'): OSPF adjacency state that is expected
            interface ('str'): Name of interface
            neighbor_address ('str'): Neighbor address
            extensive ('bool'): If ospf command is extensive
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check

        Returns:
            True/False

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            if extensive:
                output = device.parse('show ospf neighbor extensive')
            else:
                output = device.parse('show ospf neighbor')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        #{'ospf-neighbor-information': {'ospf-neighbor': [{}]}}
        neighbors = output.q.get_values('ospf-neighbor')
        for neighbor in neighbors:
            #'interface-name': 'ge-0/0/0.0'
            #'ospf-neighbor-state': 'Full'
            if not neighbor_address:
                if neighbor.get('interface-name',[]) == interface and \
                neighbor.get('ospf-neighbor-state',[]).lower() == expected_state.lower():
                    return True
            else:
                if neighbor.get('neighbor-address',[]) == neighbor_address and \
                neighbor.get('ospf-neighbor-state',[]).lower() == expected_state.lower():
                    return True

        timeout.sleep()

    return False


def verify_no_ospf_neigbor_output(device,
                                  expected_interface=None,
                                  extensive=False,
                                  max_time=60,
                                  check_interval=10):
    """ Verifies ospf neighbor doesn't exists

        Args:
            device ('obj'): device to use
            expected_interface ('str'): Interface being searched for
            extensive ('bool'): If ospf command is extensive
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check

        Returns:
            True/False

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)
    exists = False

    while timeout.iterate():

        if extensive:
            try:
                output = device.parse('show ospf neighbor extensive')
            except SchemaEmptyParserError:
                output = None
                timeout.sleep()
                continue

        else:
            try:
                output = device.parse('show ospf neighbor')
            except SchemaEmptyParserError:
                output = None
                timeout.sleep()
                continue

        for neighbor in Dq(output).get_values('ospf-neighbor'):
            if neighbor.get('interface-name') == expected_interface:
                exists = True
                timeout.sleep()
                break
            else:
                exists = False

        timeout.sleep()


    if not output or not exists:
        return True
    else:
        return False


def verify_neighbor_state_went_down(device,
                                    interface,
                                    realm,
                                    fail_reason,
                                    max_time=60,
                                    check_interval=10):
    """ Verifies message in log

        Args:
            device ('obj'): device to use
            interface ('str'): Interface that went down
            realm ('str'): ospf/ospf3 realm
            fail_reason ('str'): Reason state changed from full to down
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check

        Returns:
            True/False

        Raises:
            N/A
    """
    regex_string1 = 'area +0.0.0.0\)) +state +'\
                    'changed +from +Full +to +Down +due +to +(?P<asdf>'
    regex_string2 = '[\s\S]+)$'
    temp = ('^(?P<ignored_portion>[\s\S]+)realm +(?P<interface>'
            '{realm} {interface} {regex_string1}{fail_reason}{regex_string2}'.
            format(
                realm=realm,
                interface=interface,
                regex_string1=regex_string1,
                regex_string2=regex_string2,
                fail_reason=fail_reason))

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        output = device.execute('show log messages')
        for line in output.splitlines():
            line = line.strip()

            m = re.match(temp, line)
            if m:
                return True
        timeout.sleep()

    return False


def verify_ospf_interface_type(device,
                               interface,
                               interface_type,
                               max_time=60,
                               check_interval=10):
    """ Verifies ospf interface type

        Args:
            device ('obj'): device to use
            interface ('str'): Interface to use
            interface_type ('str'): Interface type
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check

        Returns:
            True/False

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show ospf interface extensive')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        ##{'ospf-interface': [{'interface-name': 'ge-0/0/1.0'}]}
        for ospf_interface in out.q.get_values('ospf-interface'):

            #{'interface-name': 'ge-0/0/1.0'}
            intf = ospf_interface.get('interface-name', None)

            #{'interface-type': 'LAN'}
            intf_type = ospf_interface.get('interface-type', None)
            if intf == interface and intf_type == interface_type:
                return True
        timeout.sleep()
    return False


def verify_ospf_interface(device,
                          expected_interface=None,
                          expected_interface_type=None,
                          expected_state=None,
                          extensive=True,
                          max_time=60,
                          check_interval=10,
                          expected_hello_interval=None):
    """ Verifies ospf interface exists with criteria

        Args:
            device ('obj'): device to use
            expected_interface ('str'): Interface to use
            expected_interface_type ('str'): Interface type
            expected_state ('str'): Interface state
            extensive ('boolean'): Flag for extensive command
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check
            expected_hello_interval ('str'): Expected hello interval

        Returns:
            True/False

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        try:
            if extensive:
                out = device.parse('show ospf interface extensive')
            else:
                out = device.parse('show ospf interface')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # {
        # "ospf-interface-information": {
        #     "ospf-interface": [
        #         {
        #             "interface-name": "ge-0/0/0.0",
        #             "interface-type": "P2P",
        #             "ospf-interface-state": "PtToPt",
        #             "hello-interval": "100",
        #         },

        for ospf_interface in out.q.get_values('ospf-interface'):
            # check variables
            intf = ospf_interface.get('interface-name', None)
            if expected_interface and expected_interface != intf:
                continue

            intf_type = ospf_interface.get('interface-type', None)
            if expected_interface_type and expected_interface_type != intf_type:
                continue

            intf_state = ospf_interface.get('ospf-interface-state', None)
            if expected_state and expected_state != intf_state:
                continue

            intf_hello_interval = ospf_interface.get('hello-interval', None)
            if expected_hello_interval and str(expected_hello_interval) != intf_hello_interval:
                continue

            return True
        timeout.sleep()
    return False


def verify_ospf_neighbor_number(device,
                                expected_interface=None,
                                expected_number=None,
                                expected_state=None,
                                extensive=False,
                                max_time=60,
                                check_interval=10):
    """ Verifies the number of ospf neighbors that meets the criteria

        Args:
            device ('obj'): device to use
            expected_interface ('str'): Interface to use
            expected_number ('str'): State occurrence
            expected_state ('str'): Interface state
            extensive ('bool'): Flag to differentiate show commands
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check

        Returns:
            Boolean

        Raises:
            N/A
    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            if not extensive:
                out = device.parse("show ospf neighbor")
            else:
                out = device.parse("show ospf neighbor extensive")
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # {
        # "ospf3-neighbor-information": {
        #     "ospf3-neighbor": [
        #         {
        #             "interface-name": "ge-0/0/0.0",
        #             "ospf-neighbor-state": "Full"
        #         },

        count = 0
        for neighbor in out.q.get_values('ospf-neighbor'):
            # check variables

            interface_name = neighbor.get('interface-name', None)
            if expected_interface and expected_interface != interface_name:
                continue

            neighbor_state = neighbor.get('ospf-neighbor-state', None)
            if expected_state and expected_state.lower(
            ) != neighbor_state.lower():
                continue

            # if all variables exist, count plus 1
            count += 1

        if count == expected_number:
            return True

        timeout.sleep()

    return False


def verify_ospf_metric(device,
                       interface,
                       metric,
                       max_time=60,
                       check_interval=10):
    """Verify the OSPF metric

    Args:
        device (obj): Device object
        interface (str): Interface name
        metric (str): OSPF metric
    Returns:
        True/False
    Raises:
        N/A
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show ospf interface extensive')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example dictionary

        # "ospf-interface": [
        #         {
        #             "interface-name": "ge-0/0/0.0",
        #             "ospf-interface-topology": {
        #                 "ospf-topology-metric": "5",
        #             },
        #         },

        ospf_interface_list = Dq(out).get_values('ospf-interface')

        for ospf_interface_dict in ospf_interface_list:

            #{'interface-name': 'ge-0/0/1.0'}
            interface_ = Dq(ospf_interface_dict).get_values(
                'interface-name', 0)

            #{'ospf-topology-metric': '5'}
            metric_ = Dq(ospf_interface_dict).get_values(
                'ospf-topology-metric', 0)

            if interface_.lower() == interface.lower() and str(metric_) == str(
                    metric):
                return True
        timeout.sleep()
    return False


def verify_ospf_neighbors_found(device, extensive=False,
    max_time=90, check_interval=10, expected_interface=None, instance=None):
    """ Verifies ospf neighbors values exists

        Args:
            device ('obj'): device to use
            extensive ('str'): If to check with extensive command
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check
            expected_interface ('str'): Interface to check for
            instance ('str'): Instance to check for

        Returns:
            True/False

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            if instance:
                out = device.parse('show ospf neighbor instance {instance}'.format(
                    instance=instance
                ))
            elif extensive:
                out = device.parse('show ospf neighbor extensive')
            else:
                out = device.parse('show ospf neighbor')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        ospf_neighbors = out.q.get_values('ospf-neighbor')

        if expected_interface:
            if len([
                neighbor for neighbor in ospf_neighbors if neighbor.get('interface-name') == expected_interface
                ]) > 0:
                return True
            else:
                timeout.sleep()
                continue

        if len(ospf_neighbors) > 0:
            return True
        timeout.sleep()
    return False


def verify_ospf_neighbors_not_found(device, extensive=False,
    max_time=90, check_interval=10, expected_interface=None):
    """ Verifies ospf neighbors values don't exist

        Args:
            device ('obj'): device to use
            extensive ('str'): If to check with extensive command. Defaults to False
            max_time ('int'): Maximum time to keep checking. Defaults to 90
            check_interval ('int'): How often to check. Defaults to 10
            expected_interface ('str'): Interface to check for. Defaults to None

        Returns:
            True/False

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            if extensive:
                out = device.parse('show ospf neighbor extensive')
            else:
                out = device.parse('show ospf neighbor')
        except SchemaEmptyParserError:
            return True

        ospf_neighbors = out.q.get_values('ospf-neighbor')

        if expected_interface:
            if len([
                neighbor for neighbor in ospf_neighbors \
                    if neighbor.get('interface-name') == expected_interface
                ]) == 0:
                return True
            else:
                timeout.sleep()
                continue

        if len(ospf_neighbors) == 0:
            return True
        timeout.sleep()
    return False


def verify_ospf_overview(device, router_id=None, max_time=90, check_interval=10,
                          expected_configured_overload=None):
    """ Verifies ospf overview values

        Args:
            device ('obj'): device to use
            router_id ('str'): Router ID
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check
            expected_configured_overload ('str'/'int'): Configured overload time or * for any

        Returns:
            True/False

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show ospf overview')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        if router_id:
            router_id_ = out.q.contains_key_value('ospf-router-id',
                                                router_id,
                                                value_regex=True)
            if router_id_:
                return True

        if expected_configured_overload:
            configured_overload = out.q.get_values(
                'ospf-configured-overload-remaining-time', None)

            if configured_overload and expected_configured_overload == "*":
                return True
            
            if configured_overload:
                try:
                    if int(configured_overload) == int(expected_configured_overload):
                        return True
                except ValueError as e:
                    log.info("Non-integer value given")
                    raise

        timeout.sleep()
    return False


def verify_ospf_spf_delay(device,
                          expected_spf_delay=None,
                          max_time=60,
                          check_interval=10):
    """ Verify SPF delay

        Args:
            device('obj'): device to use
            expected_spf_delay('float'): SPF delay time
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check

        Returns:
            True/False


        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)            

    # show commands: "show ospf overview"
    while timeout.iterate():
        try:
            output = device.parse('show ospf overview')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        spf_delay = output.q.get_values('ospf-spf-delay', None)

        if spf_delay:
            spf_delay = float(spf_delay[0])

        if spf_delay == expected_spf_delay:
            return True

        timeout.sleep()
    return False      


def verify_ospf_interface_in_database(device,
                                      expected_interface,
                                      expected_interface_type=None,
                                      subnet_mask=None,
                                      expected_metric=None,
                                      adv_router=False,
                                      max_time=60,
                                      check_interval=10):
    """ Verifies ospf interface exists with criteria

        Args:
            device ('obj'): device to use
            expected_interface ('str'): Interface to use
            expected_interface_type ('str'): Interface type
            subnet_mask ('str'): Subnet mask
            expected_metric ('str'): Metric of Interface
            adv_router ('bool'): Whether to look for address in adversiting router
            max_time ('int', optional): Maximum time to keep checking. Defaults to 60 seconds.
            check_interval (`int`): Check interval, default: 10

        Returns:
            Boolean
        Raises:
            N/A
    """            
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show ospf database extensive')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue


        #'ospf-database':[
        #    {'lsa-type':
        #        'Router',
        #        'lsa-id': '1.1.1.1'
        #    }
        #]

        for ospf_database in Dq(out).get_values('ospf-database'):

            #'ospf-external-lsa':
            #   {'address-mask': '255.255.255.255',
            #   'ospf-external-lsa-topology': {
            #        'ospf-topology-name':
            #            'default'}}
            ospf_external_lsa = ospf_database.get('ospf-external-lsa',{})
            if not adv_router:
                if subnet_mask != None:
                    if 'address-mask' not in ospf_external_lsa:
                        continue
                    else:
                        #{'address-mask': '255.255.255.255'}
                        current_mask = IPAddress(ospf_external_lsa.get('address-mask')).netmask_bits()
                        if str(current_mask) != subnet_mask:
                            continue

                #'type-value': '2'
                if not ospf_external_lsa:
                    continue
                if not ospf_external_lsa.get('ospf-external-lsa-topology',{}):
                    continue
                if str(expected_metric) != ospf_external_lsa.get('ospf-external-lsa-topology',{}).get('type-value',{}):
                    continue

                if expected_interface_type != None:
                    #'lsa-type': 'Extern'
                    lsa_type = ospf_database.get('lsa-type', None)
                    lsa_type = lsa_type.lower() if lsa_type else lsa_type

                    if expected_interface_type.lower() != lsa_type:
                            continue

                #'lsa-id': '11.11.11.11'
                lsa_id = ospf_database.get('lsa-id', None)
                if expected_interface != lsa_id:
                    continue
            else:
                advertising_router = ospf_database.get('advertising-router', None)
                if expected_interface != advertising_router:
                    continue

            return True

        timeout.sleep()

    return False

def verify_ospf_advertising_router_metric_in_database(device,
                                      lsa_id,
                                      ospf_link_id,
                                      expected_metric,
                                      max_time=60,
                                      check_interval=10):
    """ Verifies ospf advertising router metric in database

        Args:
            device ('obj'): Device to use
            lsa_id: lsa_id to check
            ospf_link_id ('str'): Ospf link id to check
            expected_metric ('str'): Metric of desired ospf link
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check

        Returns:
            Boolean
        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            cmd = 'show ospf database advertising-router {ipaddress} extensive'.format(
                ipaddress=lsa_id)
            out = device.parse(cmd)
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example output:
        # {
        #     "ospf-database-information": {
        #         "ospf-database": [
        #             {
        #                 "ospf-router-lsa": {
        #                     "ospf-link": [
        #                         {
        #                             "link-id": "106.187.14.240",
        #                             "metric": "1"
        #                         }]}}]}}


        for ospf_database in out.q.get_values('ospf-database'):
            ospf_links = Dq(ospf_database).get_values('ospf-link')
            for ospf_link in ospf_links:
                if ospf_link.get('link-id', None) == ospf_link_id \
                        and ospf_link.get('metric', None) == str(expected_metric):
                    return True

        timeout.sleep()

    return False

def verify_no_ospf_interface_in_database(device,
                                         expected_interface,
                                         max_time=60,
                                         check_interval=10):
    """ Verifies ospf interface exists with criteria

        Args:
            device ('obj'): device to use
            expected_interface ('str'): Interface to use
            max_time ('int', optional): Maximum time to keep checking. Defaults to 60 seconds.
            check_interval (`int`): Check interval, default: 10

        Returns:
            Boolean

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        exist = False
        try:
            out = device.parse('show ospf database extensive')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        

        #'ospf-database':[
        #    {'lsa-type': 
        #        'Router', 
        #        'lsa-id': '1.1.1.1'
        #    }
        #]

        for ospf_database in Dq(out).get_values('ospf-database'):
            
            #'ospf-external-lsa': 
            #   {'address-mask': '255.255.255.255', 
            #   'ospf-external-lsa-topology': {
            #        'ospf-topology-name': 
            #            'default'}}
            ospf_external_lsa = ospf_database.get('ospf-external-lsa',{})

            advertising_router = ospf_database.get('advertising-router', None)
            if expected_interface == advertising_router:
                exist = True
        
        if exist:
            timeout.sleep()
            continue
        else:
            return False

    return True


def verify_ospf_database_lsa_id(device,
                                lsa_id,
                                max_time=60,
                                check_interval=10,
                                expected_node_id=None):
    """Verify 'show ospf database lsa-id {lsa_id}' against criteria

    Args:
        lsa_id ('str'): lsa_id to check
        max_time ('int'): Maximum time to keep checking
        check_interval ('int'): How often to check
        expected_node_id ('str'): Expected node ID to check for

    Raise: None

    Returns: Boolean

    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        try:
            out = device.parse(
                'show ospf database lsa-id {lsa_id} detail'.format(
                    lsa_id=lsa_id))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue


        if expected_node_id:
            node_ids_ = Dq(out).get_values('ospf-lsa-topology-link-node-id')
            if expected_node_id not in node_ids_:
                timeout.sleep()
                continue


        # add criteria to test against
        return True

    return False


def verify_show_ospf_database_lsa_types(device,
                                        expected_types,
                                        max_time=60,
                                        check_interval=10):
    """Verify 'show ospf database' lsa-types contains expected_types

    Args:
        device ('obj'): device to use
        expected_types ('str'): types to verify
        max_time ('int'): Maximum time to keep checking
        check_interval ('int'): How often to check

    Raise: None

    Returns: Boolean

    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        try:
            out = device.parse('show ospf database')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        found_types = out.q.get_values("lsa-type")

        verified = set(found_types).issuperset(set(expected_types))

        if verified:
            return True
        else:
            timeout.sleep()
            continue

    return False


def verify_show_ospf_route_network_extensive(device,
                                             expected_types,
                                             max_time=60,
                                             check_interval=10):
    """Verify 'show ospf database' lsa-types contains expected_types

    Args:
        device ('obj'): device to use
        expected_types ('str'): types to verify
        max_time ('int'): Maximum time to keep checking. Defaults to 60
        check_interval ('int'): How often to check. Defaults to 10

    Raise: None

    Returns: Boolean

    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        try:
            
            out = device.parse('show ospf database')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue


        found_types = out.q.get_values("lsa-type")

        if set(found_types).issuperset(set(expected_types)):
            return True
        else:
            timeout.sleep()
            continue

    return False


def verify_path_type(device,
                     expected_interface,
                     expected_path_type,
                     max_time=60,
                     check_interval=10):
    """Verify 'show ospf route network extensive'

    Args:
        device ('obj'): device to use
        expected_interface ('str'): address to verify
        expected_path_type ('str'): path to verify
        max_time ('int'): Maximum time to keep checking. Defaults to 60
        check_interval ('int'): How often to check. Defaults to 10

    Raise: None

    Returns: Boolean

    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        try:
            
            out = device.parse('show ospf route network extensive')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        #{'ospf-route-entry': 
        #   {'address-prefix': '1.1.1.1/32', 
        #                      'route-path-type': 'Intra', 'route-type': 'Network', 
        #                      'next-hop-type': 'IP', 'interface-cost': '0', 
        #                      'ospf-next-hop': {'next-hop-name': {'interface-name': 'lo0.0'}}, 
        #                      'ospf-area': '0.0.0.0', 
        #                      'route-origin': '1.1.1.1', 
        #                      'route-priority': 'low'
        #                       }
        #                       }
        ospf_route = Dq(out).get_values('ospf-route')
        
        for routes in ospf_route:
            
            #{'address-prefix': '1.1.1.1/32'}
            address_prefix = Dq(routes).get_values('address-prefix',0)
            if address_prefix and address_prefix != expected_interface:
                continue

            #{'route-path-type': 'Intra'}
            path_type = Dq(routes).get_values('route-path-type',0)
            if path_type and path_type.lower() != expected_path_type.lower():
                continue

            return True
        timeout.sleep()

    return False


def verify_ospf_router_id(device, ipaddress, expected_id,max_time=60,check_interval=10):

    """Verify 'show ospf database network lsa-id {ipaddress} detail' attached-router contains expected_id

    Args:
        device ('obj'): device to use
        expected_id ('str'): expected router id
        ipaddress ('str'): address to use in show command
        max_time ('int'): Maximum time to keep checking
        check_interval ('int'): How often to check

    Raise: None

    Returns: Boolean

    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        try:        
            out = device.parse(f'show ospf database network lsa-id {ipaddress} detail')   
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        if expected_id in out.q.get_values("attached-router"):           
            return True
        else:
            timeout.sleep()
            continue

    return False


def verify_ospf_no_router_id(device, ipaddress, expected_id,max_time=60,check_interval=10):

    """Verify 'show ospf database network lsa-id {ipaddress} detail' attached-router doesn't contain expected_id

    Args:
        device ('obj'): device to use
        expected_id ('str'): expected router id
        ipaddress ('str'): address to use in show command
        max_time ('int'): Maximum time to keep checking
        check_interval ('int'): How often to check

    Raise: None

    Returns: Boolean

    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        try:
            out = device.parse(f'show ospf database network lsa-id {ipaddress} detail')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        attached_router_list = out.q.get_values("attached-router")
        if expected_id not in attached_router_list:
            return True
        else:
            timeout.sleep()
            continue

    return False    


def verify_ospf_two_router_id(device, ipaddress, expected_id_1, expected_id_2, max_time=60,check_interval=10):

    """Verify 'show ospf database lsa-id ipaddress detail' contains expected_id_1 and expected_id_2

    Args:
        device ('obj'): device to use
        expected_id_1 ('str'): expected router id
        expected_id_2 ('str'): expected router id
        ipaddress ('str'): address to use in show command
        max_time ('int'): Maximum time to keep checking
        check_interval ('int'): How often to check            
    Raise: None

    Returns: Boolean

    """

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        try:        
            out = device.parse('show ospf database lsa-id {ipaddress} detail'.format(ipaddress=ipaddress))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue
        
        attached_router_list = out.q.get_values("attached-router")

        if (expected_id_1 in attached_router_list) and (expected_id_2 in attached_router_list):
            return True
        else:
            timeout.sleep()
            continue

    return False             


def verify_ospf_database(device, lsa_type=None, expected_lsa_id=None, 
                         max_time=60, check_interval=10, extensive=True, invert=False):
    """ Verifies information from show ospf database

    Args:
        device ([obj]): Device object
        lsa_type ([str], optional): LSA type to check. Defaults to None.
        expected_lsa_id ([str], optional): Expected LSA ID to find. Defaults to None.
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.
        extensive (bool, optional): Extensive or not. Default to True.
        invert (bool, optional): Inverts verification to check if criteria doesn't exist
    """

    op = operator.ne
    if invert:
        op = operator.eq

    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        out = None
        try:
            if extensive:
                if lsa_type:
                    out = device.parse('show ospf database {lsa_type} extensive'.format(
                        lsa_type=lsa_type.lower()
                    ))
                else:    
                    out = device.parse('show ospf database extensive')
            else:
                if lsa_type:
                    out = device.parse('show ospf database {lsa_type}'.format(
                        lsa_type=lsa_type.lower()
                    ))
                else:    
                    out = device.parse('show ospf database')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        count = 0

        ospf_database_ = out.q.get_values('ospf-database')
        for database in ospf_database_:
            if expected_lsa_id and op(expected_lsa_id.split('/')[0], database.get('lsa-id')):
                continue

            # Add criteria to check against

            count += 1
            if not invert:
                return True
            else:
                if count == len(ospf_database_):
                    return True

        timeout.sleep()

    return False

def verify_ospf_neighbor_address(device, neighbor_address, 
    expected_state='Full', max_time=90, check_interval=10, expected_failure=False):
    """ Verifies ospf neighbors address
        Args:
            device ('obj'): device to use
            max_time ('int'): Maximum time to keep checking
                              Default to 90 secs
            check_interval ('int'): How often to check
                                    Default to 10 secs
            neighbor_address ('str'): neighbor_address
            expected_state (`str`): expected neighbor state
                                    Default to `Full`
            expected_failure (`bool`): flag to make result opposite
                                       Default to False
        Returns:
            True/False
        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show ospf neighbor')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # example of out
        # {
        #   "ospf-neighbor-information": {
        #     "ospf-neighbor": [ # <-----
        #       {
        #         "activity-timer": "32",
        #         "interface-name": "ge-0/0/0.0",
        #         "neighbor-address": "10.189.5.94",
        #         "neighbor-id": "10.189.5.253",
        #         "neighbor-priority": "128",
        #         "ospf-neighbor-state": "Full"
        #       },
        ospf_neighbors = out.q.get_values('ospf-neighbor')

        result = []
        for neighbor in ospf_neighbors:
            if (
                neighbor['neighbor-address'] == neighbor_address
                and neighbor['ospf-neighbor-state'] == expected_state
            ):
                result.append(True)
            else:
                continue

        if expected_failure:
            if False == all(result) or result == []:
                return True
        else:
            if True == all(result):
                return True

        timeout.sleep()

    return False

def verify_ospf_route_nexthop(device, route, expected_nexthop, 
    max_time=90, check_interval=10):
    """ Verifies nexthop of ospf route
        Args:
            device (`obj`): device to use
            route (`str`): target route
            expected_nexthop (`str`): expected nexthop of ospf route
            max_time (`int`): Maximum time to keep checking
                              Default to 90 secs
            check_interval (`int`): How often to check
                                    Default to 10 secs
        Returns:
            True/False
        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        out = None
        try:
            out = device.parse('show ospf route {route}'.format(route=route))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # example of out
        # {
        #   "ospf-route-information": {
        #     "ospf-topology-route-table": {
        #       "ospf-route": {
        #         "ospf-route-entry": {
        #           "address-prefix": "30.0.0.0/24",
        #           "interface-cost": "2",
        #           "next-hop-type": "IP",
        #           "ospf-next-hop": {
        #             "next-hop-address": {
        #               "interface-address": "10.0.0.2" # <-----
        #             },
        #            "next-hop-name": {
        #              "interface-name": "ge-0/0/4.0"
        #            }
        if expected_nexthop in out.q.get_values('interface-address'):
            return True
        else:
            timeout.sleep()
    return False

def verify_single_ospf_neighbor_address(device,
                                        neighbor_address,
                                        max_time=60,
                                        check_interval=10):
    """ Verifies single ospf neighbor exists

        Args:
            device ('obj'): device to use
            neighbor_address ('str'): ospf neighbor address
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check

        Returns:
            True/False

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse('show ospf neighbor')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        #{'ospf-neighbor-information': {'ospf-neighbor': [{"neighbor-address": "10.189.5.94",
        #                                                "interface-name": "ge-0/0/0.0",}]}}
        neighbors = set(output.q.get_values('neighbor-address'))

        if neighbor_address in neighbors and len(neighbors) == 1:
            return True
        else:
            timeout.sleep()

    return False


def verify_all_ospf_neighbor_states(device,
                                    expected_state,
                                    max_time=60,
                                    check_interval=10):
    """ Verifies state of ospf neighbor

        Args:
            device ('obj'): device to use
            expected_state ('str'): OSPF adjacency state that is expected
            max_time ('int'): Maximum time to keep checking
            check_interval ('int'): How often to check

        Returns:
            True/False

        Raises:
            N/A
    """
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        try:
            output = device.parse('show ospf neighbor')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        #{'ospf-neighbor-information': {'ospf-neighbor': [{"neighbor-address": "10.189.5.94",
        #                                                "ospf-neighbor-state": "Full",}]}}
        neighbor_states = set(output.q.get_values('ospf-neighbor-state'))

        if len(neighbor_states) == 1 and expected_state in neighbor_states:
            return True
        else:
            timeout.sleep()

    return False

def verify_ospf_neighbor_instance_state_all(device, instance_name, expected_state, max_time=60, check_interval=10):
    """Verifies all states of ospf neighbor instance

    Args:
        device (obj): Device object
        instance_name (str): Instance name
        expected_state (str): Expected state to check for
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show ospf neighbor instance {instance_name}'.format(
                instance_name=instance_name
            ))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        if all([state == expected_state for state in out.q.get_values('ospf-neighbor-state')]) and out.q.get_values('ospf-neighbor-state'):
            return True

        timeout.sleep()

    return False
