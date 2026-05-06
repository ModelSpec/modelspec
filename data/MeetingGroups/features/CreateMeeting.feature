Feature: Create Meeting

    Background:
        Given there is a UserAccess system
        And there is a Administration system
        And there is a Meetings system
        And there is a Payments system
        And there is a member with id 1
        And the current system date is "2025-11-30"

    Scenario: Successfully create a meeting
        When member 1 creates a meeting with title "meeting1" and description "description" and locationName "location" and locationAddress "address" and locationCity "city" and locationCountryCode "ca" and startDate "2025-12-01" and endDate "2025-12-01" and rsvpStartDate "2025-11-30" and rsvpEndDate "2025-11-30" and attendeesLimit 10 and guestsLimit 5
        Then the system shall not throw an error
        Then the number of meetings shall be 1
        Then the meeting shall have an id
        Then the meeting title shall be "meeting1"
        Then the meeting description shall be "description"
        Then the meeting location name shall be "location"
        Then the meeting location address shall be "address"
        Then the meeting location city shall be "city"
        Then the meeting location countryCode shall be "ca"
        Then the meeting term startDate shall be "2025-12-01"
        Then the meeting term endDate shall be "2025-12-01"
        Then the meeting rsvp term startDate shall be "2025-11-30"
        Then the meeting rsvp term endDate shall be "2025-11-30"
        Then the meeting limit attendeesLimit shall be 10
        Then the meeting limit guestsLimit shall be 5
        Then the number of meetings shall be 1

    Scenario: Successfully create a meeting with automatically unique id
        Given there is a meeting with id 1
        When member 1 creates a meeting with title "meeting1" and description "description" and locationName "location" and locationAddress "address" and locationCity "city" and locationCountryCode "ca" and startDate "2025-12-01" and endDate "2025-12-01" and rsvpStartDate "2025-11-30" and rsvpEndDate "2025-11-30" and attendeesLimit 10 and guestsLimit 5
        Then the system shall not throw an error
        Then the number of meetings shall be 1
        Then the meeting shall have an id
        Then the meeting id shall not be 1
        Then the meeting title shall be "meeting1"
        Then the meeting description shall be "description"
        Then the meeting location name shall be "location"
        Then the meeting location address shall be "address"
        Then the meeting location city shall be "city"
        Then the meeting location countryCode shall be "ca"
        Then the meeting term startDate shall be "2025-12-01"
        Then the meeting term endDate shall be "2025-12-01"
        Then the meeting rsvp term startDate shall be "2025-11-30"
        Then the meeting rsvp term endDate shall be "2025-11-30"
        Then the meeting limit attendeesLimit shall be 10
        Then the meeting limit guestsLimit shall be 5
        Then the number of meetings shall be 1

    Scenario Outline: Unsuccessfully create a meeting with invalid values
        When member 1 creates a meeting with title "<title>" and description "<description>" and locationName "<locationName>" and locationAddress "<locationAddress>" and locationCity "<locationCity>" and locationCountryCode "<locationCountryCode>" and startDate "<startDate>" and endDate "<endDate>" and rsvpStartDate "<rsvpStartDate>" and rsvpEndDate "<rsvpEndDate>" and attendeesLimit <attendeesLimit> and guestsLimit <guestsLimit>
        Then the system shall throw with error message "<errorMessage>"
        Then the number of meetings shall be 0

        Examples:
            | title    | description | locationName | locationAddress | locationCity | locationCountryCode | startDate  | endDate    | rsvpStartDate | rsvpEndDate | attendeesLimit | guestsLimit | errorMessage                                                   |
            |          | description | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | The title must not be empty.                                   |
            | meeting1 |             | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | The description must not be empty.                             |
            | meeting1 | description |              | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | The locationName must not be empty.                            |
            | meeting1 | description | location     |                 | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | The locationAddress must not be empty.                         |
            | meeting1 | description | location     | address         |              | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | The locationCity must not be empty.                            |
            | meeting1 | description | location     | address         | city         |                     | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | The locationCountryCode must not be empty.                     |
            | meeting1 | description | location     | address         | city         | c                   | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | The locationCountryCode must be either 2 or 3 characters long. |
            | meeting1 | description | location     | address         | city         | cabd                | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | The locationCountryCode must be either 2 or 3 characters long. |
            | meeting1 | description | location     | address         | city         | ca                  |            | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | The startDate must not be empty.                               |
            | meeting1 | description | location     | address         | city         | ca                  | 2025-12-01 |            | 2025-11-30    | 2025-11-30  | 10             | 5           | The endDate must not be empty.                                 |
            | meeting1 | description | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 |               | 2025-11-30  | 10             | 5           | The rsvpStartDate must not be empty.                           |
            | meeting1 | description | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    |             | 10             | 5           | The rsvpEndDate must not be empty.                             |
            | meeting1 | description | location     | address         | city         | ca                  | 2025-12-02 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | The startDate must be before or equal to endDate.              |
            | meeting1 | description | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-12-02    | 2025-11-30  | 10             | 5           | The rsvpStartDate must be before or equal to rsvpEndDate.      |
            | meeting1 | description | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 0              | 5           | The attendeesLimit must be greater than 0.                     |
            | meeting1 | description | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | -1             | 5           | The attendeesLimit must be greater than 0.                     |
            | meeting1 | description | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 0           | The guestsLimit must be greater than 0.                        |
            | meeting1 | description | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | -1          | The guestsLimit must be greater than 0.                        |
