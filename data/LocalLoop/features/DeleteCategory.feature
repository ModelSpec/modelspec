Feature: Delete Category
    As an admin, I want to delete categories from the system.

    Background:
        Given the following user accounts exist in the system
            | userID | firstName | lastName | username  | email               | phoneNumber | role        | name             |
            | id1    | Admin     | User     | adminuser | admin@example.com   | 555-0100    | Admin       |                  |
            | id2    | John      | Doe      | johndoe   | john@example.com    | 555-0200    | Participant |                  |
            | id3    | Alice     | Johnson  | alicej    | alice@example.com   | 555-0300    | Organizer   | AliceEvents Inc. |
            | id4    | Carol     | White    | carolorg  | carol@organizer.com | 555-0400    | Organizer   | CarolEvents Co.  |
            | id5    | Peter     | Poe      | ppoe      | peter@example.com   | 555-0500    | Participant |                  |
        And the following categories exist in the system
            | categoryId | name   | description           |
            | id1        | Sports | Sports related events |
            | id2        | Music  | Music and concerts    |

    Scenario: Successfully delete a category with no events, as admin
        When an admin with userID "id1" attempts to delete category "id1"
        Then the category with categoryId "id1" shall not exist in the system
        Then the number of categories in the system shall be 1

    Scenario: Successfully delete a category with events with no registrations to that event, as admin
        Given the following event exists in the system
            | eventId | organizerId | name             | description      | categoryId | fee  | eventStart    | eventEnd      | capacity |
            | id1     | id3         | Summer Concert   | A summer concert | id2        | 50.0 | 1735689600000 | 1735693200000 | 2        |
        When an admin with userID "id1" attempts to delete category "id2"
        Then the category with categoryId "id2" shall not exist in the system
        Then the number of categories in the system shall be 1
        Then the number of events in the system shall be 0

    Scenario: Successfully delete a category with events with registrations to that event, as admin
        Given the following event exists in the system
            | eventId | organizerId | name             | description      | categoryId | fee  | eventStart    | eventEnd      | capacity |
            | id1     | id3         | Olympics         | Summer olympics  | id1        | 50.0 | 1735689600000 | 1735693200000 | 2        |
            | id2     | id4         | Winter Concert   | A winter concert | id2        | 50.0 | 1735689600000 | 1735693200000 | 2        |
        Given the following registration exists in the system
            | registrationId | eventId | participantId | organizerId | status   | timestamp     |
            | id1            | id1     | id2           | id3         | approved | 1735600000000 |
            | id2            | id2     | id5           | id4         | approved | 1735600000000 |
        When an admin with userID "id1" attempts to delete category "id1"
        Then the category with categoryId "id1" shall not exist in the system
        Then the number of categories in the system shall be 1
        Then the number of events in the system shall be 1
        Then the event with eventId "id1" shall not exist in the system
        Then the number of registrations for eventId "id1" in the system shall be 0
        Then the number of registrations in the system shall be 1 

    Scenario Outline: Unsuccessfully delete a category as non-admin user
        When a user with userID "<userID>" attempts to delete category "id1"
        Then the error "Only admin users can delete categories." shall be raised
        Then the category with categoryId "id1" shall exist in the system
        Then the number of categories in the system shall be 2

        Examples:
            | userID |
            | id2    |
            | id3    |

    Scenario: Unsuccessfully delete a category as non-existent account
        When a user with userID "id999" attempts to delete category "id1"
        Then the error "Account with ID id999 does not exist." shall be raised
        Then the category with categoryId "id1" shall exist in the system
        Then the number of categories in the system shall be 2

    Scenario: Unsuccessfully delete a category that does not exist
        When an admin with userID "id1" attempts to delete category "id999"
        Then the error "Category with ID id999 does not exist." shall be raised
        Then the number of categories in the system shall be 2
