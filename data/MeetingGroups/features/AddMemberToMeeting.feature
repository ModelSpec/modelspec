Feature: Add Member To Meeting

    Background:
      Given there is a UserAccess system
      And there is a Administration system
      And there is a Meetings system
      And there is a Payments system
      And there is a member with id 1
      And there is a member with id 2
      And there is a member with id 3
      And the current system date is "2025-11-30"
      And the following meetings exist:
        | id | title    | description | locationName | locationAddress | locationCity | locationCountryCode | startDate  | endDate    | rsvpStartDate | rsvpEndDate | attendeesLimit | guestsLimit | creatorId |
        | 1  | meeting1 | description | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | 1         |

    Scenario: Successfully add a member to a meeting as attendee
      When member 2 is added to meeting 1
      Then the system shall not throw an error
      Then the number of meeting attendees shall be 1
      Then the following meeting attendees shall exist:
        | meetingId | memberId | guestNumber | role     | decisionDate |
        | 1         | 2        | 0           | Attendee | 2025-11-30   |
      Then the number of meeting waitlist members shall be 0

    Scenario: Successfully add a member to a meeting as waitlist member when attendees limit is reached
      Given the following meetings exist:
        | id | title    | description | locationName | locationAddress | locationCity | locationCountryCode | startDate  | endDate    | rsvpStartDate | rsvpEndDate | attendeesLimit | guestsLimit | creatorId |
        | 2  | meeting2 | description | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 1              | 5           | 1         |
      And the following meeting attendees exist:
        | meetingId | memberId | guestNumber | role     | decisionDate |
        | 2         | 2        | 0           | Attendee | 2025-11-29   |
      When member 3 is added to meeting 2
      Then the system shall not throw an error
      Then the number of meeting attendees shall be 1
      Then the number of meeting waitlist members shall be 1
      Then the following meeting waitlist members shall exist:
        | meetingId | memberId | decisionDate |
        | 2         | 3        | 2025-11-30   |

    Scenario: Unsuccessfully add a member to a non-existent meeting
      When member 2 is added to meeting 999
      Then the system shall throw with error message "Meeting does not exist."
      Then the number of meeting attendees shall be 0
      Then the number of meeting waitlist members shall be 0

    Scenario: Unsuccessfully add a non-existent member to a meeting
      When member 999 is added to meeting 1
      Then the system shall throw with error message "Member does not exist."
      Then the number of meeting attendees shall be 0
      Then the number of meeting waitlist members shall be 0

    Scenario: Unsuccessfully add a member who is already an attendee
      Given the following meeting attendees exist:
        | meetingId | memberId | guestNumber | role     | decisionDate |
        | 1         | 2        | 0           | Attendee | 2025-11-29   |
      When member 2 is added to meeting 1
      Then the system shall throw with error message "Member is already part of the meeting."
      Then the number of meeting attendees shall be 1
      Then the number of meeting waitlist members shall be 0

    Scenario: Unsuccessfully add a member who is already on the waitlist
      Given the following meetings exist:
        | id | title    | description | locationName | locationAddress | locationCity | locationCountryCode | startDate  | endDate    | rsvpStartDate | rsvpEndDate | attendeesLimit | guestsLimit | creatorId |
        | 2  | meeting2 | description | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 1              | 5           | 1         |
      And the following meeting attendees exist:
        | meetingId | memberId | guestNumber | role     | decisionDate |
        | 2         | 2        | 0           | Attendee | 2025-11-29   |
      And the following meeting waitlist members exist:
        | meetingId | memberId | signUpDate |
        | 2         | 3        | 2025-11-29 |
      When member 3 is added to meeting 2
      Then the system shall throw with error message "Member is already part of the meeting."
      Then the number of meeting attendees shall be 1
      Then the number of meeting waitlist members shall be 1

    Scenario: Unsuccessfully add a member who is a not-attendee
      Given the following meeting not attendees exist:
        | meetingId | memberId | decisionDate |
        | 1         | 2        | 2025-11-29   |
      When member 2 is added to meeting 1
      Then the system shall throw with error message "Member is already part of the meeting."
      Then the number of meeting attendees shall be 0
      Then the number of meeting not attendees shall be 1
      Then the number of meeting waitlist members shall be 0
