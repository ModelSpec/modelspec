Feature: Create User Registration

    Background:
        Given there is a UserAccess system
        And there is a Administration system
        And there is a Meetings system
        And there is a Payments system
        And the current system date is "2025-11-30"

    Scenario: Successfully create a user registration
        When a user registration is created with login "user1" and email "user1@example.com" and firstName "John" and lastName "Doe" and name "John Doe"
        Then the system shall not throw an error
        Then the number of user registrations shall be 1
        Then the user registration shall have an id
        Then the user registration login shall be "user1"
        Then the user registration email shall be "user1@example.com"
        Then the user registration firstName shall be "John"
        Then the user registration lastName shall be "Doe"
        Then the user registration name shall be "John Doe"
        Then the user registration status shall be "WaitingForConfirmation"
        Then the user registration registerDate shall be "2025-11-30"
        Then the user registration confirmedDate shall be null

    Scenario: Successfully create a user registration with automatically unique id
        Given there is a user registration with id 1
        When a user registration is created with login "user1" and email "user1@example.com" and firstName "John" and lastName "Doe" and name "John Doe"
        Then the system shall not throw an error
        Then the number of user registrations shall be 1
        Then the user registration shall have an id
        Then the user registration id shall not be 1
        Then the user registration login shall be "user1"
        Then the user registration email shall be "user1@example.com"
        Then the user registration firstName shall be "John"
        Then the user registration lastName shall be "Doe"
        Then the user registration name shall be "John Doe"
        Then the user registration status shall be "WaitingForConfirmation"
        Then the user registration registerDate shall be "2025-11-30"
        Then the user registration confirmedDate shall be null

    Scenario Outline: Unsuccessfully create a user registration with invalid values
        When a user registration is created with login "<login>" and email "<email>" and firstName "<firstName>" and lastName "<lastName>" and name "<name>"
        Then the system shall throw with error message "<errorMessage>"
        Then the number of user registrations shall be 0

        Examples:
            | login | email              | firstName | lastName | name     | errorMessage                                                    |
            |       | user1@example.com  | John      | Doe      | John Doe | The login must not be empty.                                    |
            | user1 |                    | John      | Doe      | John Doe | The email must not be empty.                                    |
            | user1 | user1example.com   | John      | Doe      | John Doe | The email must contain exactly one "@" character.               |
            | user1 | user1@@example.com | John      | Doe      | John Doe | The email must contain exactly one "@" character.               |
            | user1 | user1@examplecom   | John      | Doe      | John Doe | The email must contain a "." character after the "@" character. |
            | user1 | user1@example.     | John      | Doe      | John Doe | The email must not end with a "." character.                    |
            | user1 | user1@example.com  |           | Doe      | John Doe | The firstName must not be empty.                                |
            | user1 | user1@example.com  | John      |          | John Doe | The lastName must not be empty.                                 |
            | user1 | user1@example.com  | John      | Doe      |          | The name must not be empty.                                     |