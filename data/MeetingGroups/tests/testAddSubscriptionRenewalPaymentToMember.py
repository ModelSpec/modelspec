from datetime import datetime

import pytest


@pytest.fixture
def controller(modelingTool, mw):
    global MeetingGroupsController, UserAccess, Administration, Meetings, Payments
    global User, MeetingGroup, MeetingGroupProposal, Meeting, UserRegistration
    global Member, Subscription, SubscriptionPeriod, SubscriptionStatus, SubscriptionRenewalPayment, SubscriptionRenewalPaymentStatus

    if modelingTool == "umple":
        from ..umple.controller import MeetingGroupsController
        from ..umple.generated_model_layer import (
            Administration,
            Meeting,
            MeetingGroup,
            MeetingGroupProposal,
            Meetings,
            Member,
            Payments,
            Subscription,
            SubscriptionRenewalPayment,
            User,
            UserAccess,
            UserRegistration,
        )
        SubscriptionPeriod = Subscription.SubscriptionPeriod
        SubscriptionStatus = Subscription.SubscriptionStatus
        SubscriptionRenewalPaymentStatus = SubscriptionRenewalPayment.SubscriptionRenewalPaymentStatus

        User.usersById.clear()
        MeetingGroup.meetinggroupsById.clear()
        MeetingGroupProposal.nextId = 1
        Meeting.nextId = 1
        UserRegistration.nextId = 1
    else:
        from ..ecore.controller import MeetingGroupsController
        from ..ecore.generated_model_layer import (
            Administration,
            Meeting,
            MeetingGroup,
            MeetingGroupProposal,
            Meetings,
            Member,
            Payments,
            Subscription,
            SubscriptionPeriod,
            SubscriptionRenewalPayment,
            SubscriptionRenewalPaymentStatus,
            SubscriptionStatus,
            User,
            UserAccess,
            UserRegistration,
        )

    c = MeetingGroupsController()
    c.userAccess = mw(UserAccess).model
    c.administration = mw(Administration).model
    c.meetings = mw(Meetings).model
    c.payments = mw(Payments).model

    member1 = mw(Member, id=1, login="user1", email="user1@email.com", firstName="John", lastName="Doe", name="John Doe", userAccess=c.userAccess, meetings=c.meetings)
    mw(Member, id=2, login="user2", email="user2@email.com", firstName="Jane", lastName="Smith", name="Jane Smith", userAccess=c.userAccess, meetings=c.meetings)

    mw(
        Subscription,
        countryCode="ca",
        expirationDate=datetime(2025, 12, 31),
        subscriptionPeriod=SubscriptionPeriod.Month,
        status=SubscriptionStatus.Active,
        subscriber=member1.model,
        payments=c.payments,
    )

    yield c


def testAddRenewalPaymentSuccessfully(controller, mw):
    # Act
    controller.addSubscriptionRenewalPaymentToMember(1, 10.00, 'CAD')

    # Assert
    payments = mw(controller.payments)
    assert payments.numberOfSubscriptionRenewalPayments() == 1
    payment = payments.getSubscriptionRenewalPayment(0)
    assert payment.getPayer().getId() == 1
    assert payment.getCountryCode() == 'ca'
    assert payment.getStatus().name == SubscriptionRenewalPaymentStatus.WaitingForPayment.name
    assert payment.getValue().getValue() == 10.00
    assert payment.getValue().getCurrency() == 'CAD'


def testAddMultipleRenewalPayments(controller, mw):
    # Act
    controller.addSubscriptionRenewalPaymentToMember(1, 10.00, 'CAD')
    controller.addSubscriptionRenewalPaymentToMember(1, 20.00, 'CAD')

    # Assert
    payments = mw(controller.payments)
    assert payments.numberOfSubscriptionRenewalPayments() == 2
    payment1 = next(p for p in payments.getSubscriptionRenewalPayments()
                    if p.getValue().getValue() == 10.00)
    assert payment1.getPayer().getId() == 1
    assert payment1.getCountryCode() == 'ca'
    assert payment1.getStatus().name == SubscriptionRenewalPaymentStatus.WaitingForPayment.name
    assert payment1.getValue().getCurrency() == 'CAD'
    payment2 = next(p for p in payments.getSubscriptionRenewalPayments()
                    if p.getValue().getValue() == 20.00)
    assert payment2.getPayer().getId() == 1
    assert payment2.getCountryCode() == 'ca'
    assert payment2.getStatus().name == SubscriptionRenewalPaymentStatus.WaitingForPayment.name
    assert payment2.getValue().getCurrency() == 'CAD'


def testAddRenewalPaymentNoSubscription(controller, mw):
    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.addSubscriptionRenewalPaymentToMember(2, 10.00, 'CAD')

    # Assert
    assert str(excInfo.value) == 'Member does not have a subscription.'
    assert mw(controller.payments).numberOfSubscriptionRenewalPayments() == 0


def testAddRenewalPaymentNonexistentMember(controller, mw):
    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.addSubscriptionRenewalPaymentToMember(999, 10.00, 'CAD')

    # Assert
    assert str(excInfo.value) == 'Member does not exist.'
    assert mw(controller.payments).numberOfSubscriptionRenewalPayments() == 0


def testAddRenewalPaymentExpiredSubscription(controller, mw):
    meetings = mw(controller.meetings)
    member2 = next(m for m in meetings.getMembers() if m.getId() == 2)
    mw(
        Subscription,
        countryCode="ca",
        expirationDate=datetime(2025, 10, 30),
        subscriptionPeriod=SubscriptionPeriod.Month,
        status=SubscriptionStatus.Expired,
        subscriber=member2.model,
        payments=controller.payments,
    )

    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.addSubscriptionRenewalPaymentToMember(2, 10.00, 'CAD')

    # Assert
    assert str(excInfo.value) == 'Member does not have an active subscription.'
    assert mw(controller.payments).numberOfSubscriptionRenewalPayments() == 0


@pytest.mark.parametrize("value,currency,errorMessage", [
    (-10.00, 'CAD', 'The value must be positive.'),
    (0.00, 'CAD', 'The value must be positive.'),
    (10.00, '', 'The currency must not be empty.'),
])
def testAddRenewalPaymentInvalidValues(controller, mw, value, currency, errorMessage):
    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.addSubscriptionRenewalPaymentToMember(1, value, currency)

    # Assert
    assert str(excInfo.value) == errorMessage
    assert mw(controller.payments).numberOfSubscriptionRenewalPayments() == 0


