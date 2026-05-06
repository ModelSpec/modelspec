Feature: Delete Gear
  As a manager, I want to delete existing pieces of gear so that I can restrict the gear available to participants

  Background: 
    Given the following BikeTourPlus system exists:
      | startDate  | nrWeeks | priceOfGuidePerWeek |
      | 2023-03-13 |      10 |                 100 |
    Given the following pieces of gear exist in the system:
      | name     | pricePerWeek |
      | helmet   |           25 |
      | e-bike   |          150 |
      | bike bag |           19 |
      | tire kit |           15 |

  Scenario Outline: Delete a piece of gear successfully
    When the manager attempts to delete the piece of gear with name "<name>"
    Then a piece of gear shall not exist with name "<name>"
    Then the number of pieces of gear shall be "<numberOfGear>"

    Examples: 
      | name          | numberOfGear |
      | helmet        |            3 |
      | bike bag      |            3 |
      | mountain bike |            4 |
      | spare tire    |            4 |

  Scenario Outline: Successfully delete a piece of gear that has been requested by a participant
    Given the following participants exist in the system:
      | email           | password | name  | emergencyContact | nrWeeks | weeksAvailableFrom | weeksAvailableUntil | lodgeRequired |
      | peter@email.com | pass1    | Peter | (666)555-5555    |       1 |                 1  |                  2  | true          |
    Given the following participants request the following pieces of gear:
      | email           | gear     | quantity |
      | peter@email.com | helmet   |        1 |
      | peter@email.com | bike bag |        2 |
    When the manager attempts to delete the piece of gear with name "<name>"
    Then a piece of gear shall not exist with name "<name>"
    Then the number of pieces of gear shall be "3"
    Then the participant with email "<email>" shall have a piece of gear with name "<requestedGearName>" and quantity "<quantity>"
    Then the number of pieces of gear for the participant with email "<email>" shall be "<numberOfRequestedGear>"

    Examples: 
      | name          | email           | requestedGearName | quantity | numberOfRequestedGear |
      | helmet        | peter@email.com | bike bag          |        2 |                     1 |
      | bike bag      | peter@email.com | helmet            |        1 |                     1 |

  Scenario Outline: Unsuccessfully delete a piece of gear that is in an existing combo
    Given the following combos exist in the system:
      | name        | discount | items                  | quantity |
      | small combo |       10 | e-bike,helmet          |      1,2 |
    When the manager attempts to delete the piece of gear with name "<name>"
    Then a piece of gear shall exist with name "<name>" and price per week "<pricePerWeek>"
    Then the number of pieces of gear shall be "4"
    Then the combo with name "<comboName>" shall have a piece of gear with name "<name>" and quantity "<quantity>"
    Then the number of pieces of gear for the combo with name "<comboName>" shall be "<numberOfGearInCombo>"
    Then the system shall raise the error "The piece of gear is in a combo and cannot be deleted"

    Examples: 
      | name   | pricePerWeek | comboName   | quantity | numberOfGearInCombo |
      | helmet |           25 | small combo |        2 |                   2 |
      | e-bike |          150 | small combo |        1 |                   2 |
