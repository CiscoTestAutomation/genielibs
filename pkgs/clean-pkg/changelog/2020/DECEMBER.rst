December 2020
=============

December 15
-----------

| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.clean``    |  20.12        |

--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* CLEAN
    * At The End Of Clean All Connection Will Be Destroyed

* COM
    * Added Power_Cycle Stage
    * Modified Apply_Configuration
        * To Add Argument 'Skip_Copy_Run_Start'

* IOSXE
    * Added Grub Menu Booting During Device Recovery

* JUNOS
    * Added Get_Task_Memory_Information
    * Added Verify_Chassis_Routing_Engine
    * Added Verify_Chassis_Environment_Status
    * Added Verify_Chassis_Alarm_No_Output
    * Added Verify_Chassis_Alarm_Output
    * Added Verify_Chassis_Slot_Missing
    * Added Verify_Log_Multiple_Attributes
    * Added Verify_No_Log_Output
    * Added Get_Chassis_Cpu_Util_Alternative
    * Added Verify_Traffic_Statistics_Data

* NXOS
    * Aci
        * Added Fabric_Upgrade Stage
        * Added Fabric_Clean Stage
        * Added Node_Registration Stage
    * Added Support For N3K
        * Support N3K For Genie Clean


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* NXOS
    * Fixed Break_Dialog In Device_Discovery
        * To Recover From Autobooting With Bad Image For Nexus7K/9K

* IOSXR
    * Fixed Break_Dialog In Device_Discovery
        * To Recover From Autobooting With Bad Image

* DEVICE RECOVERY
    * Modified Ctrl-C Code For Nxos
        * To Bring The Device To Loader Mode Properly

* JUNOS
    * Modified Verify_Bgp_Updown_Time
        * Returned True As Soon As Passed Status Is Reached, Instead Of Executing Another Iteration
    * Modified Verify_Ping
        * Added Parameters Tos, Size, And Ping_Size.
        * Added New Command 'Ping {Address} Source {Source} Size {Size} Count {Count} Tos {Tos} Rapid'

* STAGES
    * Modified Delete_Backup_From_Device
        * Removed Error Pattern Which Is Not Needed

* COM
    * Modified Copy_To_Device Stage
        * Enhanced Ha Device Support And Check/Cleanup Disk Space On Standby Rp
    * Modified Copy_To_Device Stage
        * To Enable Server Address Resolution From Testbed.Servers Block


