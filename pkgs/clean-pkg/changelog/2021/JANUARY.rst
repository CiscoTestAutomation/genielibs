--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* JUNOS
    * Added Verify_Chassis_Environment_Multiple_Status
    * Added Verify_Chassis_Fabric_Summary_Status
    * Added Verify_Chassis_Fabric_Plane_Status
    * Added Verify_Chassis_Environment_Item
    * Added Verify_Chassis_Fabric_Plane_Exists
    * Added Verify_Single_Ospf_Neighbor_Address
    * Added Verify_All_Ospf_Neighbor_States
    * Verify_Single_Ospf3_Neighbor_Address
    * Verify_All_Ospf3_Neighbor_States
    * Verify_Ppm_Transmissions

* NXOS
    * Aci
        * Removed Node_Registration (Moved To Os=Apic)
        * Removed Fabric_Upgrade (Moved To Os=Apic)

* APIC
    * Added Node_Registration (From Os=Nxos, Platform=Aci)
    * Added Fabric_Upgrade (From Os=Nxos, Platform=Aci)
    * Added Fabric_Clean


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* JUNOS
    * Modified Verify_Chassis_Hardware_Item_Present
        * Added Invert Option
    * Modified Verify_Pcap_Mpls_Packet 
        * Get Correct Tos Value For Ipv6 Address
    * Modified Verify_Bfd_Session_Detail  
        * Get Correct Data From Parsed Output
    * Modified Verify_Chassis_Alarm_Output
        * Now Iterates Through List Of Alarm Descriptions
    * Modified Verify_Chassis_Environment_Multiple_Status
        * Now Using Regex To Capture Item Name
    * Modified Verify_Chassis_Fabric_Summary_Status
        * Changed Type Of Variables To Str When Doing Comparison
    * Modified Verify_Chassis_Fabric_Plane_Status
        * Checked Dq Returned Empty List, If So Skip That Iteration
    * Modified Verify_Log_Exists
        * Increased Max Time
    * Updated Verify_Ospf_Neighbor_State
        * Added Neighbor_Address Parameter
    * Added Verify_Ospf3_Neighbor_State
        * Added Neighbor_Address Parameter
    * Modified Verify_Chassis_Alarm_Output
        * Added Loop Through List To Properly Check Alarm Description
    * Modified Verify_Chassis_Environment_Item
        * Returned None Value If Key Doesn'T Exist
        * Returned None Value If Key Doesn'T Exist
    * Modified Verify_Pcap_Mpls_Packet
        * Added Ipv6_Flag As Parameter

* NXOS
    * Aci
        * Modified Fabric_Clean To Remove Aci_Device_Type From Schema
    * N7K
        * Modified Imagehandler
            * To Fix A Bug With Passing Image To Verify_Running_Image

* APIC
    * Modified Fabric_Clean To Remove Aci_Device_Type From Schema
    * Modified Imagehandler
        * To Fix A Bug With Passing Image To Verify_Running_Image

* COM
    * Modified Copy_To_Device
        * To Copy The Image If Unable To Determine If Image Already Exists On The Device
    * Modified Device_Recovery
        * To Make Breakboot Patterns Optional For Tftpboot
    * Modified Copy_To_Device
        * To Fix A Bug Where It Would Not Copy Tertiary Images If The First Image Copy Was Skipped
    * Modified Copy_To_Device Stage
        * Fixed A Bug When Copying More Than One File, Every File But The Last Would Get Copied More Than Once
    * Modified Device_Recovery
        * To Properly Rollup The Results

* IOSXE
    * Modified Recovery Code To Handle If The Grub_Activity_Pattern Is Not Provided

* UTILS
    * Modified Validate_Clean
        * Validate_Clean Now Accepts A String Instead Of A Dict For Loading
        * Validate_Clean No Longer Parses Environment-Dependent Markup


