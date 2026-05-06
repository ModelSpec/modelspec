Feature: Create job log

  Background:
    Given there is a House system
    Given the following houses exist in the system
      | address     | buildingMaterial |
      | 123 Main St | WOOD             |
    Given the following companies exist in the system
      | name     | address     |
      | FixIt Co | 456 Oak Ave |

  Scenario: Creating a new job log successfully
    When a job log with 5 hours and price 100.00 is created for house "123 Main St" and company "FixIt Co"
    Then the created job log has 5 hours and price 100.00
    Then the number of job logs in the system is 1

  Scenario Outline: Creating a new job log with invalid input
    When a job log with <hours> hours and price <price> is created for house "<houseAddress>" and company "<companyName>"
    Then the system displays the error message "<error>"
    Then the number of job logs in the system is 0

    Examples:
      | houseAddress | companyName | hours | price  | error                                       |
      | 123 Main St  | FixIt Co    | 0     | 100.00 | The number of hours must be greater than 0. |
      | 123 Main St  | FixIt Co    | 5     | -1.00  | The price must be at least 0.               |
      | 999 Fake St  | FixIt Co    | 5     | 100.00 | The house does not exist.                   |
      | 123 Main St  | Fake Co     | 5     | 100.00 | The company does not exist.                 |
