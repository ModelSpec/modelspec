Feature: Delete Guide
  As a manager, I want to delete guide accounts at the end of the season so that old accounts do not clutter the system

  Background: 
    Given the following BikeTourPlus system exists:
      | startDate  | nrWeeks | priceOfGuidePerWeek |
      | 2023-03-13 |      10 |                 100 |
    Given the following guides exist in the system:
      | email          | password | name | emergencyContact |
      | jeff@email.com | pass1    | Jeff | (555)555-5555    |
      | john@email.com | pass2    | John | (444)444-4444    |
    Given the following participants exist in the system:
      | email           | password | name  | emergencyContact | nrWeeks | weeksAvailableFrom | weeksAvailableUntil | lodgeRequired |
      | peter@email.com | pass1    | Peter | (666)555-5555    |       1 |                  1 |                   2 | true          |
      | tyler@email.com | pass2    | Tyler | (777)444-4444    |       2 |                  2 |                   5 | false         |

  Scenario Outline: Delete a guide successfully
    When the manager attempts to delete the guide with email "<email>"
    Then a guide account shall not exist with email "<email>"
    Then the number of guides shall be "<numberOfGuides>"

    Examples: 
      | email          | numberOfGuides |
      | jeff@email.com |              1 |
      | john@email.com |              1 |
      | kyle@email.com |              2 |
      | paul@email.com |              2 |

  Scenario Outline: Successfully delete a guide that does not exist but participant exists
    When the manager attempts to delete the guide with email "<email>"
    Then a participant account shall exist with email "<email>"
    Then the number of guides shall be "2"
    Then the number of participants shall be "2"

    Examples: 
      | email           |
      | peter@email.com |
      | tyler@email.com |

  Scenario: Successfully delete a guide that does not exist but manager exists
    When the manager attempts to delete the guide with email "manager@btp.com"
    Then a manager account shall exist with email "manager@btp.com"
    Then the number of guides shall be "2"
    Then the number of managers shall be "1"
