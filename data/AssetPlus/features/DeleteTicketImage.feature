Feature: Delete ticket image
As manager, I want to delete a ticket image from a ticket

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
    Given the following ticket images exist in the system
      | imageUrl                   | ticketId |
      | https://imageurl.com/i.jpg |        1 |
      | http://thisimage.com/1.png |        1 |
      | http://thisimage.com/2.png |        2 |

  Scenario Outline: Successfully delete ticket image from a ticket
    When the manager deletes the ticket image "<imageURL>" from the ticket with id "<ticketId>"
    Then the number of images in the system shall be "2"
    Then the number of images for the ticket with id "<ticketId>" in the system shall be "<numberOfImagesOfTicket>"
    Then the ticket with id "<ticketId>" shall not have an image with url "<imageUrl>"

    Examples: 
      | ticketId | imageURL                   | numberOfImagesOfTicket |
      |        1 | http://thisimage.com/1.png |                      1 |
      |        2 | http://thisimage.com/2.png |                      0 |

  Scenario Outline: Successfully delete nonexisting ticket image from a ticket
    When the manager deletes the ticket image "<imageURL>" from the ticket with id "<ticketId>"
    Then the number of images in the system shall be "3"
    Then the number of images for the ticket with id "<ticketId>" in the system shall be "<numberOfImagesOfTicket>"
    Then the ticket with id "<ticketId>" shall not have an image with url "<imageUrl>"

    Examples: 
      | ticketId | imageURL                   | numberOfImagesOfTicket |
      |        1 | http://thisimage.com/0.png |                      2 |
      |        2 | http://thisimage.com/0.png |                      1 |

  Scenario Outline: Successfully delete nonexisting ticket image from a nonexisting ticket
    When the manager deletes the ticket image "<imageURL>" from the ticket with id "<ticketId>"
    Then the number of images in the system shall be "3"

    Examples: 
      | ticketId | imageURL                   |
      |        3 | http://thisimage.com/1.png |