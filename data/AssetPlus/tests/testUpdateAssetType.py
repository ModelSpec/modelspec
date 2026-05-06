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
        from ..ecore.generated_model_layer import AssetType
    controller = AssetPlusController()
    ap = controller.assetPlus
    at1 = mw(AssetType, name="lamp", expectedLifeSpan=1800, assetPlus=ap)
    mw(ap).addAssetType(at1.model)
    at2 = mw(AssetType, name="pillow", expectedLifeSpan=700, assetPlus=ap)
    mw(ap).addAssetType(at2.model)
    at3 = mw(AssetType, name="bed", expectedLifeSpan=5000, assetPlus=ap)
    mw(ap).addAssetType(at3.model)
    yield controller


def testUpdateAssetTypeSuccess(givenController, mw):
    givenController.updateAssetType("lamp", "lamp", 1900)
    assetTypes = mw(givenController.assetPlus).getAssetTypes()
    assert len(assetTypes) == 3

    updated = None
    for at in assetTypes:
        if at.getName() == "lamp":
            updated = at
            break

    assert updated is not None
    assert updated.getExpectedLifeSpan() == 1900

    oldPairStillExists = False
    for at in assetTypes:
        if at.getName() == "lamp" and at.getExpectedLifeSpan() == 1800:
            oldPairStillExists = True
            break

    assert oldPairStillExists is False


def testUpdateAssetTypeSuccessSecondExample(givenController, mw):
    givenController.updateAssetType("pillow", "closet", 2500)
    assetTypes = mw(givenController.assetPlus).getAssetTypes()
    assert len(assetTypes) == 3

    updated = None
    for at in assetTypes:
        if at.getName() == "closet":
            updated = at
            break

    assert updated is not None
    assert updated.getExpectedLifeSpan() == 2500

    oldPairStillExists = False
    for at in assetTypes:
        if at.getName() == "pillow" and at.getExpectedLifeSpan() == 700:
            oldPairStillExists = True
            break

    assert oldPairStillExists is False


def testUpdateAssetTypeSuccessThirdExample(givenController, mw):
    givenController.updateAssetType("bed", "pot", 600)

    assetTypes = mw(givenController.assetPlus).getAssetTypes()
    assert len(assetTypes) == 3

    updated = None
    for at in assetTypes:
        if at.getName() == "pot":
            updated = at
            break

    assert updated is not None
    assert updated.getExpectedLifeSpan() == 600

    oldPairStillExists = False
    for at in assetTypes:
        if at.getName() == "bed" and at.getExpectedLifeSpan() == 5000:
            oldPairStillExists = True
            break

    assert oldPairStillExists is False


@pytest.mark.parametrize(
    "newName, newExpectedLifeSpan, errorMessage",
    [
        ("table lamp", 0, "The expected life span must be greater than 0 days"),
        ("table lamp", -30, "The expected life span must be greater than 0 days"),
        ("", 30, "The name must not be empty"),
        ("pillow", 240, "The asset type already exists"),
    ],
)
def testUpdateAssetTypeInvalidValuesFail(givenController, mw, newName, newExpectedLifeSpan, errorMessage):
    with pytest.raises(ValueError) as errorInfo:
        givenController.updateAssetType("lamp", newName, newExpectedLifeSpan)

    assert str(errorInfo.value) == errorMessage

    assetTypes = mw(givenController.assetPlus).getAssetTypes()
    assert len(assetTypes) == 3

    namesToSpan = {at.getName(): at.getExpectedLifeSpan() for at in assetTypes}
    assert namesToSpan.get("lamp") == 1800
    assert namesToSpan.get("pillow") == 700
    assert namesToSpan.get("bed") == 5000


def testUpdateAssetTypeDoesNotExistFail(givenController, mw):
    with pytest.raises(ValueError) as errorInfo:
        givenController.updateAssetType("table lamp", "desk", 6000)

    assert str(errorInfo.value) == "The asset type does not exist"

    assetTypes = mw(givenController.assetPlus).getAssetTypes()
    assert len(assetTypes) == 3

    namesToSpan = {at.getName(): at.getExpectedLifeSpan() for at in assetTypes}
    assert namesToSpan.get("lamp") == 1800
    assert namesToSpan.get("pillow") == 700
    assert namesToSpan.get("bed") == 5000
