Feature: Update Obligation Status

  Background:
    Given there is an Obligation with name "obligation"

  Scenario Outline: Update an obligation status successfully
    Given the obligation's status is "<current_status>"
    Given the obligation's active status is "<current_active_status>"
    When the obligation's status is set to "<new_status>"
    Then the obligation's status shall be "<new_status>"
    Then the obligation's active status shall be "<new_active_status>"

    Examples:
      | current_status | current_active_status | new_status              | new_active_status |
      | Start          | Null                  | Create                  | Null              |
      | Start          | Null                  | Active                  | InEffect          |
      | Create         | Null                  | Active                  | InEffect          |
      | Create         | Null                  | Discharge               | Null              |
      | Active         | InEffect              | Violation               | Null              |
      | Active         | InEffect              | Discharge               | Null              |
      | Active         | InEffect              | Fulfillment             | Null              |
      | Active         | InEffect              | UnsuccessfulTermination | Null              |
      | Active         | Suspension            | UnsuccessfulTermination | Null              |

  Scenario Outline: Update an obligation status unsuccessfully because of obligation status
    Given the obligation's status is "<current_status>"
    When the obligation's status is set to "<new_status>"
    Then the system shall raise the error "Invalid status transition from <current_status> to <new_status>"
    Then the obligation's status shall be "<current_status>"

    Examples:
      | current_status          | new_status              |
      | Start                   | Discharge               |
      | Start                   | Violation               |
      | Start                   | Fulfillment             |
      | Start                   | UnsuccessfulTermination |
      | Create                  | Start                   |
      | Create                  | Violation               |
      | Create                  | Fulfillment             |
      | Create                  | UnsuccessfulTermination |
      | Active                  | Start                   |
      | Active                  | Create                  |
      | Violation               | Start                   |
      | Violation               | Create                  |
      | Violation               | Active                  |
      | Violation               | Discharge               |
      | Violation               | Fulfillment             |
      | Violation               | UnsuccessfulTermination |
      | Discharge               | Start                   |
      | Discharge               | Create                  |
      | Discharge               | Active                  |
      | Discharge               | Violation               |
      | Discharge               | Fulfillment             |
      | Discharge               | UnsuccessfulTermination |
      | Fulfillment             | Start                   |
      | Fulfillment             | Create                  |
      | Fulfillment             | Active                  |
      | Fulfillment             | Violation               |
      | Fulfillment             | Discharge               |
      | Fulfillment             | UnsuccessfulTermination |
      | UnsuccessfulTermination | Start                   |
      | UnsuccessfulTermination | Create                  |
      | UnsuccessfulTermination | Active                  |
      | UnsuccessfulTermination | Violation               |
      | UnsuccessfulTermination | Discharge               |
      | UnsuccessfulTermination | Fulfillment             |

    Scenario Outline: Update obligation status unsuccessfully because obligation is suspended
      Given the obligation's status is "Active"
      Given the obligation's active status is "Suspension"
      When the obligation's status is set to "<new_status>"
      Then the system shall raise the error "Cannot change status while obligation is suspended"
      Then the obligation's status shall be "Active"

      Examples:
        | new_status              |
        | Violation               |
        | Discharge               |
        | Fulfillment             |