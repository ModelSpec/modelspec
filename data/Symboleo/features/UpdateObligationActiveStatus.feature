Feature: Update Obligation ActiveStatus

  Background:
    Given there is an Obligation with name "obligation"

  Scenario Outline: Update obligation active status successfully
    Given the obligation's status is "Active"
    Given the obligation's active status is "<current_active_status>"
    When the obligation's active status is set to "<new_active_status>"
    Then the obligation's active status shall be "<new_active_status>"

    Examples:
      | current_active_status | new_active_status |
      | InEffect              | Suspension        |
      | Suspension            | InEffect          |

  Scenario Outline: Update obligation active status unsuccessfully because of obligation status
    Given the obligation's status is "<current_status>"
    When the obligation's active status is set to "<new_active_status>"
    Then the system shall raise the error "Cannot set active status when obligation status is <current_status>"
    Then the obligation's active status shall be "Null"

    Examples:
        | current_status          | new_active_status |
        | Start                   | Suspension        |
        | Start                   | InEffect          |
        | Create                  | Suspension        |
        | Create                  | InEffect          |
        | Violation               | Suspension        |
        | Violation               | InEffect          |
        | Discharge               | Suspension        |
        | Discharge               | InEffect          |
        | Fulfillment             | Suspension        |
        | Fulfillment             | InEffect          |
        | UnsuccessfulTermination | Suspension        |
        | UnsuccessfulTermination | InEffect          |