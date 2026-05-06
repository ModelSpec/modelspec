Feature: Create Person
  Background:
    Given there is a HomeForTheElderly system
    Given the current system date is "2020-01-01"

  Scenario: Creating a new person
    When a person with name "John Doe" and birthdate "1950-01-01" is created
    Then the system shall not throw an error
    Then the created person shall have a non-empty id
    Then the created person shall have name "John Doe"
    Then the created person shall have birthdate "1950-01-01"
    Then the created person shall have registrationDate "2020-01-01"
    Then the created person shall have abilities ""
    Then the number of people in HomeForTheElderly shall be 1

  Scenario Outline: Creating a person with invalid values
    When a person with name "<name>" and birthdate "<birthdate>" is created
    Then the system shall throw with error message "<error>"
    Then the number of people in HomeForTheElderly shall be 0

    Examples:
      | name      | birthdate   | error                                                |
      |           | 1950-01-01  | The name of a person must not be empty.              |
      | John Doe  |             | The birthdate of a person must not be empty.         |
      | John Doe  | 2020-01-02  | The birthdate of a person must not be in the future. |