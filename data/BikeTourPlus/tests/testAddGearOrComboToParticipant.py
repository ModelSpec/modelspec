import pytest
from datetime import datetime


@pytest.fixture
def controllerWithToParticipant(modelingTool, mw):
    if modelingTool == "umple":
        from ..umple.controller import BikeTourPlusController
        from ..umple.generated_model_layer import BookableItem, User, Gear, Combo, ComboItem, Guide, Participant, BookedItem
        if hasattr(BookableItem, "bookableitemsByName"):
            BookableItem.bookableitemsByName.clear()
        if hasattr(User, "usersByEmail"):
            User.usersByEmail.clear()
    else:
        from ..ecore.controller import BikeTourPlusController
        from ..ecore.generated_model_layer import Gear, Combo, ComboItem, Guide, Participant, BookedItem

    controller = BikeTourPlusController()
    btp = mw(controller.btp)
    btp.setStartDate(datetime(2023, 3, 13))
    btp.setNrWeeks(10)
    btp.setPriceOfGuidePerWeek(100)

    gHelmet = mw(Gear, name="helmet", pricePerWeek=25, bikeTourPlus=controller.btp)
    gEbike = mw(Gear, name="e-bike", pricePerWeek=150, bikeTourPlus=controller.btp)
    gBag = mw(Gear, name="bike bag", pricePerWeek=19, bikeTourPlus=controller.btp)

    cSmall = mw(Combo, name="small combo", discount=10, bikeTourPlus=controller.btp)
    mw(ComboItem, quantity=1, bikeTourPlus=controller.btp, combo=cSmall.model, gear=gEbike.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=cSmall.model, gear=gHelmet.model)

    cLarge = mw(Combo, name="large combo", discount=25, bikeTourPlus=controller.btp)
    mw(ComboItem, quantity=1, bikeTourPlus=controller.btp, combo=cLarge.model, gear=gEbike.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=cLarge.model, gear=gHelmet.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=cLarge.model, gear=gBag.model)

    mw(Guide, email="jeff@email.com", password="pass1", name="Jeff", emergencyContact="(555)555-5555", bikeTourPlus=controller.btp)
    mw(Guide, email="john@email.com", password="pass2", name="John", emergencyContact="(444)444-4444", bikeTourPlus=controller.btp)

    pPeter = mw(Participant, email="peter@email.com", password="pass1", name="Peter", emergencyContact="(666)555-5555",
                 nrWeeks=1, weekAvailableFrom=1, weekAvailableUntil=2, lodgeRequired=True,
                 authorizationCode="no-lodge", refundedPercentageAmount=0, bikeTourPlus=controller.btp)
    pTyler = mw(Participant, email="tyler@email.com", password="pass2", name="Tyler", emergencyContact="(777)444-4444",
                 nrWeeks=2, weekAvailableFrom=2, weekAvailableUntil=5, lodgeRequired=False,
                 authorizationCode="no-lodge", refundedPercentageAmount=0, bikeTourPlus=controller.btp)
    pMary = mw(Participant, email="mary@email.com", password="pass3", name="Mary", emergencyContact="(555)666-6666",
                nrWeeks=1, weekAvailableFrom=1, weekAvailableUntil=2, lodgeRequired=False,
                authorizationCode="no-lodge", refundedPercentageAmount=0, bikeTourPlus=controller.btp)

    mw(BookedItem, quantity=1, bikeTourPlus=controller.btp, participant=pPeter.model, item=gHelmet.model)
    mw(BookedItem, quantity=2, bikeTourPlus=controller.btp, participant=pPeter.model, item=gBag.model)
    mw(BookedItem, quantity=1, bikeTourPlus=controller.btp, participant=pPeter.model, item=cSmall.model)

    mw(BookedItem, quantity=2, bikeTourPlus=controller.btp, participant=pTyler.model, item=cLarge.model)
    mw(BookedItem, quantity=1, bikeTourPlus=controller.btp, participant=pMary.model, item=cLarge.model)

    yield controller


@pytest.mark.parametrize("name, quantity, email, numberOfItemsForParticipant", [
    ("bike bag", 3, "peter@email.com", 3),
    ("bike bag", 1, "tyler@email.com", 2),
    ("e-bike", 1, "peter@email.com", 4),
    ("e-bike", 1, "tyler@email.com", 2),
    ("helmet", 2, "peter@email.com", 3),
    ("helmet", 1, "tyler@email.com", 2),
    ("small combo", 2, "peter@email.com", 3),
    ("small combo", 1, "tyler@email.com", 2),
    ("large combo", 1, "peter@email.com", 4),
    ("large combo", 3, "tyler@email.com", 1),
])
def testAddGearOrComboSuccess(controllerWithToParticipant, mw, name, quantity, email, numberOfItemsForParticipant):
    controllerWithToParticipant.addGearOrComboToParticipant(name, email)

    btp = mw(controllerWithToParticipant.btp)
    participant = next((p for p in btp.getParticipants() if p.getEmail() == email), None)
    bookedItems = participant.getBookedItems()

    target = next((bi for bi in bookedItems if bi.getItem().getName() == name), None)
    assert target is not None, f"Item {name} should exist for {email}"
    assert target.getQuantity() == int(quantity)

    assert len(bookedItems) == int(numberOfItemsForParticipant)
    assert len(btp.getParticipants()) == 3


@pytest.mark.parametrize("nonExistingName, name, quantity, email, numberOfItemsForParticipant, error", [
    ("spare tire", "bike bag", 2, "peter@email.com", 3, "The piece of gear or combo does not exist"),
    ("bike lock", "helmet", 1, "peter@email.com", 3, "The piece of gear or combo does not exist"),
    ("spare tire", "small combo", 1, "peter@email.com", 3, "The piece of gear or combo does not exist"),
    ("combo plus", "large combo", 2, "tyler@email.com", 1, "The piece of gear or combo does not exist"),
    ("deluxe combo", "large combo", 1, "mary@email.com", 1, "The piece of gear or combo does not exist"),
])
def testAddNonExistingItem(controllerWithToParticipant, mw, nonExistingName, name, quantity, email, numberOfItemsForParticipant, error):
    with pytest.raises(ValueError) as excinfo:
        controllerWithToParticipant.addGearOrComboToParticipant(nonExistingName, email)

    assert str(excinfo.value) == error

    btp = mw(controllerWithToParticipant.btp)
    participant = next((p for p in btp.getParticipants() if p.getEmail() == email), None)
    bookedItems = participant.getBookedItems()
    target = next((bi for bi in bookedItems if bi.getItem().getName() == name), None)
    assert target.getQuantity() == int(quantity)
    assert len(bookedItems) == int(numberOfItemsForParticipant)


@pytest.mark.parametrize("name, email, error", [
    ("e-bike", "john@email.com", "The participant does not exist"),
    ("helmet", "john@email.com", "The participant does not exist"),
    ("e-bike", "joe@email.com", "The participant does not exist"),
    ("small combo", "joe@email.com", "The participant does not exist"),
    ("large combo", "joe@email.com", "The participant does not exist"),
])
def testAddtoNonExistingParticipant(controllerWithToParticipant, mw, name, email, error):
    with pytest.raises(ValueError) as excinfo:
        controllerWithToParticipant.addGearOrComboToParticipant(name, email)

    assert str(excinfo.value) == error
    assert len(mw(controllerWithToParticipant.btp).getParticipants()) == 3
