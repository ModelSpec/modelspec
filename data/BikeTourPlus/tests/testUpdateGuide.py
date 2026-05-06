import pytest
from datetime import datetime


@pytest.fixture
def controllerWithGuide(modelingTool, mw):
    if modelingTool == "umple":
        from ..umple.controller import BikeTourPlusController
        from ..umple.generated_model_layer import User, Guide, Participant
        if hasattr(User, "usersByEmail"):
            User.usersByEmail.clear()
    else:
        from ..ecore.controller import BikeTourPlusController
        from ..ecore.generated_model_layer import Guide, Participant

    controller = BikeTourPlusController()
    btp = mw(controller.btp)
    btp.setStartDate(datetime(2023, 3, 13))
    btp.setNrWeeks(10)
    btp.setPriceOfGuidePerWeek(100)

    mw(Guide, email="jeff@email.com", password="pass1", name="Jeff", emergencyContact="(555)555-5555", bikeTourPlus=controller.btp)
    mw(Guide, email="john@email.com", password="pass2", name="John", emergencyContact="(444)444-4444", bikeTourPlus=controller.btp)
    mw(Participant, email="peter@email.com", password="pass1", name="Peter", emergencyContact="(666)555-5555",
       nrWeeks=1, weekAvailableFrom=1, weekAvailableUntil=2, lodgeRequired=True,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controller.btp)
    mw(Participant, email="tyler@email.com", password="pass2", name="Tyler", emergencyContact="(777)444-4444",
       nrWeeks=2, weekAvailableFrom=2, weekAvailableUntil=5, lodgeRequired=False,
       authorizationCode="", refundedPercentageAmount=0, bikeTourPlus=controller.btp)

    yield controller


@pytest.mark.parametrize("email, password, name, emergencyContact, newPassword, newName, newEmergencyContact", [
    ("jeff@email.com", "pass1", "Jeff", "(555)555-5555", "pass5", "Jake", "(111)111-1111"),
    ("john@email.com", "pass2", "John", "(444)444-4444", "pass6", "Johnny", "(111)777-7777"),
])
def testUpdateGuideSuccess(controllerWithGuide, mw, email, password, name, emergencyContact, newPassword, newName, newEmergencyContact):
    controllerWithGuide.updateGuide(email, newPassword, newName, newEmergencyContact)

    btp = mw(controllerWithGuide.btp)
    guide = next((g for g in btp.getGuides() if g.getEmail() == email), None)
    assert guide is not None
    assert guide.getPassword() == newPassword
    assert guide.getName() == newName
    assert guide.getEmergencyContact() == newEmergencyContact

    assert len(btp.getGuides()) == 2


@pytest.mark.parametrize("email, password, name, emergencyContact, newPassword, newName, newEmergencyContact, error", [
    ("jeff@email.com", "pass1", "Jeff", "(555)555-5555", "", "Jeff", "(555)666-5555", "Password cannot be empty"),
    ("john@email.com", "pass2", "John", "(444)444-4444", "pass2", "", "(444)444-7777", "Name cannot be empty"),
    ("john@email.com", "pass2", "John", "(444)444-4444", "pass2", "John", "", "Emergency contact cannot be empty"),
])
def testUpdateGuideUnsuccessful(controllerWithGuide, mw, email, password, name, emergencyContact, newPassword, newName, newEmergencyContact, error):
    with pytest.raises(ValueError) as error_info:
        controllerWithGuide.updateGuide(email, newPassword, newName, newEmergencyContact)

    assert str(error_info.value) == error

    btp = mw(controllerWithGuide.btp)
    guide = next((g for g in btp.getGuides() if g.getEmail() == email), None)
    assert guide is not None
    assert guide.getPassword() == password
    assert guide.getName() == name
    assert guide.getEmergencyContact() == emergencyContact

    assert len(btp.getGuides()) == 2


@pytest.mark.parametrize("email, password, name, emergencyContact, newPassword, newName, newEmergencyContact, error", [
    ("jane@email.com", "pass1", "Jane", "(333)333-3333", "pass2", "Jeff", "(555)666-4444", "The guide account does not exist"),
])
def testUpdateGuideNonExistent(controllerWithGuide, mw, email, password, name, emergencyContact, newPassword, newName, newEmergencyContact, error):
    with pytest.raises(ValueError) as error_info:
        controllerWithGuide.updateGuide(email, newPassword, newName, newEmergencyContact)

    assert str(error_info.value) == error

    btp = mw(controllerWithGuide.btp)
    guide = next((g for g in btp.getGuides() if g.getEmail() == email), None)
    assert guide is None

    assert len(btp.getGuides()) == 2
