Feature: Update Person Abilities
  Background:
    Given there is a HomeForTheElderly system
    Given there is a person with id "person" and name "John Doe" and birthdate "1950-01-01"
    Given the current system date is "2020-01-01"

  Scenario Outline: Updating a person's abilities
    When the abilities of person "person" is updated to "<abilities>"
    Then the system shall not throw an error
    Then person "person" shall have abilities "<abilities>"

    Examples:
    | abilities           |
    | requires wheelchair |
    |                     |
    

  Scenario: Updating abilities of a person that does not exist
    When the abilities of person "unknown" is updated to "requires wheelchair"
    Then the system shall throw with error message "Person with ID \"unknown\" does not exist."