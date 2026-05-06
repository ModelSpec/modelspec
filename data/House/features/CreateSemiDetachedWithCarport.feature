Feature: Create semi-detached house with carport

  Background:
    Given there is a House system

  Scenario: Creating a new semi-detached house with carports successfully
    When a semi-detached house with carports is created with address "123 Main St", building material WOOD, 4 windows, garden true, carport 1 doublePort true flatRoof false, carport 2 doublePort false flatRoof true, and empty basement type
    Then the created semi-detached house with carports has address "123 Main St", building material WOOD, 4 windows, and garden true
    Then carport 1 has doublePort true and flatRoof false
    Then carport 2 has doublePort false and flatRoof true
    Then the house has no basement
    Then the number of semi-detached houses with carports in the system is 1

  Scenario: Creating a new semi-detached house with carports and a basement successfully
    When a semi-detached house with carports is created with address "123 Main St", building material WOOD, 4 windows, garden true, carport 1 doublePort true flatRoof false, carport 2 doublePort false flatRoof true, basement type "earth", basement name "South", basement size 15.0, basement quality 0.0 and basement humidity 0.4
    Then the created semi-detached house with carports has address "123 Main St", building material WOOD, 4 windows, and garden true
    Then carport 1 has doublePort true and flatRoof false
    Then carport 2 has doublePort false and flatRoof true
    Then the house has an earth basement with name "South", size 15.0 and humidity 0.4
    Then the number of semi-detached houses with carports in the system is 1

  Scenario Outline: Creating a new semi-detached house with carports with invalid input
    When a semi-detached house with carports is created with address "<address>", building material <buildingMaterial>, <windows> windows, garden <garden>, carport 1 doublePort <dp1> flatRoof <fr1>, carport 2 doublePort <dp2> flatRoof <fr2>, basement type "<basementType>", basement name "<basementName>", basement size <basementSize>, basement quality <basementQuality> and basement humidity <basementHumidity>
    Then the system displays the error message "<error>"
    Then the number of semi-detached houses with carports in the system is 0

    Examples:
      | address     | buildingMaterial | windows | garden | dp1  | fr1   | dp2   | fr2  | basementType | basementName | basementSize | basementQuality | basementHumidity | error                                                               |
      |             | WOOD             | 4       | true   | true | false | false | true | concrete     | basement     | 20.0         | 0.9             | 0.0              | The address of a house cannot be empty.                             |
      | 123 Main St |                  | 4       | true   | true | false | false | true | concrete     | basement     | 20.0         | 0.9             | 0.0              | The building material cannot be empty.                              |
      | 123 Main St | WOOD             | -1      | true   | true | false | false | true | concrete     | basement     | 20.0         | 0.9             | 0.0              | The number of windows must be non-negative.                         |
      | 123 Main St | WOOD             | 4       | false  | true | false | false | true | concrete     |              | 20.0         | 0.9             | 0.0              | The name of a basement cannot be empty.                             |
      | 123 Main St | WOOD             | 4       | true   | true | false | false | true | concrete     | basement     | -1.0         | 0.9             | 0.0              | The size of a basement must be greater than 0.                      |
      | 123 Main St | WOOD             | 4       | true   | true | false | false | true | metal        | basement     | 20.0         | 0.5             | 0.5              | The type of a basement must be either "concrete", "earth" or empty. |
      | 123 Main St | WOOD             | 4       | true   | true | false | false | true | concrete     | basement     | 20.0         | -0.1            | 0.0              | The quality of a concrete basement must be between 0 and 1.         |
      | 123 Main St | WOOD             | 4       | true   | true | false | false | true | concrete     | basement     | 20.0         | 2.0             | 0.0              | The quality of a concrete basement must be between 0 and 1.         |
      | 123 Main St | WOOD             | 4       | true   | true | false | false | true | concrete     | basement     | 20.0         | 0.9             | 0.5              | The humidity of a concrete basement must be 0.                      |
      | 123 Main St | WOOD             | 4       | true   | true | false | false | true | earth        | basement     | 20.0         | 0.0             | -0.1             | The humidity of an earth basement must be between 0 and 1.          |
      | 123 Main St | WOOD             | 4       | true   | true | false | false | true | earth        | basement     | 20.0         | 0.0             | 2.0              | The humidity of an earth basement must be between 0 and 1.          |
      | 123 Main St | WOOD             | 4       | true   | true | false | false | true | earth        | basement     | 20.0         | 0.5             | 0.9              | The quality of an earth basement must be 0.                         |
