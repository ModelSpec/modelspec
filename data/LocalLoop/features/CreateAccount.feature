Feature: Create Account
    As a user, I want to create an account in the system.

    Background:
        Given the following user account exists in the system
            | userID | firstName | lastName | username | email            | phoneNumber | isOrganizer | companyName |
            | id1    | John      | Doe      | johndoe  | john@example.com | 555-0100    | false       |             |

    Scenario Outline: Successfully create a user account
        When a user attempts to create an account with firstName "<firstName>", lastName "<lastName>", username "<username>", email "<email>", phoneNumber "<phoneNumber>", password "<password>", confirmPassword "<confirmPassword>", isOrganizer "<isOrganizer>", and companyName "<companyName>"
        Then a user account with firstName "<firstName>", lastName "<lastName>", username "<username>", email "<email>", phoneNumber "<phoneNumber>", isOrganizer "<isOrganizer>", and companyName "<companyName>" shall exist in the system
        Then the userID shall be automatically assigned and not be "id1"
        Then the number of user accounts in the system shall be 2

        Examples:
            | firstName | lastName | username | email               | phoneNumber | password  | confirmPassword | isOrganizer | companyName      |
            | Alice     | Johnson  | alicej   | alice@example.com   | 555-0300    | P@ssw0rd1 | P@ssw0rd1       | false       |                  |
            | Bob       | Williams | bobw     | bob@example.com     |             | Pass$123  | Pass$123        | false       |                  |
            | Charlie   | Brown    | charlieb | charlie@example.com | 555-0400    | Secure#45 | Secure#45       | true        | BrownEvents Inc. |
            | Diana     | Lee      | dianalee | diana@example.com   |             | MyP@ss99  | MyP@ss99        | true        | Lee Organizers   |

    Scenario Outline: Unsuccessfully create a user account with invalid values
        When a user attempts to create an account with firstName "<firstName>", lastName "<lastName>", username "<username>", email "<email>", phoneNumber "<phoneNumber>", password "<password>", confirmPassword "<confirmPassword>", isOrganizer "<isOrganizer>", and companyName "<companyName>"
        Then the error "<error>" shall be raised
        Then the number of user accounts in the system shall be 2

        Examples:
            | firstName | lastName | username | email               | phoneNumber | password  | confirmPassword | isOrganizer | companyName | error                                         |
            |           | Johnson  | alicej   | alice@example.com   | 555-0300    | P@ssw0rd1 | P@ssw0rd1       | false       |             | First name must not be empty.                 |
            | Alice     |          | alicej   | alice@example.com   | 555-0300    | P@ssw0rd1 | P@ssw0rd1       | false       |             | Last name must not be empty.                  |
            | Alice     | Johnson  |          | alice@example.com   | 555-0300    | P@ssw0rd1 | P@ssw0rd1       | false       |             | Username must not be empty.                   |
            | Alice     | Johnson  | alicej   |                     | 555-0300    | P@ssw0rd1 | P@ssw0rd1       | false       |             | Email must not be empty.                      |
            | Alice     | Johnson  | alicej   | alice.example.com   | 555-0300    | P@ssw0rd1 | P@ssw0rd1       | false       |             | Email must contain @ symbol.                  |
            | Alice     | Johnson  | alicej   | @example.com        | 555-0300    | P@ssw0rd1 | P@ssw0rd1       | false       |             | Email must have characters before @.          |
            | Alice     | Johnson  | alicej   | alice@              | 555-0300    | P@ssw0rd1 | P@ssw0rd1       | false       |             | Email must contain a dot after @.             |
            | Alice     | Johnson  | alicej   | alice@example       | 555-0300    | P@ssw0rd1 | P@ssw0rd1       | false       |             | Email must contain a dot after @.             |
            | Alice     | Johnson  | alicej   | alice@example.      | 555-0300    | P@ssw0rd1 | P@ssw0rd1       | false       |             | Email must have characters after dot.         |
            | Alice     | Johnson  | alicej   | alice @example.com  | 555-0300    | P@ssw0rd1 | P@ssw0rd1       | false       |             | Email must not contain spaces.                |
            | Alice     | Johnson  | alicej   | john@example.com    | 555-0300    | P@ssw0rd1 | P@ssw0rd1       | false       |             | The email already exists.                     |
            | Alice     | Johnson  | johndoe  | alice@example.com   | 555-0300    | P@ssw0rd1 | P@ssw0rd1       | false       |             | The username already exists.                  |
            | Alice     | Johnson  | alicej   | alice@example.com   | 555-0300    |           | P@ssw0rd1       | false       |             | Password must not be empty.                   |
            | Alice     | Johnson  | alicej   | alice@example.com   | 555-0300    | P@ssw0rd1 |                 | false       |             | Confirm password must not be empty.           |
            | Alice     | Johnson  | alicej   | alice@example.com   | 555-0300    | P@ssw0rd1 | DifferentPass   | false       |             | Passwords must match.                         |
            | Charlie   | Brown    | charlieb | charlie@example.com | 555-0400    | Secure#45 | Secure#45       | true        |             | Company name must be provided for organizers. |
