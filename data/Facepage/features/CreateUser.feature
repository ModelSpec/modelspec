Feature: Create User
  Background:
    Given there is a Facepage system
    Given the current system date is "2020-01-01"

  Scenario: Creating a new user
    When a user with userID "1" and name "John Doe" and email "john.doe@mail.com" and date of birth "2000-01-01" is created
    Then the system shall not throw an error
    Then the created user shall have userID "1"
    Then the created user shall have name "John Doe"
    Then the created user shall have email "john.doe@mail.com"
    Then the created user shall have date of birth "2000-01-01"
    Then the number of users in Facepage shall be 1

  Scenario Outline: Creating a user with invalid values
    When a user with userID "<userID>" and name "<name>" and email "<email>" and date of birth "<dateOfBirth>" is created
    Then the system shall throw with error message "<error>"
    Then the number of users in Facepage shall be 0

    Examples:
      | userID | name      | email                 | dateOfBirth | error                                                                      |
      |        | John Doe  | john.doe@mail.com     | 2000-01-01  | The userID of a user must not be empty.                                    |
      | 1      |           | john.doe@mail.com     | 2000-01-01  | The name of a user must not be empty.                                      |
      | 1      | John Doe  | john.doe.mail.com     | 2000-01-01  | The email of a user must contain exactly one "@" character.                |
      | 1      | John Doe  | john.doe@@mail.com    | 2000-01-01  | The email of a user must contain exactly one "@" character.                |
      | 1      | John Doe  | johndoe@mailcom       | 2000-01-01  | The email of a user must contain at least one "." after the "@" character. |
      | 1      | John Doe  | johndoe@mail.         | 2000-01-01  | The email of a user must not end with a "." character.                     |
      | 1      | John Doe  | john.doe@mail.com     | 2020-01-02  | The date of birth of a user must not be in the future.                     |

  Scenario: Creating a user with duplicate userID
    Given there is a user with userID "1" and name "John Doe" and email "john.doe@mail.com" and date of birth "2000-01-01" is created
    When a user with userID "1" and name "Jane Smith" and email "jane.smith@mail.com" and date of birth "1995-05-05" is created
    Then the system shall throw with error message "A user with the ID \"1\" already exists."
    Then the number of users in Facepage shall be 1