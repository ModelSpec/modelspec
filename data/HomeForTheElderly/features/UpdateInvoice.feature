Feature: Update Invoice
  Background:
    Given there is a HomeForTheElderly system
    Given there is a person with id "person" and name "John Doe" and birthdate "1950-01-01" and abilities "requires wheelchair"
    Given the current system date is "2020-01-01"
    Given there is an invoice for person "person" with invoiceDate "2020-01-01" and outstandingAmount 1000 and status "active"

  Scenario: Updating an invoice's outstanding amount
    When the outstandingAmount of invoice for person "person" with invoiceDate "2020-01-01" is updated to 500
    Then the system shall not throw an error
    Then the invoice for person "person" with invoiceDate "2020-01-01" shall have outstandingAmount 500
    Then the invoice for person "person" with invoiceDate "2020-01-01" shall have status "active"

  Scenario Outline: Updating an invoice's outstanding amount to zero or less
    When the outstandingAmount of invoice for person "person" with invoiceDate "2020-01-01" is updated to <amount>
    Then the system shall not throw an error
    Then the invoice for person "person" with invoiceDate "2020-01-01" shall have outstandingAmount <amount>
    Then the invoice for person "person" with invoiceDate "2020-01-01" shall have status "paid"

    Examples:
      | amount |
      | 0      |
      | -1     |

  Scenario: Updating an invoice when status is paid
    Given the invoice for person "person" with invoiceDate "2020-01-01" has outstanding amount 0 and status "paid"
    When the outstandingAmount of invoice for person "person" with invoiceDate "2020-01-01" is updated to 500
    Then the system shall throw with error message "Cannot update paid invoice."
    Then the invoice for person "person" with invoiceDate "2020-01-01" shall have outstandingAmount 0
    Then the invoice for person "person" with invoiceDate "2020-01-01" shall have status "paid"

  Scenario: Updating an invoice that does not exist
    When the outstandingAmount of invoice for person "person" with invoiceDate "2020-01-02" is updated to 500
    Then the system shall throw with error message "Invoice for person \"person\" with invoiceDate \"2020-01-02\" does not exist."