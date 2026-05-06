Feature: Create Category
    As an admin, I want to create categories in the system.

    Background:
        Given the following user accounts exist in the system
            | userID | firstName | lastName | username  | email             | phoneNumber | role        |
            | id1    | Admin     | User     | adminuser | admin@example.com | 555-0100    | Admin       |
            | id2    | Bob       | Smith    | bobsmith  | bob@example.com   | 555-0200    | Organizer   |
            | id3    | Jane      | Doe      | janedoe   | jane@example.com  | 555-0300    | Participant |
        And the following categories exist in the system
            | categoryId | name   | description           |
            | id1        | Sports | Sports related events |

    Scenario: Successfully create a category as admin
        When an admin with userID "id1" attempts to create a category with name "Music" and description "Music concerts and performances"
        Then a category with name "Music" and description "Music concerts and performances" shall exist in the system
        Then the categoryId shall be automatically assigned and not be "id1"
        Then the number of categories in the system shall be 2

    Scenario Outline: Unsuccessfully create a category with invalid values
        When an admin with userID "id1" attempts to create a category with name "<name>" and description "<description>"
        Then the error "<error>" shall be raised
        Then the number of categories in the system shall be 1

        Examples:
            | name  | description                     | error                          |
            |       | Music concerts and performances | Name must not be empty.        |
            | Music |                                 | Description must not be empty. |

    Scenario Outline: Unsuccessfully create a category as non-admin user
        When a user with userID "<userID>" attempts to create a category with name "Music" and description "Music concerts and performances"
        Then the error "Only admin users can update categories." shall be raised
        Then the number of categories in the system shall be 1

        Examples:
            | userID |
            | id2    |
            | id3    |
