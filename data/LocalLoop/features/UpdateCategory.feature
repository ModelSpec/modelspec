Feature: Update Category
    As an admin, I want to update categories in the system.

    Background:
        Given the following user accounts exist in the system
            | userID | firstName | lastName | username  | email             | phoneNumber | role        |
            | id1    | Admin     | User     | adminuser | admin@example.com | 555-0100    | Admin       |
            | id2    | Bob       | Smith    | bobsmith  | bob@example.com   | 555-0200    | Organizer   |
            | id3    | Jane      | Doe      | janedoe   | jane@example.com  | 555-0300    | Participant |
        And the following categories exist in the system
            | categoryId | name   | description           |
            | id1        | Sports | Sports related events |

    Scenario: Successfully update a category as admin
        When an admin with userID "id1" attempts to update category "id1" with name "Athletics" and description "Athletic competitions and sports events"
        Then the category with categoryId "id1" shall have name "Athletics" and description "Athletic competitions and sports events"
        Then the number of categories in the system shall be 1

    Scenario Outline: Unsuccessfully update a category with invalid values
        When an admin with userID "id1" attempts to update category "id1" with name "<name>" and description "<description>"
        Then the error "<error>" shall be raised
        Then the category with categoryId "id1" shall have name "Sports" and description "Sports related events"
        Then the number of categories in the system shall be 1
        Examples:
            | name   | description                | error                          |
            |        | Updated sports description | Name must not be empty.        |
            | Sports |                            | Description must not be empty. |

    Scenario Outline: Unsuccessfully update a category as non-admin user
        When a user with userID "<userID>" attempts to update category "id1" with name "Updated Sports" and description "Updated description"
        Then the error "Only admin users can update categories." shall be raised
        Then the category with categoryId "id1" shall have name "Sports" and description "Sports related events"
        Then the number of categories in the system shall be 1

        Examples:
            | userID |
            | id2    |
            | id3    |

    Scenario: Unsuccessfully update a category as non-existent account
        When a user with userID "id999" attempts to update category "id1" with name "Updated Sports" and description "Updated description"
        Then the error "Account with ID id999 does not exist." shall be raised
        Then the category with categoryId "id1" shall have name "Sports" and description "Sports related events"
        Then the number of categories in the system shall be 1

    Scenario: Unsuccessfully update a category that does not exist
        When an admin with userID "id1" attempts to update category "id999" with name "NonExistent" and description "This category does not exist"
        Then the error "Category with ID id999 does not exist." shall be raised
        Then the number of categories in the system shall be 1
