Feature: Update Stay
  Background:
    Given there is a HomeForTheElderly system
    Given there is a department with id "dept1"
    Given there is a room in department "dept1" with room number 1 and category type "RH" and price 1000
    Given there is a bed in room 1 of department "dept1" with bed number 1
    Given there is a person with id "person" and name "John Doe" and birthdate "1950-01-01" and abilities "requires wheelchair"
    Given there is a proposal for bed 1 of room 1 of department "dept1" to person "person"
    Given the current system date is "2020-01-01"
    Given there is a stay for person "person" and bed 1 of room 1 of department "dept1" with intakeDate "2020-01-02"

  Scenario: Updating a stay's intake date
    When the intakeDate of stay for person "person" and bed 1 of room 1 of department "dept1" is updated to "2020-01-15"
    Then the system shall not throw an error
    Then the stay for person "person" and bed 1 of room 1 of department "dept1" shall have intakeDate "2020-01-15"

  Scenario Outline: Updating a stay's intake date with invalid intake date
    When the intakeDate of stay for person "person" and bed 1 of room 1 of department "dept1" is updated to "<intakeDate>"
    Then the system shall throw with error message "<error>"
    Then the stay for person "person" and bed 1 of room 1 of department "dept1" shall have intakeDate "2020-01-02"

    Examples:
      | intakeDate | error                                             |
      |            | Intake date must not be empty.                    |
      | 2019-12-31 | Intake date must be on or after the current date. |

  Scenario Outline: Updating a stay's end date
    When the endDate of stay for person "person" and bed 1 of room 1 of department "dept1" is updated to "<endDate>"
    Then the system shall not throw an error
    Then the stay for person "person" and bed 1 of room 1 of department "dept1" shall have endDate "<endDate>"

    Examples:
      | endDate    |
      |            |
      | 2019-12-31 |
      | 2021-01-01 |
      | 2020-01-15 |

  Scenario: Updating a stay that does not exist
    Given there is a person with id "person2" and name "Jane Smith" and birthdate "1950-01-01" and abilities "requires wheelchair"
    When the intakeDate of stay for person "person2" and bed 1 of room 1 of department "dept1" is updated to "2020-01-03"
    Then the system shall throw with error message "Stay for person \"person2\" and bed 1 of room 1 of department \"dept1\" does not exist."