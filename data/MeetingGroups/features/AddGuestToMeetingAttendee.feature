Feature: Add Guest To Meeting Attendee

    Background:
      Given there is a UserAccess system
      And there is a Administration system
      And there is a Meetings system
      And there is a Payments system
      And there is a member with id 1
      And there is a member with id 2
      And the current system date is "2025-11-30"
      And the following meetings exist:
        | id | title    | description | locationName | locationAddress | locationCity | locationCountryCode | startDate  | endDate    | rsvpStartDate | rsvpEndDate | attendeesLimit | guestsLimit | meetingGroupId | creatorId |
        | 1  | meeting1 | description | location     | address         | city         | ca                  | 2025-12-01 | 2025-12-01 | 2025-11-30    | 2025-11-30  | 10             | 5           | 1              | 1         |
      And the following meeting attendees exist:
        | meetingId | memberId | guestNumber | role     | decisionDate |
        | 1         | 2        | 0           | Attendee | 2025-11-29   |

    Scenario: Successfully add guests to a meeting attendee
      When member 2 adds 3 guests to their attendance at meeting 1
      Then the system shall not throw an error
      Then the meeting attendee for member 2 at meeting 1 shall have guestNumber 3

    Scenario: Successfully add zero guests to a meeting attendee
      When member 2 adds 0 guests to their attendance at meeting 1
      Then the system shall not throw an error
      Then the meeting attendee for member 2 at meeting 1 shall have guestNumber 0

    Scenario: Unsuccessfully add negative guests to a meeting attendee
      When member 2 adds -1 guests to their attendance at meeting 1
      Then the system shall throw with error message "The guestNumber must be zero or positive."
      Then the meeting attendee for member 2 at meeting 1 shall have guestNumber 0

    Scenario: Unsuccessfully add guests for a non-existent meeting
      When member 2 adds 3 guests to their attendance at meeting 999
      Then the system shall throw with error message "Meeting does not exist."

    Scenario: Unsuccessfully add guests for a non-existent member
      When member 999 adds 3 guests to their attendance at meeting 1
      Then the system shall throw with error message "Member does not exist."

    Scenario: Unsuccessfully add guests for a member who is not an attendee
      Given there is a member with id 3
      When member 3 adds 3 guests to their attendance at meeting 1
      Then the system shall throw with error message "Member is not an attendee of the meeting."

    Scenario: Unsuccessfully add guests exceeding the guests limit
      When member 2 adds 6 guests to their attendance at meeting 1
      Then the system shall throw with error message "The guestNumber exceeds the meeting's guestsLimit."
      Then the meeting attendee for member 2 at meeting 1 shall have guestNumber 0
