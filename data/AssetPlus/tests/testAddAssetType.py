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


def testAddAssetTypeSuccess(givenController, mw):
    givenController.addAssetType("fridge", 5000)

    assetTypes = mw(givenController.assetPlus).getAssetTypes()
    assert len(assetTypes) == 4

    created = None
    for at in assetTypes:
        if at.getName() == "fridge":
            created = at
            break

    assert created is not None
    assert created.getExpectedLifeSpan() == 5000


def testAddAssetTypeSuccessSecondExample(givenController, mw):
    givenController.addAssetType("microwave", 2000)

    assetTypes = mw(givenController.assetPlus).getAssetTypes()
    assert len(assetTypes) == 4

    created = None
    for at in assetTypes:
        if at.getName() == "microwave":
            created = at
            break

    assert created is not None
    assert created.getExpectedLifeSpan() == 2000


@pytest.mark.parametrize(
    "name, expectedLifeSpan, errorMessage",
    [
        ("television", 0, "The expected life span must be greater than 0 days"),
        ("television", -180, "The expected life span must be greater than 0 days"),
        ("", 180, "The name must not be empty"),
        ("lamp", 60, "The asset type already exists"),
        ("bed", 96, "The asset type already exists"),
    ],
)
def testAddAssetTypeInvalidValuesFail(givenController, mw, name, expectedLifeSpan, errorMessage):
    with pytest.raises(ValueError) as errorInfo:
        givenController.addAssetType(name, expectedLifeSpan)

    assert str(errorInfo.value) == errorMessage

    assetTypes = mw(givenController.assetPlus).getAssetTypes()
    assert len(assetTypes) == 3

    namesToSpan = {at.getName(): at.getExpectedLifeSpan() for at in assetTypes}
    assert namesToSpan.get("lamp") == 1800
    assert namesToSpan.get("pillow") == 700
    assert namesToSpan.get("bed") == 5000
