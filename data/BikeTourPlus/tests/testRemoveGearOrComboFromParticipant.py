import pytest
from datetime import datetime


@pytest.fixture
def controllerWithParticipantsAndBookedItems(modelingTool, mw):
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

    h = mw(Gear, name="helmet", pricePerWeek=25, bikeTourPlus=controller.btp)
    e = mw(Gear, name="e-bike", pricePerWeek=150, bikeTourPlus=controller.btp)
    b = mw(Gear, name="bike bag", pricePerWeek=19, bikeTourPlus=controller.btp)

    s = mw(Combo, name="small combo", discount=10, bikeTourPlus=controller.btp)
    mw(ComboItem, quantity=1, bikeTourPlus=controller.btp, combo=s.model, gear=e.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=s.model, gear=h.model)

    l = mw(Combo, name="large combo", discount=25, bikeTourPlus=controller.btp)
    mw(ComboItem, quantity=1, bikeTourPlus=controller.btp, combo=l.model, gear=e.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=l.model, gear=h.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=l.model, gear=b.model)

    mw(Guide, email="jeff@email.com", password="pass1", name="Jeff", emergencyContact="(555)555-5555", bikeTourPlus=controller.btp)
    mw(Guide, email="john@email.com", password="pass2", name="John", emergencyContact="(444)444-4444", bikeTourPlus=controller.btp)

    peter = mw(Participant, email="peter@email.com", password="pass1", name="Peter", emergencyContact="(666)555-5555",
               nrWeeks=1, weekAvailableFrom=1, weekAvailableUntil=2, lodgeRequired=True,
               authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controller.btp)
    tyler = mw(Participant, email="tyler@email.com", password="pass2", name="Tyler", emergencyContact="(777)444-4444",
               nrWeeks=2, weekAvailableFrom=2, weekAvailableUntil=5, lodgeRequired=False,
               authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controller.btp)
    mary = mw(Participant, email="mary@email.com", password="pass3", name="Mary", emergencyContact="(555)666-6666",
              nrWeeks=1, weekAvailableFrom=1, weekAvailableUntil=2, lodgeRequired=False,
              authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controller.btp)

    mw(BookedItem, quantity=1, bikeTourPlus=controller.btp, participant=peter.model, item=h.model)
    mw(BookedItem, quantity=2, bikeTourPlus=controller.btp, participant=peter.model, item=b.model)
    mw(BookedItem, quantity=1, bikeTourPlus=controller.btp, participant=peter.model, item=s.model)

    mw(BookedItem, quantity=2, bikeTourPlus=controller.btp, participant=tyler.model, item=l.model)

    mw(BookedItem, quantity=1, bikeTourPlus=controller.btp, participant=mary.model, item=l.model)

    yield controller


@pytest.mark.parametrize("name, quantity, email, numberOfItemsForParticipant", [
    ("bike bag", 1, "peter@email.com", 3),
    ("large combo", 1, "tyler@email.com", 1),
])
def testRemoveGearOrComboSuccess(controllerWithParticipantsAndBookedItems, mw, name, quantity, email, numberOfItemsForParticipant):
    controllerWithParticipantsAndBookedItems.removeGearOrComboFromParticipant(name, email)

    btp = mw(controllerWithParticipantsAndBookedItems.btp)
    participant = next((p for p in btp.getParticipants() if p.getEmail() == email), None)
    assert participant is not None

    targetItem = next((item for item in participant.getBookedItems() if item.getItem().getName() == name), None)
    assert targetItem is not None
    assert targetItem.getQuantity() == quantity

    assert len(participant.getBookedItems()) == numberOfItemsForParticipant
    assert len(btp.getParticipants()) == 3


@pytest.mark.parametrize("name, email, numberOfItemsForParticipant", [
    ("e-bike", "peter@email.com", 3),
    ("e-bike", "tyler@email.com", 1),
    ("helmet", "peter@email.com", 2),
    ("helmet", "tyler@email.com", 1),
    ("small combo", "peter@email.com", 2),
    ("small combo", "tyler@email.com", 1),
    ("large combo", "peter@email.com", 3),
    ("large combo", "mary@email.com", 0),
])
def testRemoveLastItemOfGearOrCombo(controllerWithParticipantsAndBookedItems, mw, name, email, numberOfItemsForParticipant):
    controllerWithParticipantsAndBookedItems.removeGearOrComboFromParticipant(name, email)

    btp = mw(controllerWithParticipantsAndBookedItems.btp)
    participant = next((p for p in btp.getParticipants() if p.getEmail() == email), None)
    assert participant is not None

    items = participant.getBookedItems()
    assert not any(item.getItem().getName() == name for item in items)
    assert len(items) == numberOfItemsForParticipant
    assert len(btp.getParticipants()) == 3


@pytest.mark.parametrize("name, email, error", [
    ("e-bike", "john@email.com", "The participant does not exist"),
    ("helmet", "john@email.com", "The participant does not exist"),
    ("e-bike", "joe@email.com", "The participant does not exist"),
    ("small combo", "joe@email.com", "The participant does not exist"),
    ("large combo", "joe@email.com", "The participant does not exist"),
])
def testRemoveGearOrComboNonExistentParticipant(controllerWithParticipantsAndBookedItems, mw, name, email, error):
    with pytest.raises(ValueError) as error_info:
        controllerWithParticipantsAndBookedItems.removeGearOrComboFromParticipant(name, email)

    assert str(error_info.value) == error
    assert len(mw(controllerWithParticipantsAndBookedItems.btp).getParticipants()) == 3
