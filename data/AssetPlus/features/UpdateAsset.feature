Feature: Update Asset
As the manager, I want to update an asset in the system.

  Background: 
    Given the following asset types exist in the system
      | name | expectedLifeSpan |
      | lamp |             1800 |
      | bed  |             5000 |
    Given the following assets exist in the system
      | assetNumber | type | purchaseDate | floorNumber | roomNumber |
      |           1 | lamp |   2022-03-20 |           9 |         23 |
      |           2 | bed  |   2010-01-30 |          10 |         35 |

  Scenario Outline: Successfully update all information for an asset
    When the manager attempts to update asset number "<assetNumber>" in the system with type "<newType>", purchaseDate "<newPurchaseDate>", floorNumber "<newFloorNumber>", and roomNumber "<newRoomNumber>"
    Then the number of assets in the system shall be "2"
    Then the asset "<newType>" with asset number "<assetNumber>", purchase date "<newPurchaseDate>", floor number "<newFloorNumber>", and room number "<newRoomNumber>" shall exist in the system

    Examples: 
      | assetNumber | newType | newPurchaseDate | newFloorNumber | newRoomNumber |
      |           1 | bed     |      2022-03-21 |             12 |            10 |
      |           2 | lamp    |      2010-01-29 |              9 |            -1 |

  Scenario Outline: Unsuccessfully update an asset with a type that does not exist
    When the manager attempts to update asset number "<assetNumber>" in the system with type "<newType>", purchaseDate "<newPurchaseDate>", floorNumber "<newFloorNumber>", and roomNumber "<newRoomNumber>"
    Then the number of assets in the system shall be "2"
    Then the following assets shall exist in the system
      | assetNumber | type | purchaseDate | floorNumber | roomNumber |
      |           1 | lamp |   2022-03-20 |           9 |         23 |
      |           2 | bed  |   2010-01-30 |          10 |         35 |
    Then the error "<error>" shall be raised

    Examples: 
      | assetNumber | newType | newPurchaseDate | newFloorNumber | newRoomNumber | error                         |
      |           1 | couch   |      1999-04-20 |             12 |            10 | The asset type does not exist |

  Scenario Outline: Unsuccessfully update an asset with invalid information
    When the manager attempts to update asset number "<assetNumber>" in the system with type "<newType>", purchaseDate "<newPurchaseDate>", floorNumber "<newFloorNumber>", and roomNumber "<newRoomNumber>"
    Then the number of assets in the system shall be "2"
    Then the following assets shall exist in the system
      | assetNumber | type | purchaseDate | floorNumber | roomNumber |
      |           1 | lamp |   2022-03-20 |           9 |         23 |
      |           2 | bed  |   2010-01-30 |          10 |         35 |
    Then the error "<error>" shall be raised

    Examples: 
      | assetNumber | newType | newPurchaseDate | newFloorNumber | newRoomNumber | error                                     |
      |           2 | lamp    |      2012-01-01 |             -1 |            13 | The floor number shall not be less than 0 |
      |           1 | bed     |      2012-01-01 |              7 |            -2 | The room number shall not be less than -1 |