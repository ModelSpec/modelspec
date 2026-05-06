Feature: Assign and Remove Cheese Wheel to/from Shelf Location
As the facility manager, I want to remove cheese wheels from a shelf when needed.

  Background:
    Given the following farmer exists in the system
      | email             | password | address | name     |
      | farmer@cheecse.fr | P@ssw0rd |  112 Av | Farmer A |
    Given the following shelf exists in the system
      | id  | nrColumns | nrRows |
      | A12 |         5 |      2 |
    Given all locations are created for shelf "A12"
    Given the following purchase exists in the system
      | purchaseDate | nrCheeseWheels | monthsAged | farmerEmail       |
      |   2025-04-04 |              5 | Six        | farmer@cheecse.fr |
    Given all cheese wheels from purchase 1 are created

  Scenario: Successfully remove a cheese wheel from a shelf location
    Given cheese wheel 1 is at shelf location with column 2 and row 1 of shelf "A12"
    When the facility manager attempts to remove cheese wheel 1 from its shelf location
    Then cheese wheel 1 shall not be on any shelf
    Then the number of cheese wheels on shelf "A12" shall be 0

  Scenario: Unsuccessfully remove a cheese wheel that does not exist
    When the facility manager attempts to remove cheese wheel 10 from its shelf location
    Then the error "The cheese wheel with id 10 does not exist." shall be raised
    Then the number of cheese wheels on shelf "A12" shall be 0

  Scenario: Unsuccessfully remove a cheese wheel that is not on a shelf
    When the facility manager attempts to remove cheese wheel 3 from its shelf location
    Then the error "The cheese wheel is not on any shelf." shall be raised
    Then the number of cheese wheels on shelf "A12" shall be 0
