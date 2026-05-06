import pytest
from datetime import datetime


@pytest.fixture
def controllerWithGuide(modelingTool, mw):
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


@pytest.mark.parametrize("email, password, name, emergencyContact", [
    ("lisa@email.com", "pass1", "Lisa", "(666)666-6666"),
    ("liam@email.com", "pass2", "Liam", "(777)777-7777"),
])
def testRegisterGuideSuccess(controllerWithGuide, mw, email, password, name, emergencyContact):
    controllerWithGuide.registerGuide(email, password, name, emergencyContact)

    btp = mw(controllerWithGuide.btp)
    guide = next((g for g in btp.getGuides() if g.getEmail() == email), None)
    assert guide is not None
    assert guide.getPassword() == password
    assert guide.getName() == name
    assert guide.getEmergencyContact() == emergencyContact
    assert len(btp.getGuides()) == 3


@pytest.mark.parametrize("email, password, name, emergencyContact, error", [
    ("manager@btp.com", "pass1", "Paul", "(111)111-1111", "Email cannot be manager@btp.com"),
    ("jeff@email.com", "pass2", "Jeff", "(111)777-7777", "Email already linked to a guide account"),
    ("peter@email.com", "pass3", "Peter", "(555)555-5555", "Email already linked to a participant account"),
    ("bart @ email.com", "pass3", "Bart", "(444)666-6666", "Email must not contain any spaces"),
    ("don@email@y.com", "pass4", "Dony", "(777)555-7777", "Invalid email"),
    ("kyle@email.", "pass5", "Kyle", "(666)777-6666", "Invalid email"),
    ("greg.email@com", "pass6", "Greg", "(777)888-7777", "Invalid email"),
    ("@email.com", "pass7", "Otto", "(111)777-6666", "Invalid email"),
    ("karl@.com", "pass8", "Karl", "(111)777-6661", "Invalid email"),
    ("", "pass9", "Vino", "(777)888-5555", "Email cannot be empty"),
    ("luke@email.com", "", "Luke", "(999)888-5555", "Password cannot be empty"),
    ("owen@email.com", "pass10", "", "(888)888-5555", "Name cannot be empty"),
    ("noah@email.com", "pass11", "Noah", "", "Emergency contact cannot be empty"),
])
def testRegisterGuideFailure(controllerWithGuide, mw, email, password, name, emergencyContact, error):
    with pytest.raises(ValueError) as excInfo:
        controllerWithGuide.registerGuide(email, password, name, emergencyContact)

    assert str(excInfo.value) == error
    assert len(mw(controllerWithGuide.btp).getGuides()) == 2
