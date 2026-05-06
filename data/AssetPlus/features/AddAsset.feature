Feature: Add Asset
As the manager, I want to add an asset in the system.

  Background: 
    Given the following asset types exist in the system
      | name | expectedLifeSpan |
      | lamp |             1800 |
      | bed  |             5000 |
    Given the following assets exist in the system
      | assetNumber | type | purchaseDate | floorNumber | roomNumber |
      |           1 | lamp |   2022-03-20 |           9 |         23 |
      |           2 | bed  |   2010-01-30 |          10 |         35 |

  Scenario Outline: Successfully add an asset
    When the manager attempts to add a new asset to the system with asset number "<assetNumber>", type "<type>", purchase date "<purchaseDate>", floor number "<floorNumber>", and room number "<roomNumber>"
    Then the number of assets in the system shall be "3"
    Then the asset "<type>" with asset number "<assetNumber>", purchase date "<purchaseDate>", floor number "<floorNumber>", and room number "<roomNumber>" shall exist in the system

    Examples: 
      | assetNumber | type | purchaseDate | floorNumber | roomNumber |
      |           3 | bed  |   2020-06-23 |           2 |         32 |
      |           3 | lamp |   2012-01-01 |           3 |         78 |
      |           3 | lamp |   2012-01-01 |           0 |         -1 |

  Scenario Outline: Unsuccessfully add an asset with a type that does not exist
    When the manager attempts to add a new asset to the system with asset number "<assetNumber>", type "<type>", purchase date "<purchaseDate>", floor number "<floorNumber>", and room number "<roomNumber>"
    Then the number of assets in the system shall be "2"
    Then the following assets shall exist in the system
      | assetNumber | type | purchaseDate | floorNumber | roomNumber |
      |           1 | lamp |   2022-03-20 |           9 |         23 |
      |           2 | bed  |   2010-01-30 |          10 |         35 |
    Then the error "<error>" shall be raised

    Examples: 
      | assetNumber | type       | purchaseDate | floorNumber | roomNumber | error                         |
      |           3 | television |   2012-01-01 |           5 |         43 | The asset type does not exist |

  Scenario Outline: Unsuccessfully add an asset with invalid information
    When the manager attempts to add a new asset to the system with asset number "<assetNumber>", type "<type>", purchase date "<purchaseDate>", floor number "<floorNumber>", and room number "<roomNumber>"
    Then the number of assets in the system shall be "2"
    Then the following assets shall exist in the system
      | assetNumber | type | purchaseDate | floorNumber | roomNumber |
      |           1 | lamp |   2022-03-20 |           9 |         23 |
      |           2 | bed  |   2010-01-30 |          10 |         35 |
    Then the error "<error>" shall be raised

    Examples: 
      | assetNumber | type | purchaseDate | floorNumber | roomNumber | error                                     |
      |           0 | lamp |   2012-01-01 |           1 |         13 | The asset number shall not be less than 1 |
      |           3 | lamp |   2012-01-01 |          -1 |         13 | The floor number shall not be less than 0 |
      |           3 | bed  |   2012-01-01 |           7 |         -2 | The room number shall not be less than -1 |