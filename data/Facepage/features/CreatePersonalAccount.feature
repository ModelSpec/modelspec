Feature: Create Personal Account
  Background:
    Given there is a Facepage system
    Given there is a user with userID "1" and name "John Doe" and email "john.doe@mail.com" and date of birth "2000-01-01"

  Scenario: Creating a new personal account
    When a personal account is created by user "1"
    Then the system shall not throw an error
    Then the created account shall be associated with user "1"
    Then the created account shall have a non-empty accountNumber
    Then the number of accounts in Facepage shall be 1

  Scenario Outline: Creating a new personal account with automatically unique accountNumber
    Given there is a user with userID "2" and name "Jane Smith" and email "jane.smith@mail.com" and date of birth "2000-01-01"
    Given there is an account of type "<accountType>" and company name "<companyName>" associated with user "2"
    When a personal account is created by user "1"
    Then the system shall not throw an error
    Then the created account shall be associated with user "1"
    Then the created account shall have an accountNumber different from the accountNumber of the account associated with user "2"
    Then the number of accounts in Facepage shall be 2

    Examples:
      | accountType     | companyName |
      | BusinessAccount | company1    |
      | PersonalAccount |             |

  Scenario Outline: Creating a personal account with duplicate userID
    Given there is an account of type "<accountType>" and company name "<companyName>" associated with user "1"
    When a personal account is created by user "1"
    Then the system shall throw with error message "A user with the ID \"1\" already has an account."
    Then the number of accounts in Facepage shall be 1

    Examples:
      | accountType     | companyName |
      | BusinessAccount | company1    |
      | PersonalAccount |             |