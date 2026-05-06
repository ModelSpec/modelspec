Feature: Create Friend Request
  Background:
    Given there is a Facepage system
    Given the following users exist:
      | userID | name       | email               | dateOfBirth |
      | 1      | John Doe   | john.doe@mail.com   | 2000-01-01  |
      | 2      | Jane Smith | jane.smith@mail.com | 2000-01-01  |
    Given there is a personal account associated with user "1"
    Given there is a personal account associated with user "2"

  Scenario: Creating a new friend request
    When a friend request is sent from the personal account of user "1" to the personal account of user "2"
    Then the system shall not throw an error
    Then the friend request shall be associated with the personal account of user "1" as sender
    Then the friend request shall be associated with the personal account of user "2" as receiver
    Then the number of friend requests in Facepage shall be 1

  Scenario: Creating a friend request with invalid sender - business account
    Given there is a user with userID "3" and name "Bob Johnson" and email "bob.johnson@mail.com" and date of birth "2000-01-01"
    Given there is a business account with company name "company" associated with user "3"
    When a friend request is sent from the business account of user "3" to the personal account of user "2"
    Then the system shall throw with error message "Only personal accounts can send friend requests."
    Then the number of friend requests in Facepage shall be 0

  Scenario: Creating a friend request with invalid receiver - business account
    Given there is a user with userID "3" and name "Bob Johnson" and email "bob.johnson@mail.com" and date of birth "2000-01-01"
    Given there is a business account with company name "company" associated with user "3"
    When a friend request is sent from the personal account of user "1" to the business account of user "3"
    Then the system shall throw with error message "Only personal accounts can receive friend requests."
    Then the number of friend requests in Facepage shall be 0

  Scenario Outline: Creating a friend request with invalid user
    When a friend request is sent from the account of user <user1ID> to the account of user <user2ID>
    Then the system shall throw with error message "<error>"
    Then the number of friend requests in Facepage shall be 0

    Examples:
      | user1ID | user2ID | error                                              |
      | 1       | 1       | Cannot send a friend request to itself.            |
      | 1       |         | Cannot create a friend request without a receiver. |
      |         | 1       | Cannot create a friend request without a sender.   |