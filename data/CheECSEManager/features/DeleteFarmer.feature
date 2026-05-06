Feature: Delete Farmer
As the facility manager, I want to delete a farmer from the system.

  Background:
    Given the following farmer exists in the system
      | email              | password | address | name     |
      | farmer@cheecse.fr  | P@ssw0rd |  112 Av | Farmer A |
      | farmer2@domain.com | P4$$w0rd |  123 St | Farmer B |
    Given the following purchase exists in the system
      | purchaseDate | nrCheeseWheels | monthsAged | farmerEmail        |
      |   2025-09-01 |              2 | Six        | farmer2@domain.com |
    Given all cheese wheels from purchase 1 are created

  Scenario: Successfully delete a farmer from the system
    When the facility manager attempts to delete the farmer with email "farmer@cheecse.fr"
    Then the number of farmers in the system shall be 1
    Then the following farmers shall exist in the system
      | email              | password | address | name     |
      | farmer2@domain.com | P4$$w0rd |  123 St | Farmer B |
    Then the number of cheese wheels for farmer "farmer2@domain.com" shall be 2

  Scenario: Unsuccessfully delete a farmer that has supplied cheese
    When the facility manager attempts to delete the farmer with email "farmer2@domain.com"
    Then the number of farmers in the system shall be 2
    Then the following farmers shall exist in the system
      | email              | password | address | name     |
      | farmer@cheecse.fr  | P@ssw0rd |  112 Av | Farmer A |
      | farmer2@domain.com | P4$$w0rd |  123 St | Farmer B |
    Then the number of cheese wheels for farmer "farmer@cheecse.fr" shall be 0
    Then the number of cheese wheels for farmer "farmer2@domain.com" shall be 2
    Then the error "Cannot delete farmer who has supplied cheese." shall be raised

  Scenario: Unsuccessfully delete a farmer that does not exist in the system
    When the facility manager attempts to delete the farmer with email "farmer@cheecse.ca"
    Then the number of farmers in the system shall be 2
    Then the following farmers shall exist in the system
      | email              | password | address | name     |
      | farmer@cheecse.fr  | P@ssw0rd |  112 Av | Farmer A |
      | farmer2@domain.com | P4$$w0rd |  123 St | Farmer B |
    Then the number of cheese wheels for farmer "farmer@cheecse.fr" shall be 0
    Then the number of cheese wheels for farmer "farmer2@domain.com" shall be 2
    Then the error "The farmer with email farmer@cheecse.ca does not exist." shall be raised
