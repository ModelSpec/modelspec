Feature: Update Combo
  As a manager, I want to update combos so that participants can rent them

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

  Scenario Outline: Update a combo successfully
    When the manager attempts to update the combo with name "<oldName>" to have name "<newName>" and discount "<newDiscount>"
    Then a combo shall exist with name "<newName>" and discount "<newDiscount>"
    Then the number of pieces of gear for the combo with name "<newName>" shall be "<numberOfGearInCombo>"
    Then a combo shall not exist with name "<oldName>" and discount "<oldDiscount>"
    Then the number of combos shall be "2"

    Examples:
      | oldName     | oldDiscount | newName      | newDiscount | numberOfGearInCombo |
      | small combo |          10 | deluxe combo |          40 |                   2 |
      | large combo |          25 | combo plus   |          10 |                   3 |

  Scenario Outline: Update a combo unsuccessfully
    When the manager attempts to update the combo with name "<oldName>" to have name "<newName>" and discount "<newDiscount>"
    Then a combo shall exist with name "<oldName>" and discount "<oldDiscount>"
    Then the number of pieces of gear for the combo with name "<oldName>" shall be "<numberOfGearInCombo>"
    Then a combo shall not exist with name "<newName>" and discount "<newDiscount>"
    Then the number of combos shall be "2"
    Then the system shall raise the error "<error>"

    Examples:
      | oldName     | oldDiscount | newName      | newDiscount | numberOfGearInCombo | error                                             |
      | small combo |          10 | deluxe combo |          -1 |                   2 | Discount must be at least 0                       |
      | small combo |          10 | combo plus   |         101 |                   2 | Discount must be no more than 100                 |
      | small combo |          10 |              |           0 |                   2 | The name must not be empty                        |
      | large combo |          25 | helmet       |          35 |                   3 | A piece of gear with the same name already exists |
      | large combo |          25 | small combo  |          30 |                   3 | A combo with the same name already exists         |

  Scenario Outline: Unsuccessfully update a combo that does not exist
    When the manager attempts to update the combo with name "<oldName>" to have name "<newName>" and discount "<newDiscount>"
    Then a combo shall not exist with name "<oldName>" and discount "<oldDiscount>"
    Then a combo shall not exist with name "<newName>" and discount "<newDiscount>"
    Then the number of combos shall be "2"
    Then the system shall raise the error "<error>"

    Examples:
      | oldName    | oldDiscount | newName      | newDiscount | error                    |
      | combo plus |          10 | deluxe combo |          15 | The combo does not exist |
