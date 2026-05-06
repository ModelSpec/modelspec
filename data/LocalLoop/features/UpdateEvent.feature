Feature: Update Event
    As an organizer, I want to update an existing event in the system.

    Background:
        Given the following user accounts exist in the system
            | userID | firstName | lastName | username | email               | phoneNumber | role        | companyName      |
            | id1    | Alice     | Smith    | aliceorg | alice@organizer.com | 555-0100    | Organizer   | AliceEvents Inc. |
            | id2    | Bob       | Johnson  | bobpart  | bob@participant.com | 555-0200    | Participant |                  |
            | id3    | Carol     | White    | carolorg | carol@organizer.com | 555-0300    | Organizer   | CarolEvents Co.  |
        Given the following categories exist in the system
            | categoryId | name  | description        |
            | id1        | Music | Music and concerts |
        Given the following events exist in the system
            | eventId | organizerId | name           | description      | categoryId | fee  | eventStart    | eventEnd      | capacity |
            | id1     | id1         | Summer Concert | A summer concert | id1        | 50.0 | 1735689600000 | 1735693200000 | 100      |

    Scenario Outline: Successfully update an event as the organizer
        When an organizer with userID "<organizerId>" attempts to update event "<eventId>" with name "<name>", description "<description>", categoryId "<categoryId>", fee "<fee>", eventStart "<eventStart>", eventEnd "<eventEnd>", and capacity "<capacity>"
        Then an event with eventId "<eventId>", name "<name>", description "<description>", categoryId "<categoryId>", fee "<fee>", eventStart "<eventStart>", eventEnd "<eventEnd>", capacity "<capacity>", and organizerId "<organizerId>" shall exist in the system
        Then the number of events in the system shall be 1

        Examples:
            | organizerId | eventId | name            | description            | categoryId | fee  | eventStart    | eventEnd      | capacity |
            | id1         | id1     | Updated Concert | Updated summer concert | id1        | 60.0 | 1735689600000 | 1735693200000 | 120      |
            | id1         | id1     | Updated Concert | Updated summer concert | id1        | 0.0  | 1735689600000 | 1735693200000 | 120      |
            | id1         | id1     | Updated Concert | Updated summer concert | id1        | 60.0 | 1735689600000 | 1735693200000 | 0        |

    Scenario Outline: Unsuccessfully update an event with invalid values
        When an organizer with userID "<organizerId>" attempts to update event "<eventId>" with name "<name>", description "<description>", categoryId "<categoryId>", fee "<fee>", eventStart "<eventStart>", eventEnd "<eventEnd>", and capacity "<capacity>"
        Then the error "<error>" shall be raised
        Then the number of events in the system shall be 1

        Examples:
            | organizerId | eventId | name            | description            | categoryId | fee   | eventStart    | eventEnd      | capacity | error                                      |
            | id1         | id1     |                 | Annual winter festival | id1        | 25.5  | 1740000000000 | 1740010000000 | 200      | Event name must not be empty.              |
            | id1         | id1     | Winter Festival |                        | id1        | 25.5  | 1740000000000 | 1740010000000 | 200      | Event description must not be empty.       |
            | id1         | id1     | Winter Festival | Annual winter festival | id1        | -10.0 | 1740000000000 | 1740010000000 | 200      | Fee must be 0 or a positive number.        |
            | id1         | id1     | Winter Festival | Annual winter festival | id1        | 25.5  | 1740000000000 | 1740010000000 | -5       | Capacity must be 0 or a positive integer.  |
            | id1         | id1     | Winter Festival | Annual winter festival | id1        | 25.5  | 1740010000000 | 1740000000000 | 200      | Event end time must be after start time.   |
            | id1         | id1     | Winter Festival | Annual winter festival | id1        | 25.5  | 0             | 1740010000000 | 200      | Event start time must not be empty.        |
            | id1         | id1     | Winter Festival | Annual winter festival | id1        | 25.5  | 1740000000000 | 0             | 200      | Event end time must not be empty.          |
            | id1         | id1     | Winter Festival | Annual winter festival | id999      | 25.5  | 1740000000000 | 1740010000000 | 200      | Category with the given ID does not exist. |

    Scenario: Unsuccessfully update an event as a non-organizer
        When a user with userID "id2" and role "Participant" attempts to update event "id1" with name "Spring Concert", description "A beautiful concert", categoryId "id1", fee "30.0", eventStart "1740000000000", eventEnd "1740010000000", and capacity "150"
        Then the error "Only organizers can update events." shall be raised
        Then the number of events in the system shall be 1

    Scenario: Unsuccessfully update an event that does not belong to the organizer
        When an organizer with userID "id3" attempts to update event "id1" with name "Spring Concert", description "A beautiful concert", categoryId "id1", fee "30.0", eventStart "1740000000000", eventEnd "1740010000000", and capacity "150"
        Then the error "Only the event organizer can update this event." shall be raised
        Then the number of events in the system shall be 1

    Scenario: Unsuccessfully update an event with a non-existent eventId
        When an organizer with userID "id1" attempts to update event "id999" with name "Spring Concert", description "A beautiful concert", categoryId "id1", fee "30.0", eventStart "1740000000000", eventEnd "1740010000000", and capacity "150"
        Then the error "Event with ID id999 does not exist." shall be raised
        Then the number of events in the system shall be 1
