Feature: Assign and Remove Cheese Wheel to/from Shelf Location
As the facility manager, I want to assign cheese wheels to a shelf when needed.

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

  Scenario: Successfully assign a cheese wheel to an empty shelf location
    When the facility manager attempts to assign cheese wheel 1 to shelf location with column 2 and row 1 of shelf "A12"
    Then the cheese wheel 1 shall be at shelf location with column 2 and row 1 of shelf "A12"
    Then the number of cheese wheels on shelf "A12" shall be 1

  Scenario: Successfully assign a cheese wheel to a new empty shelf location on the same shelf
    Given cheese wheel 1 is at shelf location with column 2 and row 1 of shelf "A12"
    When the facility manager attempts to assign cheese wheel 1 to shelf location with column 1 and row 1 of shelf "A12"
    Then the cheese wheel 1 shall be at shelf location with column 1 and row 1 of shelf "A12"
    Then the number of cheese wheels on shelf "A12" shall be 1

  Scenario: Successfully assign a cheese wheel to a new empty shelf location on a different shelf
    Given the following shelf exists in the system
      | id  | nrColumns | nrRows |
      | B11 |         1 |      1 |
    Given all locations are created for shelf "B11"
    Given cheese wheel 1 is at shelf location with column 2 and row 1 of shelf "A12"
    When the facility manager attempts to assign cheese wheel 1 to shelf location with column 1 and row 1 of shelf "B11"
    Then the cheese wheel 1 shall be at shelf location with column 1 and row 1 of shelf "B11"
    Then the number of cheese wheels on shelf "B11" shall be 1
    Then the number of cheese wheels on shelf "A12" shall be 0

  Scenario: Unsuccessfully assign a cheese wheel that does not exist
    When the facility manager attempts to assign cheese wheel 10 to shelf location with column 2 and row 1 of shelf "A12"
    Then the error "The cheese wheel with id 10 does not exist." shall be raised
    Then the number of cheese wheels on shelf "A12" shall be 0

  Scenario: Unsuccessfully assign a spoiled cheese wheel to a shelf location
    Given cheese wheel 2 is spoiled
    When the facility manager attempts to assign cheese wheel 2 to shelf location with column 2 and row 1 of shelf "A12"
    Then the error "Cannot place a spoiled cheese wheel on a shelf." shall be raised
    Then the number of cheese wheels on shelf "A12" shall be 0

  Scenario: Unsuccessfully assign a cheese wheel to a non-existent shelf location
    When the facility manager attempts to assign cheese wheel 1 to shelf location with column 6 and row 1 of shelf "A12"
    Then the error "The shelf location does not exist." shall be raised
    Then the number of cheese wheels on shelf "A12" shall be 0

  Scenario: Unsuccessfully assign a cheese wheel to an occupied shelf location
    Given cheese wheel 1 is at shelf location with column 2 and row 1 of shelf "A12"
    When the facility manager attempts to assign cheese wheel 3 to shelf location with column 2 and row 1 of shelf "A12"
    Then the error "The shelf location is already occupied." shall be raised
    Then the cheese wheel 1 shall be at shelf location with column 2 and row 1 of shelf "A12"
    Then the number of cheese wheels on shelf "A12" shall be 1
