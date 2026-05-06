Feature: Display Farmer
As the facility manager, I want to display all farmers from the system with all their details including supplied cheese wheels.

  Background:
    Given the following farmer exists in the system
      | email              | password  | address | name     |
      | farmer@cheecse.fr  | P@ssw0rd  |  112 Av | Farmer A |
      | farmer2@cheecse.ca | Pass$word |  55 Mtl | Farmer B |
    Given the following purchase exists in the system
      | purchaseDate | nrCheeseWheels | monthsAged | farmerEmail       |
      |   2025-09-01 |              2 | Six        | farmer@cheecse.fr |
      |   2025-08-15 |              3 | Twelve     | farmer@cheecse.fr |
    Given all cheese wheels from purchase 1 are created
    Given all cheese wheels from purchase 2 are created
    Given cheese wheel 2 is spoiled

  Scenario: Successfully display all farmers from the system
    When the facility manager attempts to display from the system all the farmers
    Then the number of farmers in the system shall be 2
    Then the following farmer details shall be presented
      | email              | password  | address | name     |
      | farmer@cheecse.fr  | P@ssw0rd  |  112 Av | Farmer A |
      | farmer2@cheecse.ca | Pass$word |  55 Mtl | Farmer B |
    Then the following cheese wheels shall be presented for farmer "farmer@cheecse.fr"
      | id | monthsAged | isSpoiled | purchaseDate |
      |  1 | Six        | false     |   2025-09-01 |
      |  2 | Six        | true      |   2025-09-01 |
      |  3 | Twelve     | false     |   2025-08-15 |
      |  4 | Twelve     | false     |   2025-08-15 |
      |  5 | Twelve     | false     |   2025-08-15 |
    Then no cheese wheels shall be presented for farmer "farmer2@cheecse.ca"
