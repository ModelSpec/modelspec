Feature: Display WholesaleCompany
As the facility manager, I want to display all wholesale companies from the system with all its details.

  Background:
    Given the following wholesale company exists in the system
      | name         | address |
      | Cheesy Bites |  112 Av |
    Given the following farmer exists in the system
      | email               | password | address  | name     |
      | farmer1@example.com | pass123  | 123 Farm | Farmer 1 |
    Given the following purchase exists in the system
      | purchaseDate | nrCheeseWheels | monthsAged | farmerEmail         |
      |   2025-01-01 |              5 | Six        | farmer1@example.com |
    Given all cheese wheels from purchase 1 are created
    Given the following order exists in the system
      | transactionDate  | nrCheeseWheels | monthsAged | companyName  | deliveryDate |
      | 2025-08-15 |             10 | Six        | Cheesy Bites |   2025-12-15 |
      | 2025-09-01 |              3 | Twelve     | Cheesy Bites |   2026-03-01 |
    Given all non-spoiled cheese wheels from purchase 1 are added to order 2

  Scenario: Successfully display all wholesale companies from the system
    Given the following wholesale company exists in the system
      | name            | address     |
      | Dairy something |      55 Mtl |
      | Cheese Masters  | 456 Ontario |
    Given the following purchase exists in the system
      | purchaseDate | nrCheeseWheels | monthsAged | farmerEmail         |
      |   2025-02-01 |              3 | TwentyFour | farmer1@example.com |
    Given all cheese wheels from purchase 4 are created
    Given the following order exists in the system
      | transactionDate  | nrCheeseWheels | monthsAged | companyName    | deliveryDate |
      | 2025-10-01 |             15 | TwentyFour | Cheese Masters |   2027-02-02 |
    Given all non-spoiled cheese wheels from purchase 4 are added to order 5
    When the facility manager attempts to display from the system all the wholesale companies
    Then the number of wholesale companies in the system shall be 3
    Then the following wholesale company details shall be presented
      | name            | address     |
      | Cheesy Bites    |      112 Av |
      | Dairy something |      55 Mtl |
      | Cheese Masters  | 456 Ontario |
    Then the following order details shall be presented for wholesale company "Cheesy Bites"
      | orderDate  | monthsAged | nrCheeseWheelsOrdered | nrCheeseWheelsMissing | deliveryDate |
      | 2025-08-15 | Six        |                    10 |                     5 |   2025-12-15 |
      | 2025-09-01 | Twelve     |                     3 |                     3 |   2026-03-01 |
    Then no order details shall be presented for wholesale company "Dairy something"
    Then the following order details shall be presented for wholesale company "Cheese Masters"
      | orderDate  | monthsAged | nrCheeseWheelsOrdered | nrCheeseWheelsMissing | deliveryDate |
      | 2025-10-01 | TwentyFour |                    15 |                    12 |   2027-02-02 |
