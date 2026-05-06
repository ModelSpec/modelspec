Feature: Delete Asset
As the manager, I want to delete an asset in the system so that it is no longer available.

  Background: 
    Given the following asset types exist in the system
      | name | expectedLifeSpan |
      | lamp |             1800 |
      | bed  |             5000 |
    Given the following assets exist in the system
      | assetNumber | type | purchaseDate | floorNumber | roomNumber |
      |           1 | lamp |   2022-03-20 |           9 |         23 |
      |           2 | bed  |   2010-01-30 |          10 |         35 |
      |           3 | lamp |   2007-12-27 |          99 |         99 |

  Scenario: Successfully delete an asset
    When the manager attempts to delete the asset with number "2"
    Then the number of assets in the system shall be "2"
    Then the following assets shall exist in the system
      | assetNumber | type | purchaseDate | floorNumber | roomNumber |
      |           1 | lamp |   2022-03-20 |           9 |         23 |
      |           3 | lamp |   2007-12-27 |          99 |         99 |

  Scenario: Successfully delete an asset that does not exist in the system
    When the manager attempts to delete the asset with number "4"
    Then the number of assets in the system shall be "3"
    Then the following assets shall exist in the system
      | assetNumber | type | purchaseDate | floorNumber | roomNumber |
      |           1 | lamp |   2022-03-20 |           9 |         23 |
      |           2 | bed  |   2010-01-30 |          10 |         35 |
      |           3 | lamp |   2007-12-27 |          99 |         99 |