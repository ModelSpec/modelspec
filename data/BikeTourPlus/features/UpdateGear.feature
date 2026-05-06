Feature: Update Gear
  As a manager, I want to update pieces of gear so that participants can rent them

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

  Scenario Outline: Update a piece of gear successfully
    When the manager attempts to update the piece of gear with name "<oldName>" to have name "<newName>" and price per week "<newPricePerWeek>"
    Then a piece of gear shall exist with name "<newName>" and price per week "<newPricePerWeek>"
    Then a piece of gear shall not exist with name "<oldName>" and price per week "<oldPricePerWeek>"
    Then the number of pieces of gear shall be "3"

    Examples:
      | oldName  | oldPricePerWeek | newName             | newPricePerWeek |
      | e-bike   |             150 | lightweight e-bike  |             175 |
      | helmet   |              25 | bike helmet         |              25 |
      | bike bag |              19 | bike bag            |              17 |

  Scenario Outline: Update a piece of gear unsuccessfully
    When the manager attempts to update the piece of gear with name "<oldName>" to have name "<newName>" and price per week "<newPricePerWeek>"
    Then a piece of gear shall exist with name "<oldName>" and price per week "<oldPricePerWeek>"
    Then a piece of gear shall not exist with name "<newName>" and price per week "<newPricePerWeek>"
    Then the number of pieces of gear shall be "3"
    Then the system shall raise the error "<error>"

    Examples:
      | oldName | oldPricePerWeek | newName           | newPricePerWeek | error                                                 |
      | e-bike  |             150 | lighweight e-bike |             -35 | The price per week must be greater than or equal to 0 |
      | e-bike  |             150 |                   |              35 | The name must not be empty                            |
      | e-bike  |             150 | helmet            |             150 | A piece of gear with the same name already exists     |
      | e-bike  |             150 | small combo       |             150 | A combo with the same name already exists             |

  Scenario Outline: Unsuccessfully update a piece of gear that does not exist
    When the manager attempts to update the piece of gear with name "<oldName>" to have name "<newName>" and price per week "<newPricePerWeek>"
    Then a piece of gear shall not exist with name "<oldName>" and price per week "<oldPricePerWeek>"
    Then a piece of gear shall not exist with name "<newName>" and price per week "<newPricePerWeek>"
    Then the number of pieces of gear shall be "3"
    Then the system shall raise the error "<error>"

    Examples:
      | oldName | oldPricePerWeek | newName       | newPricePerWeek | error                            |
      | bike    |             150 | mountain bike |              35 | The piece of gear does not exist |
