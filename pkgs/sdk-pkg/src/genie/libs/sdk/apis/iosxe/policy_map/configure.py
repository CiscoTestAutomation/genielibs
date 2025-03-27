"""Common configure functions for interface"""
# Python
import logging
import re

# Unicon
from unicon.core.errors import SubCommandFailure

# Steps
from pyats.aetest.steps import Steps

log = logging.getLogger(__name__)


def configure_policy_map(device,
    policy_name,
    class_map_list):
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
             police_cir_percent(int, optional): police cir percent
             priority_percent('int',optional) : priority percent
             priority_level('int',optional): value of priority queue for 0 to 7
             bandwidth_percent(int, optional): bandwidth percent
             bandwidth_remaining_percent(int, optional): bandwidth remaining percent
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
        "Configuring policy_map {policy_name}".format(
            policy_name=policy_name,
        )
    )

    cmd = [f"policy-map {policy_name}"]
    for class_map in class_map_list:
        if isinstance(class_map, dict):
            cmd.append(f"class {class_map['class_map_name']}")
            if 'priority_level' in class_map:
                cmd.append(f"priority level {class_map['priority_level']}")
            if 'bandwidth_percent' in class_map:
                cmd.append(f"bandwidth percent {class_map['bandwidth_percent']}")
            if 'priority_percent' in class_map:
                cmd.append(f"priority percent {class_map['priority_percent']}")    
            if 'bandwidth_remaining_percent' in class_map:
                cmd.append(f"bandwidth remaining percent {class_map['bandwidth_remaining_percent']}")
            if class_map.get('match_mode', None)  and class_map.get('matched_value', None):
                for match_mode, matched_value in zip(class_map['match_mode'], class_map['matched_value']):
                    cmd.append(f"set {match_mode} {matched_value}")
            if 'table_map_name' in class_map:
                cmd.append(f"set {class_map['table_map_mode']} {class_map['table_map_mode']} table {class_map['table_map_name']}")
            if 'policer_val' in class_map:
                cmd.append(f"police rate {class_map['policer_val']}")
            if 'police_cir_percent' in class_map:
                cmd.append(f"police cir percent {class_map['police_cir_percent']}")
        else:
            cmd.append(f"{class_map}")

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

def configure_shape_map(device, queue_name=None, class_map_list=[], 
                        service_policy='service-policy', policy_name=None):
    """ Configures policy_map type queueing
        Args:
             device('obj'): device to use
             queue_name('str', optional): name of the queue policy name. Default is None
             class_map_list('list', optional): list of dict type hold number of class map. Default is empty list
             [
             {
             class_map_name('str'): name of the class
             priority_level('int',optional): value of priority queue for 0 to 7
             shape_average('str',optional): value of the shape average
             bandwidth('int',optional): bandwidth value
             bandwidth_percent('int',optional): bandwidth percent value
             queue_limit('int',optional): queue_limit value
             child_policy('str',optional): name of the child policy
             shape_average_percent('str', optional): value of shape average percent
             random_detect_type('str', optional): random-detect type. For ex: discard-class, discard-class-based
             discard_class_value('int', optional): discard class value 0 or 1
             minimum_threshold('int', optional): minumum threshold percentage
             maximum_threshold('int', optional): maximum threshold percentage
             mark_probability('int', optional): mark probability denominator
             }
             ],
             service_policy('str',optional) : service-policy name by default service-policy
             policy_name('str',optional) : name of the policy name

        example:
             class_map_list=[{'class_map_name':'queue_name',
             priority_level:7,
             shape_average:'2000000000' or 'rate 20',
             bandwidth: 20,
             queue_limit: 10000,
             shape_average_percent: 40,
             random_detect_type: 'discard-calss',
             discard_class_value: 1,
             minimum_threshold: 30,
             maximum_threshold: 70,
             mark_probability: 4
             }]

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = []
    if queue_name:
        cmd.append(f"policy-map type queueing {queue_name}")
    elif policy_name:
        cmd.append(f"policy-map {policy_name}")
    for class_map in class_map_list:
        cmd.append(f"class {class_map['class_map_name']}")
        if 'priority_level' in class_map:
            cmd.append(f"priority level {class_map['priority_level']}")
        if 'shape_average' in class_map:
            cmd.append(f"shape average {class_map['shape_average']}")
        elif 'shape_average_percent' in class_map:
            cmd.append(f"shape average percent {class_map['shape_average_percent']}")
        if 'bandwidth' in class_map:
            cmd.append(f"bandwidth remaining ratio {class_map['bandwidth']}")
        if 'bandwidth_percent' in class_map:
            cmd.append(f"bandwidth percent {class_map['bandwidth_percent']}")
        if 'queue_limit' in class_map:
            cmd.append(f"queue-limit {class_map['queue_limit']} bytes")
        if 'child_policy' in class_map:
            cmd.append(f"{service_policy} {class_map['child_policy']}")
        if 'random_detect_type' in class_map:
            if 'discard_class_value' in class_map:
                command = f"random-detect {class_map['random_detect_type']} {class_map['discard_class_value']} percent {class_map['minimum_threshold']} {class_map['maximum_threshold']}"
                command += f" {class_map['mark_probability']}" if 'mark_probability' in class_map else ""
                cmd.append(command)
            else:
                cmd.append(f"random-detect {class_map['random_detect_type']}")
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
                "Could not configure queueing policy_map. Error:\n{error}".format(
                    error=e
                 )
        )

def configure_policy_map_on_device(device, policy_map_name, class_map_name, target_bit_rate):
    """ Configure policy-map type on Device
    Args:
        device (`obj`): Device object
        policy_map_name ('str'): policy-map name to configure
        class_map_name ('str'): class map name to configure
        target_bit_rate ('str'): target bit rate to configure (in bits/sec)
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring policy-map on device
    """
    log.debug("Configuring policy-map on device")

    try:
        device.configure(
            [
                f"policy-map {policy_map_name}",
                f"class {class_map_name}",
                f"shape average {target_bit_rate}",
            ]
        )
    except SubCommandFailure:
        raise SubCommandFailure("Could not configure policy-map on device")

def configure_bandwidth_remaining_policy_map(device, policy_names, shape_average,
                                             class_names=None, bandwidth_list=None, 
                                             bandwidth_remaining=True):

    """ Configures policy_map
        Args:
             device ('obj'): device to use
             policy_names('list) : list of policy-maps i.e. parent and grandparent
             shape_average ('str') : shaper percentage value for grandparent
             class_names ('list', optional) : list of classes inside policy-map i.e voice, video etc.
             bandwidth_list ('list, optional) : list of bandwidth remainin for each class.
             bandwidth_remaining ('bool') : If true, sets percentage of remaining bandwidth.
                                            Else, sets percentage of total bandwidth.
                                            Defaults to True.
        example:
             policy_names=['parent','grandparent']
             shape_average = '100'
             class_names = ['voice','data','video','class-default']
             bandwidth_list = [20,10,10,10,30]
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    counter = 0
    cli = [f"policy-map {policy_names[0]}"]

    if (class_names) and (bandwidth_list):
        for class_val in class_names:
            cli.append(f"class {class_val}")
            if bandwidth_remaining:
                cli.append(f"bandwidth remaining percent {bandwidth_list[counter]}")
            else:
                cli.append(f"bandwidth percent {bandwidth_list[counter]}")
            counter += 1

    cli.append(f"policy-map {policy_names[1]}")
    cli.append(f"class class-default")
    cli.append(f"shape average percent {shape_average}")
    cli.append(f"service-policy {policy_names[2]}")

    try:
        device.configure(cli)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure policy-map. Error:\n{e}".format(e))

def unconfigure_bandwidth_remaining_policy_map(device,policy_names):

    """ Unconfigures policy_map
        Args:
             device ('obj'): device to use
             policy_names('list) : list of policy-maps i.e. parent and grandparent  
        example:
             policy_names=['parent','grandparent']
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cli = []

    for policy_val in policy_names:

        cli.append(f"no policy-map {policy_val}")

    try:
        device.configure(cli)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure policy-map. Error:\n{e}".format(e))

def configure_policy_map_type_service(device, policy_map_name, pppoe_service_name=None):
    """ Configure policy-map type service on Device
    Args:
        device ('obj'): Device object
        policy_map_name ('str'): policy-map name to configure
        pppoe_service_name('str',optional): service name to configure
    Return:
        None
    Raise:
        SubCommandFailure: Failed to configure policy-map service
    """
    log.info("Configuring policy-map type service on device")
    
    cmd = []
    cmd = [f"policy-map type service {policy_map_name}"]
    if pppoe_service_name:
        cmd.append(f"pppoe service {pppoe_service_name}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
                raise SubCommandFailure(
            f"Failed to configure policy-map service, Error:\n{e}"
    )

def unconfigure_policy_map_type_service(device, policy_map_name):
    """ Configure policy-map type service on Device
    Args:
        device ('obj'): Device object
        policy_map_name ('str'): policy-map name to configure
    Return:
        None
    Raise:
        SubCommandFailure: Failed to configure policy-map service
    """
    log.info("Unconfiguring policy-map type service on device")

    cmd = f"no policy-map type service {policy_map_name}"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure policy-map service, Error:\n{e}"
    )

def configure_policy_map_with_pps(device, policy_name, class_map_name, police_rate):
    """ Configures policy_map
        Args:
             device ('obj'): device to use
             policy_name ('str) : name of the policy name
             class_map_name ('str'): class map information
             police_rate ('int'): police rate details
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("configure policy_map {policy_name} with {class_map_name} and {police_rate} in pps".format(policy_name=policy_name, class_map_name=class_map_name, police_rate=police_rate))
    config = [f"policy-map {policy_name}", 
              f"class {class_map_name}", 
              f"police rate {police_rate} pps"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure policy_map {policy_name} with {class_map_name} and {police_rate} in pps. Error:\n{error}".format(policy_name=policy_name, class_map_name=class_map_name, police_rate=police_rate, error=e)
        )

def configure_policy_map_with_percent(device, policy_name, class_map_name, police_percent_val):
    """ Configures policy_map
        Args:
             device ('obj'): device to use
             policy_name ('str) : name of the policy name
             class_map_name ('str'): class map information
             police_percent_val ('int'): police rate details
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"configure policy_map {policy_name} with {class_map_name} and {police_percent_val}")
    config = [f"policy-map {policy_name}",
              f"class {class_map_name}",
              f"police rate percent {police_percent_val}"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure policy_map with {police_percent_val}. Error:\n{error}".format(
                police_percent_val=police_percent_val, error=e)
        )


def unconfigure_table_map_values(device, table_map_name, from_val, to_val):
    """ UnConfigures table_map values
        Args:
             device ('obj'): device to use
             table_map_name ('str') : name of the table map  name
             from_val ('int') : list of from values
             to_val ('int') : list of to values 
        Returns:
            None
        Raises:
            SubCommandFailure
    """
   
    cli = [f'table-map {table_map_name}',
           f'no map from {from_val} to {to_val}']
  
    
    try:
        device.configure(cli)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure table map with {from_val} to {to_val}. Error:\n{e}")

def configure_table_map_values(device, table_map_name, from_val, to_val):
    """ Configures table_map
        Args:
             device ('obj'): device to use
             table_map_name('str') : name of the table map  name
             from_val ('int') : list of from values
             to_val ('int') : list of to values 
        Returns:
            None
        Raises:
            SubCommandFailure
    """
   
    cli = [f'table-map {table_map_name}',
           f'map from {from_val} to {to_val}']
      
    try:
        device.configure(cli)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure table_map with {from_val} to {to_val}. Error:\n{e}")

def configure_policy_map_with_dscp_table(device, policy_map_name, class_map_name, match_mode, match_packet, table_map_name):
    """ Configure policy-map type with dscp table on Device
    Args:
        device ('obj'): Device object
        policy_map_name ('str'): policy-map name to configure
        class_map_name ('str'): class map name to configure
        match_mode ('str'): match mode name for cos or dscp
        match_packet ('str'): match packets for qos or dscp
        table_map_name ('str',optional): set packet dscp based on table_map_name
        
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring policy on device
    """
    cli = [f'policy-map {policy_map_name}',
           f'class {class_map_name}',
           f'set {match_mode} {match_packet} table {table_map_name}']

    try:
        device.configure(cli)
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
        "Could not configure policy map with dscp table. Error:\n{error}".format(error=e ))

def configure_policy_map_with_no_set_dscp(device, policy_map_name, class_map_name, police_bit_rate, match_mode,match_packets_precedence):
    """ Configure policy map type with no dscp on Device
    Args:
        device ('obj'): Device object
        policy_map_name ('str'): policy-map name to configure
        class_map_name ('str'): class map name to configure
        police_bit_rate ('str'): policy_bit_rate to configure
        match_mode ('str'): match mode name for cos or dscp
        match_packets_precendence ('str'): match packets with dscp

    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring policy-no-set on device
    """
    cli = [f'policy-map {policy_map_name}',
           f'class {class_map_name}',
           f'police {police_bit_rate}',
           f'no set {match_mode} {match_packets_precedence}']
    
    try:
        device.configure(cli)
        
    except SubCommandFailure as e:
        raise SubCommandFailure
        ("Could not configure policy map with no dscp value")

def configure_policy_map_with_dscp_police(device, policy_map_name, class_map_name, policy_var, table_map_mode, table_map_name):
    """ Configure policy-map type on Device
    Args:
        device ('obj'): Device object
        policy_map_name ('str'): policy-map name to configure
        class_map_name ('str'): class map name to configure
        policy_var ('str'): policy-var to configure
        table_map_mode ('str'): table map mode for dscp
        table_map_name ('str',optional): set table_map_name
        
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring policy-map on device
    """
    cli = [f'policy-map {policy_map_name}',
           f'class {class_map_name}',
           f'police {policy_var}',
           f'exit',
           f'set {table_map_mode} {table_map_mode} table {table_map_name}']
    try:
        device.configure(cli)
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
        f"Could not configure policy map with {table_map_mode} table {table_map_name}. Error:\n{e}")

def unconfigure_policy_map_with_type_queue(device, policy_type, queue_name):
    """ Unconfigures policy map with type queueing
    Args:
        device ('obj'): device to use
        policy_type ('str'): Configure Queueing policy type
        queue_name ('str') : queue name to configure
             
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cli = [f'no policy-map type {policy_type} {queue_name}']

    try:
        device.configure(cli)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure policy-map. Error:\n{e}".format(e))

def configure_service_policy_with_queueing_name(device, interface, policy_type, queue_name):
    """ Configures policy_map type queueing
        Args:
             device ('obj'): device to use
             interface ('str'): interface to configure
             policy_type ('str'): Configure Queueing Service Policy
             queue_name ('str'): name of the queue service_policy name

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f'interface {interface}',
           f'service-policy type {policy_type} output {queue_name}']
           
    try:
        output = device.configure(cmd)
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Unable to configure service policy type with {queue_name}. Error:\n{e}")
    return output

def configure_policy_map_on_device(device, policy_map_name, class_map_name, 
                                   target_bit_rate, match_mode=None,match_packets_precedence=None):
    """ Configure policy-map type on Device
    Args:
        device ('obj'): Device object
        policy_map_name ('str'): policy-map name to configure
        class_map_name ('str'): class map name to configure
        target_bit_rate ('str'): target bit rate to configure (in bits/sec)
        match_mode ('str', optional): match mode name for cos or dscp
        match_packets_precendence ('str', optional): match packets with dscp
    Return:
        None
    Raise:
        SubCommandFailure: Failed configuring policy-map on device
    """
    log.debug("Configuring policy-map on device")
    
    cmd = [
        f"policy-map {policy_map_name}",
        f"class {class_map_name}",
        f"shape average {target_bit_rate}",
    ]

    if (match_mode and match_packets_precedence):
        cmd.append(f"set {match_mode} {match_packets_precedence}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure class_map. Error:\n{error}".format(
                error=e))


def configure_hqos_policer_map(device,
    policy_name,
    class_map_name,
    policer_percent_val=None,
    table_map_name=None,
    table_map_mode=None,
    match_mode=None,
    matched_value=None,
    child_policy=None,
    policer_cir_val=None,
    police_val=None,
    set_table_map=False):

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
             policer_cir_val('str',optional): policer cir value,default is None
             police_val('str',optional): police value,default is None
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
             policer_cir_val: '60'
             police_val: '600000000'
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
    cmd = [f"policy-map {policy_name}",
           f"class {class_map_name}"]
    if (policer_percent_val) and (table_map_mode) and (table_map_name):
        cmd.append(f"police cir percent {policer_percent_val} conform-action transmit exceed-action set-dscp-transmit {table_map_mode} table {table_map_name}")
    if policer_percent_val:
        cmd.append(f"police cir percent {policer_percent_val} conform-action transmit")
    if police_val and table_map_mode and table_map_name:
        cmd.append(f"police {police_val} conform-action transmit exceed-action set-dscp-transmit {table_map_mode} table {table_map_name}")         
    if match_mode and matched_value :
        for mat_mode, mat_value in zip(match_mode, matched_value):
                cmd.append(f"set {mat_mode} {mat_value}")
    if set_table_map:
        cmd.append(f"set {table_map_mode} {table_map_mode} table {table_map_name}")
    if child_policy:
        cmd.append(f"service-policy {child_policy}")
    if policer_cir_val:
        cmd.append(f"police cir percent {policer_cir_val}")
    if police_val:
        cmd.append(f"police {police_val}")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure policy-map on device. Error:\n{e}")


def unconfigure_service_policy_with_queueing_name(device, interface, policy_type, queue_name):
    """ Unconfigures policy_map type queueing
        Args:
             device ('obj'): device to use
             interface ('str'): interface to configure
             policy_type ('str'): Configure Queueing Service Policy
             queue_name ('str'): name of the queue service_policy name

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f'interface {interface}',
           f'no service-policy type {policy_type} output {queue_name}']
    
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Unable to unconfigure service policy type with {queue_name}. Error:\n{e}")


def configure_policy_map_class_parameters(
    device, 
    policy_name, 
    class_map_name, 
    policer_rate=None, 
    cir_rate=None,
    cir_percent=None, 
    rate_value=None, 
    rate_percent=None,
    confirm_action=None,
    confirm_transmit_action=None, 
    pir_rate=None, 
    exceed_action=None, 
    exceed_transmit_action=None, 
    violate_action=None, 
    violate_transmit_action=None, 
    table_map_name=None,
    traffic_class_mode=None,
    traffic_class_table=None
    ):

    """ Configures Policy-map class 
        Args:
             device ('obj'): device to use
             policy_name('str) : name of the policy name
             class_map_name('str') : name of the class
             policer_rate('int', optional): police rate value, default is None
             cir_rate('int', optional): cir rate value, default is None
             cir_percent('int', optional): cir percentage value, default is None
             rate_value('int', optional): Rate value, default is None
             rate_percent('int', optional): rate percentage value, default is None
             confirm_action('str', optional): Confirm action. ex:'transmit'. Default is None
             confirm_transmit_action('str', optional): conform transmit action. ex: 'cos', 'dscp', default is None
             pir_rate('int',optional): pir rate value, default is None
             exceed_action('str', optional): exceed action. ex: 'drop', 'set-cos-transmit', default is None
             exceed_transmit_action('str', optional): exceed transmit action. ex: 'cos', 'dscp', default is None
             violate_action('str', optional): violate action. ex: 'drop', 'set-cos-transmit', default is None
             violate_transmit_action('str', optional): violate transmit action. ex: 'cos', 'dscp', default is None
             table_map_name('str', optional): to set the table name for policy_map, default is None
             traffic_class_mode('str', optional): traffic class mode. ex: 'cos', 'dscp', default is None
             traffic_class_table('str', optional): table map name, default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [f'policy-map {policy_name}',
           f'class {class_map_name}']
    if traffic_class_mode:
        command = f'set traffic-class {traffic_class_mode}'
        if traffic_class_table:
            command += f' table {traffic_class_table}'
        cmd.append(command)
    
    command = ''
    if policer_rate:
        command = f'police {policer_rate}'
    elif cir_rate:
        command = f'police cir {cir_rate}'
    elif cir_percent:
        command += f'police cir percent {cir_percent}'
    elif rate_value:
        command = f'police rate {rate_value}'
    elif rate_percent:
        command += f'police rate percent {rate_percent}'
    if pir_rate:
        command += f' pir {pir_rate}'
    if confirm_action:
        command += f' conform-action {confirm_action}'
        if confirm_transmit_action:
            command += f' {confirm_transmit_action}'
        if exceed_action:
            command += f' exceed-action {exceed_action}'
            if exceed_transmit_action:
                command += f' {exceed_transmit_action}'
            if violate_action:
                command += f' violate-action {violate_action}'
                if violate_transmit_action:
                    command += f' {violate_transmit_action}'
        if table_map_name:
            command += f' table {table_map_name}'
    if command:
        cmd.append(command)

    try:
        device.configure(cmd)
    
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configures Policy-map class. Error:\n{e}")


def unconfigure_policy_map_class_parameters(
    device, 
    policy_name, 
    class_map_name, 
    policer_rate=None, 
    cir_rate=None,
    cir_percent=None, 
    rate_value=None, 
    rate_percent=None,
    confirm_action=None,
    confirm_transmit_action=None, 
    pir_rate=None, 
    exceed_action=None, 
    exceed_transmit_action=None, 
    violate_action=None, 
    violate_transmit_action=None, 
    table_map_name=None,
    traffic_class_mode=None,
    traffic_class_table=None
    ):

    """ Unconfigures Policy-map class 
        Args:
             device ('obj'): device to use
             policy_name('str) : name of the policy name
             class_map_name('str') : name of the class
             policer_rate('int', optional): police rate value, default is None
             cir_rate('int', optional): cir rate value, default is None
             cir_percent('int', optional): cir percentage value, default is None
             rate_value('int', optional): Rate value, default is None
             rate_percent('int', optional): rate percentage value, default is None
             confirm_action('str', optional): Confirm action. ex:'transmit'. Default is None
             confirm_transmit_action('str', optional): conform transmit action. ex: 'cos', 'dscp', default is None
             pir_rate('int',optional): pir rate value, default is None
             exceed_action('str', optional): exceed action. ex: 'drop', 'set-cos-transmit', default is None
             exceed_transmit_action('str', optional): exceed transmit action. ex: 'cos', 'dscp', default is None
             violate_action('str', optional): violate action. ex: 'drop', 'set-cos-transmit', default is None
             violate_transmit_action('str', optional): violate transmit action. ex: 'cos', 'dscp', default is None
             table_map_name('str', optional): to set the table name for policy_map, default is None
             traffic_class_mode('str', optional): traffic class mode. ex: 'cos', 'dscp', default is None
             traffic_class_table('str', optional): table map name, default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [f'policy-map {policy_name}',
           f'class {class_map_name}']
    if traffic_class_mode:
        command = f'no set traffic-class {traffic_class_mode}'
        if traffic_class_table:
            command += f' table {traffic_class_table}'
        cmd.append(command)
    
    command = ''
    if policer_rate:
        command = f'no police {policer_rate}'
    elif cir_rate:
        command = f'no police cir {cir_rate}'
    elif cir_percent:
        command += f'no police cir percent {cir_percent}'
    elif rate_value:
        command = f'no police rate {rate_value}'
    elif rate_percent:
        command += f'no police rate percent {rate_percent}'
    if pir_rate:
        command += f' pir {pir_rate}'
    if confirm_action:
        command += f' conform-action {confirm_action}'
        if confirm_transmit_action:
            command += f' {confirm_transmit_action}'
        if exceed_action:
            command += f' exceed-action {exceed_action}'
            if exceed_transmit_action:
                command += f' {exceed_transmit_action}'
            if violate_action:
                command += f' violate-action {violate_action}'
                if violate_transmit_action:
                    command += f' {violate_transmit_action}'
        if table_map_name:
            command += f' table {table_map_name}'
    if command:
        cmd.append(command)

    try:
        device.configure(cmd)
    
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigures Policy-map class. Error:\n{e}")


def unconfigure_policy_map_class(device, policy_name, class_map_name, policy_map_type=None):
    """ Unconfigures Policy-map class 
        Args:
             device ('obj'): device to use
             policy_name ('str): name of the policy name
             class_map_name ('str'): name of the class
             policy_map_type ('str'): type of the policy-map. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = [f'policy-map{f" type {policy_map_type}" if policy_map_type else ""} {policy_name}', 
        f'no class {class_map_name}']

    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not unconfigure Policy-map. Error:\n{e}')

def configure_table_map_on_device(device, table_map_name,from_val,to_val,table_map_value):
    """ Configures table_map
        Args:
             device ('obj'): device to use
             table_map_name('str') : name of the table map  name
             from_val ('int') : list of from values
             to_val ('int') : list of to values 
             table_map_value('str',optional) : value of the table map (copy/ignore)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring table_map on device")
   
    cli = [f'table-map {table_map_name}',
           f'map from {from_val} to {to_val}']
           
    if table_map_value:
        cli.append(f"default {table_map_value}")       
      
    try:
        device.configure(cli)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure table_map with {from_val} to {to_val}. Error:\n{e}")
            
def configure_policy_map_class_precedence(device, policy_map_name,class_map_name,precedence_num):
    """ Configures policy-map with class and precedence
        Args:
             device ('obj'): device to use
             policy_map_name('str') : type of the policy-map
             class_map_name ('str') : class-map name
             precedence_num ('int') : Precedence value
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    
    log.debug("Configuring policy-map with class and precedence on device")
   
    cmd = [f'policy-map {policy_map_name}',
           f'class {class_map_name}',
           f'set precedence {precedence_num}']   
      
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure Configures policy-map with class {class_map_name} and precedence {precedence_num}. Error:\n{e}")

def unconfigure_policy_map_with_pps(device, policy_name, class_map_name, police_rate):
    """ Unconfigures policy-map with police rate in pps
        Args:
             device ('obj'): device to use
             policy_name ('str'): name of the policy name
             class_map_name ('str'): class map name information
             police_rate ('int'): police rate details in pps
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"unconfigure policy_map {policy_name} with {class_map_name} and {police_rate} in pps")
    
    config = [f"policy-map {policy_name}", 
              f"class {class_map_name}", 
              f"no police rate {police_rate} pps"]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure policy_map {policy_name} with {class_map_name} and {police_rate} in pps.  Error:\n{e}")
            

def configure_policy_map_set_cos_cos_table(device, policy_map_name, class_name, table_name):
    """ 
    Args:
        device ('obj'): device to use
        policy_map_name ('str'): name of policy-map
        class_name ('str'): class-default or any user defined class name
        table_name('str'): table name
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    if class_name == 'class-default':
        config = [
            "policy-map {}".format(policy_map_name), 
            "class {}".format(class_name), 
            "set cos cos table {}".format(table_name)
            ]
    else:
        config = [
            "class-map {}".format(class_name), 
            "policy-map {}".format(policy_map_name), 
            "class {}".format(class_name), 
            "set cos cos table {}".format(table_name)
            ]

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not configure policy map set cos cos table. Error:\n{error}".format(error=e))

def unconfigure_policy_map_set_cos_cos_table(device, policy_map_name, class_name, table_name):
    """ 
    Args:
        device ('obj'): device to use
        policy_map_name ('str'): name of policy-map
        class_name ('str'): class-default or any user defined class name
        table_name('str'): table name
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    config = []

    if class_name != 'class-default':
        config.append("class-map {}".format(class_name))

    config.extend([
        "policy-map {}".format(policy_map_name), 
        "class {}".format(class_name), 
        "no set cos cos table {}".format(table_name)
    ])

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not unconfigure policy map set cos cos table. Error:\n{error}".format(error=e))

def configure_policy_map_class(device,
    policy_name,
    class_map_list):
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
                        police_cir_percent(int, optional): police cir percent
                        priority_level('int',optional): value of priority queue for 0 to 7
                        bandwidth_percent(int, optional): bandwidth percent
                        bandwidth_remaining_percent(int, optional): bandwidth remaining percent
                    }
                ]

                example:
                    class_map_list=[
                        {
                            'class_map_name':'test1',
                            'policer_val':2000000000,
                            'match_mode':['dscp','cos']
                            'matched_value':['cs1','5']
                            'table_map_name':'table1'
                            'table_map_mode':'dscp'
                        }
                    ]

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Configuring policy_map {policy_name}".format(
            policy_name=policy_name,
        )
    )

    cmd = [f"policy-map {policy_name}"]
    for class_map in class_map_list:
        if isinstance(class_map, dict):
            cmd.append(f"class {class_map['class_map_name']}")
            if 'priority_level' in class_map:
                cmd.append(f"priority level {class_map['priority_level']}")
            if 'bandwidth_percent' in class_map:
                cmd.append(f"bandwidth percent {class_map['bandwidth_percent']}")
            if 'bandwidth_remaining_percent' in class_map:
                cmd.append(f"bandwidth remaining percent {class_map['bandwidth_remaining_percent']}")
            if class_map.get('match_mode', None)  and class_map.get('matched_value', None):
                for match_mode, matched_value in zip(class_map['match_mode'], class_map['matched_value']):
                    cmd.append(f"set {match_mode} {matched_value}")
            if 'table_map_name' in class_map:
                cmd.append(f"set {class_map['table_map_mode']} {class_map['table_map_mode']} table {class_map['table_map_name']}")
            if 'policer_val' in class_map:
                cmd.append(f"police rate {class_map['policer_val']}")
            if 'police_cir_percent' in class_map:
                cmd.append(f"police cir percent {class_map['police_cir_percent']}")
        else:
            cmd.append(f"{class_map}")

    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure class_map. Error:\n{e}"
        )

def configure_policy_map_with_police_cir_percentage(device, policy_map_name, class_name=None, percent=None, action=None):
    """ Configure policy-map with police cir percentage
        Args:
             device ('obj'): device to use
             policy_map_name('str'): Policy-map name
             class_name('str',optional) : Class-name 
             percent('int',optional) : police cir percentage  
             action('str',optional) : exceed-action to do (drop/transmit)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring policy-map with police cir percentage on device")

    config = [f'policy-map {policy_map_name}']
    if class_name:
        config.append(f'class {class_name}')
    if percent and action:
        config.append(f'police cir percent {percent} conform-action transmit exceed-action {action}')
    try:
        device.configure(config)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure policy-map with police cir percentage on device {device}.Error:\n{e}") 

def configure_policy_map_parameters(device, policy_map_name, class_name=None, priority_level=None, bandwidth_remaining_percent=None):
    """ Configure policy-map parameters on device
        Args:
             device ('obj'): device to use
             policy_map_name('str'): Policy-map name
             class_name('str',optional) : Class-name 
             priority_level('int',optional): value of priority queue from 0 to 7
             bandwidth_remaining_percent('int',optional) :bandwidth remaining percent
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring policy-map parameters on device")

    config = [f'policy-map type queueing {policy_map_name}']
    if class_name:
        config.append(f'class {class_name}')  
    if priority_level:
        config.append(f'priority level {priority_level}')
    if bandwidth_remaining_percent:
        config.append(f'bandwidth remaining ratio {bandwidth_remaining_percent}')  
    try:
        device.configure(config)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure policy-map parameters on device {device}.Error:\n{e}") 

def configure_policy_map_priority_express(device, policy_map_name, class_name=None):
    """ Configure policy-map parameters on device
        Args:
             device ('obj'): device to use
             policy_map_name('str'): Policy-map name
             class_name('str',optional) : Class-name 
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring policy-map express config on device")

    config = [
            "policy-map {}".format(policy_map_name), 
            "class {}".format(class_name), 
            "priority level 1 express"
            ]
    try:
        device.configure(config)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure policy-map express configuration on device {device}.Error:\n{e}") 

def unconfigure_policy_map_priority_express(device, policy_map_name, class_name=None):
    """ Unconfigure policy-map parameters on device
        Args:
             device ('obj'): device to use
             policy_map_name('str'): Policy-map name
             class_name('str',optional) : Class-name 
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Unconfiguring policy-map express config on device")

    config = [
            "policy-map {}".format(policy_map_name), 
            "class {}".format(class_name), 
            "no priority level 1 express"
            ]
    try:
        device.configure(config)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure policy-map express configuration on device {device}.Error:\n{e}") 
    