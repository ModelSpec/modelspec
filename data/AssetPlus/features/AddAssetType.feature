Feature: Add Asset Type
As the manager, I want to add an asset type in the system.

  Background: 
    Given the following asset types exist in the system
      | name   | expectedLifeSpan |
      | lamp   |             1800 |
      | pillow |              700 |
      | bed    |             5000 |

  Scenario Outline: Successfully add an asset type
    When the manager attempts to add a new asset type to the system with name "<name>" and expected life span of "<expectedLifeSpan>" days
    Then the number of asset types in the system shall be "4"
    Then the asset type with name "<name>" and expected life span of "<expectedLifeSpan>" days shall exist in the system

    Examples: 
      | name      | expectedLifeSpan |
      | fridge    |             5000 |
      | microwave |             2000 |

  Scenario Outline: Unsuccessfully add an asset type with invalid information
    When the manager attempts to add a new asset type to the system with name "<name>" and expected life span of "<expectedLifeSpan>" days
    Then the number of asset types in the system shall be "3"
    Then the following asset types shall exist in the system
      | name   | expectedLifeSpan |
      | lamp   |             1800 |
      | pillow |              700 |
      | bed    |             5000 |
    Then the system shall raise the error "<error>"

    Examples: 
      | name       | expectedLifeSpan | error                                              |
      | television |                0 | The expected life span must be greater than 0 days |
      | television |             -180 | The expected life span must be greater than 0 days |
      |            |              180 | The name must not be empty                         |
      | lamp       |               60 | The asset type already exists                      |
      | bed        |               96 | The asset type already exists                      |