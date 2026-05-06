Feature: Add Gear for Combo
  As a manager, I want to add gear for combos so that participants can rent them

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
    Given the following combos exist in the system:
      | name        | discount | items                  | quantity |
      | small combo |       10 | e-bike,helmet          |      1,2 |
      | large combo |       25 | e-bike,helmet,bike bag |    1,2,2 |

  Scenario Outline: Add a piece of gear to a combo successfully
    When the manager attempts to add a piece of gear with name "<gearName>" to the combo with name "<comboName>"
    Then a piece of gear shall exist with name "<gearName>" and quantity "<quantity>" for the combo with name "<comboName>"
    Then the number of pieces of gear for the combo with name "<comboName>" shall be "<numberOfGearInCombo>"
    Then the number of combos shall be "2"

    Examples:
      | gearName | quantity | comboName   | numberOfGearInCombo |
      | bike bag |        1 | small combo |                   3 |
      | bike bag |        3 | large combo |                   3 |
      | e-bike   |        2 | small combo |                   2 |
      | e-bike   |        2 | large combo |                   3 |
      | tire kit |        1 | small combo |                   3 |
      | tire kit |        1 | large combo |                   4 |

  Scenario Outline: Unsuccessfully add a piece of gear that does not exist to a combo
    When the manager attempts to add a piece of gear with name "<nonExistingGearName>" to the combo with name "<comboName>"
    Then a piece of gear shall exist with name "<gearName>" and quantity "<quantity>" for the combo with name "<comboName>"
    Then the number of pieces of gear for the combo with name "<comboName>" shall be "<numberOfGearInCombo>"
    Then the number of combos shall be "2"
    Then the system shall raise the error "<error>"

    Examples:
      | nonExistingGearName | gearName | quantity | comboName   | numberOfGearInCombo | error                            |
      | spare tire          | e-bike   |        1 | small combo |                   2 | The piece of gear does not exist |
      | bike lock           | helmet   |        2 | small combo |                   2 | The piece of gear does not exist |
      | spare tire          | e-bike   |        1 | large combo |                   3 | The piece of gear does not exist |
      | bike lock           | helmet   |        2 | large combo |                   3 | The piece of gear does not exist |
      | bike lock           | bike bag |        2 | large combo |                   3 | The piece of gear does not exist |

  Scenario Outline: Unsuccessfully add a piece of gear to a combo that does not exist
    When the manager attempts to add a piece of gear with name "<gearName>" to the combo with name "<comboName>"
    Then the number of combos shall be "2"
    Then the system shall raise the error "<error>"

    Examples:
      | gearName | comboName    | error                    |
      | e-bike   | deluxe combo | The combo does not exist |
      | helmet   | deluxe combo | The combo does not exist |
      | e-bike   | combo plus   | The combo does not exist |
      | helmet   | combo plus   | The combo does not exist |
      | bike bag | combo plus   | The combo does not exist |
