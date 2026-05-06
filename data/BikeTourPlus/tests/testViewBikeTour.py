import pytest
from datetime import datetime


@pytest.fixture
def controllerWithBikeTours(modelingTool, mw):
    global Gear, Combo
    if modelingTool == "umple":
        from ..umple.controller import BikeTourPlusController
        from ..umple.generated_model_layer import BookableItem, User, BikeTour, Gear, Combo, ComboItem, Guide, Participant, BookedItem
        if hasattr(BookableItem, "bookableitemsByName"):
            BookableItem.bookableitemsByName.clear()
        if hasattr(User, "usersByEmail"):
            User.usersByEmail.clear()
        if hasattr(BikeTour, "biketoursById"):
            BikeTour.biketoursById.clear()
    else:
        from ..ecore.controller import BikeTourPlusController
        from ..ecore.generated_model_layer import BikeTour, Gear, Combo, ComboItem, Guide, Participant, BookedItem

    controller = BikeTourPlusController()
    btp = mw(controller.btp)
    btp.setStartDate(datetime(2023, 3, 13))
    btp.setNrWeeks(10)
    btp.setPriceOfGuidePerWeek(100)

    h = mw(Gear, name="helmet", pricePerWeek=25, bikeTourPlus=controller.btp)
    e = mw(Gear, name="e-bike", pricePerWeek=150, bikeTourPlus=controller.btp)
    b = mw(Gear, name="bike bag", pricePerWeek=19, bikeTourPlus=controller.btp)
    mw(Gear, name="tire kit", pricePerWeek=15, bikeTourPlus=controller.btp)

    s = mw(Combo, name="small combo", discount=10, bikeTourPlus=controller.btp)
    l = mw(Combo, name="large combo", discount=0, bikeTourPlus=controller.btp)

    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=s.model, gear=h.model)
    mw(ComboItem, quantity=1, bikeTourPlus=controller.btp, combo=s.model, gear=e.model)

    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=l.model, gear=h.model)
    mw(ComboItem, quantity=1, bikeTourPlus=controller.btp, combo=l.model, gear=e.model)
    mw(ComboItem, quantity=2, bikeTourPlus=controller.btp, combo=l.model, gear=b.model)

    jeff = mw(Guide, email="jeff@email.com", password="pass1", name="Jeff", emergencyContact="(555)555-5555", bikeTourPlus=controller.btp)
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

    tour1 = mw(BikeTour, id=1, startWeek=1, endWeek=1, guide=jeff.model, bikeTourPlus=controller.btp)
    tour1.addParticipant(peter.model)
    tour1.addParticipant(mary.model)

    tour2 = mw(BikeTour, id=2, startWeek=2, endWeek=3, guide=jeff.model, bikeTourPlus=controller.btp)
    tour2.addParticipant(tyler.model)

    yield controller

def _calculateTotalCostsForBookableItems(participant):
    totalCost = 0
    for bi in participant.getBookedItems():
        item = bi.getItem()
        if isinstance(item, Gear):
            totalCost += item.getPricePerWeek() * bi.getQuantity() * participant.getNrWeeks()
        elif isinstance(item, Combo):
            for ci in item.getComboItems():
                gear = ci.getGear()
                totalCost += gear.getPricePerWeek() * bi.getQuantity() * ci.getQuantity() * participant.getNrWeeks() * (1 - item.getDiscount() / 100)
    return totalCost


def testViewBikeTour1Successfully(controllerWithBikeTours, mw):
    btp = mw(controllerWithBikeTours.btp)

    tourInfo = mw(controllerWithBikeTours.viewBikeTour(1))

    assert tourInfo.getId() == 1
    assert tourInfo.getStartWeek() == 1
    assert tourInfo.getEndWeek() == 1
    assert tourInfo.getGuide().getEmail() == "jeff@email.com"
    assert tourInfo.getGuide().getName() == "Jeff"
    nrWeeks = tourInfo.getEndWeek() - tourInfo.getStartWeek() + 1
    totalCostForGuide = btp.getPriceOfGuidePerWeek() * nrWeeks
    assert totalCostForGuide == 100
    participantEmails = [p.getEmail() for p in tourInfo.getParticipants()]
    assert "peter@email.com" in participantEmails
    assert "mary@email.com" in participantEmails
    for participant in tourInfo.getParticipants():
        if participant.getEmail() == "peter@email.com":
            assert participant.getName() == "Peter"
            totalCostForBookableItems = _calculateTotalCostsForBookableItems(participant)
            assert totalCostForBookableItems == 243
            assert totalCostForBookableItems + btp.getPriceOfGuidePerWeek() * participant.getNrWeeks() == 343
        elif participant.getEmail() == "mary@email.com":
            assert participant.getName() == "Mary"
            totalCostForBookableItems = _calculateTotalCostsForBookableItems(participant)
            assert totalCostForBookableItems == 238
            assert totalCostForBookableItems + btp.getPriceOfGuidePerWeek() * participant.getNrWeeks() == 338


def testViewBikeTour2Successfully(controllerWithBikeTours, mw):
    btp = mw(controllerWithBikeTours.btp)

    tourInfo = mw(controllerWithBikeTours.viewBikeTour(2))

    assert tourInfo.getId() == 2
    assert tourInfo.getStartWeek() == 2
    assert tourInfo.getEndWeek() == 3
    assert tourInfo.getGuide().getEmail() == "jeff@email.com"
    assert tourInfo.getGuide().getName() == "Jeff"
    nrWeeks = tourInfo.getEndWeek() - tourInfo.getStartWeek() + 1
    assert btp.getPriceOfGuidePerWeek() * nrWeeks == 200
    participantEmails = [p.getEmail() for p in tourInfo.getParticipants()]
    assert "tyler@email.com" in participantEmails

    for participant in tourInfo.getParticipants():
        if participant.getEmail() == "tyler@email.com":
            assert participant.getName() == "Tyler"
            totalCostForBookableItems = _calculateTotalCostsForBookableItems(participant)
            assert totalCostForBookableItems == 952
            assert totalCostForBookableItems + btp.getPriceOfGuidePerWeek() * participant.getNrWeeks()  == 1152
