import pytest
from datetime import datetime


@pytest.fixture
def controllerWithStart(modelingTool, mw):
    global Participant, Status, BikeTour
    if modelingTool == "umple":
        from ..umple.controller import BikeTourPlusController
        from ..umple.generated_model_layer import BookableItem, User, BikeTour, Gear, Guide, Participant
        if hasattr(BookableItem, "bookableitemsByName"):
            BookableItem.bookableitemsByName.clear()
        if hasattr(User, "usersByEmail"):
            User.usersByEmail.clear()
        if hasattr(BikeTour, "biketoursById"):
            BikeTour.biketoursById.clear()
        Status = Participant.Status
    else:
        from ..ecore.controller import BikeTourPlusController
        from ..ecore.generated_model_layer import BikeTour, Gear, Guide, Participant, Status

    controller = BikeTourPlusController()
    btp = mw(controller.btp)
    btp.setStartDate(datetime(2023, 3, 13))
    btp.setNrWeeks(10)
    btp.setPriceOfGuidePerWeek(100)

    mw(Gear, name="helmet", pricePerWeek=25, bikeTourPlus=controller.btp)
    mw(Gear, name="e-bike", pricePerWeek=150, bikeTourPlus=controller.btp)
    mw(Gear, name="bike bag", pricePerWeek=19, bikeTourPlus=controller.btp)
    mw(Gear, name="tire kit", pricePerWeek=15, bikeTourPlus=controller.btp)

    jeff = mw(Guide, email="jeff@email.com", password="pass1", name="Jeff", emergencyContact="(555)555-5555", bikeTourPlus=controller.btp)
    mw(Guide, email="john@email.com", password="pass2", name="John", emergencyContact="(444)444-4444", bikeTourPlus=controller.btp)

    alice = mw(Participant, email="alice@gmail.com", password="pass123", name="Alice Jones", emergencyContact="(200)5551234",
               nrWeeks=3, weekAvailableFrom=1, weekAvailableUntil=3, lodgeRequired=True,
               authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controller.btp)
    charlie = mw(Participant, email="charlie@hotmail.ca", password="charlie", name="Charles Tremblay", emergencyContact="(200)5559876",
                 nrWeeks=3, weekAvailableFrom=1, weekAvailableUntil=5, lodgeRequired=False,
                 authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controller.btp)
    johndoe = mw(Participant, email="john@hotmail.ca", password="john123", name="John Doe", emergencyContact="(200)5551234",
                 nrWeeks=3, weekAvailableFrom=1, weekAvailableUntil=3, lodgeRequired=False,
                 authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controller.btp)
    emily = mw(Participant, email="emily@hotmail.ca", password="emily007", name="Emily Green", emergencyContact="(200)5559876",
               nrWeeks=2, weekAvailableFrom=4, weekAvailableUntil=5, lodgeRequired=False,
               authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controller.btp)
    new = mw(Participant, email="new@hotmail.ca", password="newnew", name="Johnny New", emergencyContact="(200)5559999",
             nrWeeks=5, weekAvailableFrom=6, weekAvailableUntil=10, lodgeRequired=True,
             authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controller.btp)

    alice.setStatus(Status.Assigned)
    charlie.setStatus(Status.Assigned)
    johndoe.setStatus(Status.Assigned)
    emily.setStatus(Status.Assigned)
    new.setStatus(Status.NotAssigned)

    tour1 = mw(BikeTour, id=1, startWeek=1, endWeek=3, guide=jeff.model, bikeTourPlus=controller.btp)
    tour1.addParticipant(alice.model)
    tour1.addParticipant(charlie.model)
    tour1.addParticipant(johndoe.model)

    tour2 = mw(BikeTour, id=2, startWeek=4, endWeek=5, guide=jeff.model, bikeTourPlus=controller.btp)
    tour2.addParticipant(emily.model)

    yield controller


def testManagerStartsToursSuccessfully(controllerWithStart, mw):
    btp = mw(controllerWithStart.btp)
    alice = next(p for p in btp.getParticipants() if p.getEmail() == "alice@gmail.com")
    charlie = next(p for p in btp.getParticipants() if p.getEmail() == "charlie@hotmail.ca")
    johndoe = next(p for p in btp.getParticipants() if p.getEmail() == "john@hotmail.ca")
    emily = next(p for p in btp.getParticipants() if p.getEmail() == "emily@hotmail.ca")

    alice.setStatus(Status.Paid)

    controllerWithStart.processStart(1)

    assert alice.getStatus() == Status.Started
    assert charlie.getStatus() == Status.Banned
    assert johndoe.getStatus() == Status.Banned
    assert emily.getStatus() == Status.Assigned


def testStartTourNotAssigned(controllerWithStart, mw):
    btp = mw(controllerWithStart.btp)
    new = next(p for p in btp.getParticipants() if p.getEmail() == "new@hotmail.ca")

    controllerWithStart.processStart(6)

    assert new.getStatus() == Status.NotAssigned


def testStartTourAlreadyStarted(controllerWithStart, mw):
    btp = mw(controllerWithStart.btp)
    emily = next(p for p in btp.getParticipants() if p.getEmail() == "emily@hotmail.ca")
    emily.setStatus(Status.Started)

    with pytest.raises(ValueError) as error_info:
        controllerWithStart.processStart(4)

    assert str(error_info.value) == "Cannot start tour because the participant has already started their tour"
    assert emily.getStatus() == Status.Started


def testStartTourBanned(controllerWithStart, mw):
    btp = mw(controllerWithStart.btp)
    emily = next(p for p in btp.getParticipants() if p.getEmail() == "emily@hotmail.ca")
    emily.setStatus(Status.Banned)

    with pytest.raises(ValueError) as error_info:
        controllerWithStart.processStart(4)

    assert str(error_info.value) == "Cannot start tour because the participant is banned"
    assert emily.getStatus() == Status.Banned


def testStartTourCancelled(controllerWithStart, mw):
    btp = mw(controllerWithStart.btp)
    emily = next(p for p in btp.getParticipants() if p.getEmail() == "emily@hotmail.ca")
    emily.setStatus(Status.Cancelled)

    with pytest.raises(ValueError) as error_info:
        controllerWithStart.processStart(4)

    assert str(error_info.value) == "Cannot start tour because the participant has cancelled their tour"
    assert emily.getStatus() == Status.Cancelled


def testStartTourFinished(controllerWithStart, mw):
    btp = mw(controllerWithStart.btp)
    emily = next(p for p in btp.getParticipants() if p.getEmail() == "emily@hotmail.ca")
    emily.setStatus(Status.Finished)

    with pytest.raises(ValueError) as error_info:
        controllerWithStart.processStart(4)

    assert str(error_info.value) == "Cannot start tour because the participant has finished their tour"
    assert emily.getStatus() == Status.Finished
