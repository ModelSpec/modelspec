Feature: Add Member To Meeting Group

    Background:
      Given there is a UserAccess system
      And there is a Administration system
      And there is a Meetings system
      And there is a Payments system
      And there is a member with id 1
      And there is a member with id 2
      And the current system date is "2025-11-30"
      And the following meeting groups exist:
        | id | name          | description | city | countryCode | creatorId | createdDate |
        | 1  | meetinggroup1 | description | city | ca          | 1         | 2025-11-29  |

    Scenario: Successfully add a member to a meeting group
      When member 2 is added to meeting group 1
      Then the system shall not throw an error
      Then the number of meeting group members shall be 1
      Then the following meeting group members shall exist:
        | meetingGroupId | memberId | joinedDate | role   | isActive |
        | 1              | 2        | 2025-11-30 | Member | true     |

    Scenario: Unsuccessfully add a member to a non-existent meeting group
      When member 2 is added to meeting group 999
      Then the system shall throw with error message "Meeting group does not exist."
      Then the number of meeting group members shall be 0

    Scenario: Unsuccessfully add a non-existent member to a meeting group
      When member 999 is added to meeting group 1
      Then the system shall throw with error message "Member does not exist."
      Then the number of meeting group members shall be 0

    Scenario: Unsuccessfully add a member who is already part of the meeting group
      Given the following meeting group members exist:
        | meetingGroupId | memberId | joinedDate | role   | isActive |
        | 1              | 2        | 2025-11-29 | Member | true     |
      When member 2 is added to meeting group 1
      Then the system shall throw with error message "Member is already part of the meeting group."
      Then the number of meeting group members shall be 1
