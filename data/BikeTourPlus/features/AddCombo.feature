Feature: Add Combo
  As a manager, I want to add combos so that participants can rent them

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

  Scenario Outline: Add a combo successfully
    When the manager attempts to add a combo with name "<name>" and discount "<discount>"
    Then a combo shall exist with name "<name>" and discount "<discount>"
    Then the number of pieces of gear for the combo with name "<name>" shall be "0"
    Then the number of combos shall be "3"

    Examples:
      | name         | discount |
      | deluxe combo |       40 |
      | combo plus   |       10 |

  Scenario Outline: Add a combo unsuccessfully
    When the manager attempts to add a combo with name "<name>" and discount "<discount>"
    Then a combo shall not exist with name "<name>" and discount "<discount>"
    Then the number of combos shall be "2"
    Then the system shall raise the error "<error>"

    Examples:
      | name         | discount | error                                             |
      | deluxe combo |       -1 | Discount must be at least 0                       |
      | combo plus   |      101 | Discount must be no more than 100                 |
      |              |        0 | The name must not be empty                        |
      | helmet       |       35 | A piece of gear with the same name already exists |
      | small combo  |       30 | A combo with the same name already exists         |
