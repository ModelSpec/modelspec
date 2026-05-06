Feature: Update Power Status

  Background:
    Given there is a Power with name "power"

  Scenario Outline: Update a power status successfully
    Given the power's status is "<current_status>"
    Given the power's active status is "<current_active_status>"
    When the power's status is set to "<new_status>"
    Then the power's status shall be "<new_status>"
    Then the power's active status shall be "<new_active_status>"

    Examples:
      | current_status | current_active_status | new_status              | new_active_status |
      | Start          | Null                  | Create                  | Null              |
      | Start          | Null                  | Active                  | InEffect          |
      | Create         | Null                  | Active                  | InEffect          |
      | Create         | Null                  | UnsuccessfulTermination | Null              |
      | Active         | InEffect              | UnsuccessfulTermination | Null              |
      | Active         | InEffect              | SuccessfulTermination   | Null              |

  Scenario Outline: Update a power status Unsuccessfully because of power status
    Given the power's status is "<current_status>"
    When the power's status is set to "<new_status>"
    Then the system shall raise the error "Invalid status transition from <current_status> to <new_status>"
    Then the power's status shall be "<current_status>"

    Examples:
      | current_status          | new_status              |
      | Start                   | UnsuccessfulTermination |
      | Start                   | SuccessfulTermination   |
      | Create                  | Start                   |
      | Create                  | SuccessfulTermination   |
      | Active                  | Start                   |
      | Active                  | Create                  |
      | UnsuccessfulTermination | Start                   |
      | UnsuccessfulTermination | Create                  |
      | UnsuccessfulTermination | Active                  |
      | UnsuccessfulTermination | SuccessfulTermination   |
      | SuccessfulTermination   | Start                   |
      | SuccessfulTermination   | Create                  |
      | SuccessfulTermination   | Active                  |
      | SuccessfulTermination   | UnsuccessfulTermination |

    Scenario Outline: Update a power status Unsuccessfully because power is suspended
      Given the power's status is "Active"
      Given the power's active status is "Suspension"
      When the power's status is set to "<new_status>"
      Then the system shall raise the error "Cannot change status while power is suspended"
      Then the power's status shall be "Active"

      Examples:
        | new_status              |
        | UnsuccessfulTermination |
        | SuccessfulTermination   |