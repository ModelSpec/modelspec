Feature: Delete Event
    As an organizer, I want to delete an event from the system.

    Background:
        Given the following user accounts exist in the system
            | userID | firstName | lastName | username | email                | phoneNumber | role        | companyName      |
            | id1    | Admin     | User     | adminuser | admin@example.com   | 555-0100    | Admin       |                  |
            | id2    | John      | Doe      | johndoe   | john@example.com    | 555-0200    | Participant |                  |
            | id3    | Alice     | Johnson  | alicej    | alice@example.com   | 555-0300    | Organizer   | AliceEvents Inc. |
            | id4    | Carol     | White    | carolorg  | carol@organizer.com | 555-0400    | Organizer   | CarolEvents Co.  |
            | id5    | Peter     | Poe      | ppoe      | peter@example.com   | 555-0500    | Participant |                  |
        Given the following categories exist in the system
            | categoryId | name  | description        |
            | id1        | Music | Music and concerts |
        Given the following events exist in the system
            | eventId | organizerId | name           | description      | categoryId | fee  | eventStart    | eventEnd      | capacity |
            | id1     | id3         | Summer Concert | A summer concert | id1        | 50.0 | 1735689600000 | 1735693200000 | 100      |
            | id2     | id3         | Winter Concert | A winter concert | id1        | 50.0 | 1735689600000 | 1735693200000 | 100      |

    Scenario: Successfully delete an event as the organizer with no registrations
        When an organizer with userID "id3" attempts to delete event "id1"
        Then event with eventId "id1" shall not exist in the system
        Then the number of events in the system shall be 1
        Then the number of registrations in the system shall be 0

    Scenario: Successfully delete an event as the organizer with registrations
        Given the following registration exists in the system
            | registrationId | eventId | participantId | organizerId | status   | timestamp     |
            | id1            | id1     | id2           | id3         | approved | 1735600000000 |
            | id2            | id2     | id5           | id3         | approved | 1735600000000 |
        When an organizer with userID "id3" attempts to delete event "id1"
        Then event with eventId "id1" shall not exist in the system
        Then the number of events in the system shall be 1
        Then the number of registrations in the system shall be 1
        Then the number of registrations to event with eventId "id1" in the system shall be 0

    Scenario: Unsuccessfully delete an event as a non-organizer
        When a user with userID "id2" and role "Participant" attempts to delete event "id1"
        Then the error "Only organizers can delete events." shall be raised
        Then the number of events in the system shall be 2

    Scenario: Unsuccessfully delete an event that does not belong to the organizer
        When an organizer with userID "id4" attempts to delete event "id1"
        Then the error "Only the event organizer can delete this event." shall be raised
        Then the number of events in the system shall be 2

    Scenario: Unsuccessfully delete an event with a non-existent eventId
        When an organizer with userID "id3" attempts to delete event "id999"
        Then the error "Event with ID id999 does not exist." shall be raised
        Then the number of events in the system shall be 2
