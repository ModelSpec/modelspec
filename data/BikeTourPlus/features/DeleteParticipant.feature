Feature: Delete Participant
  As a manager, I want to delete participant accounts at the end of the season so that old accounts do not clutter the system

  Background: 
    Given the following BikeTourPlus system exists:
      | startDate  | nrWeeks | priceOfGuidePerWeek |
      | 2023-03-13 |      10 |                 100 |
    Given the following pieces of gear exist in the system:
      | name     | pricePerWeek |
      | helmet   |           25 |
      | e-bike   |          150 |
      | bike bag |           19 |
    Given the following combos exist in the system:
      | name        | discount | items                  | quantity |
      | small combo |       10 | e-bike,helmet          |      1,2 |
      | large combo |       25 | e-bike,helmet,bike bag |    1,2,2 |
    Given the following guides exist in the system:
      | email          | password | name | emergencyContact |
      | jeff@email.com | pass1    | Jeff | (555)555-5555    |
      | john@email.com | pass2    | John | (444)444-4444    |
    Given the following participants exist in the system:
      | email           | password | name  | emergencyContact | nrWeeks | weeksAvailableFrom | weeksAvailableUntil | lodgeRequired |
      | peter@email.com | pass1    | Peter | (666)555-5555    |       1 |                  1 |                   2 | true          |
      | tyler@email.com | pass2    | Tyler | (777)444-4444    |       2 |                  2 |                   5 | false         |
      | mary@email.com  | pass3    | Mary  | (555)666-6666    |       1 |                  1 |                   2 | false         |

  Scenario Outline: Delete a participant successfully
    When the manager attempts to delete the participant with email "<email>"
    Then a participant account shall not exist with email "<email>"
    Then the number of participants shall be "<numberOfParticipants>"

    Examples: 
      | email                | numberOfParticipants |
      | peter@email.com      |                    2 |
      | tyler@email.com      |                    2 |
      | usernotfound@mail.ca |                    3 |

  Scenario Outline: Successfully delete a participant that does not exist but guide exists
    When the manager attempts to delete the participant with email "<email>"
    Then a guide account shall exist with email "<email>"
    Then the number of guides shall be "2"
    Then the number of participants shall be "3"

    Examples: 
      | email          |
      | jeff@email.com |
      | john@email.com |

  Scenario: Successfully delete a participant that does not exist but manager exists
    When the manager attempts to delete the participant with email "manager@btp.com"
    Then a manager account shall exist with email "manager@btp.com"
    Then the number of guides shall be "2"
    Then the number of managers shall be "1"

  Scenario Outline: Successfully delete a participant that has requested a piece of gear or combo
    Given the following participants request the following pieces of gear:
      | email           | gear     | quantity |
      | peter@email.com | helmet   |        1 |
      | peter@email.com | bike bag |        2 |
    Given the following participants request the following combos:
      | email           | gear        | quantity |
      | peter@email.com | small combo |        1 |
      | tyler@email.com | large combo |        2 |
      | mary@email.com  | large combo |        1 |
    When the manager attempts to delete the participant with email "<email>"
    Then a participant account shall not exist with email "<email>"
    Then the number of participants shall be "2"
    Then the piece of gear with name "<gearName>" shall be requested by "<numberOfParticipantsForGear>"
    Then the combo with name "<comboName>" shall be requested by "<numberOfParticipantsForCombo>"

    Examples: 
      | email           | gearName | numberOfParticipantsForGear | comboName   | numberOfParticipantsForCombo |
      | peter@email.com | helmet   |                           0 | small combo |                            0 |
      | peter@email.com | bike bag |                           0 | large combo |                            2 |
      | tyler@email.com | bike bag |                           1 | large combo |                            1 |
      | mary@email.com  | helmet   |                           1 | large combo |                            1 |
