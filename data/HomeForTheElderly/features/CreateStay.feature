Feature: Create Stay
  Background:
    Given there is a HomeForTheElderly system
    Given there is a department with id "dept1"
    Given there is a room in department "dept1" with room number 1 and category type "RH" and price 1000
    Given there is a bed in room 1 of department "dept1" with bed number 1
    Given there is a person with id "person" and name "John Doe" and birthdate "1950-01-01" and abilities "requires wheelchair"
    Given the current system date is "2020-01-01"

  Scenario: Creating a new stay
    Given there is a proposal for bed 1 of room 1 of department "dept1" to person "person"
    When a stay is created for person "person" and bed 1 of room 1 of department "dept1" with intakeDate "2020-01-02"
    Then the system shall not throw an error
    Then the created stay shall have intakeDate "2020-01-02"
    Then the created stay shall have an empty endDate
    Then the created stay shall be associated with person "person"
    Then the created stay shall be associated with bed 1 of room 1 of department "dept1"
    Then the number of stays in HomeForTheElderly shall be 1

  Scenario: Creating a stay for a person with a proposal for a different room
    Given there is a room in department "dept1" with room number 2 and category type "SF" and price 3000
    Given there is a bed in room 2 of department "dept1" with bed number 1
    Given there is a proposal for bed 1 of room 1 of department "dept1" to person "person"
    When a stay is created for person "person" and bed 1 of room 2 of department "dept1" with intakeDate "2020-01-02"
    Then the system shall not throw an error
    Then the created stay shall have intakeDate "2020-01-02"
    Then the created stay shall have an empty endDate
    Then the created stay shall be associated with person "person"
    Then the created stay shall be associated with bed 1 of room 2 of department "dept1"
    Then the proposal shall be for bed 1 of room 1 of department "dept1" to person "person"
    Then the number of stays in HomeForTheElderly shall be 1

  Scenario: Creating a stay for a person without a proposal
    When a stay is created for person "person" and bed 1 of room 1 of department "dept1" with intakeDate "2020-01-02"
    Then the system shall throw with error message "Cannot create stay for \"person\" without a proposal."
    Then the number of stays in HomeForTheElderly shall be 0

  Scenario Outline: Creating a stay with invalid values
    Given there is a proposal for bed 1 of room 1 of department "dept1" to person "person"
    When a stay is created for person "<person>" and bed <bed> of room 1 of department "dept1" with intakeDate "<date>"
    Then the system shall throw with error message "<error>"
    Then the number of stays in HomeForTheElderly shall be 0

    Examples:
      | person  | bed   | date        | error                                                 |
      |         | 1     | 2020-01-02  | Person cannot be empty.                               |
      | person  |       | 2020-01-02  | Bed cannot be empty.                                  |
      | person2 | 1     | 2020-01-02  | Person "person2" does not exist.                      |
      | person  | 2     | 2020-01-02  | Bed 2 of room 1 of department "dept1" does not exist. |
      | person  | 1     | 2019-12-31  | Intake date must be on or after the current date.     |