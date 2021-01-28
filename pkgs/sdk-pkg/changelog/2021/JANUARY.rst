--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* NXOS
    * Aci
        * Removed Get_Aci_Registered_Nodes_In_State (Moved To Os=Apic)
        * Removed Verify_Aci_Registered_Nodes_In_State (Moved To Os=Apic)
        * Removed Execute_Register_Nodes (Moved To Os=Apic)
        * Removed Execute_Clean_Controller_Fabric (Moved To Os=Apic)
        * Removed Execute_Clear_Firmware_Repository (Moved To Os=Apic)
        * Removed Execute_Install_Controller_Group_Firmware (Moved To Os=Apic)
        * Removed Execute_Install_Switch_Group_Firmware (Moved To Os=Apic)
        * Removed Get_Firmware_Repository_Images (Moved To Os=Apic)
        * Removed Get_Firmware_Repository_Images_By_Polling (Moved To Os=Apic)
        * Removed Get_Firmware_Upgrade_Status (Moved To Os=Apic)
        * Removed Verify_Firmware_Upgrade_Status (Moved To Os=Apic)
        * Removed Apic_Rest_Post (Moved To Os=Apic)
        * Removed Apic_Rest_Get (Moved To Os=Apic)
        * Removed Apic_Rest_Delete (Moved To Os=Apic)

* APIC
    * Added Get_Aci_Registered_Nodes_In_State (From Os=Nxos, Platform=Aci)
    * Added Verify_Aci_Registered_Nodes_In_State (From Os=Nxos, Platform=Aci)
    * Added Execute_Register_Nodes (From Os=Nxos, Platform=Aci)
    * Added Execute_Clean_Controller_Fabric (From Os=Nxos, Platform=Aci)
    * Added Execute_Clear_Firmware_Repository (From Os=Nxos, Platform=Aci)
    * Added Execute_Install_Controller_Group_Firmware (From Os=Nxos, Platform=Aci)
    * Added Execute_Install_Switch_Group_Firmware (From Os=Nxos, Platform=Aci)
    * Added Get_Firmware_Repository_Images (From Os=Nxos, Platform=Aci)
    * Added Get_Firmware_Repository_Images_By_Polling (From Os=Nxos, Platform=Aci)
    * Added Get_Firmware_Upgrade_Status (From Os=Nxos, Platform=Aci)
    * Added Verify_Firmware_Upgrade_Status (From Os=Nxos, Platform=Aci)
    * Added Apic_Rest_Post (From Os=Nxos, Platform=Aci)
    * Added Apic_Rest_Get (From Os=Nxos, Platform=Aci)
    * Added Apic_Rest_Delete (From Os=Nxos, Platform=Aci)

* JUNOS
    * Added Get_Chassis_Fpc_Slot_Numbers
    * Added Get_Interfaces_Terse_Columns
    * Added Verify_Junos_Version
    * Added Get_Services_Accounting_Usage_One_Minute_Load
    * Added Get_Chassis_Fpc_Cpu_Util
    * Added New Apis
        * Get_Interface_Traffic_Stats
        * Get_Lacp_Stats
        * Verify_Interface_Extensive_Stats
        * Verify_Lag_Links
    * Added Verify_Interfaces_Terse_No_Ipv6
    * Created Verify_Interface_Minimum_Links And Verify_Interface_Minumum_Bandwidth
        * Verify The Minimum Links Or Bandwidth Needed Via Show Interfaces {Interface} Extensive
    * Created Verify_Interface_Protocol
        * Verify Protocol Shown Via Show Interfaces Terse {Interface}
    * Created Verify_Interface_Pps
        * Verify Interface Packets Via Show Interfaces {Interface} Extensive
    * Created Verify_Lacp_Interface
        * Verify If There Is Expected_Interface Via Show Lacp Interfaces {Interface} 
    * Created Get_Laser_Output_Stats
        * Get The Traffic Stats Of Given Interface Via Show Interfaces Diagnostics Optics {Interface}
    * Added Verify_Lacp_Role_Activity
        * Verify Interfaces Roles And Activities Via Show Lacp Interfaces {Interface}
    * Added Get_Interface_Network_Address
        * Get Interface Network Address From Device
    * Added Get_Route_Nexhop
        * Get Nexthops Of Route From Routing Table
    * Updated Get_Address_Without_Netmask
        * Support To Get Link-Local Address For Ipv6
    * Added Verify_Ospf_Route_Nexthop
        * Verifies Nexthop Of Ospf Route
    * Added Verify_Ospf_Neighbor_Address
        * Verifies Ospf Neighbors Address
    * Added Verify_Ospf3_Route_Nexthop
        * Verifies Nexthop Of Ospf Route
    * Added Verify_Ospf3_Neighbor_Address
        * Verifies Ospf Neighbors Address
    * Added Verify_Bgp_Peer_Address
        * Verify Bgp Peer State
    * Added Verify_Bgp_All_Peer_State
        * Verify Bgp All Peer State
    * Added Verify_Bfd_Session_Count
        * Verify Bfd Session Count
    * Added Get_Ospf_Neighbor_Count
        * Get Ospf Neighbors Count
    * Added Get_Ospf3_Neighbor_Count
        * Get Ospf3 Neighbors Count
    * Added Get_Route_Count
        * Get Total Route Count For Each Table Via `Show Route Target_Route Extensive`
    * Added Get_Route_Uptime
        * Get Uptime Of Active Route In Routing Table
    * Added Verify_Task_Replication
        * Verifies Task Replication Info
    * Added Get_Show_Output_Line_Count
        * Count Number Of Line From Show Command Output
    * Added Verify_Log_Contain_Keywords
        * Verify If Keywords Are In Log Messages
    * Added Verify_Lacp_Interface_Receive_State
    * Added Get_Firewall_Counter
        * Get Specific Field Value From Show Firewall Counter Filter
    * Added Get_Interface_Field
        * Get Specific Field Value From Show Interfaces
    * Added Get_Route_Mpls_Labels
        * Get Mpls Labels From Routing Table
    * Added Get_Services_Accounting_Status
        * Get Value Of Field From Show Services Accounting Status
    * Added Get_Services_Accounting_Flow
        * Get Value Of Field From Show Services Accounting Flow
    * Added Get_Services_Accounting_Errors
        * Get Value Of Field From Show Services Accounting Errors
    * Added Get_Services_Accounting_Aggregation_Template_Field
        * Get Value Of Field From Show Service Accounting Aggregation Template Template-Name {Template-Name} Extensive
    * Added Verify_Interface_Hold_Time

* IOSXE
    * Added Verify_Bfd_Neighbors_Details
    * Added Verify_Bfd_Neighbors_Details_No_Output
    * Added Get_Ipv6_Interface_Link_Local_Address
    * Added Api Delete_Files
        * Delete Files On Device By Givin Locations/Filenames
    * Added Get_Ipv6_Interface_Ip_Address

* IOSXR
    * Added Verify_Bfd_Session_Destination
    * Added Verify_Bfd_Session_Destination_Detail
    * Added Verify_Bfd_Session_Destination_Detail_No_Output
    * Added Get_Ipv6_Interface_Ip_Address

* UTILS
    * Added Verify_Keywords_In_Output
        * Verify If Keywords Are In Output


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* JUNOS
    * Modified Get_Chassis_Cpu_Util_Alternative
        * Added Support For Expected_Slot
    * Modified Get_Chassis_Memory_Util
        * Added Support For Expected_Slot
    * Modified Verify_Bfd_Session_Detail
        * Added Support For Expected_Session_Detect_Time And Expected_Remote_State
    * Modified Get_Bgp_Summary_Neighbor_State_Count
        * Updated Logic For State Count
    * Modified Verify_Chassis_Power_Item_Present To Used Dq
    * Modified Verify_Chassis_Power_Item_Present To Handle Empty Output
    * Modified Verify_Chassis_Environment_Present
        * Handled Case When Search Not Found
    * Modified Verify_Chassis_Environment_Component_Present
        * Handled No Parser Output
    * Modified Clear_Bgp_Neighbor_Soft
        * Added An Optional Argument 'Fail_Regex=None'.
    * Modified Get_Ddos_Protection_Arrival_Rate
        * Wrong Show Command Updated
    * Modified Verify_Chassis_Fan_Tray_Present
        * Added An Optional Argument 'Invert=False'.
    * Modified Verify_Chassis_Pic_Exists_Under_Mic
        * Enhanced The Invert Condition To Avoid Redundant Loop
    * Modified Verify_No_Log_Output
        * Enhanced The Api To Handle '{Master}' In Log Output
    * Modified Verify_Chassis_Mic_Exists_Under_Fpc
        * Fixed An Error In Logic.
    * Modified Verify_Interface_Output_Pps
        * Enhance The Api To Support Special Case.
    * Modified Clear_Ospf_Neighbor And Clear_Ospf3_Neighbor
        * Added Argument 'Fail_Regex'
    * Modified Verify_Chassis_No_Alarms
        * Enhance The Api To Support 'No-Active-Alarms' Output
    * Modified Verify_Chassis_Alarms_No_Error And Verify_Chassis_No_Error_Fpc_Mic
        * Fixed The Code Because The Corresponding Parser Is Updated
    * Modified Verify_No_Log_Output
        * Changed Command From 'Show Log {File_Name} | Match "{Match}"' To 'Show Log {File_Name} | Except "Show Log" | Match "{Match}"'
    * Updated Get_Interface_Ip_Address
        * Added Argument 'Link_Local'
    * Updated Verify_Ping
        * Added Argument 'Rapid'
    * Modified Verify_Chassis_Usb_Flag_Exists
        * Fixed Code Error And Fixed The Indentation
    * Modified Verify_Chassis_Environment_Present
        * Enhanced The Logic
    * Modified Verify_Ping
        * Added An Argument Do_Not_Fragment

* IOSXE
    * Added Verify_Bfd_Neighbors_Details_Session_State
    * Added Verify_Bfd_Neighbors_Details_Registered_Protocols
    * Added Get_Ipv6_Interface_Link_Local_Address

* IOSXR
    * Added Verify_Bfd_Session_Destination_Details_Session_State
    * Added Verify_Bfd_Session_Destination_Details_Client
    * Added Verify_Bfd_Ipv6_Session_Destination_Details_Session_State
    * Added Verify_Bfd_Ipv6_Session_Destination_Details_Client
    * Added Verify_Route_Known_Via

* COM
    * Modified Free_Up_Disk_Space
        * To Continue Deleting Images If One Fails

* LINUX
    * Updated Execute_By_Jinja2
        * Added Support For Post_Commands, Failure_Commands As Argument

* PROCESSOR
    * Modified Delete_Configuration To Learn Management Interface Dynamically

* UTILS
    * Modified Get_Interface_From_Yaml
        * Added Docstring
        * Allowed Passing It An Alias

* NXOS
    * Modified Execute_Install_Switch_Group_Firmware
        * To Handle The Controller Not Responding While Verifying Switch Group Install

* COMMON
    * Modified The Matching Pattern For Execute_Copy_To_Running_Config
    * Modified Get_Interface_From_Yaml To Be More Generic For Interface Name
    * Modified Get_Interface_From_Yaml To Support Link Name


