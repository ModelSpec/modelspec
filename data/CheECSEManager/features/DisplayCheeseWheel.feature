Feature: Display Cheese Wheel
As the facility manager, I want to display a cheese wheel from the system.

  Background:
    Given the following farmer exists in the system
      | email             | password | address | name     |
      | farmer@cheecse.fr | P@ssw0rd |  112 Av | Farmer A |
    Given the following purchase exists in the system
      | purchaseDate | nrCheeseWheels | monthsAged | farmerEmail       |
      |   2025-04-04 |              5 | Six        | farmer@cheecse.fr |
    Given all cheese wheels from purchase 1 are created
    Given cheese wheel 1 is spoiled

  Scenario: Successfully display a cheese wheel from the system
    When the facility manager attempts to display cheese wheel 1
    Then the following cheese wheels shall be presented
      | id | monthsAged | isSpoiled | purchaseDate | shelfId | column | row | isOrdered |
      |  1 | Six        | true      |   2025-04-04 |         |     -1 |  -1 | false     |
    Then the number of cheese wheels in the system shall be 5

  Scenario: Successfully display a cheese wheel from a system that is on a shelf and part of an order
    Given the following shelf exists in the system
      | id  | nrColumns | nrRows |
      | A12 |         5 |      2 |
    Given all locations are created for shelf "A12"
    Given the cheese wheel with id 2 is located at shelf "A12" at column 2 and row 1
    Given the following order exists in the system
      | transactionDate | nrCheeseWheels | monthsAged | deliveryDate | companyName  |
      |      2025-04-04 |              5 | Six        |   2026-04-04 | Cheesy Bites |
    Given all non-spoiled cheese wheels from purchase 1 are part of order 2
    When the facility manager attempts to display cheese wheel 2
    Then the following cheese wheels shall be presented
      | id | monthsAged | isSpoiled | purchaseDate | shelfId | column | row | isOrdered |
      |  2 | Six        | false     |   2025-04-04 | A12     |      2 |   1 | true      |
    Then the number of cheese wheels in the system shall be 5

  Scenario: Unsuccessfully display a cheese wheel that does not exist
    When the facility manager attempts to display cheese wheel 10
    Then no cheese wheels shall be presented
    Then the number of cheese wheels in the system shall be 5
