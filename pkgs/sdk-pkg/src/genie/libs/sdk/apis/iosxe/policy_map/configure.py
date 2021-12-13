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
        
