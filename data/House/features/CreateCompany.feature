Feature: Create company

  Background:
    Given there is a House system

  Scenario: Creating a new company successfully
    When a company with name "FixIt Co" and address "456 Oak Ave" is created
    Then the created company has name "FixIt Co" and address "456 Oak Ave"
    Then the number of companies in the system is 1

  Scenario Outline: Creating a new company with invalid input
    When a company with name "<name>" and address "<address>" is created
    Then the system displays the error message "<error>"
    Then the number of companies in the system is <companyCnt>

    Examples:
      | name     | address     | companyCnt | error                                     |
      |          | 456 Oak Ave | 0          | The name of a company cannot be empty.    |
      | FixIt Co |             | 0          | The address of a company cannot be empty. |
