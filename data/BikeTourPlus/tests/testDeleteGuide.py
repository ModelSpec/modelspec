import pytest
from datetime import datetime


@pytest.fixture
def controllerWithGuides(modelingTool, mw):
    if modelingTool == "umple":
        from ..umple.controller import BikeTourPlusController
        from ..umple.generated_model_layer import User, Guide, Participant, Manager
        if hasattr(User, "usersByEmail"):
            User.usersByEmail.clear()
    else:
        from ..ecore.controller import BikeTourPlusController
        from ..ecore.generated_model_layer import Guide, Participant, Manager

    controller = BikeTourPlusController()
    btp = mw(controller.btp)
    btp.setStartDate(datetime(2023, 3, 13))
    btp.setNrWeeks(10)
    btp.setPriceOfGuidePerWeek(100)

    mw(Manager, email="manager@btp.com", password="password", bikeTourPlus=controller.btp)
    mw(Guide, email="jeff@email.com", password="pass1", name="Jeff", emergencyContact="(555)555-5555", bikeTourPlus=controller.btp)
    mw(Guide, email="john@email.com", password="pass2", name="John", emergencyContact="(444)444-4444", bikeTourPlus=controller.btp)
    mw(Participant, email="peter@email.com", password="pass1", name="Peter", emergencyContact="(666)555-5555",
       nrWeeks=1, weekAvailableFrom=1, weekAvailableUntil=2, lodgeRequired=True,
       authorizationCode="None", refundedPercentageAmount=0, bikeTourPlus=controller.btp)
    mw(Participant, email="tyler@email.com", password="pass2", name="Tyler", emergencyContact="(777)444-4444",
       nrWeeks=2, weekAvailableFrom=2, weekAvailableUntil=5, lodgeRequired=False,
       authorizationCode="None", refundedPercentageAmount=0, bikeTourPlus=controller.btp)

    yield controller


@pytest.mark.parametrize("email, numberOfGuides", [
    ("jeff@email.com", 1),
    ("john@email.com", 1),
    ("kyle@email.com", 2),
    ("paul@email.com", 2),
])
def testDeleteGuideSuccess(controllerWithGuides, mw, email, numberOfGuides):
    controllerWithGuides.deleteGuide(email)

    btp = mw(controllerWithGuides.btp)
    assert not any(g.getEmail() == email for g in btp.getGuides())
    assert len(btp.getGuides()) == numberOfGuides


@pytest.mark.parametrize("email", [
    ("peter@email.com"),
    ("tyler@email.com"),
])
def testDeleteNonExistingGuideParticipantExists(controllerWithGuides, mw, email):
    controllerWithGuides.deleteGuide(email)

    btp = mw(controllerWithGuides.btp)
    assert any(p.getEmail() == email for p in btp.getParticipants())
    assert len(btp.getGuides()) == 2
    assert len(btp.getParticipants()) == 2


def testDeleteNonExistingGuideManagerExists(controllerWithGuides, mw):
    managerEmail = "manager@btp.com"
    controllerWithGuides.deleteGuide(managerEmail)

    btp = mw(controllerWithGuides.btp)
    assert btp.getManager() is not None
    assert btp.getManager().getEmail() == managerEmail
    assert len(btp.getGuides()) == 2
