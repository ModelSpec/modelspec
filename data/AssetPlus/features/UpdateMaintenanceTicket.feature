Feature: Update Maintenance Ticket
As a manager, I want to update a maintenance ticket in the system.

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

  Scenario Outline: Successfully update a maintenance ticket
    When the manager attempts to update the maintenance ticket with id "<id>" to ticket raiser "<newTicketRaiser>", date "<newRaisedOnDate>", description "<newDescription>", and asset number "<newAssetNumber>"
    Then the number of tickets in the system shall be "2"
    Then the ticket raised by "<newTicketRaiser>" and with id "<id>", date "<newRaisedOnDate>", description "<newDescription>", and asset number "<newAssetNumber>" shall exist in the system

    Examples: 
      | id | newTicketRaiser | newRaisedOnDate | newDescription         | newAssetNumber |
      |  1 | smith@ap.com    |      2023-08-20 | bed needs to be fixed  |              1 |
      |  2 | manager@ap.com  |      2023-08-10 | lamp needs to be fixed |              2 |

  Scenario Outline: Successfully remove an asset from a maintenance ticket
    When the manager attempts to update the maintenance ticket with id "<id>" to ticket raiser "<newTicketRaiser>", date "<newRaisedOnDate>", and description "<newDescription>" but no asset number
    Then the number of tickets in the system shall be "2"
    Then the ticket raised by "<newTicketRaiser>" and with id "<id>", date "<newRaisedOnDate>", and description "<newDescription>" but no asset shall exist in the system

    Examples: 
      | id | newTicketRaiser | newRaisedOnDate | newDescription |
      |  1 | smith@ap.com    |      2023-08-20 | it is noisy    |
      |  2 | manager@ap.com  |      2023-08-10 | it smells      |

  Scenario Outline: Unsuccessfully update a maintenance ticket with invalid information
    When the manager attempts to update the maintenance ticket with id "<id>" to ticket raiser "<newTicketRaiser>", date "<newRaisedOnDate>", description "<newDescription>", and asset number "<newAssetNumber>"
    Then the number of tickets in the system shall be "2"
    Then the following tickets shall exist in the system
      | id | ticketRaiser   | raisedOnDate | description                   | assetNumber |
      |  1 | manager@ap.com |   2023-07-20 | This is a dummy description 1 |           2 |
      |  2 | smith@ap.com   |   2023-07-10 | This is a dummy description 2 |           1 |
    Then the system shall raise the error "<error>"

    Examples: 
      | id | newTicketRaiser | newRaisedOnDate | newDescription                | newAssetNumber | error                              |
      |  1 | manager@ap.com  |      2023-09-23 | This is a dummy description 1 |              3 | The asset does not exist           |
      |  1 | none@ap.com     |      2023-09-23 | This is a dummy description 1 |              1 | The ticket raiser does not exist   |
      |  1 | smith@ap.com    |      2023-09-23 |                               |              1 | Ticket description cannot be empty |