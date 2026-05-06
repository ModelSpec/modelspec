Feature: Update User Registration

    Background:
        Given there is a UserAccess system
        And there is a Administration system
        And there is a Meetings system
        And there is a Payments system
        And the current system date is "2025-11-30"
        And the following user registrations exist:
            | id | login | email             | firstName | lastName | name     | status                 | registerDate |
            | 1  | user1 | user1@example.com | John      | Doe      | John Doe | WaitingForConfirmation | 2025-11-29   |

    Scenario: Successfully update a user registration
        When user registration 1 is updated with login "user1updated" and email "updated@example.com" and firstName "Jane" and lastName "Smith" and name "Jane Smith" and status "WaitingForConfirmation"
        Then the system shall not throw an error
        Then the user registration 1 login shall be "user1updated"
        Then the user registration 1 email shall be "updated@example.com"
        Then the user registration 1 firstName shall be "Jane"
        Then the user registration 1 lastName shall be "Smith"
        Then the user registration 1 name shall be "Jane Smith"
        Then the user registration 1 status shall be "WaitingForConfirmation"
        Then the user registration 1 registerDate shall be "2025-11-29"
        Then the user registration 1 confirmedDate shall be None
        Then the number of users shall be 0

    Scenario: Successfully confirm a user registration
        When user registration 1 is updated with login "user1" and email "user1@example.com" and firstName "John" and lastName "Doe" and name "John Doe" and status "Confirmed"
        Then the system shall not throw an error
        Then the user registration 1 login shall be "user1"
        Then the user registration 1 email shall be "user1@example.com"
        Then the user registration 1 firstName shall be "John"
        Then the user registration 1 lastName shall be "Doe"
        Then the user registration 1 name shall be "John Doe"
        Then the user registration 1 status shall be "Confirmed"
        Then the user registration 1 registerDate shall be "2025-11-29"
        Then the user registration 1 confirmedDate shall be "2025-11-30"
        Then the number of users shall be 1
        Then the following users shall exist:
            | id | login | email             | firstName | lastName | name     | createDate |
            | 1  | user1 | user1@example.com | John      | Doe      | John Doe | 2025-11-30 |

    Scenario: Successfully expire a user registration
        When user registration 1 is updated with login "user1" and email "user1@example.com" and firstName "John" and lastName "Doe" and name "John Doe" and status "Expired"
        Then the system shall not throw an error
        Then the user registration 1 login shall be "user1"
        Then the user registration 1 email shall be "user1@example.com"
        Then the user registration 1 firstName shall be "John"
        Then the user registration 1 lastName shall be "Doe"
        Then the user registration 1 name shall be "John Doe"
        Then the user registration 1 status shall be "Expired"
        Then the user registration 1 registerDate shall be "2025-11-29"
        Then the user registration 1 confirmedDate shall be None
        Then the number of users shall be 0

    Scenario Outline: Unsuccessfully update a user registration with invalid values
        When user registration 1 is updated with login "<login>" and email "<email>" and firstName "<firstName>" and lastName "<lastName>" and name "<name>" and status "WaitingForConfirmation"
        Then the system shall throw with error message "<errorMessage>"
        Then the user registration 1 login shall be "user1"
        Then the user registration 1 email shall be "user1@example.com"
        Then the user registration 1 firstName shall be "John"
        Then the user registration 1 lastName shall be "Doe"
        Then the user registration 1 name shall be "John Doe"
        Then the user registration 1 status shall be "WaitingForConfirmation"

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

    Scenario: Unsuccessfully update a confirmed user registration
        Given the following user registrations exist:
            | id | login | email             | firstName | lastName | name    | status    | registerDate | confirmedDate |
            | 2  | user2 | user2@example.com | Alice     | Johnson  | Alice J | Confirmed | 2025-11-28   | 2025-11-29    |
        When user registration 2 is updated with login "user2updated" and email "updated@example.com" and firstName "Bob" and lastName "Brown" and name "Bob Brown" and status "Confirmed"
        Then the system shall throw with error message "Cannot update a confirmed user registration."
        Then the user registration 2 login shall be "user2"
        Then the user registration 2 email shall be "user2@example.com"
        Then the user registration 2 firstName shall be "Alice"
        Then the user registration 2 lastName shall be "Johnson"
        Then the user registration 2 name shall be "Alice J"
        Then the user registration 2 status shall be "Confirmed"

    Scenario: Unsuccessfully update an expired user registration
        Given the following user registrations exist:
            | id | login | email             | firstName | lastName | name    | status  | registerDate |
            | 2  | user2 | user2@example.com | Alice     | Johnson  | Alice J | Expired | 2025-11-27   |
        When user registration 2 is updated with login "user2updated" and email "updated@example.com" and firstName "David" and lastName "Evans" and name "David Evans" and status "WaitingForConfirmation"
        Then the system shall throw with error message "Cannot update an expired user registration."
        Then the user registration 2 login shall be "user2"
        Then the user registration 2 email shall be "user2@example.com"
        Then the user registration 2 firstName shall be "Alice"
        Then the user registration 2 lastName shall be "Johnson"
        Then the user registration 2 name shall be "Alice J"
        Then the user registration 2 status shall be "Expired"