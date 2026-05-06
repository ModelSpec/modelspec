Feature: Create Meeting Group Proposal

  Background:
    Given there is a UserAccess system
    And there is a Administration system
    And there is a Meetings system
    And there is a Payments system
    And there is a member with id 1
    And the current system date is "2025-11-30"

  Scenario: Successfully create a meeting group proposal
    Given member 1 has an active subscription
    When member 1 creates a meeting group proposal with name "meetinggroup1" and description "description" and city "city" and countryCode "ca"
    Then the system shall not throw an error
    Then the number of meeting group proposals shall be 1
    Then the proposal shall have an id
    Then the proposal name shall be "meetinggroup1"
    Then the proposal description shall be "description"
    Then the proposal location city shall be "city"
    Then the proposal location countryCode shall be "ca"
    Then the proposal status shall be "ToVerify"
    Then the proposal shall have date "2025-11-30"
    Then the proposal shall have member 1

  Scenario: Successfully create a meeting group proposal with automatically unique id
    Given there is a meeting group proposal with id 1
    Given member 1 has an active subscription
    When member 1 creates a meeting group proposal with name "meetinggroup1" and description "description" and city "city" and countryCode "ca"
    Then the system shall not throw an error
    Then the number of meeting group proposals shall be 1
    Then the proposal shall have an id
    Then the proposal id shall not be 1
    Then the proposal name shall be "meetinggroup1"
    Then the proposal description shall be "description"
    Then the proposal location city shall be "city"
    Then the proposal location countryCode shall be "ca"
    Then the proposal status shall be "ToVerify"
    Then the proposal shall have date "2025-11-30"
    Then the proposal shall have member 1


  Scenario Outline: Unsuccessfully create a meeting group proposal with invalid values
    Given member 1 has an active subscription
    When member 1 creates a MeetingGroupProposal with name "<name>" and description "<description>" in city "<city>" and countryCode "<countryCode>"
    Then the system shall throw with error message "<errorMessage>"
    Then the number of meeting group proposals shall be 0

    Examples:
      | name          | description | city | countryCode | errorMessage                                            |
      |               | description | city | ca          | The name must not be empty.                             |
      | meetinggroup1 |             | city | ca          | The description must not be empty.                      |
      | meetinggroup1 | description |      | ca          | The city must not be empty.                             |
      | meetinggroup1 | description | city |             | The country code must not be empty.                     |
      | meetinggroup1 | description | city | c           | The country code must be either 2 or 3 characters long. |
      | meetinggroup1 | description | city | cabd        | The country code must be either 2 or 3 characters long. |

  Scenario: Unsuccessfully create a meeting group proposal without an active subscription
    Given member 1 does not have an active subscription
    When member 1 creates a meeting group proposal with name "meetinggroup1" and description "description" and city "city" and countryCode "ca"
    Then the system shall throw with error message "Must have an active subscription to create a meeting group proposal."
    Then the number of meeting group proposals shall be 0

  Scenario: Unsuccessfully create a meeting group proposal with an active subscription covering 3 meeting groups
    Given member 1 has an active subscription
    Given member 1 is the organizer of the following meeting groups:
      | name          | description | city | countryCode |
      | meetinggroup1 | description | city | ca          |
      | meetinggroup2 | description | city | ca          |
      | meetinggroup3 | description | city | ca          |
    When member 1 creates a meeting group proposal with name "meetinggroup4" and description "description" and city "city" and countryCode "ca"
    Then the system shall throw with error message "A maximum of 3 meeting groups can be covered by a subscription."
    Then the number of meeting group proposals shall be 3