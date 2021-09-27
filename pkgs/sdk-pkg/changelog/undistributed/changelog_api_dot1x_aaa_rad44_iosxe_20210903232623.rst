--------------------------------------------------------------------------------
                                 New
--------------------------------------------------------------------------------
* IOSXE
    * Added API configure_radius_attribute_6(device)
    * Added API unconfigure_radius_attribute_6(device)  
    * Added API configure_any_radius_server(device, server_name, addr_type, address, authport, acctport, secret)
    * Added API unconfigure_any_radius_server(device, server_name)
    * Added API configure_radius_server_group(device, servergrp, rad_server)
    * Added API unconfigure_radius_server_group(device, servergrp)
    * Added API configure_aaa_new_model(device)
    * Added API configure_aaa_default_dot1x_methods(device,server_grp,group_type='group',group_type2='',server_grp2='')
    * Added API unconfigure_aaa_default_dot1x_methods(device)
    * Added API configure_aaa_login_method_none(device,servergrp)
    * Added API unconfigure_aaa_login_method_none(device,servergrp)
    * Added API configure_wired_radius_attribute_44(device)
    * Added API unconfigure_wired_radius_attribute_44(device)
    * Added API configure_radius_interface(device, interface)
    * Added API unconfigure_radius_interface(device, interface)
    * Added API get_running_config_section_attr44(device, option)  
    * Added API verify_test_aaa_cmd(device, servergrp, username, password, path)  
    * Added API configure_interface_switchport_voice_vlan(device, interface, vlan)
    * Added API unconfigure_dot1x_supplicant(device, profile_name, intf, eap_profile=''):
    * Added API unconfigure_dot1x_system_auth_control(device):
    * Added API configure_authentication_host_mode(device,mode,intf,style='legacy'):
    * Added API unconfigure_authentication_host_mode(device,mode,intf,style='legacy'):
    * Added API configure_authentication_order(device,order,intf):
    * Added API unconfigure_authentication_order(device,order,intf):
    * Added API configure_authentication_priority(device,priority,intf):
    * Added API unconfigure_authentication_priority(device,priority,intf):
    * Added API configure_authentication_port_control(device,control,intf,style='legacy'):
    * Added API unconfigure_authentication_port_control(device,control,intf,style='legacy'):
    * Added API configure_authentication_periodic(device,intf):
    * Added API unconfigure_authentication_periodic(device,intf):
    * Added API configure_authentication_timer_reauth(device,value,intf):
    * Added API unconfigure_authentication_timer_reauth(device,value,intf):
    * Added API configure_auth_method(device,value,intf):
    * Added API unconfigure_auth_method(device,value,intf):
                                                                    
--------------------------------------------------------------------------------
                                 Fix
--------------------------------------------------------------------------------
* IOSXE
    * Modified API configure_dot1x_supplicant(device, interface, cred_profile_name, eap_profile='')
