from datetime import datetime
import pytest
from freezegun import freeze_time

@pytest.fixture
def givenController(modelingTool, mw):
    with freeze_time("2020-01-01"):
        if modelingTool == "umple":
            from ..umple.controller import HomeForTheElderlyController
            from ..umple.generated_model_layer import Person, Invoice
            Person.personsById.clear()
        else:
            from ..ecore.controller import HomeForTheElderlyController
            from ..ecore.generated_model_layer import Person, Invoice

        controller = HomeForTheElderlyController()

        person = mw(Person, id="person", name="John Doe", birthdate=datetime(1950, 1, 1), homeForTheElderly = controller.homeForTheElderly)
        person.setRegistrationDate(datetime.today())
        person.setAbilities("requires wheelchair")

        mw(Invoice, invoiceDate=datetime.now(), outstandingAmount=1000.0, status="active", person=person.model)

        yield controller

def testUpdateInvoiceOutstandingAmount(givenController, mw):
    # Act
    givenController.updateInvoice("person", datetime(2020, 1, 1), 500.0)

    # Assert
    updatedInvoice = None
    person = None
    for p in mw(givenController.homeForTheElderly).getPeople():
        if p.getId() == "person":
            person = p
    for inv in person.getInvoices():
        if inv.getInvoiceDate().date() == datetime(2020, 1, 1).date():
            updatedInvoice = inv
            break
    assert updatedInvoice is not None
    assert updatedInvoice.getOutstandingAmount() == 500.0
    assert updatedInvoice.getStatus() == "active"

@pytest.mark.parametrize(
    "amount",
    [
        0.,
        -1.,
    ],
)
def testUpdateInvoiceToZeroOrLess(givenController, amount, mw):
    # Act
    givenController.updateInvoice("person", datetime(2020, 1, 1), amount)

    # Assert
    updatedInvoice = None
    person = None
    for p in mw(givenController.homeForTheElderly).getPeople():
        if p.getId() == "person":
            person = p
    for inv in person.getInvoices():
        if inv.getInvoiceDate().date() == datetime(2020, 1, 1).date():
            updatedInvoice = inv
            break
    assert updatedInvoice is not None
    assert updatedInvoice.getOutstandingAmount() == amount
    assert updatedInvoice.getStatus() == "paid"

def testUpdateInvoiceWhenStatusIsPaid(givenController, mw):
    # Arrange
    person = None
    for p in mw(givenController.homeForTheElderly).getPeople():
        if p.getId() == "person":
            person = p
    invoice = None
    for inv in person.getInvoices():
        if inv.getInvoiceDate().date() == datetime(2020, 1, 1).date():
            invoice = inv
            break
    invoice.setOutstandingAmount(0.0)
    invoice.setStatus("paid")

    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.updateInvoice("person", datetime(2020, 1, 1), 500.0)

    # Assert
    assert str(errorInfo.value) == "Cannot update paid invoice."
    updatedInvoice = None
    for inv in person.getInvoices():
        if inv.getInvoiceDate().date() == datetime(2020, 1, 1).date():
            updatedInvoice = inv
            break
    assert updatedInvoice is not None
    assert updatedInvoice.getOutstandingAmount() == 0.0
    assert updatedInvoice.getStatus() == "paid"

def testUpdateInvoiceThatDoesNotExist(givenController):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        givenController.updateInvoice("person", datetime(2020, 1, 2), 500.0)

    # Assert
    assert str(errorInfo.value) == f'Invoice for person "person" with invoiceDate "{datetime(2020, 1, 2).date()}" does not exist.'