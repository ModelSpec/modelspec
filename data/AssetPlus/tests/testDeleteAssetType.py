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


def testDeleteAssetTypeSuccess(givenController, mw):
    givenController.deleteAssetType("lamp")
    assetTypes = mw(givenController.assetPlus).getAssetTypes()
    assert len(assetTypes) == 2

    namesToSpan = {at.getName(): at.getExpectedLifeSpan() for at in assetTypes}
    assert namesToSpan.get("pillow") == 700
    assert namesToSpan.get("bed") == 5000
    assert "lamp" not in namesToSpan


@pytest.mark.parametrize("name", ["table lamp", "desk"])
def testDeleteAssetTypeDoesNotExistSuccess(givenController, mw, name):
    givenController.deleteAssetType(name)
    assetTypes = mw(givenController.assetPlus).getAssetTypes()
    assert len(assetTypes) == 3

    namesToSpan = {at.getName(): at.getExpectedLifeSpan() for at in assetTypes}
    assert namesToSpan.get("lamp") == 1800
    assert namesToSpan.get("pillow") == 700
    assert namesToSpan.get("bed") == 5000
