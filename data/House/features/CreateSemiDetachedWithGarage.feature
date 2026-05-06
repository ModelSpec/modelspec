Feature: Create semi-detached house with garage

  Background:
    Given there is a House system

  Scenario: Creating a new semi-detached house with garage successfully
    When a semi-detached house with garage is created with address "123 Main St", building material WOOD, 4 windows, garden true, garage automatic true, and empty basement type
    Then the created semi-detached house with garage has address "123 Main St", building material WOOD, 4 windows, and garden true
    Then the garage has automatic true
    Then the house has no basement
    Then the number of semi-detached houses with garages in the system is 1

  Scenario: Creating a new semi-detached house with garage and a basement successfully
    When a semi-detached house with garage is created with address "123 Main St", building material WOOD, 4 windows, garden true, garage automatic true, basement type "concrete", basement name "North", basement size 20.0, basement quality 0.9 and basement humidity 0.0
    Then the created semi-detached house with garage has address "123 Main St", building material WOOD, 4 windows, and garden true
    Then the garage has automatic true
    Then the house has a concrete basement with name "North", size 20.0 and quality 0.9
    Then the number of semi-detached houses with garages in the system is 1

  Scenario Outline: Creating a new semi-detached house with garage with invalid input
    When a semi-detached house with garage is created with address "<address>", building material <buildingMaterial>, <windows> windows, garden <garden>, garage automatic <automatic>, basement type "<basementType>", basement name "<basementName>", basement size <basementSize>, basement quality <basementQuality> and basement humidity <basementHumidity>
    Then the system displays the error message "<error>"
    Then the number of semi-detached houses with garages in the system is 0

    Examples:
      | address     | buildingMaterial | windows | garden | automatic | basementType | basementName | basementSize | basementQuality | basementHumidity | error                                                               |
      |             | WOOD             | 4       | true   | true      | concrete     | basement     | 20.0         | 0.9             | 0.0              | The address of a house cannot be empty.                             |
      | 123 Main St |                  | 4       | true   | true      | concrete     | basement     | 20.0         | 0.9             | 0.0              | The building material cannot be empty.                              |
      | 123 Main St | WOOD             | -1      | true   | true      | concrete     | basement     | 20.0         | 0.9             | 0.0              | The number of windows must be non-negative.                         |
      | 123 Main St | WOOD             | 4       | false  | true      | concrete     |              | 20.0         | 0.9             | 0.0              | The name of a basement cannot be empty.                             |
      | 123 Main St | WOOD             | 4       | true   | true      | concrete     | basement     | -1.0         | 0.9             | 0.0              | The size of a basement must be greater than 0.                      |
      | 123 Main St | WOOD             | 4       | true   | true      | metal        | basement     | 20.0         | 0.5             | 0.5              | The type of a basement must be either "concrete", "earth" or empty. |
      | 123 Main St | WOOD             | 4       | true   | true      | concrete     | basement     | 20.0         | -0.1            | 0.0              | The quality of a concrete basement must be between 0 and 1.         |
      | 123 Main St | WOOD             | 4       | true   | true      | concrete     | basement     | 20.0         | 2.0             | 0.0              | The quality of a concrete basement must be between 0 and 1.         |
      | 123 Main St | WOOD             | 4       | true   | true      | concrete     | basement     | 20.0         | 0.9             | 0.5              | The humidity of a concrete basement must be 0.                      |
      | 123 Main St | WOOD             | 4       | true   | true      | earth        | basement     | 20.0         | 0.0             | -0.1             | The humidity of an earth basement must be between 0 and 1.          |
      | 123 Main St | WOOD             | 4       | true   | true      | earth        | basement     | 20.0         | 0.0             | 2.0              | The humidity of an earth basement must be between 0 and 1.          |
      | 123 Main St | WOOD             | 4       | true   | true      | earth        | basement     | 20.0         | 0.5             | 0.9              | The quality of an earth basement must be 0.                         |
