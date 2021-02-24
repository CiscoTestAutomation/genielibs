--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* JUNOS
    * Added Get_Chassis_Slot_Idle_Value
    * Added Get_Services_Accounting_Memory
    * Added Get_Firewall_Counter
    * Added Get_Interface_Snmp_Index
    * Added Get_Route_Push_Value
    * Added Get_Route_Table_First_Label
    * Added Verify_Services_Accounting_Status
    * Added Verify_Services_Accounting_Flow
    * Added Verify_Services_Accounting_Errors
    * Added Verify_Services_Accounting_Aggregation
    * Added Verify_Services_Accounting_Status_No_Output
    * Added Verify_Services_Accounting_Flow_No_Output
    * Added Get_Services_Accounting_Flow_Packets
    * Added Verify_Route_Output_Empty
    * Added Get_Chassis_Fpc_Cpu_Util


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* JUNOS
    * Modified Get_Task_Memory_Information
        * Updated Kwargs
    * Modified Verify_Bfd_Session_Destination_Detail
        * Added Ipv6 Flag
    * Modified Verify_Bfd_Session_Destination_Detail_No_Output
        * Added Ipv6 Flag
    * Modified Get_Route_Push_Value
        * Removed Subnet
    * Modified Verify_Services_Accounting_Aggregation
        * Fixed Code Logic
    * Modified Get_Route_Push_Value
        * Fixed Code Logic
    * Modified Verify_Routing_Ip_Exist
        * Verification If Rt_Destination Doesn'T Exist
    * Modified Verify_No_Log_Output
        * Returned True If Schemaparserempty Exception Comes Up
    * Modified Get_Interface_Traffic_Input_Pps
        * Modified Code To Get Parsed Output
    * Modified Verify_Bfd_Session_Detail
        * Modified Code To Get Parsed Output
    * Modified Get_Chassis_Cpu_Util_Alternative
        * Added Check To See If Log Output Exists
    * Modified Get_Chassis_Cpu_Util_Alternative
        * Updated Code Flow

* APIC
    * Modified Clean_Schema In Stages To Support Controller_Reconnect Timeout

* MODIFIED VALIDATE_CLEAN TO SUPPORT THE 'CLEAN_DEVICES' KEY

* NXOS
    * Modified
        * Changed The P2 Pattern In The Ping_Stage To Accomodate Mds Platform
    * N7K
        * Modified The Imagehandler Class
            * To Fix An Issue With Using The Kickstart Image For Both Boot Variables

* COM
    * Modified Verify_Running_Image Stage
        * To Verify The Running Image Using Either The Image Name (Original Method) Or The Image Hashes (New Method)


