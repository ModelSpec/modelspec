import pytest
from datetime import datetime


@pytest.fixture
def controllerWithInitiate(modelingTool, mw):
    global Participant, Status
    if modelingTool == "umple":
        from ..umple.controller import BikeTourPlusController
        from ..umple.generated_model_layer import BookableItem, User, BikeTour, Guide, Participant
        if hasattr(BookableItem, "bookableitemsByName"):
            BookableItem.bookableitemsByName.clear()
        if hasattr(User, "usersByEmail"):
            User.usersByEmail.clear()
        if hasattr(BikeTour, "biketoursById"):
            BikeTour.biketoursById.clear()
        Status = Participant.Status
    else:
        from ..ecore.controller import BikeTourPlusController
        from ..ecore.generated_model_layer import Guide, Participant, Status

    controller = BikeTourPlusController()
    btp = mw(controller.btp)
    btp.setStartDate(datetime(2023, 3, 13))
    btp.setNrWeeks(10)
    btp.setPriceOfGuidePerWeek(100)

    mw(Guide, email="jeff@email.com", password="pass1", name="Jeff", emergencyContact="(555)555-5555", bikeTourPlus=controller.btp)
    mw(Guide, email="john@email.com", password="pass2", name="John", emergencyContact="(444)444-4444", bikeTourPlus=controller.btp)
    mw(Guide, email="bob@email.com", password="psw0rd1", name="Bob", emergencyContact="(200)5555678", bikeTourPlus=controller.btp)

    yield controller


def testInitiateNewerParticipantAssignedBeforeOlder(controllerWithInitiate, mw):
    mw(Participant, email="alice@gmail.com", password="pass123", name="Alice Jones", emergencyContact="(200)5551234",
       nrWeeks=3, weekAvailableFrom=1, weekAvailableUntil=3, lodgeRequired=True,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)
    mw(Participant, email="new@hotmail.ca", password="newnew", name="Johnny New", emergencyContact="(200)5559999",
       nrWeeks=5, weekAvailableFrom=2, weekAvailableUntil=6, lodgeRequired=True,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)
    mw(Participant, email="charlie@hotmail.ca", password="charlie", name="Charles Tremblay", emergencyContact="(200)5559876",
       nrWeeks=3, weekAvailableFrom=1, weekAvailableUntil=5, lodgeRequired=False,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)
    mw(Participant, email="john@hotmail.ca", password="john123", name="John Doe", emergencyContact="(200)5551234",
       nrWeeks=3, weekAvailableFrom=1, weekAvailableUntil=3, lodgeRequired=False,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)
    mw(Participant, email="emily@hotmail.ca", password="emily007", name="Emily Green", emergencyContact="(200)5559876",
       nrWeeks=2, weekAvailableFrom=4, weekAvailableUntil=5, lodgeRequired=False,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)

    controllerWithInitiate.createBikeTours()

    btp = mw(controllerWithInitiate.btp)
    assert len(btp.getBikeTours()) == 3

    t1 = next((t for t in btp.getBikeTours() if t.getId() == 1), None)
    assert t1.getStartWeek() == 1
    assert t1.getEndWeek() == 3
    assert t1.getGuide().getEmail() == "jeff@email.com"
    t1Participants = [p.getEmail() for p in t1.getParticipants()]
    assert set(t1Participants) == {"alice@gmail.com", "charlie@hotmail.ca", "john@hotmail.ca"}

    t2 = next((t for t in btp.getBikeTours() if t.getId() == 2), None)
    assert t2.getStartWeek() == 4
    assert t2.getEndWeek() == 5
    assert t2.getGuide().getEmail() == "jeff@email.com"
    t2Participants = [p.getEmail() for p in t2.getParticipants()]
    assert t2Participants == ["emily@hotmail.ca"]

    t3 = next((t for t in btp.getBikeTours() if t.getId() == 3), None)
    assert t3.getStartWeek() == 2
    assert t3.getEndWeek() == 6
    assert t3.getGuide().getEmail() == "john@email.com"
    t3Participants = [p.getEmail() for p in t3.getParticipants()]
    assert t3Participants == ["new@hotmail.ca"]

    for email in ["alice@gmail.com", "new@hotmail.ca", "charlie@hotmail.ca", "john@hotmail.ca", "emily@hotmail.ca"]:
        p = next((p for p in btp.getParticipants() if p.getEmail() == email), None)
        assert p.getStatus() == Status.Assigned


def testInitiateSingleGuide(controllerWithInitiate, mw):
    mw(Participant, email="alice@gmail.com", password="pass123", name="Alice Jones", emergencyContact="(200)5551234",
       nrWeeks=3, weekAvailableFrom=1, weekAvailableUntil=3, lodgeRequired=True,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)
    mw(Participant, email="new@hotmail.ca", password="newnew", name="Johnny New", emergencyContact="(200)5559999",
       nrWeeks=4, weekAvailableFrom=1, weekAvailableUntil=10, lodgeRequired=True,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)
    mw(Participant, email="charlie@hotmail.ca", password="charlie", name="Charles Tremblay", emergencyContact="(200)5559876",
       nrWeeks=3, weekAvailableFrom=1, weekAvailableUntil=5, lodgeRequired=False,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)
    mw(Participant, email="john@hotmail.ca", password="john123", name="John Doe", emergencyContact="(200)5551234",
       nrWeeks=3, weekAvailableFrom=1, weekAvailableUntil=3, lodgeRequired=False,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)
    mw(Participant, email="emily@hotmail.ca", password="emily007", name="Emily Green", emergencyContact="(200)5559876",
       nrWeeks=2, weekAvailableFrom=4, weekAvailableUntil=10, lodgeRequired=False,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)

    controllerWithInitiate.createBikeTours()

    btp = mw(controllerWithInitiate.btp)
    assert len(btp.getBikeTours()) == 3

    t1 = next((t for t in btp.getBikeTours() if t.getId() == 1), None)
    assert t1.getStartWeek() == 1
    assert t1.getEndWeek() == 3
    assert t1.getGuide().getEmail() == "jeff@email.com"
    t1Participants = [p.getEmail() for p in t1.getParticipants()]
    assert set(t1Participants) == {"alice@gmail.com", "charlie@hotmail.ca", "john@hotmail.ca"}

    t2 = next((t for t in btp.getBikeTours() if t.getId() == 2), None)
    assert t2.getStartWeek() == 4
    assert t2.getEndWeek() == 7
    assert t2.getGuide().getEmail() == "jeff@email.com"
    t2Participants = [p.getEmail() for p in t2.getParticipants()]
    assert t2Participants == ["new@hotmail.ca"]

    t3 = next((t for t in btp.getBikeTours() if t.getId() == 3), None)
    assert t3.getStartWeek() == 8
    assert t3.getEndWeek() == 9
    assert t3.getGuide().getEmail() == "jeff@email.com"
    t3Participants = [p.getEmail() for p in t3.getParticipants()]
    assert t3Participants == ["emily@hotmail.ca"]

    for email in ["alice@gmail.com", "new@hotmail.ca", "charlie@hotmail.ca", "john@hotmail.ca", "emily@hotmail.ca"]:
        p = next((p for p in btp.getParticipants() if p.getEmail() == email), None)
        assert p.getStatus() == Status.Assigned


def testInitiateAllGuides(controllerWithInitiate, mw):
    mw(Participant, email="alice@gmail.com", password="pass123", name="Alice Jones", emergencyContact="(200)5551234",
       nrWeeks=3, weekAvailableFrom=1, weekAvailableUntil=3, lodgeRequired=True,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)
    mw(Participant, email="new@hotmail.ca", password="newnew", name="Johnny New", emergencyContact="(200)5559999",
       nrWeeks=5, weekAvailableFrom=1, weekAvailableUntil=5, lodgeRequired=True,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)
    mw(Participant, email="charlie@hotmail.ca", password="charlie", name="Charles Tremblay", emergencyContact="(200)5559876",
       nrWeeks=3, weekAvailableFrom=1, weekAvailableUntil=5, lodgeRequired=False,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)
    mw(Participant, email="john@hotmail.ca", password="john123", name="John Doe", emergencyContact="(200)5551234",
       nrWeeks=3, weekAvailableFrom=1, weekAvailableUntil=3, lodgeRequired=False,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)
    mw(Participant, email="emily@hotmail.ca", password="emily007", name="Emily Green", emergencyContact="(200)5559876",
       nrWeeks=2, weekAvailableFrom=1, weekAvailableUntil=4, lodgeRequired=False,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)

    controllerWithInitiate.createBikeTours()

    btp = mw(controllerWithInitiate.btp)
    assert len(btp.getBikeTours()) == 3

    t1 = next((t for t in btp.getBikeTours() if t.getId() == 1), None)
    assert t1.getStartWeek() == 1
    assert t1.getEndWeek() == 3
    assert t1.getGuide().getEmail() == "jeff@email.com"
    t1Participants = [p.getEmail() for p in t1.getParticipants()]
    assert set(t1Participants) == {"alice@gmail.com", "charlie@hotmail.ca", "john@hotmail.ca"}

    t2 = next((t for t in btp.getBikeTours() if t.getId() == 2), None)
    assert t2.getStartWeek() == 1
    assert t2.getEndWeek() == 5
    assert t2.getGuide().getEmail() == "john@email.com"
    t2Participants = [p.getEmail() for p in t2.getParticipants()]
    assert t2Participants == ["new@hotmail.ca"]

    t3 = next((t for t in btp.getBikeTours() if t.getId() == 3), None)
    assert t3.getStartWeek() == 1
    assert t3.getEndWeek() == 2
    assert t3.getGuide().getEmail() == "bob@email.com"
    t3Participants = [p.getEmail() for p in t3.getParticipants()]
    assert t3Participants == ["emily@hotmail.ca"]

    for email in ["alice@gmail.com", "new@hotmail.ca", "charlie@hotmail.ca", "john@hotmail.ca", "emily@hotmail.ca"]:
        p = next((p for p in btp.getParticipants() if p.getEmail() == email), None)
        assert p.getStatus() == Status.Assigned


def testInitiateGuideAssignedForAllWeeks(controllerWithInitiate, mw):
    mw(Participant, email="alice@gmail.com", password="pass123", name="Alice Jones", emergencyContact="(200)5551234",
       nrWeeks=3, weekAvailableFrom=1, weekAvailableUntil=3, lodgeRequired=True,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)
    mw(Participant, email="new@hotmail.ca", password="newnew", name="Johnny New", emergencyContact="(200)5559999",
       nrWeeks=7, weekAvailableFrom=4, weekAvailableUntil=10, lodgeRequired=True,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)
    mw(Participant, email="charlie@hotmail.ca", password="charlie", name="Charles Tremblay", emergencyContact="(200)5559876",
       nrWeeks=3, weekAvailableFrom=1, weekAvailableUntil=5, lodgeRequired=False,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)
    mw(Participant, email="john@hotmail.ca", password="john123", name="John Doe", emergencyContact="(200)5551234",
       nrWeeks=3, weekAvailableFrom=1, weekAvailableUntil=3, lodgeRequired=False,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)
    mw(Participant, email="emily@hotmail.ca", password="emily007", name="Emily Green", emergencyContact="(200)5559876",
       nrWeeks=2, weekAvailableFrom=1, weekAvailableUntil=5, lodgeRequired=False,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)

    controllerWithInitiate.createBikeTours()

    btp = mw(controllerWithInitiate.btp)
    assert len(btp.getBikeTours()) == 3

    t1 = next((t for t in btp.getBikeTours() if t.getId() == 1), None)
    assert t1.getStartWeek() == 1
    assert t1.getEndWeek() == 3
    assert t1.getGuide().getEmail() == "jeff@email.com"
    t1Participants = [p.getEmail() for p in t1.getParticipants()]
    assert set(t1Participants) == {"alice@gmail.com", "charlie@hotmail.ca", "john@hotmail.ca"}

    t2 = next((t for t in btp.getBikeTours() if t.getId() == 2), None)
    assert t2.getStartWeek() == 4
    assert t2.getEndWeek() == 10
    assert t2.getGuide().getEmail() == "jeff@email.com"
    t2Participants = [p.getEmail() for p in t2.getParticipants()]
    assert t2Participants == ["new@hotmail.ca"]

    t3 = next((t for t in btp.getBikeTours() if t.getId() == 3), None)
    assert t3.getStartWeek() == 1
    assert t3.getEndWeek() == 2
    assert t3.getGuide().getEmail() == "john@email.com"
    t3Participants = [p.getEmail() for p in t3.getParticipants()]
    assert t3Participants == ["emily@hotmail.ca"]

    for email in ["alice@gmail.com", "new@hotmail.ca", "charlie@hotmail.ca", "john@hotmail.ca", "emily@hotmail.ca"]:
        p = next((p for p in btp.getParticipants() if p.getEmail() == email), None)
        assert p.getStatus() == Status.Assigned


def testInitiatePartialAssignmentError(controllerWithInitiate, mw):
    mw(Participant, email="alice@gmail.com", password="pass123", name="Alice Jones", emergencyContact="(200)5551234",
       nrWeeks=3, weekAvailableFrom=1, weekAvailableUntil=3, lodgeRequired=True,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)
    mw(Participant, email="new@hotmail.ca", password="newnew", name="Johnny New", emergencyContact="(200)5559999",
       nrWeeks=7, weekAvailableFrom=4, weekAvailableUntil=10, lodgeRequired=True,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)
    mw(Participant, email="charlie@hotmail.ca", password="charlie", name="Charles Tremblay", emergencyContact="(200)5559876",
       nrWeeks=3, weekAvailableFrom=2, weekAvailableUntil=5, lodgeRequired=False,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)
    mw(Participant, email="john@hotmail.ca", password="john123", name="John Doe", emergencyContact="(200)5551234",
       nrWeeks=5, weekAvailableFrom=1, weekAvailableUntil=10, lodgeRequired=False,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)
    mw(Participant, email="mary@hotmail.ca", password="mary003", name="Mary Blue", emergencyContact="(200)5559988",
       nrWeeks=9, weekAvailableFrom=1, weekAvailableUntil=10, lodgeRequired=True,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)
    mw(Participant, email="emily@hotmail.ca", password="emily007", name="Emily Green", emergencyContact="(200)5559876",
       nrWeeks=2, weekAvailableFrom=1, weekAvailableUntil=5, lodgeRequired=False,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controllerWithInitiate.btp)

    with pytest.raises(ValueError) as error_info:
        controllerWithInitiate.createBikeTours()

    assert str(error_info.value) == "At least one participant could not be assigned to their bike tour"

    btp = mw(controllerWithInitiate.btp)
    assert len(btp.getBikeTours()) == 5

    t1 = next((t for t in btp.getBikeTours() if t.getId() == 1), None)
    assert t1.getStartWeek() == 1
    assert t1.getEndWeek() == 3
    assert t1.getGuide().getEmail() == "jeff@email.com"
    t1Participants = [p.getEmail() for p in t1.getParticipants()]
    assert t1Participants == ["alice@gmail.com"]

    t2 = next((t for t in btp.getBikeTours() if t.getId() == 2), None)
    assert t2.getStartWeek() == 4
    assert t2.getEndWeek() == 10
    assert t2.getGuide().getEmail() == "jeff@email.com"
    t2Participants = [p.getEmail() for p in t2.getParticipants()]
    assert t2Participants == ["new@hotmail.ca"]

    t3 = next((t for t in btp.getBikeTours() if t.getId() == 3), None)
    assert t3.getStartWeek() == 2
    assert t3.getEndWeek() == 4
    assert t3.getGuide().getEmail() == "john@email.com"
    t3Participants = [p.getEmail() for p in t3.getParticipants()]
    assert t3Participants == ["charlie@hotmail.ca"]

    t4 = next((t for t in btp.getBikeTours() if t.getId() == 4), None)
    assert t4.getStartWeek() == 5
    assert t4.getEndWeek() == 9
    assert t4.getGuide().getEmail() == "john@email.com"
    t4_participants = [p.getEmail() for p in t4.getParticipants()]
    assert t4_participants == ["john@hotmail.ca"]

    t5 = next((t for t in btp.getBikeTours() if t.getId() == 5), None)
    assert t5.getStartWeek() == 1
    assert t5.getEndWeek() == 9
    assert t5.getGuide().getEmail() == "bob@email.com"
    t5_participants = [p.getEmail() for p in t5.getParticipants()]
    assert t5_participants == ["mary@hotmail.ca"]

    for email in ["alice@gmail.com", "new@hotmail.ca", "charlie@hotmail.ca", "john@hotmail.ca", "mary@hotmail.ca"]:
        p = next((p for p in btp.getParticipants() if p.getEmail() == email), None)
        assert p.getStatus() == Status.Assigned

    emily = next((p for p in btp.getParticipants() if p.getEmail() == "emily@hotmail.ca"), None)
    assert emily.getStatus() == Status.NotAssigned
