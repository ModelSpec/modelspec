Feature: Update Power ActiveStatus

  Background:
    Given there is a Power with name "power"

  Scenario Outline: Update power active status successfully
    Given the power's status is "Active"
    Given the power's active status is "<current_active_status>"
    When the power's active status is set to "<new_active_status>"
    Then the power's active status shall be "<new_active_status>"

    Examples:
      | current_active_status | new_active_status |
      | InEffect              | Suspension        |
      | Suspension            | InEffect          |

  Scenario Outline: Update power active status unsuccessfully
    Given the power's status is "<current_status>"
    When the power's active status is set to "<new_active_status>"
    Then the system shall raise the error "Cannot set active status when power status is <current_status>"
    Then the power's active status shall be "Null"

    Examples:
      | current_status          | new_active_status |
      | Start                   | InEffect          |
      | Start                   | Suspension        |
      | Create                  | InEffect          |
      | Create                  | Suspension        |
      | UnsuccessfulTermination | InEffect          |
      | UnsuccessfulTermination | Suspension        |
      | SuccessfulTermination   | InEffect          |
      | SuccessfulTermination   | Suspension        |