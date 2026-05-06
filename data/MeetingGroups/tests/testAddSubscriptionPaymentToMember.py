from datetime import datetime

import pytest
from freezegun import freeze_time


@pytest.fixture
def controller(modelingTool, mw):
    global MeetingGroupsController, UserAccess, Administration, Meetings, Payments
    global User, MeetingGroup, MeetingGroupProposal, Meeting, UserRegistration
    global Member, Subscription, SubscriptionPeriod, SubscriptionStatus, SubscriptionPayment, SubscriptionPaymentStatus

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
            SubscriptionPayment,
            User,
            UserAccess,
            UserRegistration,
        )
        SubscriptionPeriod = Subscription.SubscriptionPeriod
        SubscriptionStatus = Subscription.SubscriptionStatus
        SubscriptionPaymentStatus = SubscriptionPayment.SubscriptionPaymentStatus

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
            SubscriptionPayment,
            SubscriptionPaymentStatus,
            SubscriptionPeriod,
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

    mw(Member, id=1, login="user1", email="user1@email.com", firstName="John", lastName="Doe", name="John Doe", userAccess=c.userAccess, meetings=c.meetings)
    mw(Member, id=2, login="user2", email="user2@email.com", firstName="Jane", lastName="Smith", name="Jane Smith", userAccess=c.userAccess, meetings=c.meetings)

    yield c


@freeze_time("2025-12-01")
def testAddSubscriptionPaymentMonth(controller, mw):
    # Act
    controller.addSubscriptionPaymentToMember(1, 10.00, 'CAD', 'Month')

    # Assert
    payments = mw(controller.payments)
    assert payments.numberOfSubscriptionPayments() == 1
    payment = payments.getSubscriptionPayment(0)
    assert payment.getPayer().getId() == 1
    assert payment.getCountryCode() == 'ca'
    assert payment.getSubscriptionPeriod().name == SubscriptionPeriod.Month.name
    assert payment.getStatus().name == SubscriptionPaymentStatus.WaitingForPayment.name
    assert payment.getValue().getValue() == 10.00
    assert payment.getValue().getCurrency() == 'CAD'
    assert payments.numberOfSubscriptions() == 1
    subscription = payments.getSubscription(0)
    assert subscription.getSubscriber().getId() == 1
    assert subscription.getCountryCode() == 'ca'
    assert subscription.getExpirationDate().year == datetime(2025, 12, 31).year
    assert subscription.getExpirationDate().month == datetime(2025, 12, 31).month
    assert subscription.getExpirationDate().day == datetime(2025, 12, 31).day
    assert subscription.getSubscriptionPeriod().name == SubscriptionPeriod.Month.name
    assert subscription.getStatus().name == SubscriptionStatus.Active.name


@freeze_time("2025-12-01")
def testAddSubscriptionPaymentSixMonths(controller, mw):
    # Act
    controller.addSubscriptionPaymentToMember(1, 50.00, 'CAD', 'HalfYear')

    # Assert
    payments = mw(controller.payments)
    assert payments.numberOfSubscriptionPayments() == 1
    payment = payments.getSubscriptionPayment(0)
    assert payment.getPayer().getId() == 1
    assert payment.getCountryCode() == 'ca'
    assert payment.getSubscriptionPeriod().name == SubscriptionPeriod.HalfYear.name
    assert payment.getStatus().name == SubscriptionPaymentStatus.WaitingForPayment.name
    assert payment.getValue().getValue() == 50.00
    assert payment.getValue().getCurrency() == 'CAD'
    assert payments.numberOfSubscriptions() == 1
    subscription = payments.getSubscription(0)
    assert subscription.getSubscriber().getId() == 1
    assert subscription.getCountryCode() == 'ca'
    assert subscription.getExpirationDate().year == datetime(2026, 5, 31).year
    assert subscription.getExpirationDate().month == datetime(2026, 5, 31).month
    assert subscription.getExpirationDate().day == datetime(2026, 5, 31).day
    assert subscription.getSubscriptionPeriod().name == SubscriptionPeriod.HalfYear.name
    assert subscription.getStatus().name == SubscriptionStatus.Active.name


def testAddSubscriptionPaymentExistingSubscription(controller, mw):
    meetings = mw(controller.meetings)
    member1 = next(m for m in meetings.getMembers() if m.getId() == 1)
    mw(
        Subscription,
        countryCode="ca",
        expirationDate=datetime(2025, 12, 31),
        subscriptionPeriod=SubscriptionPeriod.Month,
        status=SubscriptionStatus.Active,
        subscriber=member1.model,
        payments=controller.payments,
    )

    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.addSubscriptionPaymentToMember(1, 10.00, 'CAD', 'Month')

    # Assert
    assert str(excInfo.value) == 'Member already has a subscription.'
    assert mw(controller.payments).numberOfSubscriptionPayments() == 0


def testAddSubscriptionPaymentNonexistentMember(controller, mw):
    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.addSubscriptionPaymentToMember(999, 10.00, 'CAD', 'Month')

    # Assert
    assert str(excInfo.value) == 'Member does not exist.'
    assert mw(controller.payments).numberOfSubscriptionPayments() == 0


def testAddSubscriptionPaymentExpiredSubscription(controller, mw):
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
        controller.addSubscriptionPaymentToMember(2, 10.00, 'CAD', 'Month')

    # Assert
    assert str(excInfo.value) == 'Member already has a subscription.'
    assert mw(controller.payments).numberOfSubscriptionPayments() == 0


@pytest.mark.parametrize("value,currency,period,errorMessage", [
    (-10.00, 'CAD', 'Month', 'The value must be positive.'),
    (0.00, 'CAD', 'Month', 'The value must be positive.'),
    (10.00, '', 'Month', 'The currency must not be empty.'),
    (10.00, 'CAD', '', 'The subscriptionPeriod must not be empty.'),
])
def testAddSubscriptionPaymentInvalidValues(controller, value, currency, period, errorMessage):
    # Act
    with pytest.raises(ValueError) as excInfo:
        controller.addSubscriptionPaymentToMember(1, value, currency, period)

    # Assert
    assert str(excInfo.value) == errorMessage


