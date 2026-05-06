Feature: Create Privilege
  Background:
    Given there is a Facepage system
    Given the following users exist:
      | userID | name       | email               | dateOfBirth |
      | 1      | John Doe   | john.doe@mail.com   | 2000-01-01  |
      | 2      | Jane Smith | jane.smith@mail.com | 2000-01-01  |
    Given there is a personal account associated with user "1"
    Given there is a personal account associated with user "2"
    Given there is a personal page with page name "page" administrated by the personal account of user "1"

  Scenario: Creating a new privilege
    When a privilege of type "write" on personal page "page" of user "1" is granted to the personal account of user "2"
    Then the system shall not throw an error
    Then the privilege shall be associated with the personal account of user "2"
    Then the privilege shall be associated with the personal page "page" of user "1"
    Then the privilege shall be of type "write"
    Then the number of privileges granted to the personal account of user "2" shall be 1
    Then the number of privileges in Facepage shall be 1

  Scenario Outline: Creating a privilege with invalid values
    When a privilege of type "<privilegeType>" on personal page "<page>" of user "<pageOwner>" is granted to the personal account of user "<targetUser>"
    Then the system shall throw with error message "<error>"
    Then the number of privileges granted to the personal account of user "<targetUser>" shall be 0
    Then the number of privileges in Facepage shall be 0

    Examples:
      | privilegeType | page  | pageOwner | targetUser | error                                            |
      |               | page  | 1         | 2          | The type of privilege cannot be empty.           |
      | write         |       | 1         | 1          | Page cannot be empty.                            |
      | write         | page  |           | 2          | Owner of the page cannot be empty.               |
      | write         | page  | 1         |            | Target user cannot be empty.                     |
      | write         | page  | 3         | 1          | User "3" does not exist.                         |
      | write         | page  | 1         | 3          | User "3" does not exist.                         |
      | write         | page2 | 1         | 1          | Page "page2" does not exist for user "1".     |
      | write         | page  | 1         | 1          | Cannot grant privilege to the owner of the page. |

  Scenario: Creating a privilege for a business account
    Given there is a user with userID "3" and name "Bob Johnson" and email "bob.johnson@mail.com" and date of birth "2000-01-01"
    Given there is a business account with company name "company" associated with user "3"
    When a privilege of type "write" on personal page "page" of user "1" is granted to the personal account of user "3"
    Then the system shall throw with error message "Cannot grant privilege to a business account."
    Then the number of privileges granted to the personal account of user "3" shall be 0
    Then the number of privileges in Facepage shall be 0

  Scenario: Creating a privilege for an advertisement page
    Given there is a user with userID "3" and name "Bob Johnson" and email "bob.johnson@mail.com" and date of birth "2000-01-01"
    Given there is a business account with company name "company" associated with user "3"
    Given there is an advertisement page with page name "page" associated with the business account of user "3"
    When a privilege of type "write" on advertisement page "page" of user "3" is granted to the personal account of user "1"
    Then the system shall throw with error message "Cannot grant privilege on an advertisement page."
    Then the number of privileges granted to the personal account of user "1" shall be 0
    Then the number of privileges in Facepage shall be 0