--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* JUNOS
    * Modified Get_Route_Table_Output_Interface
        * Added Exception Handling For Show Command Execution
    * Modified Get_Route_Table_Output_Label
        * Added Exception Handling For Show Command Execution
    * Fixed Verify_Bgp_All_Peer_State
    * Modified Verify_Traffic_Statistics_Data
        * Added Arguments Invert And Ipv4
    * Modified Get_Diagnostics_Optics_Stats
        * Fixed If-Condition To Support Lane Number Is 0
    * Modified Get_Services_Accounting_Aggregation_Template_Field
        * Make Source/Destination Arguments As Optional
    * Modified Verify_Task_Replication
        * Fixed Logic To Return Proper Result
    * Modified Verify_Bgp_Peer_Address
        * Support Another 'Establ' Output
    * Modified Verify_Ping
        * Added Interface Option

* COMMON
    * Verification Of A Single Value From Multiple List Entries In Rpc-Reply Was Failing.
    * Return Value Still Being Processed Even Though "Selected" Is Set To False In Yaml.
    * Modified Yang Pause Handling When Auto-Validating Is Enabled
        * Pause Between Edit-Config And Auto-Validate Get-Config.

* IOSXE
    * Modified Yangexec To Handle Commit Failures
    * Fixed Rpcbuilder Test Cases
    * Modified Configure_Interfaces_Unshutdown
        * Fixed Logic Error
    * Modified Configure_Interfaces_Shutdown
        * Fixed Logic Error
    * Modified Get_Running_Image Api
        * To Get The Real Boot Image If The Boot Image Is Configured To Packages.Conf

* BLITZ
    * List Entry With Only Key Fails Auto-Validation
        * A Get-Config On A List Entry Returns At Least The Keys If Nothing Else.
    * Multiple List Entries With Same Values Are Not Validated
        * Keys Cannot Be Determined On Rpc-Reply And User Was Only Interested In
        * Values, So In This Case We Just Had A Bucket Of Values And Each Entry
        * Matched The First In The Bucket So We Ended Up With
        *  
        * Compare
        * Field-1, Id-1, Xpath-/A/B/C, Value-1234
        * Field-2, Id-2, Xpath-/A/B/C, Value-1234
        * Field-3, Id-3, Xpath-/A/B/C, Value-1234
        *  
        * Found
        * Field-1, Id-1, Xpath-/A/B/C, Value-1234
        * Field-1, Id-1, Xpath-/A/B/C, Value-1234
        * Field-1, Id-1, Xpath-/A/B/C, Value-1234
        *  
        * Only Interested In Xpath/Value And Id Does Not Matter But With Id Included
        * In Match It Was Failing.
        *  
        * User Could Make More Targeted Tests, One For Each Key, But This Test Setup
        * Should Not Fail.

* UTILS
    * Modified Verify_Pcap_Mpls_Packet
        * Handled Crash When Ip Packet Is None

* IOSXR
    * Modified Configure_Interfaces_Unshutdown
        * Fixed Logic Error
    * Modified Configure_Interfaces_Shutdown
        * Fixed Logic Error

* NXOS
    * Modified Configure_Interfaces_Unshutdown
        * Fixed Logic Error
    * Modified Configure_Interfaces_Shutdown
        * Fixed Logic Error


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* JUNOS
    * Added Verify_Ospf_Neighbor_Instance_State_All
    * Added Verify_Ospf3_Neighbor_Instance_State_All
    * Added Verify_Route_Instance_Type
    * Added Verify_Route_Instance_Exists
    * Added Verify_Route_Table_Route_Exists
    * Added Quick_Configure_By_Jinja2
    * Added Verify_Services_Accounting_Flow_Active
    * Added Get_Services_Accounting_Flow_Exported
    * Added Get_Services_Accounting_Flow_Active
    * Added Get_Services_Accounting_Flow_Expired
    * Added Get_Services_Accounting_Usage_Five_Second_Load
    * Added Verify_Bgp_Summary_Instance_Peers_State
    * Added Get_Interface_Ipv4_Address
    * Added Get_Ipv6_Interface_Ip_Address
    * Added Verify_Arp_Interface_Exists
    * Added Verify_Chassis_Fpc_Slot_Port
    * Added Verify_Ipv6_Neighbor_State
    * Modified Get_Bgp_Summary_Neighbor_State_Count
    * Modified Get_Chassis_Fpc_Cpu_Util
        * Fixed Redundant Method
    * Added Verify_Interface_Mtu
        * Verify Mtu Status Via Show Lacp Interfaces {Interface}

* IOSXE
    * Added Verify_Interface_Errors
    * Added Verify_Interface_State_Admin_Up
    * Added Verify_Ping
    * Added Get_Interfaces_Status
    * Modified Api Get_Platform_Core
        * Updated Not To Raise Exception
    * Added Get_Md5_Hash_Of_File
        * To Generate The Md5 Hash Of A File

* IOSXR
    * Added Verify_Interface_State_Up
    * Added Verify_Interface_Errors
    * Added Verify_Interface_State_Admin_Down
    * Added Verify_Interface_State_Admin_Up
    * Added Verify_Ping
    * Added Get_Interfaces_Status
    * Modified Api Get_Platform_Core
        * Added Arguments To Copy Core File To Remote Servers
    * Added Api Scp
    * Added Api Get_Platform_Logging
    * Added Get_Md5_Hash_Of_File
        * To Generate The Md5 Hash Of A File

* NXOS
    * Added Get_Interfaces_Status
    * Modified Api Scp
        * Updated Not To Raise Exception
    * Modified Api Get_Platform_Core
        * Added Arguments And Support More Features
    * Added Api Get_Platform_Logging
    * Added Api Scp
    * Added Get_Md5_Hash_Of_File
        * To Generate The Md5 Hash Of A File

* BLITZ
    * Executing Loop Iterations In Parallel
    * Updating Blitz To Save Variables Globally And Make Them Reusable In Testscript Level
    * All The Step Log Messages In Blitz Are Now Customizable
    * Updated Run_Condition To Work Without Specifying A Function
    * Updated Testbed Handling For Pyats Health Check

* LINUX
    * Added Get_Md5_Hash_Of_File
        * To Generate The Md5 Hash Of A File


