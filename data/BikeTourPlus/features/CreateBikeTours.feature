Feature: Initiate creation of bike tours
  As a manager, I want to initiate the creation of bike tours to assign guides and biking weeks to participants

  # For all scenarios, participants and guides are registered in the system following the order listed in their respective tables (top to bottom)
 
  Background: 
    Given the following BikeTourPlus system exists:
      | startDate  | nrWeeks | priceOfGuidePerWeek |
      | 2023-03-13 |      10 |                 100 |
    Given the following guides exist in the system:
      | email          | password | name | emergencyContact |
      | jeff@email.com | pass1    | Jeff | (555)555-5555    |
      | john@email.com | pass2    | John | (444)444-4444    |
      | bob@email.com  | psw0rd1  | Bob  | (200)5555678     |

  Scenario: Successfully initiate bike tour creation in which a newer participant is assigned before an older one
    Given the following participants exist in the system:
      | email              | password | name             | emergencyContact | nrWeeks | weeksAvailableFrom | weeksAvailableUntil | lodgeRequired |
      | alice@gmail.com    | pass123  | Alice Jones      | (200)5551234     |       3 |                  1 |                   3 | true          |
      | new@hotmail.ca     | newnew   | Johnny New       | (200)5559999     |       5 |                  2 |                   6 | true          |
      | charlie@hotmail.ca | charlie  | Charles Tremblay | (200)5559876     |       3 |                  1 |                   5 | false         |
      | john@hotmail.ca    | john123  | John Doe         | (200)5551234     |       3 |                  1 |                   3 | false         |
      | emily@hotmail.ca   | emily007 | Emily Green      | (200)5559876     |       2 |                  4 |                   5 | false         |
    When the administrator attempts to initiate the bike tour creation process
    Then the following bike tours shall exist in the system:
      | id | startWeek | endWeek | participants                                       | guide          |
      |  1 |         1 |       3 | alice@gmail.com,charlie@hotmail.ca,john@hotmail.ca | jeff@email.com |
      |  2 |         4 |       5 | emily@hotmail.ca                                   | jeff@email.com |
      |  3 |         2 |       6 | new@hotmail.ca                                     | john@email.com |
    Then the participant with email "alice@gmail.com" shall be marked as "Assigned"
    Then the participant with email "new@hotmail.ca" shall be marked as "Assigned"
    Then the participant with email "charlie@hotmail.ca" shall be marked as "Assigned"
    Then the participant with email "john@hotmail.ca" shall be marked as "Assigned"
    Then the participant with email "emily@hotmail.ca" shall be marked as "Assigned"
    Then the number of bike tours shall be "3"

  Scenario: Successfully initiate bike tour creation requiring a single guide
    Given the following participants exist in the system:
      | email              | password | name             | emergencyContact | nrWeeks | weeksAvailableFrom | weeksAvailableUntil | lodgeRequired |
      | alice@gmail.com    | pass123  | Alice Jones      | (200)5551234     |       3 |                  1 |                   3 | true          |
      | new@hotmail.ca     | newnew   | Johnny New       | (200)5559999     |       4 |                  1 |                  10 | true          |
      | charlie@hotmail.ca | charlie  | Charles Tremblay | (200)5559876     |       3 |                  1 |                   5 | false         |
      | john@hotmail.ca    | john123  | John Doe         | (200)5551234     |       3 |                  1 |                   3 | false         |
      | emily@hotmail.ca   | emily007 | Emily Green      | (200)5559876     |       2 |                  4 |                  10 | false         |
    When the administrator attempts to initiate the bike tour creation process
    Then the following bike tours shall exist in the system:
      | id | startWeek | endWeek | participants                                       | guide          |
      |  1 |         1 |       3 | alice@gmail.com,charlie@hotmail.ca,john@hotmail.ca | jeff@email.com |
      |  2 |         4 |       7 | new@hotmail.ca                                     | jeff@email.com |
      |  3 |         8 |       9 | emily@hotmail.ca                                   | jeff@email.com |
    Then the participant with email "alice@gmail.com" shall be marked as "Assigned"
    Then the participant with email "new@hotmail.ca" shall be marked as "Assigned"
    Then the participant with email "charlie@hotmail.ca" shall be marked as "Assigned"
    Then the participant with email "john@hotmail.ca" shall be marked as "Assigned"
    Then the participant with email "emily@hotmail.ca" shall be marked as "Assigned"
    Then the number of bike tours shall be "3"

  Scenario: Successfully initiate bike tour creation requiring all guides
    Given the following participants exist in the system:
      | email              | password | name             | emergencyContact | nrWeeks | weeksAvailableFrom | weeksAvailableUntil | lodgeRequired |
      | alice@gmail.com    | pass123  | Alice Jones      | (200)5551234     |       3 |                  1 |                   3 | true          |
      | new@hotmail.ca     | newnew   | Johnny New       | (200)5559999     |       5 |                  1 |                   5 | true          |
      | charlie@hotmail.ca | charlie  | Charles Tremblay | (200)5559876     |       3 |                  1 |                   5 | false         |
      | john@hotmail.ca    | john123  | John Doe         | (200)5551234     |       3 |                  1 |                   3 | false         |
      | emily@hotmail.ca   | emily007 | Emily Green      | (200)5559876     |       2 |                  1 |                   4 | false         |
    When the administrator attempts to initiate the bike tour creation process
    Then the following bike tours shall exist in the system:
      | id | startWeek | endWeek | participants                                       | guide          |
      |  1 |         1 |       3 | alice@gmail.com,charlie@hotmail.ca,john@hotmail.ca | jeff@email.com |
      |  2 |         1 |       5 | new@hotmail.ca                                     | john@email.com |
      |  3 |         1 |       2 | emily@hotmail.ca                                   | bob@email.com  |
    Then the participant with email "alice@gmail.com" shall be marked as "Assigned"
    Then the participant with email "new@hotmail.ca" shall be marked as "Assigned"
    Then the participant with email "charlie@hotmail.ca" shall be marked as "Assigned"
    Then the participant with email "john@hotmail.ca" shall be marked as "Assigned"
    Then the participant with email "emily@hotmail.ca" shall be marked as "Assigned"
    Then the number of bike tours shall be "3"

  Scenario: Successfully initiate bike tour creation in which a guide is assigned for all biking weeks
    Given the following participants exist in the system:
      | email              | password | name             | emergencyContact | nrWeeks | weeksAvailableFrom | weeksAvailableUntil | lodgeRequired |
      | alice@gmail.com    | pass123  | Alice Jones      | (200)5551234     |       3 |                  1 |                   3 | true          |
      | new@hotmail.ca     | newnew   | Johnny New       | (200)5559999     |       7 |                  4 |                  10 | true          |
      | charlie@hotmail.ca | charlie  | Charles Tremblay | (200)5559876     |       3 |                  1 |                   5 | false         |
      | john@hotmail.ca    | john123  | John Doe         | (200)5551234     |       3 |                  1 |                   3 | false         |
      | emily@hotmail.ca   | emily007 | Emily Green      | (200)5559876     |       2 |                  1 |                   5 | false         |
    When the administrator attempts to initiate the bike tour creation process
    Then the following bike tours shall exist in the system:
      | id | startWeek | endWeek | participants                                       | guide          |
      |  1 |         1 |       3 | alice@gmail.com,charlie@hotmail.ca,john@hotmail.ca | jeff@email.com |
      |  2 |         4 |      10 | new@hotmail.ca                                     | jeff@email.com |
      |  3 |         1 |       2 | emily@hotmail.ca                                   | john@email.com |
    Then the participant with email "alice@gmail.com" shall be marked as "Assigned"
    Then the participant with email "new@hotmail.ca" shall be marked as "Assigned"
    Then the participant with email "charlie@hotmail.ca" shall be marked as "Assigned"
    Then the participant with email "john@hotmail.ca" shall be marked as "Assigned"
    Then the participant with email "emily@hotmail.ca" shall be marked as "Assigned"
    Then the number of bike tours shall be "3"

  Scenario: Unsuccessfully initiate bike tour creation for all participants and instead provide a partial assignment
    Given the following participants exist in the system:
      | email              | password | name             | emergencyContact | nrWeeks | weeksAvailableFrom | weeksAvailableUntil | lodgeRequired |
      | alice@gmail.com    | pass123  | Alice Jones      | (200)5551234     |       3 |                  1 |                   3 | true          |
      | new@hotmail.ca     | newnew   | Johnny New       | (200)5559999     |       7 |                  4 |                  10 | true          |
      | charlie@hotmail.ca | charlie  | Charles Tremblay | (200)5559876     |       3 |                  2 |                   5 | false         |
      | john@hotmail.ca    | john123  | John Doe         | (200)5551234     |       5 |                  1 |                  10 | false         |
      | mary@hotmail.ca    | mary003  | Mary Blue        | (200)5559988     |       9 |                  1 |                  10 | true          |
      | emily@hotmail.ca   | emily007 | Emily Green      | (200)5559876     |       2 |                  1 |                   5 | false         |
    When the administrator attempts to initiate the bike tour creation process
    Then the following bike tours shall exist in the system:
      | id | startWeek | endWeek | participants       | guide          |
      |  1 |         1 |       3 | alice@gmail.com    | jeff@email.com |
      |  2 |         4 |      10 | new@hotmail.ca     | jeff@email.com |
      |  3 |         2 |       4 | charlie@hotmail.ca | john@email.com |
      |  4 |         5 |       9 | john@hotmail.ca    | john@email.com |
      |  5 |         1 |       9 | mary@hotmail.ca    | bob@email.com  |
    Then the participant with email "alice@gmail.com" shall be marked as "Assigned"
    Then the participant with email "new@hotmail.ca" shall be marked as "Assigned"
    Then the participant with email "charlie@hotmail.ca" shall be marked as "Assigned"
    Then the participant with email "john@hotmail.ca" shall be marked as "Assigned"
    Then the participant with email "mary@hotmail.ca" shall be marked as "Assigned"
    Then the participant with email "emily@hotmail.ca" shall be marked as "NotAssigned"
    Then the number of bike tours shall be "5"
    Then the system shall raise the error "At least one participant could not be assigned to their bike tour"
