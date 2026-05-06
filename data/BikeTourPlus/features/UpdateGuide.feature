Feature: Update Guide
  As a guide, I want to update my guide account so that I can work on bike tours

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

  Scenario Outline: Update a guide account successfully
    When the guide with email "<email>" attempts to update their account information to password "<newPassword>", name "<newName>", and emergency contact "<newEmergencyContact>"
    Then a guide account shall exist with email "<email>", password "<newPassword>", name "<newName>", and emergency contact "<newEmergencyContact>"
    Then a guide account shall not exist with email "<email>", password "<password>", name "<name>", and emergency contact "<emergencyContact>"
    Then the number of guides shall be "2"

    Examples:
      | email          | password | name | emergencyContact | newPassword | newName | newEmergencyContact |
      | jeff@email.com | pass1    | Jeff | (555)555-5555    | pass5       | Jake    | (111)111-1111       |
      | john@email.com | pass2    | John | (444)444-4444    | pass6       | Johnny  | (111)777-7777       |

  Scenario Outline: Update a guide account unsuccessfully
    When the guide with email "<email>" attempts to update their account information to password "<newPassword>", name "<newName>", and emergency contact "<newEmergencyContact>"
    Then a guide account shall exist with email "<email>", password "<password>", name "<name>", and emergency contact "<emergencyContact>"
    Then a guide account shall not exist with email "<email>", password "<newPassword>", name "<newName>", and emergency contact "<newEmergencyContact>"
    Then the number of guides shall be "2"
    Then the system shall raise the error "<error>"

    Examples:
      | email          | password | name | emergencyContact | newPassword | newName | newEmergencyContact | error                             |
      | jeff@email.com | pass1    | Jeff | (555)555-5555    |             | Jeff    | (555)666-5555       | Password cannot be empty          |
      | john@email.com | pass2    | John | (444)444-4444    | pass2       |         | (444)444-7777       | Name cannot be empty              |
      | john@email.com | pass2    | John | (444)444-4444    | pass2       | John    |                     | Emergency contact cannot be empty |

  Scenario Outline: Unsuccessfully update a guide account that does not exist
    When the guide with email "<email>" attempts to update their account information to password "<newPassword>", name "<newName>", and emergency contact "<newEmergencyContact>"
    Then a guide account shall not exist with email "<email>", password "<password>", name "<name>", and emergency contact "<emergencyContact>"
    Then a guide account shall not exist with email "<email>", password "<newPassword>", name "<newName>", and emergency contact "<newEmergencyContact>"
    Then the number of guides shall be "2"
    Then the system shall raise the error "<error>"

    Examples:
      | email          | password | name | emergencyContact | newPassword | newName | newEmergencyContact | error                            |
      | jane@email.com | pass1    | Jane | (333)333-3333    | pass2       | Jeff    | (555)666-4444       | The guide account does not exist |
