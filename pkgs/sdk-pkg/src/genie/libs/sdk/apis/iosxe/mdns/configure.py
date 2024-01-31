"""Common configure functions for mdns controller"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_mdns_controller(device, name, cont_addr, cont_src_intf, srvc_list, mat_option, \
                              cont_service_policy=None, msg_type=None, src_intf=None):
    """ Create mdns controller
        Args:
            device ('obj'): device to use
            name ('str')
            cont_addr ('str'): controller addresses to be configured
            cont_service_policy ('str'): service-policy to configured
            cont_src_intf ('str'): Default router ID
            srvc_list ('str'):
            mat_option ('str'):
            msg_type ('str'):
            src_intf ('str'):
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring mdns controller
    """
    log.info(
        "Configuring mdns controller with name={}, cont_addr={}, cont_service_policy={}, and "
        "cont_src_intf {} srvc_list={} mat_option={} msg_type={} src_intf={}".format(name, \
                                                                                     cont_addr, cont_service_policy,
                                                                                     cont_src_intf, srvc_list,
                                                                                     mat_option, msg_type, src_intf)
    )

    try:
        if cont_service_policy is not None:
            if msg_type is not None and src_intf is not None:
                device.configure(
                    [
                        "mdns-sd controller service-list {}".format(srvc_list),
                        "match {} message-type {} source-interface {} ".format(mat_option, msg_type, src_intf),
                        "mdns-sd controller service-policy {}".format(cont_service_policy),
                        "service-list {}".format(srvc_list),
                        "service-export mdns-sd controller {}".format(name),
                        "controller-address {}".format(cont_addr),
                        "controller-service-policy {}".format(cont_service_policy),
                        "controller-source-interface {}".format(cont_src_intf),
                    ]
                )
            elif msg_type is not None:
                device.configure(
                    [
                        "mdns-sd controller service-list {}".format(srvc_list),
                        "match {} message-type {} ".format(mat_option, msg_type),
                        "mdns-sd controller service-policy {}".format(cont_service_policy),
                        "service-list {}".format(srvc_list),
                        "service-export mdns-sd controller {}".format(name),
                        "controller-address {}".format(cont_addr),
                        "controller-service-policy {}".format(cont_service_policy),
                        "controller-source-interface {}".format(cont_src_intf),
                    ]
                )
            else:
                device.configure(
                    [
                        "mdns-sd controller service-list {}".format(srvc_list),
                        "match {}".format(mat_option),
                        "mdns-sd controller service-policy {}".format(cont_service_policy),
                        "service-list {}".format(srvc_list),
                        "service-export mdns-sd controller {}".format(name),
                        "controller-address {}".format(cont_addr),
                        "controller-service-policy {}".format(cont_service_policy),
                        "controller-source-interface {}".format(cont_src_intf),
                    ]
                )

        else:
            if msg_type is not None and src_intf is not None:
                device.configure(
                    [
                        "mdns-sd controller service-list {}".format(srvc_list),
                        "match {} message-type {} source-interface {}".format(mat_option, msg_type, src_intf),
                        "mdns-sd controller service-policy default-mdns-service-policy",
                        "service-list {}".format(srvc_list),
                        "service-export mdns-sd controller {}".format(name),
                        "controller-address {}".format(cont_addr),
                        "controller-service-policy default-mdns-service-policy",
                        "controller-source-interface {}".format(cont_src_intf),
                    ]
                )
            elif msg_type is not None:
                device.configure(
                    [
                        "mdns-sd controller service-list {}".format(srvc_list),
                        "match {} message-type {}".format(mat_option, msg_type),
                        "mdns-sd controller service-policy default-mdns-service-policy",
                        "service-list {}".format(srvc_list),
                        "service-export mdns-sd controller {}".format(name),
                        "controller-address {}".format(cont_addr),
                        "controller-service-policy default-mdns-service-policy",
                        "controller-source-interface {}".format(cont_src_intf),
                    ]
                )
            else:
                device.configure(
                    [
                        "mdns-sd controller service-list {}".format(srvc_list),
                        "match {}".format(mat_option),
                        "mdns-sd controller service-policy default-mdns-service-policy",
                        "service-list {}".format(srvc_list),
                        "service-export mdns-sd controller {}".format(name),
                        "controller-address {}".format(cont_addr),
                        "controller-service-policy default-mdns-service-policy",
                        "controller-source-interface {}".format(cont_src_intf),
                    ]
                )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure mdns controller {name}".format(
                name=name
            )
        )


def unconfigure_mdns_controller(device, name, srvc_list, cont_service_policy=None, ):
    """ Remove mdns controller
        Args:
            device ('obj'): device to use
            name ('str'): name of the controller to be created
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring bfd on interface
    """
    log.info(
        "Removing mdns controller with name={}".format(name)
    )

    try:
        if cont_service_policy is not None:
            device.configure(
                [
                    "no service-export mdns-sd controller {}".format(name),
                    "no mdns-sd controller service-policy {}".format(cont_service_policy),
                    "no mdns-sd controller service-list {}".format(srvc_list),
                ]
            )
        else:
            device.configure(
                [
                    "no service-export mdns-sd controller {}".format(name),
                    "no mdns-sd controller service-policy default-mdns-service-policy",
                    "no mdns-sd controller service-list {}".format(srvc_list),

                ]
            )


    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove mdns controller {name}".format(
                name=name
            )
        )


def configure_mdns_svi(device, vlan, act_qry, srvc_ins_suffix, srvc_mdns_qry, srvc_policy, transport):
    """ Create mdns svi
        Args:
            device ('obj'): device to use
            vlan ('str'):
            srvc_ins_suffix ('str'): controller addresses to be configured
            srvc_mdns_qry ('str'): Controller port to be configured
            srvc_policy ('str'): service-policy to configured
            transport ('str'): Default router ID
            act_qry ('int'): Default router ID
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring mdns svi config
    """
    log.info(
        "Configuring mdns svi with vlan={}, srvc_ins_suffix={}, srvc_mdns_qry={}, srvc_policy={}, and "
        "transport {} act_qry={}".format(vlan, srvc_ins_suffix, srvc_mdns_qry, srvc_policy, transport, act_qry)
    )

    try:
        device.configure(
            [
                "interface vlan {}".format(vlan),
                "mdns-sd gateway",
                "active-query timer {}".format(act_qry),
                "service-inst-suffix  {}".format(srvc_ins_suffix),
                "service-mdns-query  {} ".format(srvc_mdns_qry),
                "service-policy {}".format(srvc_policy),
                "transport {}".format(transport),
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure mdns svi {name}".format(
                vlan=vlan
            )
        )


def unconfigure_mdns_svi(device, vlan):
    """ Remove mdns svi
        Args:
            device ('obj'): device to use
            vlan ('str'): name of the controller to be created
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring mdns on interface
    """
    log.info(
        "Removing mdns svi with vlan={}".format(vlan)
    )

    try:
        device.configure(
            [
                "no interface vlan {}".format(vlan),
            ]
        )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove mdns svi {vlan}".format(
                vlan=vlan
            )
        )


def clear_mdns_statistics(device):
    """ Clears mdns statistics on device
        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed clearing statistics
    """

    try:
        device.execute(["clear mdns-sd cache",
                        "clear mdns-sd statistics all",
                        "clear mdns-sd sp-sdg statistics",
                        "clear mdns-sd service-peer statistics"])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not clear mdns statistics'
        )


def clear_mdns_query_db(device):
    """ Clears mdns query database statistics on device
        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed clearing query-db statistics
    """

    try:
        device.execute(["clear mdns-sd query-db"])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not clear mdns query-db'
        )


def unconfigure_mdns_service_definition(device, name):
    """ Unconfigure mdns service definition
        Args:
            device ('obj'): device to use
            name ('list')

        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring mdns controller
    """
    log.info(
        "Clearing  mdns service defintion with  name={}".format(name)
    )

    try:
        for defi in name:
            device.configure(
                [
                    "no mdns-sd service-definition {}".format(defi)

                ]
            )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not clear mdns service-definition {name}".format(
                name=name
            )
        )


def unconfig_mdns_sd_service_peer(device, vlan=None, ip_addr=None, \
                                  response_timer=None, timer=None, count=None, value=None):
    """ UNConfig MDNS_SD_SERVICE PEER

        Args:
            device (`obj`): Device object
            vlan ('int'): Vlan value
            ip_addr ('str'): ipv4,ipv6 address
            response_timer ('int'): active response timer
            timer ('int'): Timer value
            count ('int'): Count value
            value ('int'): rate limit value

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
        "unConfiguring mdns_sd_service_peer on globally"
    )

    try:
        if vlan is None and ip_addr is None and response_timer is None and timer is None and count is None and value is None:

            config = [
                "no mdns-sd gateway"
            ]
        else:
            config = [
                "mdns-sd gateway"
            ]

            if ip_addr is not None:
                config.extend([

                    "no sdg-agent {ipv4_ipv6}".format(ipv4_ipv6=ip_addr)
                ])
            if vlan is not None:
                config.extend([
                    "no source-interface vlan {vlan_id}".format(vlan_id=vlan)
                ])
            if response_timer is not None:
                config.extend([
                    "no active-response timer {resp_timer}".format(resp_timer=response_timer)
                ])
            if timer is not None:
                config.extend([
                    "no service-announcement-timer periodicity {timer_val}".format(timer_val=timer),
                    "no service-query-timer periodicity {timer_val}".format(timer_val=timer),

                ])
            if count is not None:
                config.extend([
                    "no service-announcement-count {count_val}".format(count_val=count),
                    "no service-query-count {count_val}".format(count_val=count)
                ])
            if value is not None:
                config.extend([
                    "no rate-limit {value}".format(value=value)
                ])
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure mdns_sd_service_peer. Error:\n{error}".format(error=e)
        )


def configure_mdns(
        device,
        service_definition_name=None,
        service_list=None,
        direction=None,
        policy_name=None,
        service_list_msg_type=None,
        direction_msg_type=None,
        message_type=None,
        service_list_filter=None,
        direction_filter_type=None,
        filter_name=None,
        policy_name1=None
):
    """ Configure mDNS (Multicast Domain Name System) services on agent and service peer

        mdns-sd gateway
        mdns-sd service-definition custom10
          service-type _airplay._tcp.local
          service-type _raop._tcp.local
          service-type _ipp._tcp.local
          service-type _afpovertcp._tcp.local
          service-type _nfs._tcp.local
          service-type _ssh._tcp.local
          service-type _dpap._tcp.local
          service-type _daap._tcp.local
          service-type _ichat._tcp.local
          service-type _presence._tcp.local
          service-type _http._tcp.local
          service-type _ipps._tcp.local
          service-type _printer._tcp.local
          service-type _smb._tcp.local
          service-type _ftp._tcp.local
        mdns-sd service-list service_list31 IN
        match custom10
        mdns-sd service-list service_list32 OUT
        match custom10
        mdns-sd service-list service_list33 OUT
        match custom10
        mdns-sd service-list service_list34 IN
        match custom10
        mdns-sd service-policy Policy41
          service-list service_list31 IN
        mdns-sd service-policy Policy42
          service-list service_list32 OUT
          service-list service_list33 OUT
          service-list service_list34 IN
        mdns-sd service-list service_list55 IN
        match custom10 message-type query
        mdns-sd service-list service_list66 OUT
        match custom10 location-filter filter8
        mdns-sd service-policy Policy43
          service-list service_list55 IN
          service-list service_list66 OUT
        end

    Args:
        device ('obj'): device to configure
        service definition ('str', optional): service definition name. Default value is None
        service_list ('list', optional): list with all services. Default value is None
        direction ('str', optional): direction. Default value is None
        policy_name ('dict', optional): dict with all Policy names and directions. Default value is None
        service_list_msg_type ('str', optional): creating service list for msg type. Default value is None
        direction_msg_type ('str', optional): creating direction for msg type. Default value is None
        message_type ('str', optional): Message type. Default value is None
        service_list_filter ('str', optional): creating service list for filter type. Default value is None
        direction_filter_type ('str', optional): creating direction for filter type. Default value is None
        filter_name ('str', optional): Filter name. Default value is None
        policy_name1 ('dict', optional): creating new dict for adding new service list for msg and filter types. Default value is None

        dict = {'Policy41': ['service_list31', 'IN'],
                'Policy42': ['service_list32',
                             'OUT',
                             'service_list33',
                             'OUT',
                             'service_list34',
                             'IN']}

        dict = {'Policy43': ['service_list55', 'IN',
                             'service_list66',
                             'OUT']}

  Returns:
      None

  Raises:
      SubCommandFailure
    """
    log.debug("Configuring mdns on globally")
    try:
        config = ["mdns-sd gateway"]
        if service_definition_name != None:
            config.extend([
                "mdns-sd service-definition {srvc_def_name}".format(srvc_def_name=service_definition_name),
                "service-type _airplay._tcp.local",
                "service-type _raop._tcp.local",
                "service-type _ipp._tcp.local",
                "service-type _afpovertcp._tcp.local",
                "service-type _nfs._tcp.local",
                "service-type _ssh._tcp.local",
                "service-type _dpap._tcp.local",
                "service-type _daap._tcp.local",
                "service-type _ichat._tcp.local",
                "service-type _presence._tcp.local",
                "service-type _http._tcp.local",
                "service-type _ipps._tcp.local",
                "service-type _printer._tcp.local",
                "service-type _smb._tcp.local",
                "service-type _ftp._tcp.local"
            ])
            # Following if block is used for creating multiple service list with direction and definition name
        if isinstance(service_list, list):
            for i in range(len(service_list)):
                config.extend([
                    "mdns-sd service-list {srvc_list_name} {direction}".format(
                        srvc_list_name=service_list[i],
                        direction=direction[i]),
                    "match {srvc_def_name}".format(
                        srvc_def_name=service_definition_name)
                ])
        # Following else block is used for creating only one service list with direction and definition name
        else:
            if service_list != None:
                config.extend([
                    "mdns-sd service-list {srvc_list_name} {direction}".format(
                        srvc_list_name=service_list,
                        direction=direction),
                    "match {srvc_def_name}".format(
                        srvc_def_name=service_definition_name)
                ])                          
        # Following if block is used for creating multiple service policies with service lists attaching them
            config.extend([
                "mdns-sd service-list {srvc_list_name} {direction}".format(
                    srvc_list_name=service_list,
                    direction=direction),
                "match {srvc_def_name}".format(
                    srvc_def_name=service_definition_name)
            ])
            # Following if block is used for creating multiple service policies with service lists attaching them
        if policy_name != None:
            for policy, dirctn in policy_name.items():
                config.extend(["mdns-sd service-policy {policy_name}".format(policy_name=policy)])
                count = 0
                # Following for loop is used for attaching multiple service lists to one policy
                for plcy in range(len(dirctn) // 2):
                    config.extend(["service-list {srvc_list_name} {direction}".format(
                        srvc_list_name=dirctn[count],
                        direction=dirctn[count + 1])
                    ])
                    count=count+2
        # Following if block is used for creating service list with message                       
        if service_list_msg_type != None:        
                    count = count + 2
                    # Following if block is used for creating service list with message
        if service_list_msg_type != None:
            config.extend([
                "mdns-sd service-list {srvc_lst_msg_type} {dirctn_msg_type}".format(
                    srvc_lst_msg_type=service_list_msg_type,
                    dirctn_msg_type=direction_msg_type),
                "match {srvc_def_name} message-type {msg_type}".format(
                    srvc_def_name=service_definition_name,
                    msg_type=message_type)
            ])
            # Following if block is used for creating service list with filter
        if service_list_filter != None:
            config.extend([
                "mdns-sd service-list {srvc_lst_filter} {dirctn_filter_type}".format(
                    srvc_lst_filter=service_list_filter,
                    dirctn_filter_type=direction_filter_type),
                "match {srvc_def_name} location-filter {filter_name}".format(
                    srvc_def_name=service_definition_name,
                    filter_name=filter_name)
            ])
            # Following if block is used for again creating new service policy for adding new service list (msg and filter) to paricular policy
        if policy_name1 != None:
            for policy, dirctn in policy_name1.items():
                config.extend(["mdns-sd service-policy {policy_name1}".format(policy_name1=policy)])
                count = 0
                for plcy in range(len(dirctn) // 2):
                    config.extend(["service-list {srvc_list_name} {direction}".format(
                        srvc_list_name=dirctn[count],
                        direction=dirctn[count + 1])
                    ])
                    count = count + 2
        device.configure(config)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mdns. Error:\n{error}".format(error=e)
        )


def unconfigure_mdns_config(
        device,
        policy_name=None,
        service_list=None,
        direction=None,
        service_definition_name=None,
        service_list_filter=None,
        direction_filter_type=None,
        filter_name=None,
        service_list_msg_type=None,
        direction_msg_type=None
):
    """ Unconfigure mDNS (Multicast Domain Name System) services on agent and service peer

        Args:
            device ('obj'): device to configure
            policy_name ('list', optional): dict with all Policy names and directions. Default value is None
            service_list ('list', optional): list with all services. Default value is None
            direction ('str', optional): direction. Default value is None
            service definition ('str', optional): service definition name. Default value is None
            service_list_filter ('str', optional): creating service list for filter type. Default value is None
            direction_filter_type ('str', optional): creating direction for filter type. Default value is None
            filter_name ('str', optional): filter name. Default value is None
            service_list_msg_type ('str', optional): creating service list for msg type. Default value is None
            direction_msg_type ('str', optional): creating direction for msg type. Default value is None

        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
    """
    log.debug("Removing mdns configurations on globally")

    try:
        config = ["no mdns-sd gateway"]

        # Following if block is used for removing multiple service policies and single policy
        if isinstance(policy_name, list):
            for policy in range(len(policy_name)):
                config.extend(["no mdns-sd service-policy {policy_name}".format(policy_name=policy_name[policy])])
        else:
            config.extend(["no mdns-sd service-policy {policy_name}".format(policy_name=policy_name)])
            # Following if block is used for removing multiple service lists and single service list
        if isinstance(service_list, list):
            for service in range(len(service_list)):
                config.extend(["no mdns-sd service-list {srvc_list_name} {direction}".format(
                    srvc_list_name=service_list[service],
                    direction=direction[service])
                ])
        else:
            config.extend(["no mdns-sd service-list {srvc_list_name} {direction}".format(
                srvc_list_name=service_list,
                direction=direction)
            ])
            # Following if block is used for removing service lists and filter
        if service_list_filter != None:
            config.extend([
                "no mdns-sd service-list {srvc_lst_filter} {dirctn_filter_type}".format(
                    srvc_lst_filter=service_list_filter,
                    dirctn_filter_type=direction_filter_type),
                "no mdns-sd location-filter {filter_name}".format(
                    filter_name=filter_name)
            ])
            # Following if block is used for removing service lists and messages
        if service_list_msg_type != None:
            config.extend(["no mdns-sd service-list {srvc_lst_msg_type} {dirctn_msg_type}".format(
                srvc_lst_msg_type=service_list_msg_type,
                dirctn_msg_type=direction_msg_type)
            ])
        # Below config used removing service definition
        config.extend(["no mdns-sd service-definition {srvc_def_name}".format(
            srvc_def_name=service_definition_name)
        ])
        device.configure(config)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not remove mdns configure. Error:\n{error}".format(error=e)
        )


def configure_vlan_agent(device, vlan, policy, active_query_timer, transport_way, vlan_src_intf=None):
    """ Configures vlan on mDNS(Multicast Domain Name System) agent

        Args:
            device (`obj`): Device object
            vlan ('int'): Vlan ID
            policy ('str'): Policy name
            active_query_timer ('int'): Active Query timer value
            transport_way ('str'): Transport way (ipv4,ipv6 or both, which need to allow)
            vlan_src_intf('int', optional): Source interface vlan. Default value is None

        Returns:
            N/A
        Raises:
            SubCommandFailure: Failed executing configure commands
    """
    log.debug("Configuring vlan on agent globally")

    try:
        config = [
            "vlan configuration {vlan_id}".format(vlan_id=vlan),
            "mdns-sd gateway",
            "service-policy {policy}".format(policy=policy),
            "active-query timer {active_query_timer}".format(
                active_query_timer=active_query_timer),
        ]
        if vlan_src_intf != None:
            config.extend([
                "source-interface vlan {vlan_src_intf}".format(
                    vlan_src_intf=vlan_src_intf),
                "service-inst-suffix {vlan_src_intf}".format(
                    vlan_src_intf=vlan_src_intf)
            ])
        config.extend(["transport {ipv4_ipv6_both}".format(ipv4_ipv6_both=transport_way)])
        device.configure(config)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure Vlan. Error:\n{error}".format(error=e)
        )


def unconfigure_mdns_vlan(device, vlan):
    """ Removing mdns-sd gateway from vlan configuartion (mDNS-Multicast Domain Name System)

        Args:
            device (`obj`): Device object
            vlan ('int'): Vlan ID value
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Removing vlan configs on mDNS globally")

    try:
        device.configure([
            "vlan configuration {vlan_id}".format(vlan_id=vlan),
            "no mdns-sd gateway"
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not remove vlan configs from mDNS. Error:\n{error}".format(error=e)
        )


def configure_vlan_sp(device, vlan, policy, active_query_timer, src_vlan, ip_address, transport_way):
    """ Configures vlan on SP(service peer)

        Args:
            device (`obj`): Device object
            vlan ('int'): Vlan ID
            policy ('str'): Policy name
            active_query_timer ('int'): Active Query timer value
            src_vlan ('int'): Source interface vlan id
            ip_address ('str'): Ip address (ipv4 or ipv6)
            transport_way ('str'): Transport way (ipv4,ipv6 or both, which need to allow)

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring vlan on sp globally")

    try:
        device.configure([
            "vlan configuration {vlan_id}".format(vlan_id=vlan),
            "mdns-sd gateway",
            "service-policy {policy}".format(policy=policy),
            "active-query timer {active_query_timer}".format(
                active_query_timer=active_query_timer),
            "source-interface vlan {src_vlan}".format(src_vlan=src_vlan),
            "sdg-agent {ip_address}".format(ip_address=ip_address),
            "transport {ipv4_ipv6_both}".format(ipv4_ipv6_both=transport_way)
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure Vlan. Error:\n{error}".format(error=e)
        )


def configure_mdns_location_filter(device, location_filter, location_group, vlan, role):
    """ Configures location filter details on vlan

        Args:
            device ('obj'): device to use
            location_filter ('str'): location filter name
            location_group ('str'): location group name
            vlan ('int'): Vlan id
            role ('str'): Role name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Configuring location filter {loc_filter} details "
        "on {vlan_id}".format(loc_filter=location_filter, vlan_id=vlan)
    )
    try:
        device.configure([
            "mdns-sd location-filter {loc_filter}".format(
                loc_filter=location_filter),
            "match location-group {loc_grp} vlan {vlan_id} role {role_name}".format(
                loc_grp=location_group,
                vlan_id=vlan, role_name=role)
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mdns-sd with location-filter"
            "{loc_filter} on vlan {vlan_id}, Error: {error}".format(
                loc_filter=location_filter, vlan_id=vlan, error=e
            )
        )


def configure_mdns_location_group(device, location_group, vlan, interface):
    """ Configures location group details on interface

        Args:
            device ('obj'): device to use
            location_group ('int'): location group name
            vlan ('int'): Vlan id value
            interface ('list'): list of interfaces to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(
        "Configuring location group {loc_grp} details "
        "on {intf}".format(loc_grp=location_group, intf=interface)
    )
    try:
        config = [
            "mdns-sd location-group {loc_grp} vlan {vlan_id}".format(
                loc_grp=location_group, vlan_id=vlan)
        ]
        if isinstance(interface, list):
            for interf in interface:
                config.extend([
                    "interface {intf}".format(intf=interf)
                ])
        else:
            config.extend(["interface {intf}".format(intf=interface)])

        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mdns-sd with location-group"
            "{loc_grp} interface {interface}, Error: {error}".format(
                loc_grp=location_group, interface=interface, error=e
            )
        )


def unconfigure_mdns_location_group(device, location_group, vlan):
    """ Removing location group details on interface

        Args:
            device ('obj'): device to use
            location_group ('int'): location group name
            vlan ('int'): Vlan id value

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Removing location group details")
    try:
        config = [
            "no mdns-sd location-group {loc_grp} vlan {vlan_id}".format(
                loc_grp=location_group,
                vlan_id=vlan)
        ]
        device.configure(config)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not remove loation-group configs on device. Error:\n{error}".format(error=e)
        )


def configure_mdns_sd_agent(device, timer=None, count=None):
    """ Configures mDNS(Multicast Domain Name System) agent

        Args:
            device (`obj`): Device object
            timer ('int', optional): Timer value. Default value is None
            count ('int', optional): Count value. Default value is None

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring mdns_sd_agent on globally")

    try:
        config = [
            "mdns-sd gateway",
            "mode sdg-agent"
        ]
        if timer != None and count != None:
            config.extend([
                "service-announcement-timer periodicity {timer_val}".format(
                    timer_val=timer),
                "service-announcement-count {count_val}".format(
                    count_val=count),
                "service-query-timer periodicity {timer_val}".format(
                    timer_val=timer),
                "service-query-count {count_val}".format(
                    count_val=count)
            ])
        device.configure(config)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mdns_sd_agent. Error:\n{error}".format(error=e)
        )


def configure_mdns_sd_service_peer(device, vlan, ip_addr, response_timer=None, timer=None, count=None, value=None):
    """ Configures mDNS(Multicast Domain Name System) service peer

        Args:
            device (`obj`): Device object
            vlan ('int'): Vlan value
            ip_addr ('str'): ipv4,ipv6 address
            response_timer ('int', optional): active response timer. Default value is None
            timer ('int', optional): Timer value. Default value is None
            count ('int', optional): Count value. Default value is None
            value ('int', optional): rate limit value . Default value is None

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring mdns_sd_service_peer on globally")

    try:
        config = [
            "mdns-sd gateway",
            "mode service-peer",
            "source-interface vlan {vlan_id}".format(vlan_id=vlan),
            "sdg-agent {ipv4_ipv6}".format(ipv4_ipv6=ip_addr)
        ]
        if response_timer != None:
            config.extend(["active-response timer {resp_timer}".format(resp_timer=response_timer)])
        if timer != None and count != None:
            config.extend([
                "service-announcement-timer periodicity {timer_val}".format(
                    timer_val=timer),
                "service-announcement-count {count_val}".format(
                    count_val=count),
                "service-query-timer periodicity {timer_val}".format(
                    timer_val=timer),
                "service-query-count {count_val}".format(
                    count_val=count)
            ])
        if value != None:
            config.extend(["rate-limit {value}".format(value=value)])

        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mdns_sd_service_peer. Error:\n{error}".format(error=e)
        )


def configure_mdns_trust(device, interface):
    """ Configures location filter details on vlan

        Args:
            device ('obj'): device to use
            interface ('str'): interface
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring mdns-trust on interface")
    try:
        device.configure([
            "interface {intf}".format(intf=interface),
            "mdns-sd trust",
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mdns_trust. Error:\n{error}".format(error=e)
        )


def configure_mdns_service_definition(device, name, srvc_type):
    """ Configure mDNS(Multicast Domain Name System) service definition
        Args:
            device ('obj'): device to use
            name ('str')
            srvc_type ('list'):

        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring mdns service-definition
    """
    log.debug("Configuring mdns service defintion with  name={},srvc_type={}".format(name, srvc_type))

    try:
        for type in srvc_type:
            device.configure([
                "mdns-sd service-definition {}".format(name),
                "service-type  {} ".format(type)
            ])

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure mdns service-definition {name}".format(
                name=name
            )
        )
               
def clear_mdns_cache(device):
    """ Clears mdns cache on device

        Args:
            device ('obj'): device to use
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.execute("clear mdns-sd cache")
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clears mdns cache. Error:\n{error}".format(error=e)
        )
        
def clear_mdns_statistics_all(device):
    """ Clears mdns statistics on device
        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed clearing statistics
    """

    try:
        device.execute("clear mdns-sd statistics all")
        
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not clear mdns statistics'
        )
        
def clear_mdns_statistics_sp_sdg(device):
    """ Clears mdns statistics on sp-sdg
        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed clearing statistics
    """

    try:
        device.execute("clear mdns-sd sp-sdg statistics")
                        
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not clear mdns statistics on sp-sdg'
        )
        
def clear_mdns_statistics_servicepeer(device):
    """ Clears mdns statistics on service-peer
        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed clearing statistics
    """

    try:
        device.execute("clear mdns-sd service-peer statistics")
        
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not clear mdns statistics on service-peer'
        )
        
def configure_mdns_boot_level_license(device, license):

    """ Configures mdns boot level license

        Args:
            device ('obj'): device to use
            license ('str'): license name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring mdns boot level license")
    try:
        device.configure([
            "license boot level network-advantage addon {license}".format(license=license),
            "do write memory"
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mdns license. Error:\n{error}".format(error=e)
        )
        
def configure_mdns_service_record_ttl(device, cache_record_type):

    """ Configures mdns service record ttl

        Args:
            device ('obj'): device to use
            cache_record_type ('str'): cache record like enhanced or original
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring mdns service record ttl")
    try:
        device.configure([
            "mdns-sd gateway",
            "service-record-ttl {cache_record_type}".format(cache_record_type=cache_record_type)
            
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mdns ttl. Error:\n{error}".format(error=e)
        ) 


def unconfigure_mdns_location_filter(device, location_filter):
    """ Unconfigures location filter details on vlan
        Args:
            device ('obj'): device to use
            location_filter ('str'): location filter name

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug(
        "Unconfiguring location filter {loc_filter} details ".format(loc_filter=location_filter)
    )
    try:
        device.configure([
            "no mdns-sd location-filter {loc_filter}".format(
                loc_filter=location_filter)
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure mdns-sd with location-filter"
            "{loc_filter}, Error: {error}".format(
                loc_filter=location_filter,  error=e
            )
        )

def configure_mdns_service_receiver_purge_timer(device, timer):

    """ Configures mdns service-receiver-purge timer

        Args:
            device ('obj'): device to use
            timer ('int'): timer value
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring mdns service receiver purge timer")
    try:
        device.configure([
            "mdns-sd gateway",
            "service-receiver-purge timer {timer}".format(timer=timer)
            
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mdns purge timer. Error:\n{error}".format(error=e)
        ) 
        
def configure_mdns_query_response_mode(device, mode):

    """ Configures mdns query-response mode

        Args:
            device ('obj'): device to use
            mode ('str'): mode like recurring or on-demand
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring mdns query-response mode")
    try:
        device.configure([
            "mdns-sd gateway",
            "query-response mode {mode}".format(mode=mode)
            
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mdns query-response mode. Error:\n{error}".format(error=e)
        )

def configure_mdns_service_list(device, name, direction, service_type):
    """ Configure mDNS(Multicast Domain Name System) service list
    
        mdns-sd service-list policie5 IN
        match apple-tv
        end
        
        Args:
            device ('obj'): device to use
            name ('str') : name of the list
            direction ('str'): direction of the list
            service_type ('list'): services names

        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring mdns service-list
    """
    log.debug("Configuring mdns service list with  name={}, direction ={}, service_type={}".format(name, direction, service_type))

    try:
        for type in service_type:
            device.configure([
                "mdns-sd service-list {} {}".format(name, direction),
                "match {}".format(type)
            ])

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure mdns service-list {name}".format(
                name=name
            )
        ) 
        
def unconfigure_match_service_type_mdns_service_list(device, name, direction, service_type):
    """ Unconfigure mDNS(Multicast Domain Name System) service list
    
        mdns-sd service-list policie5 IN
        no match apple-tv
        end
    
        Args:
            device ('obj'): device to use
            name ('str') : name of the list
            direction ('str'): direction of the list
            service_type ('list'): services names

        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring mdns service-list
    """
    log.debug("Removing the match entries from the mdns service list name={}".format(name))

    try:
        for type in service_type:
            device.configure([
                "mdns-sd service-list {} {}".format(name, direction),
                "no match {}".format(type)
            ])

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not unconfigure mdns service-list {name}".format(
                name=name
            )
        )
        
def unconfigure_service_type_mdns_service_definition(device, name, service_type):
    """ Unconfigure mDNS(Multicast Domain Name System) service definition
    
        mdns-sd service-definition custom3
        no service-type  _smb._tcp.local
        end
    
        Args:
            device ('obj'): device to use
            name ('str')
            service_type ('list'):

        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring mdns service-definition
    """
    log.debug("Removing the specific service type from the mdns service defintion with  name={}".format(name))

    try:
        for type in service_type:
            device.configure([
                "mdns-sd service-definition {}".format(name),
                "no service-type {}".format(type)
            ])

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove the services from mdns service-definition {name}".format(
                name=name
            )
        ) 
        
def configure_mdns_controller_service_list(device, name, service_type):
    """ Configure mDNS(Multicast Domain Name System) controller service list
    
        mdns-sd controller service-list contrl-list3
        match apple-tv
        end
    
        Args:
            device ('obj'): device to use
            name ('str') : name of the list
            service_type ('list'): services names

        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring mdns controller service-list
    """
    log.debug("Configuring mdns controller service list with  name={}, service_type={}".format(name, service_type))

    try:
        for type in service_type:
            device.configure([
                "mdns-sd controller service-list {}".format(name),
                "match {}".format(type)
            ])

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure mdns controller service-list {name}".format(
                name=name
            )
        ) 
        
def unconfigure_match_service_type_mdns_controller_service_list(device, name, service_type):
    """ Unconfigure mDNS(Multicast Domain Name System) controller service list
    
        mdns-sd controller service-list contrl-list3
        no match airplay
        end
    
        Args:
            device ('obj'): device to use
            name ('str') : name of the list
            service_type ('list'): services names

        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring mdns controller service-list
    """
    log.debug("Removing the match entries from the controller service list name={}".format(name))

    try:
        for type in service_type:
            device.configure([
                "mdns-sd controller service-list {}".format(name),
                "no match {}".format(type)
            ])

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove match entries from controller service-list {name}".format(
                name=name
            )
        ) 

def configure_controller_service_policy(device, name, service_list):
    """ Configure mDNS(Multicast Domain Name System) controller service-policy
    
        mdns-sd controller service-policy contrl-policy
        service-list contrl-list3
        end
    
        Args:
            device ('obj'): device to use
            name ('str')
            service_list ('list'):

        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring mdns controller service-policy
    """
    log.debug("Configuring mdns controller service-policy with  name={}".format(name))

    try:
        device.configure([
            "mdns-sd controller service-policy {}".format(name),
            "service-list {}".format(service_list)
        ])


    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure mdns controller service-policy {name}".format(
                name=name
            )
        )

def unconfigure_controller_service_policy_service_export(device, name, policy_name):
    """ Unconfigure mDNS(Multicast Domain Name System) controller service-policy
    
        service-export mdns-sd controller DNAC
        no controller-service-policy policy_name contrl-policy
        end
    
        Args:
            device ('obj'): device to use
            name ('str'): controller name
            policy_name ('str'): Policy any name

        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring mdns controller service-policy
    """
    log.debug("Unconfiguring mdns controller service-policy from service export name={},policy_name={}".format(name, policy_name))

    try:
            device.configure([
                "service-export mdns-sd controller {}".format(name),
                "no controller-service-policy {}".format(policy_name)
            ])

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not unconfigure mdns controller service-policy from service export {name}".format(
                name=name
            )
        ) 
       
def configure_mdns_service_peer_group(device,peer_grp_no,policy_name,peer_ip,loc_grp_no,role):
    """ Configures service-peer group details for with peer ip and policy name
    
        mdns-sd service-peer group
        peer-group 3
        service-policy policy44
        service-peer 20.0.0.20 location-group 4096 role bonjour
        end

        Args:
            device ('obj'): device to use
            peer_grp_no ('int'): peer group number to be configured should in be this range <1-1000> 
            policy_name ('str'): policy_name to be mapped to peer
            peer_ip ('str'): service peer ip  to be configured
            loc_grp_no ('str'): location group number which location group of to be allowed
            role ('str'): Role name
        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(
            "Configuring service-peer group details on {peer_grp_no}, for peer {peer_ip}".format(peer_grp_no=peer_grp_no, peer_ip=peer_ip)
            )
    try:
        device.configure([
            "mdns-sd service-peer group",
            "peer-group {peer_grp_no}".format(peer_grp_no=peer_grp_no),
            "service-policy {policy_name}".format(policy_name=policy_name),
            "service-peer {peer_ip} location-group {loc_grp_no} role {role_name}".format(peer_ip=peer_ip,loc_grp_no=loc_grp_no,role_name=role),
            ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mdns-sd with service-peer group "
            "{peer_grp_no} for peer {peer_ip}, Error: {error}".format(
            peer_grp_no=peer_grp_no, peer_ip=peer_ip, error=e
            )
        )

def configure_mdns_active_response_timer(device, timer):
    """ Configure mDNS(Multicast Domain Name System) active response timer
    
        mdns-sd gateway
        active-response timer 20
        end
    
        Args:
            device ('obj'): device to use
            timer ('int'): 5-60 sec

        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring mdns active response timer
    """
    log.debug(" Configuring mdns active response timer ")

    try:
        device.configure([
            "mdns-sd gateway" ,
            "active-response timer {}".format(timer)
        ])
    except SubCommandFailure as e:

        raise SubCommandFailure(

            "Could not configure mdns active response timer {e}"
        )
        
def unconfigure_mdns_active_response_timer(device, timer):
    """ Unconfigure mDNS(Multicast Domain Name System) active response timer
    
        mdns-sd gateway
        no active-response timer 20
        end
    
        Args:
            device ('obj'): device to use
            timer ('int'): 5-60 sec

        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring mdns active response timer
    """
    log.debug(" Unconfiguring mdns active response timer ")

    try:
        device.configure([
            "mdns-sd gateway" ,
            "no active-response timer {}".format(timer)
        ])
    
    except SubCommandFailure as e:

        raise SubCommandFailure(

            "Could not unconfigure mdns active response timer {e}"
        )

def configure_mdns_service_query_timer_periodicity(device, timer):
    """ Configure mDNS(Multicast Domain Name System) service query timer periodicity
    
        mdns-sd gateway
        active-response timer 20
        end
    
        Args:
            device ('obj'): device to use
            timer ('int'): 5-36000 sec

        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring mdns service query timer periodicity
    """
    log.debug(" Configuring mdns service query timer periodicity ")

    try:
        device.configure([
            "mdns-sd gateway" ,
            "service-query-timer periodicity {}".format(timer)
        ])
    except SubCommandFailure as e:

        raise SubCommandFailure(

            "Could not configure mdns service query timer periodicity {e}"
        )
        
def clear_mdns_controller_statistics(device):
    """ Clears mdns controller statistics on SDG
        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed clearing controller statistics
    """

    try:
        device.execute("clear mdns-sd controller statistics")
        
    except SubCommandFailure as e:

        raise SubCommandFailure(

            "Could not clear mdns controller statistics on SDG {e}"
        ) 
        
def configure_mdns_service_policy(device, name, service_list, direction):
    """ Configure mDNS(Multicast Domain Name System) service-policy
        Args:
            device ('obj'): device to use
            name ('str')
            service_list ('list'):

        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring mdns controller service-policy
    """
    log.debug("Configuring mdns service-policy with  name={},service_list={}".format(name, service_list, direction))

    try:
        device.configure([
            "mdns-sd service-policy {}".format(name),
            "service-list {} {}".format(service_list,direction)
        ])
    except SubCommandFailure as e:

        raise SubCommandFailure(

            "Could not configure mdns service-policy {e}"
        )
        
def configure_default_mdns_controller(device, name,cont_addr,cont_src_intf,srvc_list,mat_option,cont_service_policy, msg_type):

    """ Creating default mdns controller
        Args:
            device ('obj'): device to use
            name ('str')
            cont_addr ('str'): controller addresses to be configured
            cont_service_policy ('str'): service-policy to configured
            cont_src_intf ('str'): Default router ID
            srvc_list ('str'):
            mat_option ('str'):
            msg_type ('str'):
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring mdns controller
    """
    log.info(
        "Configuring default mdns controller with name={}, cont_addr={}, cont_service_policy={}, and "
        "cont_src_intf {} srvc_list={} mat_option={} msg_type={}".format(name,cont_addr,cont_service_policy, cont_src_intf, srvc_list, mat_option, msg_type))

    try:
        device.configure([
            "mdns-sd controller service-list {}".format(srvc_list),
            "match {} message-type {}".format(mat_option,msg_type),
            "mdns-sd controller service-policy {}".format(cont_service_policy),
            "service-list {}".format(srvc_list),
            "service-export mdns-sd controller {}".format(name),
            "controller-address {}".format(cont_addr),
            "controller-source-interface {}".format(cont_src_intf),
            ])
    except SubCommandFailure as e:

        raise SubCommandFailure(

            "Could not configure mdns controller {e}"
        ) 

def configure_controller_policy(device, name, service_list):
    """ Configure mDNS(Multicast Domain Name System) controller service-policy
        Args:
            device ('obj'): device to use
            name ('str')
            service_list ('list'):

        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring mdns controller service-policy
    """
    log.debug("Configuring mdns controller service-policy with  name={},service_list={}".format(name, service_list))

    try:
        device.configure([
            "mdns-sd controller service-policy {}".format(name),
            "service-list {}".format(service_list)
        ])
    except SubCommandFailure as e:

        raise SubCommandFailure(

            "Could not configure mdns controller service-policy {e}"
        )

def unconfigure_controller_policy_service_export(device, name, policy_name):
    """ Unconfigure mDNS(Multicast Domain Name System) controller service-policy
        Args:
            device ('obj'): device to use
            name ('str')
            policy_name ('list'):

        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring mdns controller service-policy
    """
    log.debug("Unconfiguring mdns controller service-policy with  name={},policy_name={}".format(name, policy_name))

    try:
        for type in policy_name:
            device.configure([
                "service-export mdns-sd controller {}".format(name),
                "no controller-service-policy {}".format(type)
            ])
    except SubCommandFailure as e:

        raise SubCommandFailure(

            "Could not unconfigure mdns controller service-policy {e}"
        )
        
def unconfigure_mdns_service_policy(device, policy):
    """ Unconfigures mdns service policy

        Args:
            device (`obj`): Device object
            policy ('str'): Policy name

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Unconfigures service policy")

    try:
        device.configure([
            "no mdns-sd service-policy {policy}".format(policy=policy)
        ])
    except SubCommandFailure as e:

        raise SubCommandFailure(

            "Could not unconfigure service-policy {e}"
        ) 
        
def unconfigure_mdns_service_policy_vlan(device, vlan, policy):
    """ Unconfigures mdns service policy from vlan configuration

        Args:
            device (`obj`): Device object
            vlan ('int'): Vlan ID
            policy ('str'): Policy name

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Unconfigures service policy from vlan configuration")

    try:
        device.configure([
            "vlan configuration {vlan_id}".format(vlan_id=vlan),
            "mdns-sd gateway",
            "no service-policy {policy}".format(policy=policy)
        ])
    except SubCommandFailure as e:

        raise SubCommandFailure(

            "Could not unconfigure service-policy from Vlan {e}"
        )

def unconfigure_mdns_gateway_globally(device):
    """ Unconfigure mdns gateway globally
        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed unconfiguring mdns gateway
    """

    try:
        device.configure([
            "no mdns-sd gateway"
        ])
                        
    except SubCommandFailure as e:

        raise SubCommandFailure(

            "Could not configure mdns active response timer {e}"
        )
    
def unconfigure_mdns_trust(device, interface):
    """ Unconfiguring mdns trust on interface

        Args:
            device ('obj'): device to use
            interface ('str'): interface
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Unconfiguring mdns-trust on interface")
    try:
        device.configure([
            "interface {intf}".format(intf=interface),
            "no mdns-sd trust"
        ])
    except SubCommandFailure as e:

        raise SubCommandFailure(

            "Could not unconfigure mdns_trust {e}"
        )
        
def clear_mdns_cache_remote(device):
    """ Clears mdns remote cache on device
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.execute("clear mdns-sd cache remote")
        
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not clears mdns remote cache. Error:\n{error}".format(error=e)
        )
    
def configure_mdns_remote_cache_enable(device):
    """ Enable mDNS(Multicast Domain Name System) remote cache    
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed enabling mdns remote cache
    """
    log.debug(" Enabling mdns-sd remote cache")

    try:
        device.configure([
            "mdns-sd gateway" ,
            "remote-cache-enable"
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not enable mdns remote cache {e}"
        )
    
def unconfigure_mdns_remote_cache_enable(device):
    """ Disable mDNS(Multicast Domain Name System) remote cache
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed disabling mdns remote cache
    """
    log.debug(" Disabling mdns-sd remote cache")

    try:
        device.configure([
            "mdns-sd gateway" ,
            "no remote-cache-enable"
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not disable mdns remote cache {e}"
        )
        
def configure_mdns_remote_cache_max_limit(device, limit):
    """ Configure mDNS(Multicast Domain Name System) remote cache max limit
        Args:
            device ('obj'): device to use
            limit ('int'): remote cache maximum service-instance limit
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring mdns remote cache max limit
    """
    log.debug(" Configuring mdns-sd remote cache max limit")

    try:
        device.configure([
            "mdns-sd gateway" ,
            "remote-cache-max-limit {}".format(limit)
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mdns remote cache max limit {e}"
        )    

def unconfigure_mdns_remote_cache_max_limit(device):
    """ Unconfigure mDNS(Multicast Domain Name System) remote cache max limit
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring mdns remote cache max limit
    """
    log.debug(" Unconfiguring mdns-sd remote cache max limit")

    try:
        device.configure([
            "mdns-sd gateway" ,
            "no remote-cache-max-limit"
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure mdns remote cache max limit {e}"
        )    
        
def configure_mdns_remote_purge_timer(device, timer):
    """ Configure mDNS(Multicast Domain Name System) remote cache purge timer
        Args:
            device ('obj'): device to use
            timer ('int'): remote cache purge timer value
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring mdns remote purge timer 
    """
    log.debug(" Configuring mdns-sd remote cache purge timer")

    try:
        device.configure([
            "mdns-sd gateway" ,
            "remote-cache-purge-timer {}".format(timer)
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mdns remote cache purge timer {e}"
        )    

def unconfigure_mdns_remote_purge_timer(device):
    """ unconfigure mDNS(Multicast Domain Name System) remote cache purge timer
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring mdns remote purge timer 
    """
    log.debug(" Unconfiguring mdns-sd remote cache purge timer")

    try:
        device.configure([
            "mdns-sd gateway" ,
            "no remote-cache-purge-timer"
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure mdns remote cache purge timer {e}"
        )    
    
def configure_mdns_global_service_buffer(device, controllername, mode):
    """ Configure mDNS(Multicast Domain Name System) global service-buffer
        Args:
            device ('obj'): device to use
            controllername ('str'): controller name
            mode ('str'): enable/disable
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring mdns global service-buffer 
    """
    log.debug(" Configuring mdns-sd global service-buffer")

    try:
        device.configure([
            "service-export mdns-sd controller {ctrlName}".format(ctrlName=controllername),
            "global-service-buffer {mde}".format(mde=mode)
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure mdns global service-buffer {e}"
        )    
    
def unconfigure_mdns_global_service_buffer(device, controllername):
    """ unconfigure mDNS(Multicast Domain Name System) global service-buffer
        Args:
            device ('obj'): device to use
            controllername ('str'): controller name
        Returns:
            None
        Raises:
            SubCommandFailure: Failed unconfiguring mdns global service-buffer 
    """
    log.debug(" Unonfiguring mdns-sd global service-buffer")

    try:
        device.configure([
            "service-export mdns-sd controller {ctrlName}".format(ctrlName=controllername),
            "no global-service-buffer"
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure mdns global service-buffer {e}"
        )    