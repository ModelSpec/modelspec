Feature: Update Contract Active Status

  Background:
    Given there is a Contract with id "contract"

  Scenario Outline: Update contract active status successfully
    Given the contract's status is "Active"
    Given the contract's active status is "<current_active_status>"
    When the contract's active status is set to "<new_active_status>"
    Then the contract's active status shall be "<new_active_status>"

    Examples:
      | current_active_status | new_active_status |
      | InEffect              | Suspension        |
      | InEffect              | Unassign          |
      | InEffect              | Rescission        |
      | Suspension            | InEffect          |
      | Unassign              | InEffect          |

  Scenario Outline: Update contract active status unsuccessfully because of contract status
    Given the contract's status is "<current_status>"
    When the contract's active status is set to "<new_active_status>"
    Then the system shall raise the error "Cannot set active status when contract status is <current_status>"
    Then the contract's active status shall be "Null"

    Examples:
      | current_status          | new_active_status |
      | Form                    | InEffect          |
      | Form                    | Suspension        |
      | Form                    | Unassign          |
      | Form                    | Rescission        |
      | SuccessfulTermination   | InEffect          |
      | SuccessfulTermination   | Suspension        |
      | SuccessfulTermination   | Unassign          |
      | SuccessfulTermination   | Rescission        |
      | UnsuccessfulTermination | InEffect          |
      | UnsuccessfulTermination | Suspension        |
      | UnsuccessfulTermination | Unassign          |
      | UnsuccessfulTermination | Rescission        |

  Scenario Outline: Update contract active status unsuccessfully because of contract active status
    Given the contract's status is "Active"
    Given the contract's active status is "<current_active_status>"
    When the contract's active status is set to "<new_active_status>"
    Then the system shall raise the error "Invalid active status transition from <current_active_status> to <new_active_status>"
    Then the contract's active status shall be "<current_active_status>"

    Examples:
      | current_active_status | new_active_status |
      | Suspension            | Unassign          |
      | Suspension            | Rescission        |
      | Unassign              | Suspension        |
      | Unassign              | Rescission        |
      | Rescission            | InEffect          |
      | Rescission            | Suspension        |
      | Rescission            | Unassign          |