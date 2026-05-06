Feature: Create Advertisement Page
  Background:
    Given there is a Facepage system
    Given there is a user with userID "1" and name "John Doe" and email "john.doe@mail.com" and date of birth "2000-01-01"
    Given there is a business account with company name "company" associated with user "1"

  Scenario: Creating a new advertisement page
    When an advertisement page with page name "page" is created by the business account of user "1"
    Then the system shall not throw an error
    Then the created page shall be associated with the business account of user "1"
    Then the created page shall have page name "page"
    Then the number of visits on the created page shall be 0
    Then the bounce rate on the created page shall be 0
    Then the click-through rate on the created page shall be 0
    Then the conversion rate on the created page shall be 0
    Then the number of pages associated with the business account of user "1" shall be 1
    Then the number of pages in Facepage shall be 1

  Scenario: Creating a new advertisement page with same pageName as another account's page
    Given there is a user with userID "2" and name "Jane Smith" and email "jane.smith@mail.com" and date of birth "2000-01-01"
    Given there is a business account with company name "company2" associated with user "2"
    Given there is an advertisement page with page name "page" associated with the business account of user "2"
    When an advertisement page with page name "page" is created by the business account of user "1"
    Then the system shall not throw an error
    Then the created page shall be associated with the business account of user "1"
    Then the created page shall have page name "page"
    Then the number of visits on the created page shall be 0
    Then the bounce rate on the created page shall be 0
    Then the click-through rate on the created page shall be 0
    Then the conversion rate on the created page shall be 0
    Then the number of pages associated with the business account of user "1" shall be 1
    Then the number of pages associated with the business account of user "2" shall be 1
    Then the number of pages in Facepage shall be 2

  Scenario: Creating a new advertisement page with duplicate pageName
    Given there is an advertisement page with page name "<pageName>" associated with the business account of user "<user>"
    When an advertisement page with page name "<pageName>" is created by the business account of user "<user>"
    Then the system shall throw with error message "A page with the name \"<pageName>\" already exists."
    Then the number of pages associated with the business account of user "<user>" shall be 1
    Then the number of pages in Facepage shall be 1

  Scenario: Creating an advertisement page with invalid pageName
    When an advertisement page with page name "" is created by the business account of user "1"
    Then the system shall throw with error message "The page name cannot be empty."
    Then the number of pages associated with the business account of user "1" shall be 0
    Then the number of pages in Facepage shall be 0

  Scenario: Creating an advertisement page with a personal account
    Given there is a user with userID "2" and name "Jane Smith" and email "jane.smith@mail.com" and date of birth "2000-01-01"
    Given there is a personal account associated with user "2"
    When an advertisement page with page name "page" is created by the personal account of user "2"
    Then the system shall throw with error message "Only business accounts can create advertisement pages."
    Then the number of pages associated with the personal account of user "2" shall be 0
    Then the number of pages in Facepage shall be 0