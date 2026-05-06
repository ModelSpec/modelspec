Feature: Create Meeting Group Proposal Decision

  Background:
    Given there is a UserAccess system
    And there is a Administration system
    And there is a Meetings system
    And there is a Payments system
    And there is an administrator with id 1
    And there is a member with id 2
    And the current system date is "2025-11-30"
    And the following meeting group proposals exist:
      | id | name          | description | city  | countryCode | memberId | status    | date       |
      | 1  | meetinggroup1 | description | city  | ca          | 2        | ToVerify  | 2025-11-29 |

  Scenario: Successfully verify a meeting group proposal
    Given member 2 has an active subscription
    When administrator 1 creates a meeting group proposal decision for proposal 1 with code "Accept" and reject reason ""
    Then the system shall not throw an error
    Then the proposal 1 shall have 1 decision
    Then the proposal 1 decision code shall be "Accept"
    Then the proposal 1 decision reject reason shall be ""
    Then the proposal 1 decision shall have date "2025-11-30"
    Then the proposal 1 status shall be "Verified"
    Then the following meeting groups shall exist:
      | id | name          | description | city  | countryCode | creatorId | createdDate |
      | 1  | meetinggroup1 | description | city  | ca          | 2         | 2025-11-30  |
    Then the number of meeting groups shall be 1
    Then the following meeting group members shall exist:
      | meetingGroupId | memberId | joinedDate | role      |
      | 1              | 2        | 2025-11-30 | Organizer |

  Scenario: Successfully reject a meeting group proposal
    Given member 2 has an active subscription
    When administrator 1 creates a meeting group proposal decision for proposal 1 with code "Reject" and reject reason "reason"
    Then the system shall not throw an error
    Then the proposal 1 shall have 1 decision
    Then the proposal 1 decision code shall be "Reject"
    Then the proposal 1 decision reject reason shall be "reason"
    Then the proposal 1 decision shall have date "2025-11-30"
    Then the proposal 1 status shall be "Rejected"
    Then the number of meeting groups shall be 0

  Scenario: Unsuccessfully verify meeting group proposal for member without an active subscription
    Given member 2 does not have an active subscription
    When administrator 1 creates a meeting group proposal decision for proposal 1 with code "Accept" and reject reason ""
    Then the system shall throw an error "Member does not have an active subscription"
    Then the proposal 1 shall have 0 decision
    Then the proposal 1 status shall be "ToVerify"
    Then the number of meeting groups shall be 0


  Scenario: Unsuccessfully verify meeting group proposal for member with an active subscription covering 3 meeting groups
    Given member 2 has an active subscription
    Given member 2 is the organizer of the following meeting groups:
      | name           | description | city | countryCode |
      | meetinggroup1  | description | city | ca          |
      | meetinggroup2  | description | city | ca          |
      | meetinggroup3  | description | city | ca          |
    When administrator 1 creates a meeting group proposal decision for proposal 1 with code "Accept" and reject reason ""
    Then the system shall throw an error "A maximum of 3 meeting groups can be covered by a subscription."
    Then the proposal 1 shall have 0 decision
    Then the proposal 1 status shall be "ToVerify"
    Then the number of meeting groups shall be 3