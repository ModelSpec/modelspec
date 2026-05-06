Feature: Process payment for participants
  As a manager, I want to confirm payments so that participants can proceed with their bike tours

  Background:
    Given the following BikeTourPlus system exists:
      | startDate  | nrWeeks | priceOfGuidePerWeek |
      | 2023-03-13 |      10 |                 100 |
    Given the following pieces of gear exist in the system:
      | name     | pricePerWeek |
      | helmet   |           25 |
      | e-bike   |          150 |
      | bike bag |           19 |
      | tire kit |           15 |
    Given the following combos exist in the system:
      | name        | discount | items                  | quantity |
      | small combo |       10 | e-bike,helmet          |      1,2 |
      | large combo |       25 | e-bike,helmet,bike bag |    1,2,2 |
    Given the following guides exist in the system:
      | email          | password | name | emergencyContact |
      | jeff@email.com | pass1    | Jeff | (555)555-5555    |
      | john@email.com | pass2    | John | (444)444-4444    |
    Given the following participants exist in the system:
      | email              | password | name             | emergencyContact | nrWeeks | weeksAvailableFrom | weeksAvailableUntil | lodgeRequired |
      | alice@gmail.com    | pass123  | Alice Jones      | (200)5551234     |       3 |                  1 |                   3 | true          |
      | charlie@hotmail.ca | charlie  | Charles Tremblay | (200)5559876     |       3 |                  1 |                   5 | false         |
      | john@hotmail.ca    | john123  | John Doe         | (200)5551234     |       3 |                  1 |                   3 | false         |
      | emily@hotmail.ca   | emily007 | Emily Green      | (200)5559876     |       2 |                  4 |                   5 | false         |
      | new@hotmail.ca     | newnew   | Johnny New       | (200)5559999     |       5 |                  6 |                  10 | true          |

  Scenario Outline: Successfully pay for participant
    When the manager attempts to confirm payment for email "<email>" using authorization code "<code>"
    Then the participant with email "<email>" shall be marked as "Paid"
    Then a participant account shall exist with email "<email>" and authorization code "<code>"

    Examples:
      | email              | code        |
      | alice@gmail.com    | BIKETOUR200 |
      | charlie@hotmail.ca | CODE321     |

  Scenario Outline: Unsuccessfully pay for participant with an email address that does not exist
    When the manager attempts to confirm payment for email "<email>" using authorization code "<code>"
    Then a participant account shall not exist with email "<email>"
    Then the number of participants shall be "5"
    Then the system shall raise the error "<error>"

    Examples:
      | email            | code        | error |
      | steve@yahoo.com  | BIKETOUR200 | Participant with email address steve@yahoo.com does not exist |
      | dave@hotmail.com | CODE321     | Participant with email address dave@hotmail.com does not exist |

  Scenario Outline: Unsuccessfully pay for participant with an invalid authorization code
    When the manager attempts to confirm payment for email "<email>" using authorization code "<code>"
    Then the participant with email "<email>" shall be marked as "Assigned"
    Then the system shall raise the error "<error>"

    Examples:
      | email              | code | error                      |
      | alice@gmail.com    |      | Invalid authorization code |
      | charlie@hotmail.ca |      | Invalid authorization code |

  Scenario: Unsuccessfully pay for participant who has not been assigned to their tour
    When the manager attempts to confirm payment for email "new@hotmail.ca" using authorization code "PAYup"
    Then the participant with email "new@hotmail.ca" shall be marked as "NotAssigned"
    Then the system shall raise the error "The participant has not been assigned to their tour"

  Scenario: Unsuccessfully pay for participant who has paid
    Given the participant with email "charlie@hotmail.ca" has paid for their tour
    When the manager attempts to confirm payment for email "charlie@hotmail.ca" using authorization code "PAYup"
    Then the participant with email "charlie@hotmail.ca" shall be marked as "Paid"
    Then the system shall raise the error "The participant has already paid for their tour"

  Scenario: Unsuccessfully pay for participant who has started their tour
    Given the participant with email "john@hotmail.ca" has started their tour
    When the manager attempts to confirm payment for email "john@hotmail.ca" using authorization code "PAYup"
    Then the participant with email "john@hotmail.ca" shall be marked as "Started"
    Then the system shall raise the error "The participant has already paid for their tour"

  Scenario: Unsuccessfully pay for a banned participant
    Given the participant with email "emily@hotmail.ca" is banned
    When the manager attempts to confirm payment for email "emily@hotmail.ca" using authorization code "PAYup"
    Then the participant with email "emily@hotmail.ca" shall be marked as "Banned"
    Then the system shall raise the error "Cannot pay for tour because the participant is banned"

  Scenario: Unsuccessfully pay for participant who has cancelled their tour
    Given the participant with email "alice@gmail.com" has cancelled their tour
    When the manager attempts to confirm payment for email "alice@gmail.com" using authorization code "PAYup"
    Then the participant with email "alice@gmail.com" shall be marked as "Cancelled"
    Then the system shall raise the error "Cannot pay for tour because the participant has cancelled their tour"

  Scenario: Unsuccessfully pay for participant who has finished their tour
    Given the participant with email "charlie@hotmail.ca" has finished their tour
    When the manager attempts to confirm payment for email "charlie@hotmail.ca" using authorization code "PAYup"
    Then the participant with email "charlie@hotmail.ca" shall be marked as "Finished"
    Then the system shall raise the error "The participant has already paid for their tour"
