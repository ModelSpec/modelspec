import pytest
from datetime import datetime


@pytest.fixture
def givenController(modelingTool, mw):
    if modelingTool == "umple":
        from ..umple.controller.controller import AssetPlusController
        from ..umple.generated_model_layer import (
            User, Employee, Guest, Manager, AssetType, SpecificAsset, MaintenanceTicket, TicketImage
        )
        uniqueKeywords = ["byemail", "byname", "byid", "byassetnumber", "byimageurl"]
        for cls in [User, Employee, Guest, Manager, AssetType, SpecificAsset, MaintenanceTicket, TicketImage]:
            for attr in dir(cls):
                name = attr.lower()
                if any(k in name for k in uniqueKeywords):
                    mapping = getattr(cls, attr)
                    if isinstance(mapping, dict):
                        mapping.clear()
    else:
        from ..ecore.controller.controller import AssetPlusController
        from ..ecore.generated_model_layer import AssetType, SpecificAsset
    controller = AssetPlusController()
    ap = controller.assetPlus
    atLamp = mw(AssetType, name="lamp", expectedLifeSpan=1800, assetPlus=ap)
    mw(ap).addAssetType(atLamp.model)
    atBed = mw(AssetType, name="bed", expectedLifeSpan=5000, assetPlus=ap)
    mw(ap).addAssetType(atBed.model)
    sa1 = mw(SpecificAsset, assetNumber=1, floorNumber=9, roomNumber=23, purchaseDate=datetime(2022, 3, 20), assetType=atLamp.model, assetPlus=ap)
    mw(ap).addSpecificAsset(sa1.model)
    sa2 = mw(SpecificAsset, assetNumber=2, floorNumber=10, roomNumber=35, purchaseDate=datetime(2010, 1, 30), assetType=atBed.model, assetPlus=ap)
    mw(ap).addSpecificAsset(sa2.model)
    sa3 = mw(SpecificAsset, assetNumber=3, floorNumber=99, roomNumber=99, purchaseDate=datetime(2007, 12, 27), assetType=atLamp.model, assetPlus=ap)
    mw(ap).addSpecificAsset(sa3.model)
    yield controller


def testDeleteAssetSuccess(givenController, mw):
    givenController.deleteAsset(2)
    assets = mw(givenController.assetPlus).getSpecificAssets()
    assert len(assets) == 2

    remainingNumbers = {a.getAssetNumber() for a in assets}
    assert remainingNumbers == {1, 3}

    asset1 = None
    for a in assets:
        if a.getAssetNumber() == 1:
            asset1 = a
            break

    assert asset1 is not None
    assert asset1.getAssetType().getName() == "lamp"
    d1 = asset1.getPurchaseDate()
    assert d1.year == 2022
    assert d1.month == 3
    assert d1.day == 20
    assert asset1.getFloorNumber() == 9
    assert asset1.getRoomNumber() == 23

    asset3 = None
    for a in assets:
        if a.getAssetNumber() == 3:
            asset3 = a
            break

    assert asset3 is not None
    assert asset3.getAssetType().getName() == "lamp"
    d3 = asset3.getPurchaseDate()
    assert d3.year == 2007
    assert d3.month == 12
    assert d3.day == 27
    assert asset3.getFloorNumber() == 99
    assert asset3.getRoomNumber() == 99


def testDeleteAssetDoesNotExistSuccess(givenController, mw):
    givenController.deleteAsset(4)
    assets = mw(givenController.assetPlus).getSpecificAssets()
    assert len(assets) == 3

    assetNumbers = {a.getAssetNumber() for a in assets}
    assert assetNumbers == {1, 2, 3}

    asset1 = None
    asset2 = None
    asset3 = None
    for a in assets:
        if a.getAssetNumber() == 1:
            asset1 = a
        elif a.getAssetNumber() == 2:
            asset2 = a
        elif a.getAssetNumber() == 3:
            asset3 = a

    assert asset1 is not None
    assert asset1.getAssetType().getName() == "lamp"
    d1 = asset1.getPurchaseDate()
    assert d1.year == 2022
    assert d1.month == 3
    assert d1.day == 20
    assert asset1.getFloorNumber() == 9
    assert asset1.getRoomNumber() == 23

    assert asset2 is not None
    assert asset2.getAssetType().getName() == "bed"
    d2 = asset2.getPurchaseDate()
    assert d2.year == 2010
    assert d2.month == 1
    assert d2.day == 30
    assert asset2.getFloorNumber() == 10
    assert asset2.getRoomNumber() == 35

    assert asset3 is not None
    assert asset3.getAssetType().getName() == "lamp"
    d3 = asset3.getPurchaseDate()
    assert d3.year == 2007
    assert d3.month == 12
    assert d3.day == 27
    assert asset3.getFloorNumber() == 99
    assert asset3.getRoomNumber() == 99
