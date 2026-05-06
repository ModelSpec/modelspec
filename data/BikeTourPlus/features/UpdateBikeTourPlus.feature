Feature: Update BikeTourPlus Information
  As a manager, I want to update the BikeTourPlus information so that the information is accurate

  Background: 
    Given the following BikeTourPlus system exists:
      | startDate  | nrWeeks | priceOfGuidePerWeek |
      | 2023-03-13 |      10 |                 100 |

  Scenario Outline: Update BikeTourPlus information successfully
    When the manager attempts to update the BikeTourPlus information to start date "<startDate>", number of weeks "<nrWeeks>", and price of guide per week "<priceOfGuidePerWeek>"
    Then the BikeTourPlus information shall be start date "<startDate>", number of weeks "<nrWeeks>", and price of guide per week "<priceOfGuidePerWeek>"

    Examples: 
      | startDate  | nrWeeks | priceOfGuidePerWeek |
      | 2023-03-14 |      10 |                 100 |
      | 2023-03-13 |       0 |                 100 |
      | 2023-03-13 |      10 |                   0 |

  Scenario Outline: Update BikeTourPlus information unsuccessfully
    When the manager attempts to update the BikeTourPlus information to start date "<startDate>", number of weeks "<nrWeeks>", and price of guide per week "<priceOfGuidePerWeek>"
    Then the BikeTourPlus information shall be start date "2023-03-13", number of weeks "10", and price of guide per week "100"
    Then the system shall raise the error "<error>"

    Examples: 
      | startDate  | nrWeeks | priceOfGuidePerWeek | error                                                             |
      | 2023-01-13 |      -1 |                 100 | The number of riding weeks must be greater than or equal to zero  |
      | 2023-01-13 |      10 |                  -1 | The price of guide per week must be greater than or equal to zero |
      | 2021-01-13 |      10 |                 100 | The start date cannot be from previous year or earlier            |
