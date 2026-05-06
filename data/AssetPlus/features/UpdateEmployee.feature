Feature: Update Employee
As an employee, I wish to update an employee account in the system

  Background: 
    Given the following employees exist in the system
      | email       | password | name | phoneNumber   |
      | jeff@ap.com | pass1    | Jeff | (555)555-5555 |
      | john@ap.com | pass2    | John | (444)444-4444 |
    Given the following manager exists in the system
      | email          | password |
      | manager@ap.com | manager  |

  Scenario Outline: An employee updates their info successfully
    When the employee with "<email>" attempts to update their account information to "<newPassword>", "<newName>", and "<newPhoneNumber>"
    Then their employee account information will be updated and is now "<email>", "<newPassword>", "<newName>", and "<newPhoneNumber>"
    Then the number of employees in the system shall be "2"

    Examples: 
      | email       | newPassword | newName | newPhoneNumber |
      | jeff@ap.com | pass5       | Jake    | (111)111-1111  |
      | john@ap.com | pass6       | Johnny  | (111)777-7777  |
      | john@ap.com | pass2       |         | (444)444-7777  |
      | john@ap.com | pass2       | Jon     |                |

  Scenario Outline: An employee updates their info unsuccessfully
    When the employee with "<email>" attempts to update their account information to "<newPassword>", "<newName>", and "<newPhoneNumber>"
    Then the following "<error>" shall be raised
    Then the number of employees in the system shall be "2"
    Then the following employees shall exist in the system
      | email       | password | name | phoneNumber   |
      | jeff@ap.com | pass1    | Jeff | (555)555-5555 |
      | john@ap.com | pass2    | John | (444)444-4444 |

    Examples:
      | email       | newPassword | newName | newPhoneNumber | error                    |
      | jeff@ap.com |             | Jeff    | (555)666-5555  | Password cannot be empty |