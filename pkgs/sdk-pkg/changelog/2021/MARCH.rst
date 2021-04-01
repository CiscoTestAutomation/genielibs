--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* JUNOS
    * Modified Get_Firewall_Counter
    * Removed Duplicate Verify_Bgp_Peer_Address
    * Modified Get_Interface_Snmp_Index
        * Removed .Split('.')[0] From Command Parsing
    * Modified Verify_File_Details_Exists
    * Modified Verify_Services_Accounting_Flow
    * Modified Get_Route_Table_First_Label
    * Modified Get_Route_Push_Value
    * Modified Verify_Services_Accounting_Aggregation
    * Modified Verify_Task_Replication

* ABSTRACTED_LIBS
    * Modified Post_Execute_Command Processor
        * Made The `Valid_Section_Results` Argument Work As Intended

* IOSXE
    * Modified Triggerissu To Set The 'Device.Filetranser_Attributes' Attribute If Run Through Run_Genie_Sdk
    * Modified Verify_Chassis_Alarm_Output
        * Fixed Broken Functionality
    * Modified Write_Erase_Reload_Device
        * Moved Error Pattern Settings To Unicon
    * Modified Execute_Install_Package
        * To Ensure The Device Is In The Enable State After Reload
    * Modified Verify_Ping

* BLITZ
    * If Parent Keys Are Not Returned In Get-Config Of Empty Nested List Pass Test.
    * Preventing Possible Exception Of Not Saving A Value
    * Auto-Validation Failed For Edit-Config Of Multiple List Entries In One Rpc.
    * "Parent Keys Are Not Returned" Fix Broke Deleted Leaf Logic.

* NXOS
    * Modified Get_Interfaces_Status

* MAPLE_BLITZ
    * Replacing Xr()Xr Cases In Show Commands

* UTILS
    * Modified Stop Method In Tcpdump
        * To Use Actual Server Name For Searching In Server Block In Testbed Yaml

* GENERAL
    * Moved Reconnect Error Pattern Handling To Unicon


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* IOSXR
    * Added Verify_Interface_State_Down
        * Verify Interface State Is Down And Line Protocol Is Down
    * Asr9K
        * Added Verify_Current_Image
        * Added Get_Software_Version
    * Ncs5K
        * Added Verify_Current_Image
        * Added Get_Software_Version

* Linux
    * Added topic search API which can be used with the decoded output file

* NXOS
    * Added Get_Software_Version

* IOSXE
    * Cat9K
        * Added Verify_Boot_Variable

* COM
    * Added Get_Structure_Output
        * Generate Structure Data From Output Based On Spaces


