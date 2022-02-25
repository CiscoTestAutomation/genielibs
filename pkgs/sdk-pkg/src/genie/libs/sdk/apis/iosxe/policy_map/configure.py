"""Common configure functions for interface"""
# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Steps
from pyats.aetest.steps import Steps

log = logging.getLogger(__name__)
def configure_policy_map(device,
        policy_name,
        class_map_list
        ):
    """ Configures policy_map
        Args:
             device ('obj'): device to use
             policy_name('str) : name of the policy name
             class_map_list('list'): list of data type hold number class map information
             [
             {
             class_map_name('str') : name of the class
             policer_val('int',optional): police rate value,
             match_mode('list',optional): match mode name for cos,
             matched_value('list',optional): match mode values for cos traffic_class and dscp,
             table_map_name('str',optional): to set the table name for policy_map,
             table_map_mode('str',optional : name of the tablemode
             } ]

        example:
             class_map_list=[{'class_map_name':'test1',
             'policer_val':2000000000,
             'match_mode':['dscp','cos']
             'matched_value':['cs1','5']
             'table_map_name':'table1'
             'table_map_mode':'dscp'}]


        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Configuring policy_map {policy_name} with {class_map_name} ".format(
            policy_name=policy_name,
            class_map_name=class_map_list[0]['class_map_name'],

        )
    )
    cmd = [f"policy-map {policy_name}"]
    for class_map  in class_map_list:
        cmd.append(f"class {class_map['class_map_name']}")
        if 'policer_val' in class_map:
            cmd.append(f"police rate {class_map['policer_val']}")
        if class_map.get('match_mode', None)  and class_map.get('matched_value', None):
            for match_mode, matched_value in zip(class_map['match_mode'], class_map['matched_value']):
                cmd.append(f"set {match_mode} {matched_value}")
        if 'table_map_name' in class_map:
            cmd.append(f"set {class_map['table_map_mode']} {class_map['table_map_mode']} table {class_map['table_map_name']}")

    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure class_map. Error:\n{error}".format(
                error=e
            )
        )

def unconfigure_policy_map(device, policy_name):
    """ Unconfigures policy-map
        Args:
             device ('obj'): device to use
             policy_name ('str'): name of the class

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Unconfiguring class_map {policy_name}".format(
            policy_name=policy_name,
        )
    )

    cmd = f"no policy-map {policy_name}"

    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure class_map. Error:\n{error}".format(
                error=e
            )
        )


def configure_hqos_policer_map(device,
        policy_name,
        class_map_name,
        policer_percent_val=None,
        table_map_name=None,
        table_map_mode=None,
        match_mode=None,
        matched_value=None,
        child_policy=None,
        set_table_map=False
        ):

    """ Configures HQos policy_map
        Args:
             device ('obj'): device to use
             policy_name('str) : name of the policy name
             class_map_name('str') : name of the class
             policer_percent_val('int',optional): police rate value, default is None
             table_map_name('str',optional): to set the table name for policy_map, default is None
             table_map_mode('str',optional) : name of the tablemode,default is None
             match_mode('list',optional): match mode name for cos, default is None
             matched_value('list',optional): match mode values for cos traffic_class and dscp, default is None
             child_policy('str',optional): name of child policy map,default is None
             set_table_map('boolean'): to configure set table map for HQos, default is False

        example:
             policy_name:'policy1'
             class_map_name:'class-default',
             policer_percent_val:1,
             table_map_name:'table1'
             table_map_mode:'dscp'
             match_mode:['dscp','cos']
             matched_value:['cs1','5']
             child_policy: 'child_policy_map'
             set_table_map:False


        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug(
        "Configuring HQos_policy_map {policy_name} with {child_policy} ".format(
            policy_name=policy_name,
            child_policy=child_policy,

        )
    )
    cmd = [f"policy-map {policy_name}"]
    cmd.append(f"class {class_map_name}")
    if policer_percent_val:
        cmd.append(f" police cir percent {policer_percent_val} conform-action transmit exceed-action set-dscp-transmit {table_map_mode} table {table_map_name}")
    if match_mode and matched_value :
        for mat_mode, mat_value in zip(match_mode, matched_value):
                cmd.append(f"set {mat_mode} {mat_value}")
    if set_table_map:
        cmd.append(f"set {table_map_mode} {table_map_mode} table {table_map_name}")

    if child_policy:
        cmd.append(f"service-policy {child_policy}")
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure class_map. Error:\n{error}".format(
                error=e
            )
        )

def configure_shape_map(device,
        queue_name,
        class_map_list
        ):
    """ Configures policy_map type queueing
        Args:
             device('obj'): device to use
             queue_name('str'): name of the queue policy name
             class_map_list('list'): list of dict type hold number of class map
             [
             {
             class_map_name('str'): name of the class
             priority_level('int',optional): value of priority queue for 0 to 7
             shape_average('str',optional): value of the shape average
             bandwidth('int',optional): bandwidth value
             queue_limit('int',optional): queue_limit value
             child_policy('str',optional): name of the child policy
             }
             ]

        example:
             class_map_list=[{'class_map_name':'queue_name',
             priority_level:7,
             shape_average:'2000000000' or 'rate 20'
             bandwidth: 20
             queue_limit: 10000
             }]

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Configuring policy_map type {queue_name} with {class_map_name}".format(queue_name=queue_name,class_map_name=class_map_list[0]['class_map_name'],
            )
        )

    cmd = [f"policy-map type queueing {queue_name}"]
    for class_map in class_map_list:
        cmd.append(f"class {class_map['class_map_name']}")
        if 'priority_level' in class_map:
            cmd.append(f"priority level {class_map['priority_level']}")
        if 'shape_average' in class_map:
            cmd.append(f"shape average {class_map['shape_average']}")
        if 'bandwidth' in class_map:
            cmd.append(f"bandwidth remaining ratio {class_map['bandwidth']}")
        if 'queue_limit' in class_map:
            cmd.append(f"queue-limit {class_map['queue_limit']} bytes")
        if 'child_policy' in class_map:
            cmd.append(f"service-policy {class_map['child_policy']}")

    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
                "Could not configure queueing policy_map. Error:\n{error}".format(
                    error=e
                 )
        )

