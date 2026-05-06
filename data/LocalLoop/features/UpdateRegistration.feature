Feature: Update Registration
    As an organizer, I want to update registration statuses for my events.

    Background:
        Given the following user accounts exist in the system
            | userID | firstName | lastName | username | email               | phoneNumber | role        | companyName      |
            | id1    | Alice     | Smith    | aliceorg | alice@organizer.com | 555-0100    | Organizer   | AliceEvents Inc. |
            | id2    | Bob       | Johnson  | bobpart  | bob@participant.com | 555-0200    | Participant |                  |
            | id3    | Alice     | Johnson  | alicej   | alice@example.com   | 555-0300    | Participant |                  |
        Given the following categories exist in the system
            | categoryId | name  | description        |
            | id1        | Music | Music and concerts |
        Given the following events exist in the system
            | eventId | organizerId | name           | description      | categoryId | fee  | eventStart    | eventEnd      | capacity |
            | id1     | id1         | Summer Concert | A summer concert | id1        | 50.0 | 1735689600000 | 1735693200000 | 2        |
        Given the following registrations exist in the system
            | registrationId | eventId | participantId | organizerId | status   | timestamp     |
            | id1            | id1     | id2           | id1         | approved | 1735600000000 |

    Scenario Outline: Successfully update a registration
        Given the following registration exists in the system
            | registrationId | eventId | participantId | organizerId | status  | timestamp     |
            | id2            | id1     | id3           | id1         | pending | 1735600000000 |
        When an user with userID "<userId>" attempts to update registration "<registrationId>" to status "<newStatus>"
        Then the registration with registrationId "<registrationId>" shall have status "<newStatus>"
        Then the number of registrations for event "id1" shall be 2

        Examples:
            | userId | registrationId | newStatus |
            | id1    | id2            | cancelled |
            | id3    | id2            | cancelled |
            | id1    | id2            | approved  |
            | id1    | id2            | pending   |

    Scenario Outline: Unsuccessfully update an approved or cancelled registration
        Given the following registration exists in the system with status "<currentStatus>"
            | registrationId | eventId | participantId | organizerId | timestamp     |
            | id2            | id1     | id3           | id1         | 1735600000000 |
        When an user with userID "id1" attempts to update registration "id2" to status "<newStatus>"
        Then the error "Cannot update registration with status '<currentStatus>'." shall be raised
        Then the registration with registrationId "id2" shall have status "<currentStatus>"
        Then the number of registrations for event "id1" shall be 2

        Examples:
            | currentStatus | newStatus |
            | approved      | approved  |
            | approved      | cancelled |
            | approved      | pending   |
            | cancelled     | cancelled |
            | cancelled     | approved  |
            | cancelled     | pending   |

    Scenario: Unsuccessfully update a registration by non-organizer
        Given the following registration exists in the system
            | registrationId | eventId | participantId | organizerId | status  | timestamp     |
            | id2            | id1     | id3           | id1         | pending | 1735600000000 |
        When an user with userID "id2" attempts to update registration "id2" to status "approved"
        Then the error "User id2 is not authorized to update this registration." shall be raised
        Then the registration with registrationId "id2" shall have status "pending"
        Then the number of registrations for event "id1" shall be 2

    Scenario: Unsuccessfully approve a registration when event is at capacity
        Given the following event exists in the system
            | eventId | organizerId | name             | description            | categoryId | fee  | eventStart    | eventEnd      | capacity |
            | id2     | id1         | Summer Concert 2 | Another summer concert | id1        | 50.0 | 1735689600000 | 1735693200000 | 1        |
        Given the following registration exists in the system
            | registrationId | eventId | participantId | organizerId | status   | timestamp     |
            | id2            | id2     | id2           | id1         | approved | 1735600000000 |
            | id3            | id2     | id3           | id1         | pending  | 1735600000000 |
        When an user with userID "id1" attempts to update registration "id3" to status "approved"
        Then the error "Cannot approve registration if event is at full capacity." shall be raised
        Then the registration with registrationId "id3" shall have status "pending"
        Then the number of registrations for event "id2" shall be 2

    Scenario Outline: Unsuccessfully update a registration with invalid values
        Given the following registration exists in the system
            | registrationId | eventId | participantId | organizerId | status  | timestamp     |
            | id2            | id1     | id3           | id1         | pending | 1735600000000 |
        When an user with userID "<userId>" attempts to update registration "<registrationId>" to status "<newStatus>"
        Then the error "<error>" shall be raised

        Examples:
            | userId | registrationId | newStatus | error                                                   |
            | id999  | id2            | approved  | Invalid user ID.                                        |
            | id1    | id999          | cancelled | Invalid registration ID.                                |
            | id1    | id2            |           | Invalid status. Must be pending, approved or cancelled. |
            | id1    | id2            | invalid   | Invalid status. Must be pending, approved or cancelled. |