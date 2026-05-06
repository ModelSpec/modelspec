Feature: Add Maintenance Ticket
As a ticket raiser, I want to add a maintenance ticket in the system.

  Background: 
    Given the following employees exist in the system
      | email        | password | name  | phoneNumber   |
      | jeff@ap.com  | pass1    | Jeff  | (555)555-5555 |
      | smith@ap.com | pass2    | Smith | (555)555-5555 |
    Given the following manager exists in the system
      | email          | password |
      | manager@ap.com | manager  |
    Given the following guests exist in the system
      | email          | password | name | phoneNumber   |
      | jeff@gmail.com | pass1    | Jeff | (555)555-5555 |
      | john@gmail.com | pass2    | John | (444)444-4444 |
    Given the following asset types exist in the system
      | name | expectedLifeSpan |
      | lamp |             1800 |
      | bed  |             5000 |
    Given the following assets exist in the system
      | assetNumber | type | purchaseDate | floorNumber | roomNumber |
      |           1 | lamp |   2022-03-20 |           9 |         23 |
      |           2 | bed  |   2010-01-30 |          10 |         35 |
    Given the following tickets exist in the system
      | id | ticketRaiser   | raisedOnDate | description                   | assetNumber |
      |  1 | manager@ap.com |   2023-07-20 | This is a dummy description 1 |           2 |
      |  2 | smith@ap.com   |   2023-07-10 | This is a dummy description 2 |           1 |

  Scenario Outline: Successfully add a maintenance ticket to the system by a guest, employee, or manager
    When the user with email "<ticketRaiser>" attempts to add a new maintenance ticket to the system with id "<id>", date "<raisedOnDate>", description "<description>", and asset number "<assetNumber>"
    Then the number of tickets in the system shall be "3"
    Then the ticket raised by "<ticketRaiser>" and with id "<id>", date "<raisedOnDate>", description "<description>", and asset number "<assetNumber>" shall exist in the system

    Examples: 
      | id | ticketRaiser   | raisedOnDate | description                   | assetNumber |
      |  3 | john@gmail.com |   2023-09-23 | This is a dummy description 3 |           2 |
      |  4 | smith@ap.com   |   2023-10-05 | This is a dummy description 2 |           1 |
      |  3 | manager@ap.com |   2023-09-23 | This is a dummy description 1 |           1 |

  Scenario Outline: Successfully add a maintenance ticket without an asset to the system by a guest, employee, or manager
    When the user with email "<ticketRaiser>" attempts to add a new maintenance ticket to the system with id "<id>", date "<raisedOnDate>", and description "<description>" but no asset number
    Then the number of tickets in the system shall be "3"
    Then the ticket raised by "<ticketRaiser>" and with id "<id>", date "<raisedOnDate>", and description "<description>" but no asset shall exist in the system

    Examples: 
      | id | ticketRaiser   | raisedOnDate | description               |
      |  3 | john@gmail.com |   2023-09-23 | it is noisy               |
      |  4 | smith@ap.com   |   2023-10-05 | it smells                 |
      |  3 | manager@ap.com |   2023-09-23 | it smells and it is noisy |

  Scenario Outline: Unsuccessfully add a maintenance ticket to the system
    When the user with email "<ticketRaiser>" attempts to add a new maintenance ticket to the system with id "<id>", date "<raisedOnDate>", description "<description>", and asset number "<assetNumber>"
    Then the number of tickets in the system shall be "2"
    Then the following tickets shall exist in the system
      | id | ticketRaiser   | raisedOnDate | description                   | assetNumber |
      |  1 | manager@ap.com |   2023-07-20 | This is a dummy description 1 |           2 |
      |  2 | smith@ap.com   |   2023-07-10 | This is a dummy description 2 |           1 |
    Then the system shall raise the error "<error>"

    Examples: 
      | id | ticketRaiser   | raisedOnDate | description                   | assetNumber | error                              |
      |  2 | smith@ap.com   |   2023-09-23 | This is a dummy description 1 |           2 | Ticket id already exists           |
      |  3 | manager@ap.com |   2023-09-23 | This is a dummy description 1 |           3 | The asset does not exist           |
      |  3 | none@ap.com    |   2023-09-23 | This is a dummy description 1 |           1 | The ticket raiser does not exist   |
      |  3 | smith@ap.com   |   2023-09-23 |                               |           1 | Ticket description cannot be empty |