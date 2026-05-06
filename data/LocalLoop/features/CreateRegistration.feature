Feature: Create Registration
    As a participant, I want to register for an event in the system.

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
            | id1     | id1         | Summer Concert | A summer concert | id1        | 50.0 | 1735689600000 | 1735693200000 | 1        |
        Given the following registrations exist in the system
            | registrationId | eventId | participantId | organizerId | status   | timestamp     |
            | id1            | id1     | id2           | id1         | approved | 1735600000000 |

    Scenario: Successfully create a registration
        When a participant with userID "id3" attempts to register for event "id1" at timestamp 1735600000000
        Then a registration with eventId "id1", participantId "id3", organizerId "id1", status "pending", and timestamp 1735600000000 shall exist in the system
        Then the registrationId shall be automatically assigned and not be "id1"
        Then the number of registrations for event "id1" shall be 2

    Scenario: Unsuccessfully create a registration with non-existent participant
        When a participant with userID "id999" attempts to register for event "id1" at timestamp 1735600000000
        Then the error "Participant with ID id999 does not exist." shall be raised
        Then the number of registrations for event "id1" shall be 1

    Scenario: Unsuccessfully create a registration with non-existent event
        When a participant with userID "id2" attempts to register for event "id999" at timestamp 1735600000000
        Then the error "Event with ID id999 does not exist." shall be raised
        Then the number of registrations for event "id1" shall be 1