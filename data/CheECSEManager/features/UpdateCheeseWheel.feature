Feature: Update Cheese Wheel
As the facility manager, I want to update a cheese wheel in the system to mark it as spoiled.

  Background:
    Given the following farmer exists in the system
      | email             | password | address | name     |
      | farmer@cheecse.fr | P@ssw0rd |  112 Av | Farmer A |
    Given the following purchase exists in the system
      | purchaseDate | nrCheeseWheels | monthsAged | farmerEmail       |
      |   2025-04-04 |              5 | Six        | farmer@cheecse.fr |
    Given all cheese wheels from purchase 1 are created
    Given cheese wheel 1 is spoiled

  Scenario Outline: Successfully update a cheese wheel in the system
    When the facility manager attempts to update cheese wheel <id> in the system with isSpoiled "<updatedIsSpoiled>" and monthsAged "<updatedMonthsAged>"
    Then the number of cheese wheels in the system shall be 5
    Then the cheese wheel <id> with monthsAged "<updatedMonthsAged>", isSpoiled "<updatedIsSpoiled>", and purchaseId 1 shall exist in the system
    Then the purchase 1 shall have 5 cheese wheels

    Examples:
      | id | updatedIsSpoiled | updatedMonthsAged |
      |  1 | false            | ThirtySix         |
      |  2 | true             | Twelve            |

  Scenario: Successfully update a cheese wheel on a shelf to be spoiled
    Given the following shelf exists in the system
      | id  | nrColumns | nrRows |
      | A12 |         5 |      2 |
    Given all locations are created for shelf "A12"
    Given cheese wheel 2 is at shelf location with column 2 and row 1 of shelf "A12"
    When the facility manager attempts to update cheese wheel 2 in the system with isSpoiled "true" and monthsAged "Six"
    Then the number of cheese wheels in the system shall be 5
    Then the cheese wheel 2 with monthsAged "Six", isSpoiled "true", and purchaseId 1 shall exist in the system
    Then the purchase 1 shall have 5 cheese wheels
    Then the cheese wheel 2 shall not be on any shelf
    Then the number of cheese wheels on shelf "A12" shall be 0

  Scenario: Successfully update a cheese wheel in an order to be spoiled
    Given the following order exists in the system
      | transactionDate | nrCheeseWheels | monthsAged | deliveryDate | companyName  |
      |      2025-04-04 |              5 | Six        |   2025-10-10 | Cheesy Bites |
    Given all non-spoiled cheese wheels from purchase 1 are added to order 2
    When the facility manager attempts to update cheese wheel 3 in the system with isSpoiled "true" and monthsAged "Six"
    Then the number of cheese wheels in the system shall be 5
    Then the cheese wheel 3 with monthsAged "Six", isSpoiled "true", and purchaseId 1 shall exist in the system
    Then the purchase 1 shall have 5 cheese wheels
    Then the cheese wheel 3 shall not be part of any order
    Then the order 2 shall have 3 cheese wheels

  Scenario: Successfully update a cheese wheel in an order to a new months aged value
    Given the following order exists in the system
      | transactionDate | nrCheeseWheels | monthsAged | deliveryDate | companyName  |
      |      2025-04-04 |              5 | Six        |   2025-10-10 | Cheesy Bites |
    Given all non-spoiled cheese wheels from purchase 1 are added to order 2
    When the facility manager attempts to update cheese wheel 4 in the system with isSpoiled "false" and monthsAged "Twelve"
    Then the number of cheese wheels in the system shall be 5
    Then the cheese wheel 4 with monthsAged "Twelve", isSpoiled "false", and purchaseId 1 shall exist in the system
    Then the purchase 1 shall have 5 cheese wheels
    Then the cheese wheel 4 shall not be part of any order
    Then the order 2 shall have 3 cheese wheels

  Scenario: Unsuccessfully update a cheese wheel with an invalid monthsAged value
    When the facility manager attempts to update cheese wheel 2 in the system with isSpoiled "true" and monthsAged "notALiteral"
    Then the number of cheese wheels in the system shall be 5
    Then the cheese wheel 2 with monthsAged "Six", isSpoiled "false", and purchaseId 1 shall exist in the system
    Then the purchase 1 shall have 5 cheese wheels
    Then the error "The monthsAged must be Six, Twelve, TwentyFour, or ThirtySix." shall be raised

  Scenario Outline: Unsuccessfully update a cheese wheel to decrease its monthsAged value
    Given the following purchase exists in the system
      | purchaseDate | nrCheeseWheels | monthsAged | farmerEmail       |
      |   2025-04-04 |              2 | ThirtySix  | farmer@cheecse.fr |
    Given all cheese wheels from purchase 2 are created
    When the facility manager attempts to update cheese wheel <id> in the system with isSpoiled "<updatedIsSpoiled>" and monthsAged "<updatedMonthsAged>"
    Then the number of cheese wheels in the system shall be 7
    Then the cheese wheel <id> with monthsAged "<originalMonthsAged>", isSpoiled "<originalIsSpoiled>", and purchaseId <originalPurchaseId> shall exist in the system
    Then the purchase <originalPurchaseId> shall have 2 cheese wheels
    Then the error "Cannot decrease the monthsAged of a cheese wheel." shall be raised

    Examples:
      | id | updatedIsSpoiled | updatedMonthsAged | originalMonthsAged | originalIsSpoiled | originalPurchaseId |
      |  6 | false            | Twelve            | ThirtySix          | false             |                  2 |
      |  6 | false            | TwentyFour        | ThirtySix          | false             |                  2 |
      |  7 | true             | Six               | ThirtySix          | false             |                  2 |

  Scenario: Unsuccessfully update a cheese wheel that does not exist in the system
    When the facility manager attempts to update cheese wheel 30 in the system with isSpoiled "false" and monthsAged "Twelve"
    Then the number of cheese wheels in the system shall be 5
    Then the cheese wheel 30 shall not exist in the system
    Then the purchase 1 shall have 5 cheese wheels
    Then the error "The cheese wheel with id 30 does not exist." shall be raised
