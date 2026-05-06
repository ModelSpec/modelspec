from datetime import date, datetime
import pytest


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
    yield controller


@pytest.mark.parametrize(
    "assetNumber,typeName,purchaseDate,floorNumber,roomNumber",
    [
        (3, "bed",  date(2020, 6, 23), 2, 32),
        (3, "lamp", date(2012, 1, 1), 3, 78),
        (3, "lamp", date(2012, 1, 1), 0, -1),
    ],
)
def testAddAssetSuccess(givenController, mw, assetNumber, typeName, purchaseDate, floorNumber, roomNumber):
    givenController.addAsset(assetNumber, typeName, purchaseDate, floorNumber, roomNumber)
    assert len(mw(givenController.assetPlus).getSpecificAssets()) == 3

    created = None
    for a in mw(givenController.assetPlus).getSpecificAssets():
        if a.getAssetNumber() == assetNumber:
            created = a
            break

    assert created is not None
    assetType = created.getAssetType()
    assert assetType is not None
    assert assetType.getName() == typeName
    d = created.getPurchaseDate()
    assert d.year == purchaseDate.year
    assert d.month == purchaseDate.month
    assert d.day == purchaseDate.day
    assert created.getFloorNumber() == floorNumber
    assert created.getRoomNumber() == roomNumber


@pytest.mark.parametrize(
    "assetNumber,typeName,purchaseDate,floorNumber,roomNumber,error",
    [
        (3, "television", date(2012, 1, 1), 5, 43, "The asset type does not exist"),
    ],
)
def testAddAssetTypeDoesNotExistFail(givenController, mw, assetNumber, typeName, purchaseDate, floorNumber, roomNumber, error):
    with pytest.raises(ValueError) as err:
        givenController.addAsset(assetNumber, typeName, purchaseDate, floorNumber, roomNumber)
    assert str(err.value) == error
    assert len(mw(givenController.assetPlus).getSpecificAssets()) == 2

    a1 = None
    a2 = None
    for a in mw(givenController.assetPlus).getSpecificAssets():
        if a.getAssetNumber() == 1:
            a1 = a
        if a.getAssetNumber() == 2:
            a2 = a

    assert a1 is not None
    assert a1.getAssetType().getName() == "lamp"
    d1 = a1.getPurchaseDate()
    assert d1.year == 2022
    assert d1.month == 3
    assert d1.day == 20
    assert a1.getFloorNumber() == 9
    assert a1.getRoomNumber() == 23

    assert a2 is not None
    assert a2.getAssetType().getName() == "bed"
    d2 = a2.getPurchaseDate()
    assert d2.year == 2010
    assert d2.month == 1
    assert d2.day == 30
    assert a2.getFloorNumber() == 10
    assert a2.getRoomNumber() == 35


@pytest.mark.parametrize(
    "assetNumber,typeName,purchaseDate,floorNumber,roomNumber,error",
    [
        (0, "lamp", date(2012, 1, 1), 1, 13, "The asset number shall not be less than 1"),
        (3, "lamp", date(2012, 1, 1), -1, 13, "The floor number shall not be less than 0"),
        (3, "bed",  date(2012, 1, 1), 7, -2, "The room number shall not be less than -1"),
    ],
)
def testAddAssetInvalidValuesFail(givenController, mw, assetNumber, typeName, purchaseDate, floorNumber, roomNumber, error):
    with pytest.raises(ValueError) as err:
        givenController.addAsset(assetNumber, typeName, purchaseDate, floorNumber, roomNumber)
    assert str(err.value) == error
    assert len(mw(givenController.assetPlus).getSpecificAssets()) == 2

    a1 = None
    a2 = None
    for a in mw(givenController.assetPlus).getSpecificAssets():
        if a.getAssetNumber() == 1:
            a1 = a
        if a.getAssetNumber() == 2:
            a2 = a

    assert a1 is not None
    assert a1.getAssetType().getName() == "lamp"
    d1 = a1.getPurchaseDate()
    assert d1.year == 2022
    assert d1.month == 3
    assert d1.day == 20
    assert a1.getFloorNumber() == 9
    assert a1.getRoomNumber() == 23

    assert a2 is not None
    assert a2.getAssetType().getName() == "bed"
    d2 = a2.getPurchaseDate()
    assert d2.year == 2010
    assert d2.month == 1
    assert d2.day == 30
    assert a2.getFloorNumber() == 10
    assert a2.getRoomNumber() == 35
