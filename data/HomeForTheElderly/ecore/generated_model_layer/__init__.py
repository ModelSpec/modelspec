
from .homeForTheElderly import getEClassifier, eClassifiers
from .homeForTheElderly import name, nsURI, nsPrefix, eClass
from .homeForTheElderly import HomeForTheElderly, Department, Category, Room, Bed, Proposal, Stay, Person, Invoice, InvoiceItem, InvoiceLine


from . import homeForTheElderly

__all__ = ['HomeForTheElderly', 'Department', 'Category', 'Room', 'Bed',
           'Proposal', 'Stay', 'Person', 'Invoice', 'InvoiceItem', 'InvoiceLine']

eSubpackages = []
eSuperPackage = None
homeForTheElderly.eSubpackages = eSubpackages
homeForTheElderly.eSuperPackage = eSuperPackage

HomeForTheElderly.departments.eType = Department
HomeForTheElderly.people.eType = Person
Department.rooms.eType = Room
Department.homeForTheElderly.eType = HomeForTheElderly
Department.homeForTheElderly.eOpposite = HomeForTheElderly.departments
Category.rooms.eType = Room
Room.beds.eType = Bed
Room.department.eType = Department
Room.department.eOpposite = Department.rooms
Room.category.eType = Category
Room.category.eOpposite = Category.rooms
Bed.person.eType = Person
Bed.staies.eType = Stay
Bed.room.eType = Room
Bed.room.eOpposite = Room.beds
Bed.proposals.eType = Proposal
Proposal.bed.eType = Bed
Proposal.bed.eOpposite = Bed.proposals
Proposal.person.eType = Person
Stay.person.eType = Person
Stay.bed.eType = Bed
Stay.bed.eOpposite = Bed.staies
Stay.invoiceItems.eType = InvoiceItem
Person.staies.eType = Stay
Person.staies.eOpposite = Stay.person
Person.invoices.eType = Invoice
Person.bed.eType = Bed
Person.bed.eOpposite = Bed.person
Person.proposals.eType = Proposal
Person.proposals.eOpposite = Proposal.person
Person.homeForTheElderly.eType = HomeForTheElderly
Person.homeForTheElderly.eOpposite = HomeForTheElderly.people
Invoice.person.eType = Person
Invoice.person.eOpposite = Person.invoices
Invoice.invoiceLines.eType = InvoiceLine
InvoiceItem.invoiceLine.eType = InvoiceLine
InvoiceItem.stay.eType = Stay
InvoiceItem.stay.eOpposite = Stay.invoiceItems
InvoiceLine.invoice.eType = Invoice
InvoiceLine.invoice.eOpposite = Invoice.invoiceLines
InvoiceLine.invoiceItem.eType = InvoiceItem
InvoiceLine.invoiceItem.eOpposite = InvoiceItem.invoiceLine
HomeForTheElderly.departments.eOpposite = Department.homeForTheElderly
HomeForTheElderly.people.eOpposite = Person.homeForTheElderly

Department.rooms.eOpposite = Room.department
Bed.person.eOpposite = Person.bed
Bed.staies.eOpposite = Stay.bed
Proposal.person.eOpposite = Person.proposals
InvoiceItem.invoiceLine.eOpposite = InvoiceLine.invoiceItem

Room.beds.eOpposite = Bed.room
Bed.room.eOpposite = Room.beds
Department.rooms.eOpposite = Room.department
Room.department.eOpposite = Department.rooms
HomeForTheElderly.departments.eOpposite = Department.homeForTheElderly
Department.homeForTheElderly.eOpposite = HomeForTheElderly.departments
Person.bed.eOpposite = Bed.person
Bed.person.eOpposite = Person.bed
Person.staies.eOpposite = Stay.person
Stay.person.eOpposite = Person.staies
Bed.staies.eOpposite = Stay.bed
Stay.bed.eOpposite = Bed.staies
Person.proposals.eOpposite = Proposal.person
Proposal.person.eOpposite = Person.proposals
Bed.proposals.eOpposite = Proposal.bed
Proposal.bed.eOpposite = Bed.proposals
Category.rooms.eOpposite = Room.category
Room.category.eOpposite = Category.rooms
HomeForTheElderly.people.eOpposite = Person.homeForTheElderly
Person.homeForTheElderly.eOpposite = HomeForTheElderly.people
Person.invoices.eOpposite = Invoice.person
Invoice.person.eOpposite = Person.invoices
Invoice.invoiceLines.eOpposite = InvoiceLine.invoice
InvoiceLine.invoice.eOpposite = Invoice.invoiceLines
InvoiceLine.invoiceItem.eOpposite = InvoiceItem.invoiceLine
InvoiceItem.invoiceLine.eOpposite = InvoiceLine.invoiceItem
Stay.invoiceItems.eOpposite = InvoiceItem.stay
InvoiceItem.stay.eOpposite = Stay.invoiceItems

otherClassifiers = []

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
