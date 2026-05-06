Feature: Create house

  Background:
    Given there is a House system

  Scenario: Creating a new house successfully
    When a house with address "123 Main St", building material WOOD and empty basement type is created
    Then the created house has address "123 Main St" and building material WOOD
    Then the house has no basement
    Then the number of houses in the system is 1

  Scenario: Creating a new house with a basement successfully
    When a house with address "123 Main St", building material WOOD, basement type "concrete", basement name "basement", basement size 20.0, basement quality 0.9 and basement humidity 0.0 is created
    Then the created house has address "123 Main St" and building material WOOD
    Then the house has a concrete basement with name "basement", size 20.0 and quality 0.9
    Then the number of houses in the system is 1

  Scenario Outline: Creating a new house with invalid input
    When a house with address "<address>", building material <material>, basement type "<basementType>", basement name "<basementName>", basement size <basementSize>, basement quality <basementQuality> and basement humidity <basementHumidity> is created
    Then the system displays the error message "<error>"
    Then the number of houses in the system is 0

    Examples:
      | address     | material | basementType | basementName | basementSize | basementQuality | basementHumidity | error                                                               |
      |             | WOOD     | concrete     | basement     | 20.0         | 0.9             | 0.0              | The address of a house cannot be empty.                             |
      | 123 Main St |          | concrete     | basement     | 20.0         | 0.9             | 0.0              | The building material cannot be empty.                              |
      | 123 Main St | WOOD     | concrete     |              | 20.0         | 0.9             | 0.0              | The name of a basement cannot be empty.                             |
      | 123 Main St | WOOD     | concrete     | basement     | 0.0          | 0.9             | 0.0              | The size of a basement must be greater than 0.                      |
      | 123 Main St | WOOD     | metal        | basement     | 20.0         | 0.5             | 0.5              | The type of a basement must be either "concrete", "earth" or empty. |
      | 123 Main St | WOOD     | concrete     | basement     | 20.0         | -0.1            | 0.0              | The quality of a concrete basement must be between 0 and 1.         |
      | 123 Main St | WOOD     | concrete     | basement     | 20.0         | 2.0             | 0.0              | The quality of a concrete basement must be between 0 and 1.         |
      | 123 Main St | WOOD     | concrete     | basement     | 20.0         | 0.9             | 0.5              | The humidity of a concrete basement must be 0.                      |
      | 123 Main St | WOOD     | earth        | basement     | 20.0         | 0.0             | -0.1             | The humidity of an earth basement must be between 0 and 1.          |
      | 123 Main St | WOOD     | earth        | basement     | 20.0         | 0.0             | 2.0              | The humidity of an earth basement must be between 0 and 1.          |
      | 123 Main St | WOOD     | earth        | basement     | 20.0         | 0.5             | 0.9              | The quality of an earth basement must be 0.                         |
