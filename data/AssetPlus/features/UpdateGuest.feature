Feature: Update Guest
As a guest, I wish to update a guest account in the system

  Background: 
    Given the following guests exist in the system
      | email          | password | name | phoneNumber   |
      | jeff@gmail.com | pass1    | Jeff | (555)555-5555 |
      | john@gmail.com | pass2    | John | (444)444-4444 |
    Given the following manager exists in the system
      | email          | password |
      | manager@ap.com | manager  |

  Scenario Outline: A guest updates their info successfully
    When the guest with "<email>" attempts to update their account information to "<newPassword>", "<newName>", and "<newPhoneNumber>"
    Then their guest account information will be updated and is now "<email>", "<newPassword>", "<newName>", and "<newPhoneNumber>"
    Then the number of guests in the system shall be "2"

    Examples: 
      | email          | newPassword | newName | newPhoneNumber |
      | jeff@gmail.com | pass5       | Jake    | (111)111-1111  |
      | john@gmail.com | pass6       | Johnny  | (111)777-7777  |
      | john@gmail.com | pass2       |         | (444)444-7777  |
      | john@gmail.com | pass2       | Jon     |                |

  Scenario Outline: A guest updates their info unsuccessfully
    When the guest with "<email>" attempts to update their account information to "<newPassword>", "<newName>", and "<newPhoneNumber>"
    Then the following "<error>" shall be raised
    Then the number of guests in the system shall be "2"
    Then the following guests shall exist in the system
      | email          | password | name | phoneNumber   |
      | jeff@gmail.com | pass1    | Jeff | (555)555-5555 |
      | john@gmail.com | pass2    | John | (444)444-4444 |

    Examples:
      | email          | newPassword | newName | newPhoneNumber | error                    |
      | jeff@gmail.com |             | Jeff    | (555)666-5555  | Password cannot be empty |