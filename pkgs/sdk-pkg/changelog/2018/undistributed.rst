* Please follow the template we introduced in NOVEMBER.md file.
* Every Trigger/verification need to be added under the corresponding feature.

| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |               |

--------------------------------------------------------------------------------
                               YAML FILES
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                               Features
--------------------------------------------------------------------------------
* Libs
    * NXOS N7K
        * Add abstracted libs of save_bootvar for N7K devices.
    * Generic
        * Raise warning for failures from HA commands return output
        * Update the class UpdateLearntDatabase to not execute commands when
          there are no previous verifications/pts
    * Generic
        * Create libs.utils.triggeractions.verify_ops_or_logic to support check
          Or logic for triggers mapping requirements in verify_ops

--------------------------------------------------------------------------------
                               VERIFICATIONS
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
                               TRIGGERS
--------------------------------------------------------------------------------
* NXOS
    * Update TriggerReloadActiveRp to have one active|ok|standby LC