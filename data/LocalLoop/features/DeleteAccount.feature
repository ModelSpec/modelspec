Feature: Delete Account
    As a user or admin, I want to delete an account from the system.

    Background:
        Given the following user accounts exist in the system
            | userID | firstName | lastName | username  | email               | phoneNumber | role        | companyName      |
            | id1    | Admin     | User     | adminuser | admin@example.com   | 555-0100    | Admin       |                  |
            | id2    | John      | Doe      | johndoe   | john@example.com    | 555-0200    | Participant |                  |
            | id3    | Alice     | Johnson  | alicej    | alice@example.com   | 555-0300    | Organizer   | AliceEvents Inc. |
            | id4    | Carol     | White    | carolorg  | carol@organizer.com | 555-0400    | Organizer   | CarolEvents Co.  |
            | id5    | Peter     | Poe      | ppoe      | peter@example.com   | 555-0500    | Participant |                  |

    Scenario: Successfully delete an account, who has an organizer role with no organized any events, as admin
        When user with userID "id1" attempts to delete the account with userID "id3"
        Then the account with userID "id3" shall not exist in the system
        Then the number of user accounts in the system shall be 4
        Then the number of organized events in the system shall be 0

    Scenario: Successfully delete an account, who has an organizer role with organized events with no registrations, as admin
        Given the following categories exist in the system
            | categoryId | name  | description        |
            | id1        | Music | Music and concerts |
        Given the following event exists in the system
            | eventId | organizerId | name           | description            | categoryId | fee  | eventStart    | eventEnd      | capacity |
            | id1     | id3         | Summer Concert | Another summer concert | id1        | 50.0 | 1735689600000 | 1735693200000 | 1        |
        When user with userID "id1" attempts to delete the account with userID "id3"
        Then the account with userID "id3" shall not exist in the system
        Then the number of user accounts in the system shall be 4
        Then the organized event with eventId "id1" shall not exist in the system
        Then the number of organized events in the system shall be 0

    Scenario: Successfully delete an account, who has an organizer role with organized events with registrations, as admin
        Given the following categories exist in the system
            | categoryId | name  | description        |
            | id1        | Music | Music and concerts |
        Given the following event exists in the system
            | eventId | organizerId | name           | description      | categoryId | fee  | eventStart    | eventEnd      | capacity |
            | id1     | id3         | Summer Concert | A summer concert | id1        | 50.0 | 1735689600000 | 1735693200000 | 2        |
            | id2     | id4         | Winter Concert | A winter concert | id1        | 50.0 | 1735689600000 | 1735693200000 | 2        |
        Given the following registration exists in the system
            | registrationId | eventId | participantId | organizerId | status   | timestamp     |
            | id1            | id1     | id2           | id3         | approved | 1735600000000 |
            | id2            | id2     | id5           | id4         | approved | 1735600000000 |
        When user with userID "id1" attempts to delete the account with userID "id3"
        Then the account with userID "id3" shall not exist in the system
        Then the number of user accounts in the system shall be 4
        Then the organized event with eventId "id1" shall not exist in the system
        Then the number of organized events in the system shall be 1
        Then the number of registrations to event "id1" shall be 0
        Then the number of registrations in the system shall be 1
        Then the registration with registrationId "id1" shall not exist in the system

    Scenario: Successfully delete an account, who has a participant role with no event registrations, as admin
        When user with userID "id1" attempts to delete the account with userID "id2"
        Then the account with userID "id2" shall not exist in the system
        Then the number of user accounts in the system shall be 4
        Then the number of registrations in the system shall be 0

    Scenario: Successfully delete an account, who has a participant role with event registrations, as admin
        Given the following categories exist in the system
            | categoryId | name  | description        |
            | id1        | Music | Music and concerts |
        Given the following event exists in the system
            | eventId | organizerId | name           | description      | categoryId | fee  | eventStart    | eventEnd      | capacity |
            | id1     | id3         | Summer Concert | A summer concert | id1        | 50.0 | 1735689600000 | 1735693200000 | 2        |
            | id2     | id4         | Winter Concert | A winter concert | id1        | 50.0 | 1735689600000 | 1735693200000 | 2        |
        Given the following registration exists in the system
            | registrationId | eventId | participantId | organizerId | status   | timestamp     |
            | id1            | id1     | id2           | id3         | approved | 1735600000000 |
            | id2            | id2     | id5           | id4         | approved | 1735600000000 |
        When user with userID "id1" attempts to delete the account with userID "id2"
        Then the account with userID "id2" shall not exist in the system
        Then the number of user accounts in the system shall be 4
        Then the number of registrations to event "id1" shall be 0
        Then the number of registrations in the system shall be 1
        Then the registration with registrationId "id1" shall not exist in the system

    Scenario: Successfully delete an account, who has an organizer role with no organized any events, as account owner
        When user with userID "id3" attempts to delete the account with userID "id3"
        Then the account with userID "id3" shall not exist in the system
        Then the number of user accounts in the system shall be 4
        Then the number of organized events in the system shall be 0

    Scenario: Successfully delete an account, who has an organizer role with organized events with no registrations, as account owner
        Given the following categories exist in the system
            | categoryId | name  | description        |
            | id1        | Music | Music and concerts |
        Given the following event exists in the system
            | eventId | organizerId | name           | description            | categoryId | fee  | eventStart    | eventEnd      | capacity |
            | id1     | id3         | Summer Concert | Another summer concert | id1        | 50.0 | 1735689600000 | 1735693200000 | 1        |
        When user with userID "id3" attempts to delete the account with userID "id3"
        Then the account with userID "id3" shall not exist in the system
        Then the number of user accounts in the system shall be 4
        Then the organized event with eventId "id1" shall not exist in the system
        Then the number of organized events in the system shall be 0

    Scenario: Successfully delete an account, who has an organizer role with organized events with registrations, as account owner
        Given the following categories exist in the system
            | categoryId | name  | description        |
            | id1        | Music | Music and concerts |
        Given the following event exists in the system
            | eventId | organizerId | name           | description      | categoryId | fee  | eventStart    | eventEnd      | capacity |
            | id1     | id3         | Summer Concert | A summer concert | id1        | 50.0 | 1735689600000 | 1735693200000 | 2        |
            | id2     | id4         | Winter Concert | A winter concert | id1        | 50.0 | 1735689600000 | 1735693200000 | 2        |
        Given the following registration exists in the system
            | registrationId | eventId | participantId | organizerId | status   | timestamp     |
            | id1            | id1     | id2           | id3         | approved | 1735600000000 |
            | id2            | id2     | id5           | id4         | approved | 1735600000000 |
        When user with userID "id3" attempts to delete the account with userID "id3"
        Then the account with userID "id3" shall not exist in the system
        Then the number of user accounts in the system shall be 4
        Then the organized event with eventId "id1" shall not exist in the system
        Then the number of organized events in the system shall be 1
        Then the number of registrations to event "id1" shall be 0
        Then the number of registrations in the system shall be 1
        Then the registration with registrationId "id1" shall not exist in the system

    Scenario: Successfully delete an account, who has a participant role with no event registrations, as account owner
        When user with userID "id2" attempts to delete the account with userID "id2"
        Then the account with userID "id2" shall not exist in the system
        Then the number of user accounts in the system shall be 4
        Then the number of registrations in the system shall be 0

    Scenario: Successfully delete an account, who has a participant role with event registrations, as account owner
        Given the following categories exist in the system
            | categoryId | name  | description        |
            | id1        | Music | Music and concerts |
        Given the following event exists in the system
            | eventId | organizerId | name           | description      | categoryId | fee  | eventStart    | eventEnd      | capacity |
            | id1     | id3         | Summer Concert | A summer concert | id1        | 50.0 | 1735689600000 | 1735693200000 | 2        |
            | id2     | id4         | Winter Concert | A winter concert | id1        | 50.0 | 1735689600000 | 1735693200000 | 2        |
        Given the following registration exists in the system
            | registrationId | eventId | participantId | organizerId | status   | timestamp     |
            | id1            | id1     | id2           | id3         | approved | 1735600000000 |
            | id2            | id2     | id5           | id4         | approved | 1735600000000 |
        When user with userID "id2" attempts to delete the account with userID "id2"
        Then the account with userID "id2" shall not exist in the system
        Then the number of user accounts in the system shall be 4
        Then the number of registrations to event "id1" shall be 0
        Then the number of registrations in the system shall be 1
        Then the registration with registrationId "id1" shall not exist in the system

    Scenario Outline: Unsuccessfully delete another user's account without admin privileges
        When user with userID "<requestingUserID>" attempts to delete the account with userID "<targetUserID>"
        Then the error "<error>" shall be raised
        Then the account with userID "<targetUserID>" shall exist in the system
        Then the number of user accounts in the system shall be 5

        Examples:
            | requestingUserID | targetUserID | error                                                 |
            | id2              | id3          | Only admins or account owners can delete the account. |
            | id3              | id2          | Only admins or account owners can delete the account. |

    Scenario: Unsuccessfully delete an account with non-existent account
        When user with userID "id999" attempts to delete the account with userID "id1"
        Then the error "Account does not exist." shall be raised
        Then the number of user accounts in the system shall be 5


    Scenario: Unsuccessfully delete a non-existent account
        When user with userID "id1" attempts to delete the account with userID "id999"
        Then the error "User account does not exist." shall be raised
        Then the number of user accounts in the system shall be 5
