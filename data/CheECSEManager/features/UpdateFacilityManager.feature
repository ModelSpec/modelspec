Feature: Update Facility Manager
As the facility manager, I want to update the password of a facility manager in the system.

  Background:
    Given the following facility manager exists in the system
      | email              | password |
      | manager@cheecse.fr | p#Ssw0rd |

  Scenario Outline: Successfully update the password of a facility manager in the system
    When the facility manager attempts to update the facility manager password to "<updatedPassword>"
    Then the number of facility managers in the system shall be 1
    Then the facility manager with password "<updatedPassword>" shall exist in the system

    Examples:
      | updatedPassword |
      | pAssword!       |
      | Pa$$word        |
      | Test#1234       |
      | abcD!           |

  Scenario Outline: Unsuccessfully update the password of a facility manager due to invalid password format
    When the facility manager attempts to update the facility manager password to "<updatedPassword>"
    Then the number of facility managers in the system shall be 1
    Then the facility manager with password "p#Ssw0rd" shall exist in the system
    Then the error "<error>" shall be raised

    Examples:
      | updatedPassword | error                                                      |
      | a$D             | Password must be at least 4 characters long.               |
      | Password        | Password must contain a special character from !, #, or $. |
      | password!       | Password must contain an uppercase character.              |
      | PASSWORD!       | Password must contain a lowercase character.               |
