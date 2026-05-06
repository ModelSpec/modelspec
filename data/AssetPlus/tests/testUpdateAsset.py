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


def testUpdateAssetSuccess(givenController, mw):
    givenController.updateAsset(1, "bed", date(2022, 3, 21), 12, 10)
    updated = None
    for a in mw(givenController.assetPlus).getSpecificAssets():
        if a.getAssetNumber() == 1:
            updated = a
            break

    assert updated is not None
    assetType = updated.getAssetType()
    assert assetType is not None
    assert assetType.getName() == "bed"
    d = updated.getPurchaseDate()
    assert d.year == 2022
    assert d.month == 3
    assert d.day == 21
    assert updated.getFloorNumber() == 12
    assert updated.getRoomNumber() == 10
    assert len(mw(givenController.assetPlus).getSpecificAssets()) == 2


def testUpdateAssetSuccessSecondExample(givenController, mw):
    givenController.updateAsset(2, "lamp", date(2010, 1, 29), 9, -1)
    updated = None
    for a in mw(givenController.assetPlus).getSpecificAssets():
        if a.getAssetNumber() == 2:
            updated = a
            break

    assert updated is not None
    assetType = updated.getAssetType()
    assert assetType is not None
    assert assetType.getName() == "lamp"
    d = updated.getPurchaseDate()
    assert d.year == 2010
    assert d.month == 1
    assert d.day == 29
    assert updated.getFloorNumber() == 9
    assert updated.getRoomNumber() == -1
    assert len(mw(givenController.assetPlus).getSpecificAssets()) == 2


def testUpdateAssetTypeDoesNotExistFail(givenController, mw):
    with pytest.raises(ValueError) as errorInfo:
        givenController.updateAsset(1, "couch", date(1999, 4, 20), 12, 10)

    assert str(errorInfo.value) == "The asset type does not exist"

    a1 = None
    a2 = None
    for a in mw(givenController.assetPlus).getSpecificAssets():
        if a.getAssetNumber() == 1:
            a1 = a
        elif a.getAssetNumber() == 2:
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
    assert len(mw(givenController.assetPlus).getSpecificAssets()) == 2


@pytest.mark.parametrize(
    "assetNumber, newType, newPurchaseDate, newFloorNumber, newRoomNumber, errorMessage",
    [
        (2, "lamp", date(2012, 1, 1), -1, 13, "The floor number shall not be less than 0"),
        (1, "bed", date(2012, 1, 1), 7, -2, "The room number shall not be less than -1"),
    ],
)
def testUpdateAssetInvalidValuesFail(
    givenController,
    mw,
    assetNumber,
    newType,
    newPurchaseDate,
    newFloorNumber,
    newRoomNumber,
    errorMessage,
):
    with pytest.raises(ValueError) as errorInfo:
        givenController.updateAsset(assetNumber, newType, newPurchaseDate, newFloorNumber, newRoomNumber)

    assert str(errorInfo.value) == errorMessage

    a1 = None
    a2 = None
    for a in mw(givenController.assetPlus).getSpecificAssets():
        if a.getAssetNumber() == 1:
            a1 = a
        elif a.getAssetNumber() == 2:
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
    assert len(mw(givenController.assetPlus).getSpecificAssets()) == 2
