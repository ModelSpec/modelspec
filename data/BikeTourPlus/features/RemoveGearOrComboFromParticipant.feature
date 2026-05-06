Feature: Remove Gear and Combo for Participant
  As a participant, I want to remove gear and combos so that I can update what I use during my bike tour

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
    Given the following participants request the following pieces of gear:
      | email           | gear     | quantity |
      | peter@email.com | helmet   |        1 |
      | peter@email.com | bike bag |        2 |
    Given the following participants request the following combos:
      | email           | gear        | quantity |
      | peter@email.com | small combo |        1 |
      | tyler@email.com | large combo |        2 |
      | mary@email.com  | large combo |        1 |

  Scenario Outline: Remove a piece of gear or combo from a participant successfully
    When the manager attempts to remove a piece of gear or combo with name "<name>" from the participant with email "<email>"
    Then a piece of gear or combo shall exist with name "<name>" and quantity "<quantity>" for the participant with email "<email>"
    Then the number of pieces of gear or combos for the participant with email "<email>" shall be "<numberOfItemsForParticipant>"
    Then the number of participants shall be "3"

    Examples:
      | name        | quantity | email           | numberOfItemsForParticipant |
      | bike bag    |        1 | peter@email.com |                           3 |
      | large combo |        1 | tyler@email.com |                           1 |

  Scenario Outline: Remove the last item of a piece of gear or combo from a participant successfully
    When the manager attempts to remove a piece of gear or combo with name "<name>" from the participant with email "<email>"
    Then a piece of gear or combo shall not exist with name "<name>" for the participant with email "<email>"
    Then the number of pieces of gear or combos for the participant with email "<email>" shall be "<numberOfItemsForParticipant>"
    Then the number of participants shall be "3"

    Examples:
      | name        | email           | numberOfItemsForParticipant |
      | e-bike      | peter@email.com |                           3 |
      | e-bike      | tyler@email.com |                           1 |
      | helmet      | peter@email.com |                           2 |
      | helmet      | tyler@email.com |                           1 |
      | small combo | peter@email.com |                           2 |
      | small combo | tyler@email.com |                           1 |
      | large combo | peter@email.com |                           3 |
      | large combo | mary@email.com  |                           0 |

  Scenario Outline: Unsuccessfully remove a piece of gear or combo from a participant that does not exist
    When the manager attempts to remove a piece of gear or combo with name "<name>" from the participant with email "<email>"
    Then the number of participants shall be "3"
    Then the system shall raise the error "<error>"

    Examples:
      | name        | email          | error                          |
      | e-bike      | john@email.com | The participant does not exist |
      | helmet      | john@email.com | The participant does not exist |
      | e-bike      | joe@email.com  | The participant does not exist |
      | small combo | joe@email.com | The participant does not exist |
      | large combo | joe@email.com | The participant does not exist |
