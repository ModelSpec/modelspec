Feature: Add Maintenance Note
As hotel staff, I want to add a maintenance note to a ticket in the system.

  Background: 
    Given the following employees exist in the system
      | email        | password | name  | phoneNumber   |
      | jeff@ap.com  | pass1    | Jeff  | (555)555-5555 |
      | smith@ap.com | pass2    | Smith | (555)555-5555 |
    Given the following manager exists in the system
      | email          | password |
      | manager@ap.com | manager  |
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
    Given the following notes exist in the system
      | noteTaker    | ticketId | addedOnDate | description                               |
      | jeff@ap.com  |        2 |  2023-09-01 | This is a dummy note 1 for a ticket       |
      | smith@ap.com |        1 |  2023-09-10 | This is another dummy note 2 for a ticket |

  Scenario Outline: Successfully add a note to a maintenance ticket to the system by an employee
    When hotel staff with email "<noteTaker>" attempts to add a new note with date "<date>" and description "<description>" to an existing maintenance ticket "<ticketId>"
    Then the number of notes in the system shall be "3"
    Then the number of notes for ticket "<ticketId>" in the system shall be "<numberOfNotes>"
    Then the note number "<noteIndex>" for ticket <ticketId> with noteTaker "<noteTaker>", date "<date>", and description "<description>" shall exist in the system

    Examples: 
      | ticketId | noteTaker      | date       | description                   | noteIndex | numberOfNotes |
      |        1 | jeff@ap.com    | 2023-09-23 | This is a dummy description 1 |         1 |             2 |
      |        1 | manager@ap.com | 2023-10-05 | This is a dummy description 2 |         1 |             2 |

  Scenario Outline: Unsuccessfully add a maintenance note to the system.
    When hotel staff with email "<noteTaker>" attempts to add a new note with date "<date>" and description "<description>" to an existing maintenance ticket "<ticketId>"
    Then the number of notes in the system shall be "2"
    Then the following notes shall exist in the system
      | noteTaker    | ticketId | addedOnDate | description                                |
      | jeff@ap.com  |        2 |  2023-09-01 | This is a dummy note 1 for a ticket       |
      | smith@ap.com |        1 |  2023-09-10 | This is another dummy note 2 for a ticket |
    Then the system shall raise the error "<error>"

    Examples: 
      | ticketId | noteTaker      | date       | description                   | error                              |
      |        1 | abdul@ap.com   | 2023-09-23 | This is a dummy description 1 | Hotel staff does not exist         |
      |        3 | manager@ap.com | 2023-10-05 | This is a dummy description 2 | Ticket does not exist              |
      |        1 | manager@ap.com | 2023-10-05 |                               | Ticket description cannot be empty |