Feature: Update Proposal
  Background:
    Given there is a HomeForTheElderly system
    Given there is a department with id "dept1"
    Given there is a room in department "dept1" with room number 1 and category type "RH" and price 1000
    Given there is a bed in room 1 of department "dept1" with bed number 1
    Given there is a person with id "person" and name "John Doe" and birthdate "1950-01-01" and abilities "requires wheelchair"
    Given there is a proposal for bed 1 of room 1 of department "dept1" to person "person"
    Given the current system date is "2020-01-01"

  Scenario Outline: Updating a proposal's status
    When the status of proposal for bed 1 of room 1 of department "dept1" to person "person" is updated to "<status>"
    Then the system shall not throw an error
    Then the proposal for bed 1 of room 1 of department "dept1" to person "person" shall have status "<status>"

    Examples:
      | status       |
      | waiting      |
      | accepted     |
      | refused      |
      | invalidated  |

  Scenario Outline: Updating a proposal's status with invalid values
    When the status of proposal for bed 1 of room 1 of department "dept1" to person "person" is updated to "<status>"
    Then the system shall throw with error message "<error>"
    Then the proposal for bed 1 of room 1 of department "dept1" to person "person" shall have status "waiting"

    Examples:
      | status  | error                                                                             |
      |         | The status of a proposal must not be empty.                                       |
      | unknown | The status of a proposal must be one of: waiting, accepted, refused, invalidated. |

  Scenario Outline: Validating a proposal
    Given the proposal for bed 1 of room 1 of department "dept1" to person "person" has validated <currentValidated>
    When the validated of proposal for bed 1 of room 1 of department "dept1" to person "person" is updated to <newValidated>
    Then the system shall not throw an error
    Then the proposal for bed 1 of room 1 of department "dept1" to person "person" shall have validated <newValidated>

    Examples:
      | currentValidated | newValidated |
      | false            | true         |
      | true             | false        |
      | false            | false        |
      | true             | true         |

  Scenario: Updating a proposal's bed
    Given there is a bed in room 1 of department "dept1" with bed number 2
    When the bed of proposal for bed 1 of room 1 of department "dept1" to person "person" is updated to bed 2 of room 1 of department "dept1"
    Then the system shall not throw an error
    Then the proposal shall be updated for bed 2 of room 1 of department "dept1" to person "person"
    Then the proposal for bed 1 of room 1 of department "dept1" to person "person" shall no longer exist

  Scenario: Updating a proposal's bed to a non-existent bed
    When the bed of proposal for bed 1 of room 1 of department "dept1" to person "person" is updated to bed 3 of room 1 of department "dept1"
    Then the system shall throw with error message "Bed 3 of room 1 of department \"dept1\" does not exist."
    Then the proposal shall be for bed 1 of room 1 of department "dept1" to person "person"

  Scenario: Updating a proposal's person
    Given there is a person with id "person2" and name "Jane Smith" and birthdate "1950-01-01" and abilities "requires wheelchair"
    When the person of proposal for bed 1 of room 1 of department "dept1" to person "person" is updated to person "person2"
    Then the system shall not throw an error
    Then the proposal shall be updated for bed 1 of room 1 of department "dept1" to person "person2"
    Then the proposal for bed 1 of room 1 of department "dept1" to person "person" shall no longer exist

  Scenario: Updating a proposal's person to a non-existent person
    When the person of proposal for bed 1 of room 1 of department "dept1" to person "person" is updated to person "person3"
    Then the system shall throw with error message "Person \"person3\" does not exist."
    Then the proposal shall be for bed 1 of room 1 of department "dept1" to person "person"

  Scenario: Updating a proposal that does not exist
    When the status of proposal for bed 1 of room 1 of department "dept1" to person "person2" is updated to "accepted"
    Then the system shall throw with error message "Proposal for bed 1 of room 1 of department \"dept1\" to person \"person2\" does not exist."