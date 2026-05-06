Feature: Add Gear
  As a manager, I want to add pieces of gear so that participants can rent them

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

  Scenario Outline: Add a piece of gear successfully
    When the manager attempts to add a new piece of gear with name "<name>" and price per week "<pricePerWeek>"
    Then a piece of gear shall exist with name "<name>" and price per week "<pricePerWeek>"
    Then the number of pieces of gear shall be "4"

    Examples:
      | name          | pricePerWeek |
      | mountain bike |          100 |
      | tire kit      |           15 |

  Scenario Outline: Add a piece of gear unsuccessfully
    When the manager attempts to add a new piece of gear with name "<name>" and price per week "<pricePerWeek>"
    Then a piece of gear shall not exist with name "<name>" and price per week "<pricePerWeek>"
    Then the number of pieces of gear in the system shall be "3"
    Then the system shall raise the error "<error>"

    Examples:
      | name             | pricePerWeek | error                                                 |
      | lightweight bike |          -35 | The price per week must be greater than or equal to 0 |
      |                  |           35 | The name must not be empty                            |
      | helmet           |           35 | A piece of gear with the same name already exists     |
      | small combo      |           30 | A combo with the same name already exists             |
