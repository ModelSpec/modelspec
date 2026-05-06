Feature: Update Asset Type
As the manager, I want to update an asset type in the system.

  Background: 
    Given the following asset types exist in the system
      | name   | expectedLifeSpan |
      | lamp   |             1800 |
      | pillow |              700 |
      | bed    |             5000 |

  Scenario Outline: Successfully update all information for an asset type
    When the manager attempts to update an asset type in the system with name "<oldName>" to have name "<newName>" and expected life span of "<newExpectedLifeSpan>" days
    Then the number of asset types in the system shall be "3"
    Then the asset type with name "<newName>" and expected life span of "<newExpectedLifeSpan>" days shall exist in the system
    Then the asset type with name "<oldName>" and expected life span of "<oldExpectedLifeSpan>" days shall not exist in the system

    Examples: 
      | oldName | oldExpectedLifeSpan | newName | newExpectedLifeSpan |
      | lamp    |                1800 | lamp    |                1900 |
      | pillow  |                 700 | closet  |                2500 |
      | bed     |                5000 | pot     |                 600 |

  Scenario Outline: Unsuccessfully update an asset type with invalid information
    When the manager attempts to update an asset type in the system with name "lamp" to have name "<newName>" and expected life span of "<newExpectedLifeSpan>" days
    Then the number of asset types in the system shall be "3"
    Then the following asset types shall exist in the system
      | name   | expectedLifeSpan |
      | lamp   |             1800 |
      | pillow |              700 |
      | bed    |             5000 |
    Then the system shall raise the error "<error>"

    Examples: 
      | newName    | newExpectedLifeSpan | error                                              |
      | table lamp |                   0 | The expected life span must be greater than 0 days |
      | table lamp |                 -30 | The expected life span must be greater than 0 days |
      |            |                  30 | The name must not be empty                         |
      | pillow     |                 240 | The asset type already exists                      |

  Scenario Outline: Unsuccessfully update an asset type that does not exist in the system
    When the manager attempts to update an asset type in the system with name "table lamp" to have name "<newName>" and expected life span of "<newExpectedLifeSpan>" days
    Then the number of asset types in the system shall be "3"
    Then the following asset types shall exist in the system
      | name   | expectedLifeSpan |
      | lamp   |             1800 |
      | pillow |              700 |
      | bed    |             5000 |
    Then the system shall raise the error "The asset type does not exist"

    Examples: 
      | newName | newExpectedLifeSpan |
      | desk    |                6000 |