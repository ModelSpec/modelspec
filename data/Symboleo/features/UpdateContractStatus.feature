Feature: Update Contract Status

  Background:
    Given there is a Contract with id "contract"

  Scenario Outline: Update contract status successfully
    Given the contract's status is "<current_status>"
    When the contract's status is set to "<new_status>"
    Then the contract's status shall be "<new_status>"

    Examples:
      | current_status | new_status              |
      | Form           | Active                  |
      | Active         | SuccessfulTermination   |
      | Active         | UnsuccessfulTermination |

  Scenario Outline: Update contract status unsuccessfully because of contract status
    Given the contract's status is "<current_status>"
    When the contract's status is set to "<new_status>"
    Then the system shall raise the error "Invalid status transition from <current_status> to <new_status>"
    Then the contract's status shall remain "<current_status>"

    Examples:
      | current_status          | new_status              |
      | Form                    | SuccessfulTermination   |
      | Form                    | UnsuccessfulTermination |
      | Active                  | Form                    |
      | SuccessfulTermination   | Form                    |
      | SuccessfulTermination   | Active                  |
      | SuccessfulTermination   | UnsuccessfulTermination |
      | UnsuccessfulTermination | Form                    |
      | UnsuccessfulTermination | Active                  |
      | UnsuccessfulTermination | SuccessfulTermination   |

  Scenario Outline: Update a contract status unsuccessfully because of contract active status
    Given the contract's status is "Active"
    Given the contract's active status is "<current_active_status>"
    When the contract's status is set to "<new_status>"
    Then the system shall raise the error "Cannot change status while contract active status is <current_active_status>"
    Then the contract's status shall be "Active"

    Examples:
      | current_active_status | new_status              |
      | Suspension            | SuccessfulTermination   |
      | Suspension            | UnsuccessfulTermination |
      | Unassign              | SuccessfulTermination   |
      | Unassign              | UnsuccessfulTermination |
      | Rescission            | SuccessfulTermination   |
      | Rescission            | UnsuccessfulTermination |