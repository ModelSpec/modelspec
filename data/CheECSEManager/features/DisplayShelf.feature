Feature: Display Shelf
As the facility manager, I want to display a shelf from the system with all its details.

  Background:
    Given the following shelf exists in the system
      | id  | nrColumns | nrRows |
      | A12 |         5 |      1 |
      | B16 |         6 |      2 |
    Given all locations are created for shelf "A12"
    Given all locations are created for shelf "B16"
    Given the following farmer exists in the system
      | email             | password | address | name     |
      | farmer@cheecse.fr | P@ssw0rd |  112 Av | Farmer A |
    Given the following purchase exists in the system
      | purchaseDate | nrCheeseWheels | monthsAged | farmerEmail       |
      |   2025-09-01 |              2 | Six        | farmer@cheecse.fr |
      |   2025-08-01 |              3 | Twelve     | farmer@cheecse.fr |
    Given all cheese wheels from purchase 1 are created
    Given all cheese wheels from purchase 2 are created
    Given the following cheese wheel exists on shelf "A12"
      | column | row | id |
      |      1 |   1 |  1 |
      |      3 |   1 |  2 |
      |      4 |   1 |  3 |

  Scenario: Successfully display a shelf from the system
    When the facility manager attempts to display from the system the shelf with id "A12"
    Then the number of shelves in the system shall be 2
    Then the following shelf details shall be presented
      | id  | nrColumns | nrRows |
      | A12 |         5 |      1 |
    Then the following cheese wheels shall be presented for shelf "A12"
      | column | row | id | monthsAged |
      |      1 |   1 |  1 | Six        |
      |      3 |   1 |  2 | Six        |
      |      4 |   1 |  3 | Twelve     |

  Scenario: Unsuccessfully display a shelf that does not exist in the system
    When the facility manager attempts to display from the system the shelf with id "C34"
    Then the number of shelves in the system shall be 2
    Then no shelves shall be presented
