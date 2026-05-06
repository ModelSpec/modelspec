Feature: Remove Gear for Combo
  As a manager, I want to remove gear for combos so that participants can rent them

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

  Scenario Outline: Remove a piece of gear from a combo successfully
    When the manager attempts to remove a piece of gear with name "<gearName>" from the combo with name "<comboName>"
    Then a piece of gear shall exist with name "<gearName>" and quantity "<quantity>" for the combo with name "<comboName>"
    Then the number of pieces of gear for the combo with name "<comboName>" shall be "<numberOfGearInCombo>"
    Then the number of combos shall be "2"

    Examples:
      | gearName | quantity | comboName   | numberOfGearInCombo |
      | helmet   |        1 | small combo |                   2 |
      | helmet   |        1 | large combo |                   3 |
      | bike bag |        1 | large combo |                   3 |

  Scenario Outline: Remove the last item of a piece of gear from a combo successfully
    When the manager attempts to remove a piece of gear with name "<gearName>" from the combo with name "<comboName>"
    Then a piece of gear shall not exist with name "<gearName>" for the combo with name "<comboName>"
    Then the number of pieces of gear for the combo with name "<comboName>" shall be "<numberOfGearInCombo>"
    Then the number of combos shall be "2"

    Examples:
      | gearName   | comboName   | numberOfGearInCombo |
      | e-bike     | large combo |                   2 |
      | spare tire | small combo |                   2 |
      | spare tire | large combo |                   3 |

  Scenario Outline: Remove a piece of gear from a combo unsuccessfully
    When the manager attempts to remove a piece of gear with name "<gearName>" from the combo with name "<comboName>"
    Then a piece of gear shall exist with name "<gearName>" and quantity "<quantity>" for the combo with name "<comboName>"
    Then the number of pieces of gear for the combo with name "<comboName>" shall be "<numberOfGearInCombo>"
    Then the number of combos shall be "2"
    Then the system shall raise the error "<error>"

    Examples:
      | gearName | quantity | comboName   | numberOfGearInCombo | error                                         |
      | e-bike   |        1 | small combo |                   2 | A combo must have at least two pieces of gear |

  Scenario Outline: Unsuccessfully remove a piece of gear from a combo that does not exist
    When the manager attempts to remove a piece of gear with name "<gearName>" from the combo with name "<comboName>"
    Then the number of combos shall be "2"
    Then the system shall raise the error "<error>"

    Examples:
      | gearName | comboName    | error                    |
      | e-bike   | deluxe combo | The combo does not exist |
      | helmet   | deluxe combo | The combo does not exist |
      | e-bike   | combo plus   | The combo does not exist |
      | helmet   | combo plus   | The combo does not exist |
      | bike bag | combo plus   | The combo does not exist |
