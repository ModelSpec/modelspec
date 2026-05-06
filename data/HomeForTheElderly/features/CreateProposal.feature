Feature: Create Proposal
  Background:
    Given there is a HomeForTheElderly system
    Given there is a department with id "dept1"
    Given there is a room in department "dept1" with room number 1 and category type "RH" and price 1000
    Given there is a bed in room 1 of department "dept1" with bed number 1
    Given there is a person with id "person" and name "John Doe" and birthdate "1950-01-01" and abilities "requires wheelchair"
    Given the current system date is "2020-01-01"

  Scenario: Creating a new proposal
    When a proposal is created for bed 1 of room 1 of department "dept1" to person "person"
    Then the system shall not throw an error
    Then the proposal shall be associated with bed 1 of room 1 of department "dept1"
    Then the proposal shall be associated with person "person"
    Then the proposal shall have status "waiting"
    Then the proposal shall have validated false
    Then the number of proposals in HomeForTheElderly shall be 1

  Scenario Outline: Creating a proposal with invalid values
    When a proposal is created for bed <bed> of room 1 of department "dept1" to person "<person>"
    Then the system shall throw with error message "<error>"
    Then the number of proposals in HomeForTheElderly shall be 0

    Examples:
      | bed   | person  | error                            |
      |       | person  | Bed cannot be empty.             |
      | 1     |         | Person cannot be empty.          |
      | 2     | person  | Bed "bed2" does not exist.       |
      | 1     | person2 | Person "person2" does not exist. |