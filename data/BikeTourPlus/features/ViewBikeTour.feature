Feature: View Bike Tour
  As a manager, I want to view the bike tours so that I can keep track of the participants' and guides' activities

  Background:
    Given the following BikeTourPlus system exists:
      | startDate  | nrWeeks | priceOfGuidePerWeek |
      | 2023-03-13 | 10      | 100                 |
    Given the following pieces of gear exist in the system:
      | name     | pricePerWeek |
      | helmet   | 25           |
      | e-bike   | 150          |
      | bike bag | 19           |
      | tire kit | 15           |
    Given the following combos exist in the system:
      | name        | discount | items                  | quantity |
      | small combo | 10       | e-bike,helmet          | 1,2      |
      | large combo | 0        | e-bike,helmet,bike bag | 1,2,2    |
    Given the following guides exist in the system:
      | email          | password | name | emergencyContact |
      | jeff@email.com | pass1    | Jeff | (555)555-5555    |
      | john@email.com | pass2    | John | (444)444-4444    |
    Given the following participants exist in the system:
      | email           | password | name  | emergencyContact | nrWeeks | weeksAvailableFrom | weeksAvailableUntil | lodgeRequired |
      | peter@email.com | pass1    | Peter | (666)555-5555    | 1       | 1                  | 2                   | true          |
      | tyler@email.com | pass2    | Tyler | (777)444-4444    | 2       | 2                  | 5                   | false         |
      | mary@email.com  | pass3    | Mary  | (555)666-6666    | 1       | 1                  | 2                   | false         |
    Given the following participants request the following pieces of gear:
      | email           | gear     | quantity |
      | peter@email.com | helmet   | 1        |
      | peter@email.com | bike bag | 2        |
    Given the following participants request the following combos:
      | email           | gear        | quantity |
      | peter@email.com | small combo | 1        |
      | tyler@email.com | large combo | 2        |
      | mary@email.com  | large combo | 1        |
    Given the following bike tours exist in the system:
      | id | startWeek | endWeek | participants                   | guide          |
      | 1  | 1         | 1       | peter@email.com,mary@email.com | jeff@email.com |
      | 2  | 2         | 3       | tyler@email.com                | jeff@email.com |

  Scenario: Successfully view bike tour 1
    When the manager attempts to view the bike tour with id "1"
    # totalCostsForBookableItems for Peter: helmet (25) + 2 bike bags (19 * 2) + discounted small combo (e-bike (150) + 2 helmets (25 * 2)) * 0.90 = 243, then 243 * number of weeks = 243 * ( 1 - 1 + 1 ) = 243
    # totalCostsForBookableItems for Mary: large combo (e-bike (150) + 2 helmets (25 * 2) + 2 bike bags (19 * 2)) = 238, then 238 * number of weeks = 238 * ( 1 - 1 + 1 ) = 238		# (round down in case of 0.5)
    Then the following bike tour information shall be provided:
      | id | startWeek | endWeek | guideEmail     | guideName | totalCostForGuide | participantsEmail              | participantsName | totalCostsForBookableItems | totalCostsForBikeTour |
      | 1  | 1         | 1       | jeff@email.com | Jeff      | 100               | peter@email.com,mary@email.com | Peter,Mary       | 243,238                    | 343,338               |

  Scenario: Successfully view bike tour 2
    When the manager attempts to view the bike tour with id "2"
    # totalCostsForBookableItems for Tyler: 2 large combos (e-bike (150) + 2 helmets (25 * 2) + 2 bike bags (19 * 2)) * 2 = 476, then 476 * number of weeks = 476 * ( 3 - 2 + 1 ) = 952		# (round down in case of 0.5)
    Then the following bike tour information shall be provided:
      | id | startWeek | endWeek | guideEmail     | guideName | totalCostForGuide | participantsEmail | participantsName | totalCostsForBookableItems | totalCostsForBikeTour |
      | 2  | 2         | 3       | jeff@email.com | Jeff      | 200               | tyler@email.com   | Tyler            | 952                        | 1152                  |
