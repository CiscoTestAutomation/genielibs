
| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |  20.12        |

--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* IOSXE
    * Modified Execute_Install_Package
        * Added Timeout In Execute Command
    * Modified Get_Platform_Logging
        * Support To Have Include Keywords With Space
        * Catching Schemaemptyparsererror And Returning Empty List
    * Updated Execute_Install_Package To Support Sleep Before Install Command
    * Modified Get_Platform_Core
        * Changed To Using Device.Api.Execute For The Case User Uses Alias With Device Object
    * Modified Decode_Core
        * Changed To Using Device.Api.Execute For The Case User Uses Alias With Device Object
    * Modified Restore_Running_Config
        * Updated Exception Message To Be Inline With Abstracted Apis

* JUNOS
    * Modified Verify_Route_Has_As_Path
        * Removed Possibility For False Positives
    * Modified Execute
        * Added Parameter To Fail Is Regex Is Hit
    * Modified Clear_Bgp_Neighbor
        * Added Parameter For `Fail_Regex`
    * Updated Verify_Log_Exists To Support Match With Pipe
    * Updated Verify_No_Log_Output To Support Match With Pipe
    * Modified Verify_Chassis_Fpc_Slot_State
        * Added A New Argument 'All_Slots' To Support Verifying All Slots States. 
    * Fixed Get_Interface_Speed To Cover More Speed Output
    * Modified Verify_Route_Best_Path
        * Enhanced The If-Condition To Make It Works Properly.
    * Modified Verify_Chassis_Fpc_Slot_State
        * Enhanced The Api To Support Command Show Chassis Environment Fpc
    * Modified Verify_Traceroute_Final_Hop
        * Enhanced If-Confition To Support Various Outputs. 
    * Updated Verify_Interface_Load_Balance
        * Traffic_Upper_Limit_Interfaces And Traffic_Upper_Limit Added As Argument
    * Modified Verify_Interface_Errors
        * Added An Optional Argument 'Expected_Value'
    * Updated Get_Platform_Default_Dir To Add File_Name As Argument

* NXOS
    * Modified To Add Vty For Nxos
        * Added The Capability Of Use Vty As An Option

* BLITZ
    * Fixed The Issue With Negative Testing On Apis In Blitz
    * Fixed The Issue With Continue Equal False In Loop In Blitz
    * Modified Error Message
        * Check Xml Validity For Custom Rpcs And Print Error
    * Modified Create
        * For Edit-Configs, Skip "Create" If Device Is Set To "Report-All" And Leaf Has A Default Value
    * Modified Boolean
        * Check For 0, 1, True, Or False When Checking Boolean Values
    * Modified Identityref
        * If Datatype Is Identityref, Strip Prefix Before Comparing Values
    * Modified Updates
        * Check For Multiple Updates In A Single Gnmi Notification Response
    * Modified Formats
        * Moved "Pause" In Yang Action To After Rpc Is Sent
        * Placed Check For "Negative_Test" Into Appropriate Locations
        * Typo; "Auto-Validate" Should Be "Auto_Validate" (Check For Both)

* PROCESSOR
    * Include_Os, Exclude_Os And Include_Devices Support Added For Delete_Configuration Processor.

* UTILS
    * Modified Verify_Pcap_Dscp_Bits
        * Fixed Rsvp Check In Packet

* XR
    * Modified Configure Unshut In Xr Api
        * Added Prompt_Recovery When Unshut Interface


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* JUNOS
    * Added Verify_Chassis_Fpc_Pic_Status
        * Verify Fpc Pic Status Via Show Chassis Fpc Pic-Status
    * Added Verify_Chassis_Fpc_Pic_Not_Exists
        * Verify Pic Slot Does Not Exist Via Show Chassis Fpc Pic-Status
    * Added Verify_Chassis_Pic_Exists_Under_Mic
        * Verify Pic Exists Under Mic $Mic Of Fpc $Fpc Via Show Chassis Hardware
    * Added Verify_Chassis_Mic_Exists_Under_Fpc
        * Verify Mic $Mic Exists Under Fpc $Fpc Via Show Chassis Hardware
    * Added Verify_Chassis_No_Error_Fpc_Mic
        * Verify No Errored Fpc $Fpc Mic $Mic Via Show Chassis Alarms
    * Added Verify_Chassis_Fan_Tray_Present
        * Verify Fan_Tray_List Is Present In 'Show Chassis Hardware'
    * Added Verify_Chassis_Environment_Present
        * Verify All Item In Fan_Tray_List Have Expected_Status In 'Show Chassis Environment'
    * Added Verify_Chassis_No_Alarms
        * Verify There Are No Alarms Via 'Show Chassis Alarms'
    * Added Clear_Bgp_Neighbor_Soft
        * To Run One Of The Command From 'Clear Bgp Neighbor Soft All' And 'Clear Bgp Neighbor Soft'
    * Added Get_Ddos_Protection_Arrival_Rate
    * Added Get_Pfe_Hardware_Input_Drops
    * Added Verify_Route_Logical_System_Has_No_Output
    * Added Verify_Chassis_Usb_Flag_Exists
        * Verify There Is/Isn'T Use Flag In Given Usb In The Routing Engine Via Show Chassis Hardware Detail
    * Added Verify_Chassis_Slots_Present
        * Executes 'Show Chassis Routing-Engine' And Verifies The Given Slots Are Present
    * Added Verify_Chassis_Slot_State
        * Executes 'Show Chassis Routing-Engine' And Verifies The Given Slots' States
    * Added Verify_Configuration_Hostname
        * Runs 'Show Configuration System Host-Name' And Verifies That The Hostname
    * Added Get_Hostname
        * Runs 'Show Version' And Checks The Hostname
    * Added Get_Route_Summary_Table_Total_Route_Count
    * Added Verify_Chassis_Alarms_No_Error
        * Verify There Are No Error About Target Fpc Via 'Show Chassis Alarms'
    * Added Get_Interfaces_Description
        * Get Description Of Given Interface From 'Show Interfaces Descriptions {Interface}'
    * Added Request_Login_Other_Re In Utils.Py
        * Executes 'Request Routing-Engine Login Other-Routing-Engine'
    * Added Verify_Interface_Total_Queue_Counters_Dropped_Packets
    * Added Get_Ntp_System_Config_Source_Address
    * Added Verify_Traceroute_Final_Hop
        * Verify The Final Hop Is Expected_Final_Hop
    * Added Verify_Traceroute_Intermediate_Hop
        * Verify The Intermediate Hop Is Expected_Intermediate_Hop      
    * Added Verify_No_Interface_Errors
    * Added Verify_Ddos_Statistics
        * Verify Statictis Via Show Ddos-Protection Statistics
    * Added Verify_Configuration_Ddos_Protection_No_Output
        * Verifies There Is No Otuput Via Show Configuration System Ddos-Protection
    * Added Verify_Pcap_Capability
        * Analyzes The Pcap File And Checks The Message From Given_Source To Given_Destination And Verifies There Is Capability Attached
    * Added Verify_Pcap_As_Path
        * Analyzes The Pcap File And Check The Message Advertised From Given_Layer And Verifies That As Path Has Expected_As_Path
    * Added Verify_Route_Four_Byte_As
        * Verify The As Path Has Four_Byte_As Via Show Route Advertising-Protocol Bgp {Interface} {Target_Route}
    * Added Execute
        * Executes Alternative_Command If Command Generates Error.
    * Added Clear_Bgp_Neighbor
        * Provides Two Commands That Clear Bgp Neighbor
    * Added Clear_Ospf_Neighbor
    * Added Clear_Ospf3_Neighbor

* IOSXE
    * Platform
        * Added Get_Stack_Size
        * Added Get_Slot_Model
        * Added Get_Chassis_Type
        * Added Get_Chassis_Sn
        * Added Get_Platform_Type
    * Interface
        * Added Get_Interface_Names
    * Added Cdets_Lookup Api To Decoder Plug-In
        * Get A List Of Cdets Given A Corefile Post-Decode
    * Modified Get_Platform_Core
        * Api Will Not Add `/Core`. User Is Supposed To Have The Location In Default_Dir
        * `Default_Dir` Accept Both String Or List. With List, User Can Provide Multiple Locations
        * Regardless Decoding Or Not, Api Will Delete Core File Ore System-Report If The File Is Successfully Copied To Remove_Device
        * Support System-Report. Api Will Extract System-Report.Tar.Gz And Use Only Core Files For Decode
    * Modified Get_Platform_Core
        * Support To Check/Collect Standby Storage On Ha Device

* NXOS
    * Platform
        * Added Get_Slot_Model
        * Added Get_Chassis_Type
        * Added Get_Chassis_Sn
        * Added Get_Platform_Type
    * Interface
        * Added Get_Interface_Names
    * Added Restore_Running_Config
    * Aci
        * Added Get_Aci_Registered_Nodes_In_State
        * Added Verify_Aci_Registered_Nodes_In_State
        * Added Execute_Register_Nodes
        * Added Execute_Clean_Controller_Fabric
        * Added Execute_Clean_Node_Fabric
        * Added Execute_Clear_Firmware_Repository
        * Added Execute_Install_Controller_Group_Firmware
        * Added Execute_Install_Switch_Group_Firmware
        * Added Get_Firmware_Repository_Images
        * Added Get_Firmware_Repository_Images_By_Polling
        * Added Get_Firmware_Upgrade_Status
        * Added Verify_Firmware_Upgrade_Status
        * Added Copy_To_Device
        * Added

* LINUX
    * Added Extract_Tar_Gz Api
        * User Can Extract Tar.Gz File On Device And Api Returns Extracted Files As List

* UTILS
    * Added Get_Device_Connections_Info
    * Enhanced Verify_Device_Connection_State
        * Support Ha Device To Reconnect

* GENERAL
    * Added Get_Running_Config_All

* COMMON
    * Added Execute Api
        * Wrapper Of Device.Execute Which Find Out Connected Alias And Issue Command

* IOSXR
    * Added Restore_Running_Config

* ABSTRACTED_LIBS
    * Added Reconnect Processor

* POWERCYCLERS
    * Added Esxi Powercycler


