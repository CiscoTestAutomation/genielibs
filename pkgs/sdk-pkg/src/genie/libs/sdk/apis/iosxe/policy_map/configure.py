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
            if 'policer_val' in class_map:
                cmd.append(f"police rate {class_map['policer_val']}")
            if class_map.get('match_mode', None)  and class_map.get('matched_value', None):
                for match_mode, matched_value in zip(class_map['match_mode'], class_map['matched_value']):
                    cmd.append(f"set {match_mode} {matched_value}")
            if 'table_map_name' in class_map:
                cmd.append(f"set {class_map['table_map_mode']} {class_map['table_map_mode']} table {class_map['table_map_name']}")
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

def configure_shape_map(device,
                        class_map_list,
                        service_policy='service-policy',
                        queue_name=None, 
                        policy_name=None):
    """ Configures policy_map type queueing
        Args:
             device('obj'): device to use
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
             ],
             service_policy('str',optional) : service-policy name by default service-policy
             queue_name('str', optional): name of the queue policy name
             policy_name('str', optional): name of the queue policy name

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
        if 'bandwidth' in class_map:
            cmd.append(f"bandwidth remaining ratio {class_map['bandwidth']}")
        if 'queue_limit' in class_map:
            cmd.append(f"queue-limit {class_map['queue_limit']} bytes")
        if 'child_policy' in class_map:
            cmd.append(f"{service_policy} {class_map['child_policy']}")

    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
                "Could not configure queueing policy_map. Error:\n{error}".format(
                    error=e
                 )
        )

def configure_bandwidth_remaining_policy_map(device,policy_names,
                     class_names,bandwidth_list,shape_average,bandwidth_remaining=True):

    """ Configures policy_map
        Args:
             device ('obj'): device to use
             policy_names('list) : list of policy-maps i.e. parent and grandparent
             class_names ('list') : list of classes inside policy-map i.e voice, video etc.
             bandwidth_list ('list) : list of bandwidth remainin for each class.
             shape_average ('str') : shaper percentage value for grandparent
             bandwidth_remaining ('bool') : If true, sets percentage of remaining bandwidth.
                                            Else, sets percentage of total bandwidth.
                                            Defaults to True.
        example:
             policy_names=['parent','grandparent']
             class_names = ['voice','data','video','class-default']
             bandwidth_list = [20,10,10,10,30]
             shape_average = 100
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    counter = 0
    cli = [f"policy-map {policy_names[0]}"]

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
    cli.append(f"service-policy {policy_names[0]}")

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


def unconfigure_table_map(device, table_map_name,from_val,to_val,):
    """ UnConfigures table_map
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

def configure_table_map(device, table_map_name,from_val,to_val,):
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
        device.configure(cmd)
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Unable to configure service policy type with {queue_name}. Error:\n{e}")

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
    cmd = [f"policy-map {policy_name}",
           f"class {class_map_name}"]
    if (policer_percent_val) and (table_map_mode) and (table_map_name):
        cmd.append(f"police cir percent {policer_percent_val} conform-action transmit exceed-action set-dscp-transmit {table_map_mode} table {table_map_name}")
    if policer_percent_val:
        cmd.append(f"police cir percent {policer_percent_val} conform-action transmit")
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
        raise SubCommandFailure(f"Could not configure policy-map on device. Error:\n{e}")