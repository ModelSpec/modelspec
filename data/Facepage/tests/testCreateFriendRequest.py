from datetime import datetime
import pytest


@pytest.fixture
def givenController(modelingTool, mw):
    global User, PersonalAccount, BusinessAccount
    if modelingTool == "umple":
        from ..umple.controller import FacepageController
        from ..umple.generated_model_layer import User, PersonalAccount, BusinessAccount
        User.usersByUserID.clear()
    else:
        from ..ecore.controller import FacepageController
        from ..ecore.generated_model_layer import User, PersonalAccount, BusinessAccount

    controller = FacepageController()
    u1 = mw(User, userID=1, name="John Doe", email="john.doe@mail.com", birthDate=datetime(2000, 1, 1), facepage=controller.facepage)
    u2 = mw(User, userID=2, name="Jane Smith", email="jane.smith@mail.com", birthDate=datetime(2000, 1, 1), facepage=controller.facepage)
    mw(PersonalAccount, accountNumber=1, facepage=controller.facepage, user=u1.model)
    mw(PersonalAccount, accountNumber=2, facepage=controller.facepage, user=u2.model)
    yield controller


def testCreateFriendRequestNewSuccess(givenController, mw):
    givenController.createFriendRequest(1, 2)

    face = mw(givenController.facepage)
    u1 = None
    u2 = None
    for u in face.getUsers():
        if u.getUserID() == 1:
            u1 = u
        if u.getUserID() == 2:
            u2 = u
    assert u1 is not None and u2 is not None

    a1 = u1.getAccount()
    a2 = u2.getAccount()
    assert isinstance(a1, PersonalAccount)
    assert isinstance(a2, PersonalAccount)

    fr_from_sender = None
    for fr in a1.getSenderOf():
        if fr.getSender() == a1 and fr.getReceiver() == a2:
            fr_from_sender = fr
            break
    assert fr_from_sender is not None

    fr_from_receiver = None
    for fr in a2.getReceiverOf():
        if fr.getSender() == a1 and fr.getReceiver() == a2:
            fr_from_receiver = fr
            break
    assert fr_from_receiver is not None

    assert fr_from_sender == fr_from_receiver

    all_friend_requests = set()
    for acc in face.getAccounts():
        if isinstance(acc, PersonalAccount):
            for fr in acc.getSenderOf():
                all_friend_requests.add(fr)
            for fr in acc.getReceiverOf():
                all_friend_requests.add(fr)

    assert len(all_friend_requests) == 1


def testCreateFriendRequestInvalidSenderBusinessAccountFail(givenController, mw):
    u3 = mw(User, userID=3, name="Bob Johnson", email="bob.johnson@mail.com", birthDate=datetime(2000, 1, 1), facepage=givenController.facepage)
    mw(BusinessAccount, accountNumber=3, facepage=givenController.facepage, user=u3.model, companyName="company")

    with pytest.raises(ValueError) as err:
        givenController.createFriendRequest(3, 2)

    assert str(err.value) == "Only personal accounts can send friend requests."

    face = mw(givenController.facepage)
    all_friend_requests = set()
    for acc in face.getAccounts():
        if isinstance(acc, PersonalAccount):
            for fr in acc.getSenderOf():
                all_friend_requests.add(fr)
            for fr in acc.getReceiverOf():
                all_friend_requests.add(fr)

    assert len(all_friend_requests) == 0


def testCreateFriendRequestInvalidReceiverBusinessAccountFail(givenController, mw):
    u3 = mw(User, userID=3, name="Bob Johnson", email="bob.johnson@mail.com", birthDate=datetime(2000, 1, 1), facepage=givenController.facepage)
    mw(BusinessAccount, accountNumber=3, facepage=givenController.facepage, user=u3.model, companyName="company")

    with pytest.raises(ValueError) as err:
        givenController.createFriendRequest(1, 3)

    assert str(err.value) == "Only personal accounts can receive friend requests."

    face = mw(givenController.facepage)
    all_friend_requests = set()
    for acc in face.getAccounts():
        if isinstance(acc, PersonalAccount):
            for fr in acc.getSenderOf():
                all_friend_requests.add(fr)
            for fr in acc.getReceiverOf():
                all_friend_requests.add(fr)

    assert len(all_friend_requests) == 0


@pytest.mark.parametrize("user1ID,user2ID,error", [(1, 1, "Cannot send a friend request to itself."), (1, None, "Cannot create a friend request without a receiver."), (None, 1, "Cannot create a friend request without a sender."),],)
def testCreateFriendRequestInvalidUserFail(givenController, mw, user1ID, user2ID, error):
    with pytest.raises(ValueError) as err:
        givenController.createFriendRequest(user1ID, user2ID)

    assert str(err.value) == error

    face = mw(givenController.facepage)
    all_friend_requests = set()
    for acc in face.getAccounts():
        if isinstance(acc, PersonalAccount):
            for fr in acc.getSenderOf():
                all_friend_requests.add(fr)
            for fr in acc.getReceiverOf():
                all_friend_requests.add(fr)

    assert len(all_friend_requests) == 0
