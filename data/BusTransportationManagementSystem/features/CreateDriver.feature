Feature: Create driver

  Background:
    Given there is a BTMS system

  Scenario Outline: Creating a new driver
    When a driver with name "<drivername>" is created
    Then the number of drivers in the BTMS is <driverCnt>
    Then there have been <errorCnt> errors
    Then there has been an error message "<error>"

    Examples:
      | drivername | driverCnt | errorCnt | error                                 |
      | John Doe   |         1 |        0 |                                       |
      |            |         0 |        1 | The name of a driver cannot be empty. |