Feature: Start bike tours
  As a manager, I want to start bike tours so that participants can begin their biking activities

  Background:
    Given the following BikeTourPlus system exists:
      | startDate  | nrWeeks | priceOfGuidePerWeek |
      | 2023-03-13 |      10 |                 100 |
    Given the following pieces of gear exist in the system:
      | name     | pricePerWeek |
      | helmet   |           25 |
      | e-bike   |          150 |
      | bike bag |           19 |
      | tire kit |           15 |
    Given the following combos exist in the system:
      | name        | discount | items                  | quantity |
      | small combo |       10 | e-bike,helmet          |      1,2 |
      | large combo |       25 | e-bike,helmet,bike bag |    1,2,2 |
    Given the following guides exist in the system:
      | email          | password | name | emergencyContact |
      | jeff@email.com | pass1    | Jeff | (555)555-5555    |
      | john@email.com | pass2    | John | (444)444-4444    |
    Given the following participants exist in the system:
      | email              | password | name             | emergencyContact | nrWeeks | weeksAvailableFrom | weeksAvailableUntil | lodgeRequired |
      | alice@gmail.com    | pass123  | Alice Jones      | (200)5551234     |       3 |                  1 |                   3 | true          |
      | charlie@hotmail.ca | charlie  | Charles Tremblay | (200)5559876     |       3 |                  1 |                   5 | false         |
      | john@hotmail.ca    | john123  | John Doe         | (200)5551234     |       3 |                  1 |                   3 | false         |
      | emily@hotmail.ca   | emily007 | Emily Green      | (200)5559876     |       2 |                  4 |                   5 | false         |
      | new@hotmail.ca     | newnew   | Johnny New       | (200)5559999     |       5 |                  6 |                  10 | true          |
    Given the following bike tours exist in the system:
      | id | startWeek | endWeek | participants                                       | guide          |
      |  1 |         1 |       3 | alice@gmail.com,charlie@hotmail.ca,john@hotmail.ca | jeff@email.com |
      |  2 |         4 |       5 | emily@hotmail.ca                                   | jeff@email.com |

  Scenario: Manager starts tours successfully
    Given the participant with email "alice@gmail.com" has paid for their tour
    When the manager attempts to start the tours for week "1"
    Then the participant with email "alice@gmail.com" shall be marked as "Started"
    Then the participant with email "charlie@hotmail.ca" shall be marked as "Banned"
    Then the participant with email "john@hotmail.ca" shall be marked as "Banned"
    Then the participant with email "emily@hotmail.ca" shall be marked as "Assigned"

  Scenario: Unsuccessfully start a tour for a participant who has not been assigned to their tour
    When the manager attempts to start the tours for week "6"
    Then the participant with email "new@hotmail.ca" shall be marked as "NotAssigned"

  Scenario: Unsuccessfully start a tour for a participant who has started their tour
    Given the participant with email "emily@hotmail.ca" has started their tour
    When the manager attempts to start the tours for week "4"
    Then the participant with email "emily@hotmail.ca" shall be marked as "Started"
    Then the system shall raise the error "Cannot start tour because the participant has already started their tour"

  Scenario: Unsuccessfully start a tour for a banned participant
    Given the participant with email "emily@hotmail.ca" is banned
    When the manager attempts to start the tours for week "4"
    Then the participant with email "emily@hotmail.ca" shall be marked as "Banned"
    Then the system shall raise the error "Cannot start tour because the participant is banned"

  Scenario: Unsuccessfully start a tour for a participant who has cancelled their tour
    Given the participant with email "emily@hotmail.ca" has cancelled their tour
    When the manager attempts to start the tours for week "4"
    Then the participant with email "emily@hotmail.ca" shall be marked as "Cancelled"
    Then the system shall raise the error "Cannot start tour because the participant has cancelled their tour"

  Scenario: Unsuccessfully start a tour for a participant who has finished their tour
    Given the participant with email "emily@hotmail.ca" has finished their tour
    When the manager attempts to start the tours for week "4"
    Then the participant with email "emily@hotmail.ca" shall be marked as "Finished"
    Then the system shall raise the error "Cannot start tour because the participant has finished their tour"
