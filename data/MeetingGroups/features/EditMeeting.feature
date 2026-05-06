Feature: Edit Meeting

    Background:
        Given there is a UserAccess system
        And there is a Administration system
        And there is a Meetings system
        And there is a Payments system
        And there is a member with id 1
        And there is a member with id 2
        And the current system date is "2025-11-30"
        And the following meetings exist:
            | id | title    | description | locationName | locationAddress | locationCity | locationCountryCode | startDate  | endDate    | rsvpStartDate | rsvpEndDate | attendeesLimit | guestsLimit | creatorId |
            | 1  | meeting1 | description | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | 1         |

    Scenario: Successfully edit a meeting
        When member 1 edits meeting 1 with title "meeting2" and description "new description" and locationName "new location" and locationAddress "new address" and locationCity "new city" and locationCountryCode "us" and startDate "2025-12-02" and endDate "2025-12-02" and rsvpStartDate "2025-12-01" and rsvpEndDate "2025-12-01" and attendeesLimit 20 and guestsLimit 10
        Then the system shall not throw an error
        Then the meeting 1 title shall be "meeting2"
        Then the meeting 1 description shall be "new description"
        Then the meeting 1 location name shall be "new location"
        Then the meeting 1 location address shall be "new address"
        Then the meeting 1 location city shall be "new city"
        Then the meeting 1 location countryCode shall be "us"
        Then the meeting 1 term startDate shall be "2025-12-02"
        Then the meeting 1 term endDate shall be "2025-12-02"
        Then the meeting 1 rsvp term startDate shall be "2025-12-01"
        Then the meeting 1 rsvp term endDate shall be "2025-12-01"
        Then the meeting 1 limit attendeesLimit shall be 20
        Then the meeting 1 limit guestsLimit shall be 10

    Scenario Outline: Unsuccessfully edit a meeting with invalid values
        When member 1 edits meeting 1 with title "<title>" and description "<description>" and locationName "<locationName>" and locationAddress "<locationAddress>" and locationCity "<locationCity>" and locationCountryCode "<locationCountryCode>" and startDate "<startDate>" and endDate "<endDate>" and rsvpStartDate "<rsvpStartDate>" and rsvpEndDate "<rsvpEndDate>" and attendeesLimit <attendeesLimit> and guestsLimit <guestsLimit>
        Then the system shall throw with error message "<errorMessage>"
        Then the meeting 1 title shall be "meeting1"
        Then the meeting 1 description shall be "description"

        Examples:
            | title    | description     | locationName | locationAddress | locationCity | locationCountryCode | startDate  | endDate    | rsvpStartDate | rsvpEndDate | attendeesLimit | guestsLimit | errorMessage                                                   |
            |          | new description | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | The title must not be empty.                                   |
            | meeting2 |                 | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | The description must not be empty.                             |
            | meeting2 | new description |              | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | The locationName must not be empty.                            |
            | meeting2 | new description | location     |                 | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | The locationAddress must not be empty.                         |
            | meeting2 | new description | location     | address         |              | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | The locationCity must not be empty.                            |
            | meeting2 | new description | location     | address         | city         |                     | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | The locationCountryCode must not be empty.                     |
            | meeting2 | new description | location     | address         | city         | c                   | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | The locationCountryCode must be either 2 or 3 characters long. |
            | meeting2 | new description | location     | address         | city         | cabd                | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | The locationCountryCode must be either 2 or 3 characters long. |
            | meeting2 | new description | location     | address         | city         | ca                  |            | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | The startDate must not be empty.                               |
            | meeting2 | new description | location     | address         | city         | ca                  | 2025-12-01 |            | 2025-11-30    | 2025-11-30  | 10             | 5           | The endDate must not be empty.                                 |
            | meeting2 | new description | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 |               | 2025-11-30  | 10             | 5           | The rsvpStartDate must not be empty.                           |
            | meeting2 | new description | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    |             | 10             | 5           | The rsvpEndDate must not be empty.                             |
            | meeting2 | new description | location     | address         | city         | ca                  | 2025-12-02 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | The startDate must be before or equal to endDate.              |
            | meeting2 | new description | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-12-02    | 2025-11-30  | 10             | 5           | The rsvpStartDate must be before or equal to rsvpEndDate.      |
            | meeting2 | new description | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 0              | 5           | The attendeesLimit must be greater than 0.                     |
            | meeting2 | new description | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | -1             | 5           | The attendeesLimit must be greater than 0.                     |
            | meeting2 | new description | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 0           | The guestsLimit must be greater than 0.                        |
            | meeting2 | new description | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | -1          | The guestsLimit must be greater than 0.                        |

    Scenario: Unsuccessfully edit a meeting when member is not the creator
        When member 2 edits meeting 1 with title "meeting2" and description "new description" and locationName "new location" and locationAddress "new address" and locationCity "new city" and locationCountryCode "us" and startDate "2025-12-02" and endDate "2025-12-02" and rsvpStartDate "2025-12-01" and rsvpEndDate "2025-12-01" and attendeesLimit 20 and guestsLimit 10
        Then the system shall throw with error message "Only the creator of the meeting can edit it."
        Then the meeting 1 title shall be "meeting1"
        Then the meeting 1 description shall be "description"
