"""Definition of meta model 'localLoop'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'localLoop'
nsURI = 'localLoop'
nsPrefix = ''

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)


class Event(EObject, metaclass=MetaEClass):

    eventId = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    organizerId = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    description = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    categoryId = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    fee = EAttribute(eType=EDouble, unique=True, derived=False, changeable=True)
    eventStart = EAttribute(eType=ELong, unique=True, derived=False, changeable=True)
    eventEnd = EAttribute(eType=ELong, unique=True, derived=False, changeable=True)
    capacity = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    category = EReference(ordered=True, unique=True, containment=False, derived=False)
    registrations = EReference(ordered=True, unique=True,
                               containment=False, derived=False, upper=-1)
    organizer = EReference(ordered=True, unique=True, containment=False, derived=False)
    eventRepository = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, eventId=None, organizerId=None, name=None, description=None, categoryId=None, fee=None, eventStart=None, eventEnd=None, capacity=None, category=None, registrations=None, organizer=None, eventRepository=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if eventId is not None:
            self.eventId = eventId

        if organizerId is not None:
            self.organizerId = organizerId

        if name is not None:
            self.name = name

        if description is not None:
            self.description = description

        if categoryId is not None:
            self.categoryId = categoryId

        if fee is not None:
            self.fee = fee

        if eventStart is not None:
            self.eventStart = eventStart

        if eventEnd is not None:
            self.eventEnd = eventEnd

        if capacity is not None:
            self.capacity = capacity

        if category is not None:
            self.category = category

        if registrations:
            self.registrations.extend(registrations)

        if organizer is not None:
            self.organizer = organizer

        if eventRepository is not None:
            self.eventRepository = eventRepository


class Category(EObject, metaclass=MetaEClass):

    categoryId = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    description = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    events = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    categoryViewModel = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, categoryId=None, name=None, description=None, events=None, categoryViewModel=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if categoryId is not None:
            self.categoryId = categoryId

        if name is not None:
            self.name = name

        if description is not None:
            self.description = description

        if events:
            self.events.extend(events)

        if categoryViewModel is not None:
            self.categoryViewModel = categoryViewModel


class Registration(EObject, metaclass=MetaEClass):

    registrationId = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    eventId = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    participantId = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    organizerId = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    status = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    timestamp = EAttribute(eType=ELong, unique=True, derived=False, changeable=True)
    event = EReference(ordered=True, unique=True, containment=False, derived=False)
    participant = EReference(ordered=True, unique=True, containment=False, derived=False)
    registrationRepository = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, registrationId=None, eventId=None, participantId=None, organizerId=None, status=None, timestamp=None, event=None, participant=None, registrationRepository=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if registrationId is not None:
            self.registrationId = registrationId

        if eventId is not None:
            self.eventId = eventId

        if participantId is not None:
            self.participantId = participantId

        if organizerId is not None:
            self.organizerId = organizerId

        if status is not None:
            self.status = status

        if timestamp is not None:
            self.timestamp = timestamp

        if event is not None:
            self.event = event

        if participant is not None:
            self.participant = participant

        if registrationRepository is not None:
            self.registrationRepository = registrationRepository


class RegistrationForm(EObject, metaclass=MetaEClass):

    firstName = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    lastName = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    username = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    email = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    phone = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    password = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    confirmPassword = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    isOrganizer = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)
    companyName = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    createAccountActivity = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, firstName=None, lastName=None, username=None, email=None, phone=None, password=None, confirmPassword=None, isOrganizer=None, companyName=None, createAccountActivity=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if firstName is not None:
            self.firstName = firstName

        if lastName is not None:
            self.lastName = lastName

        if username is not None:
            self.username = username

        if email is not None:
            self.email = email

        if phone is not None:
            self.phone = phone

        if password is not None:
            self.password = password

        if confirmPassword is not None:
            self.confirmPassword = confirmPassword

        if isOrganizer is not None:
            self.isOrganizer = isOrganizer

        if companyName is not None:
            self.companyName = companyName

        if createAccountActivity is not None:
            self.createAccountActivity = createAccountActivity


class UserAccount(EObject, metaclass=MetaEClass):

    userID = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    firstName = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    lastName = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    username = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    email = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    phoneNumber = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    role = EReference(ordered=True, unique=True, containment=False, derived=False)
    adminViewModel = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, userID=None, firstName=None, lastName=None, username=None, email=None, phoneNumber=None, role=None, adminViewModel=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if userID is not None:
            self.userID = userID

        if firstName is not None:
            self.firstName = firstName

        if lastName is not None:
            self.lastName = lastName

        if username is not None:
            self.username = username

        if email is not None:
            self.email = email

        if phoneNumber is not None:
            self.phoneNumber = phoneNumber

        if role is not None:
            self.role = role

        if adminViewModel is not None:
            self.adminViewModel = adminViewModel


@abstract
class Role(EObject, metaclass=MetaEClass):

    def __init__(self):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class EventRepository(EObject, metaclass=MetaEClass):

    events = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    organizerViewModel = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, events=None, organizerViewModel=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if events:
            self.events.extend(events)

        if organizerViewModel is not None:
            self.organizerViewModel = organizerViewModel


class RegistrationRepository(EObject, metaclass=MetaEClass):

    registrations = EReference(ordered=True, unique=True,
                               containment=False, derived=False, upper=-1)
    registrationViewModel = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, registrations=None, registrationViewModel=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if registrations:
            self.registrations.extend(registrations)

        if registrationViewModel is not None:
            self.registrationViewModel = registrationViewModel


class AdminViewModel(EObject, metaclass=MetaEClass):

    userAccounts = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    adminDashboardActivity = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, userAccounts=None, adminDashboardActivity=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if userAccounts:
            self.userAccounts.extend(userAccounts)

        if adminDashboardActivity is not None:
            self.adminDashboardActivity = adminDashboardActivity


class OrganizerViewModel(EObject, metaclass=MetaEClass):

    eventRepo = EReference(ordered=True, unique=True, containment=False, derived=False)
    eventRepository = EReference(ordered=True, unique=True, containment=False, derived=False)
    organizerDashboardActivity = EReference(
        ordered=True, unique=True, containment=False, derived=False)
    manageEventActivity = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, eventRepo=None, eventRepository=None, organizerDashboardActivity=None, manageEventActivity=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if eventRepo is not None:
            self.eventRepo = eventRepo

        if eventRepository is not None:
            self.eventRepository = eventRepository

        if organizerDashboardActivity is not None:
            self.organizerDashboardActivity = organizerDashboardActivity

        if manageEventActivity is not None:
            self.manageEventActivity = manageEventActivity


class RegistrationViewModel(EObject, metaclass=MetaEClass):

    pendingRegistrations = EReference(ordered=True, unique=True,
                                      containment=False, derived=False, upper=-1)
    repository = EReference(ordered=True, unique=True, containment=False, derived=False)
    organizerDashboardActivity = EReference(
        ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, pendingRegistrations=None, repository=None, organizerDashboardActivity=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if pendingRegistrations:
            self.pendingRegistrations.extend(pendingRegistrations)

        if repository is not None:
            self.repository = repository

        if organizerDashboardActivity is not None:
            self.organizerDashboardActivity = organizerDashboardActivity


class ParticipantViewModel(EObject, metaclass=MetaEClass):

    participantDashboardActivity = EReference(
        ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, participantDashboardActivity=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if participantDashboardActivity is not None:
            self.participantDashboardActivity = participantDashboardActivity


class CategoryViewModel(EObject, metaclass=MetaEClass):

    categories = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    manageCategoriesActivity = EReference(
        ordered=True, unique=True, containment=False, derived=False)
    manageEventActivity = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, categories=None, manageCategoriesActivity=None, manageEventActivity=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if categories:
            self.categories.extend(categories)

        if manageCategoriesActivity is not None:
            self.manageCategoriesActivity = manageCategoriesActivity

        if manageEventActivity is not None:
            self.manageEventActivity = manageEventActivity


class LoginService(EObject, metaclass=MetaEClass):

    loginActivity = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, loginActivity=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if loginActivity is not None:
            self.loginActivity = loginActivity


class AppCompatActivity(EObject, metaclass=MetaEClass):

    def __init__(self):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class Admin(Role):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)


class Organizer(Role):

    companyName = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    events = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)

    def __init__(self, *, companyName=None, events=None, **kwargs):

        super().__init__(**kwargs)

        if companyName is not None:
            self.companyName = companyName

        if events:
            self.events.extend(events)


class Participant(Role):

    registrations = EReference(ordered=True, unique=True,
                               containment=False, derived=False, upper=-1)

    def __init__(self, *, registrations=None, **kwargs):

        super().__init__(**kwargs)

        if registrations:
            self.registrations.extend(registrations)


class AdminDashboardActivity(AppCompatActivity):

    adminViewModel = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, adminViewModel=None, **kwargs):

        super().__init__(**kwargs)

        if adminViewModel is not None:
            self.adminViewModel = adminViewModel


class OrganizerDashboardActivity(AppCompatActivity):

    organizerViewModel = EReference(ordered=True, unique=True, containment=False, derived=False)
    registrationViewModel = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, organizerViewModel=None, registrationViewModel=None, **kwargs):

        super().__init__(**kwargs)

        if organizerViewModel is not None:
            self.organizerViewModel = organizerViewModel

        if registrationViewModel is not None:
            self.registrationViewModel = registrationViewModel


class ParticipantDashboardActivity(AppCompatActivity):

    participantViewModel = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, participantViewModel=None, **kwargs):

        super().__init__(**kwargs)

        if participantViewModel is not None:
            self.participantViewModel = participantViewModel


class ManageCategoriesActivity(AppCompatActivity):

    categoryViewModel = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, categoryViewModel=None, **kwargs):

        super().__init__(**kwargs)

        if categoryViewModel is not None:
            self.categoryViewModel = categoryViewModel


class ManageEventActivity(AppCompatActivity):

    isEditMode = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)
    organizerId = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    selectedCategoryId = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    eventToEdit = EReference(ordered=True, unique=True, containment=False, derived=False)
    categoryList = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    organizerViewModel = EReference(ordered=True, unique=True, containment=False, derived=False)
    categoryViewModel = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, isEditMode=None, organizerId=None, selectedCategoryId=None, eventToEdit=None, categoryList=None, organizerViewModel=None, categoryViewModel=None, **kwargs):

        super().__init__(**kwargs)

        if isEditMode is not None:
            self.isEditMode = isEditMode

        if organizerId is not None:
            self.organizerId = organizerId

        if selectedCategoryId is not None:
            self.selectedCategoryId = selectedCategoryId

        if eventToEdit is not None:
            self.eventToEdit = eventToEdit

        if categoryList:
            self.categoryList.extend(categoryList)

        if organizerViewModel is not None:
            self.organizerViewModel = organizerViewModel

        if categoryViewModel is not None:
            self.categoryViewModel = categoryViewModel


class CreateAccountActivity(AppCompatActivity):

    registrationForm = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, registrationForm=None, **kwargs):

        super().__init__(**kwargs)

        if registrationForm is not None:
            self.registrationForm = registrationForm


class LoginActivity(AppCompatActivity):

    loginService = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, loginService=None, **kwargs):

        super().__init__(**kwargs)

        if loginService is not None:
            self.loginService = loginService


class MainActivity(AppCompatActivity):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
