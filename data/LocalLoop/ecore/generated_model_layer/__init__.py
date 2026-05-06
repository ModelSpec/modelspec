
from .localLoop import getEClassifier, eClassifiers
from .localLoop import name, nsURI, nsPrefix, eClass
from .localLoop import Event, Category, Registration, RegistrationForm, UserAccount, Role, Admin, Organizer, Participant, EventRepository, RegistrationRepository, AdminViewModel, OrganizerViewModel, RegistrationViewModel, ParticipantViewModel, CategoryViewModel, LoginService, AppCompatActivity, AdminDashboardActivity, OrganizerDashboardActivity, ParticipantDashboardActivity, ManageCategoriesActivity, ManageEventActivity, CreateAccountActivity, LoginActivity, MainActivity


from . import localLoop

__all__ = ['Event', 'Category', 'Registration', 'RegistrationForm', 'UserAccount', 'Role', 'Admin', 'Organizer', 'Participant', 'EventRepository', 'RegistrationRepository', 'AdminViewModel', 'OrganizerViewModel', 'RegistrationViewModel', 'ParticipantViewModel',
           'CategoryViewModel', 'LoginService', 'AppCompatActivity', 'AdminDashboardActivity', 'OrganizerDashboardActivity', 'ParticipantDashboardActivity', 'ManageCategoriesActivity', 'ManageEventActivity', 'CreateAccountActivity', 'LoginActivity', 'MainActivity']

eSubpackages = []
eSuperPackage = None
localLoop.eSubpackages = eSubpackages
localLoop.eSuperPackage = eSuperPackage

UserAccount.role.eType = Role
OrganizerViewModel.eventRepo.eType = EventRepository
RegistrationViewModel.pendingRegistrations.eType = Registration
ManageEventActivity.eventToEdit.eType = Event
ManageEventActivity.categoryList.eType = Category
Event.category.eType = Category
Event.registrations.eType = Registration
Event.organizer.eType = Organizer
Event.eventRepository.eType = EventRepository
Category.events.eType = Event
Category.events.eOpposite = Event.category
Category.categoryViewModel.eType = CategoryViewModel
Registration.event.eType = Event
Registration.event.eOpposite = Event.registrations
Registration.participant.eType = Participant
Registration.registrationRepository.eType = RegistrationRepository
RegistrationForm.createAccountActivity.eType = CreateAccountActivity
UserAccount.adminViewModel.eType = AdminViewModel
Organizer.events.eType = Event
Organizer.events.eOpposite = Event.organizer
Participant.registrations.eType = Registration
Participant.registrations.eOpposite = Registration.participant
EventRepository.events.eType = Event
EventRepository.events.eOpposite = Event.eventRepository
EventRepository.organizerViewModel.eType = OrganizerViewModel
RegistrationRepository.registrations.eType = Registration
RegistrationRepository.registrations.eOpposite = Registration.registrationRepository
RegistrationRepository.registrationViewModel.eType = RegistrationViewModel
AdminViewModel.userAccounts.eType = UserAccount
AdminViewModel.userAccounts.eOpposite = UserAccount.adminViewModel
AdminViewModel.adminDashboardActivity.eType = AdminDashboardActivity
OrganizerViewModel.eventRepository.eType = EventRepository
OrganizerViewModel.eventRepository.eOpposite = EventRepository.organizerViewModel
OrganizerViewModel.organizerDashboardActivity.eType = OrganizerDashboardActivity
OrganizerViewModel.manageEventActivity.eType = ManageEventActivity
RegistrationViewModel.repository.eType = RegistrationRepository
RegistrationViewModel.repository.eOpposite = RegistrationRepository.registrationViewModel
RegistrationViewModel.organizerDashboardActivity.eType = OrganizerDashboardActivity
ParticipantViewModel.participantDashboardActivity.eType = ParticipantDashboardActivity
CategoryViewModel.categories.eType = Category
CategoryViewModel.categories.eOpposite = Category.categoryViewModel
CategoryViewModel.manageCategoriesActivity.eType = ManageCategoriesActivity
CategoryViewModel.manageEventActivity.eType = ManageEventActivity
LoginService.loginActivity.eType = LoginActivity
AdminDashboardActivity.adminViewModel.eType = AdminViewModel
AdminDashboardActivity.adminViewModel.eOpposite = AdminViewModel.adminDashboardActivity
OrganizerDashboardActivity.organizerViewModel.eType = OrganizerViewModel
OrganizerDashboardActivity.organizerViewModel.eOpposite = OrganizerViewModel.organizerDashboardActivity
OrganizerDashboardActivity.registrationViewModel.eType = RegistrationViewModel
OrganizerDashboardActivity.registrationViewModel.eOpposite = RegistrationViewModel.organizerDashboardActivity
ParticipantDashboardActivity.participantViewModel.eType = ParticipantViewModel
ParticipantDashboardActivity.participantViewModel.eOpposite = ParticipantViewModel.participantDashboardActivity
ManageCategoriesActivity.categoryViewModel.eType = CategoryViewModel
ManageCategoriesActivity.categoryViewModel.eOpposite = CategoryViewModel.manageCategoriesActivity
ManageEventActivity.organizerViewModel.eType = OrganizerViewModel
ManageEventActivity.organizerViewModel.eOpposite = OrganizerViewModel.manageEventActivity
ManageEventActivity.categoryViewModel.eType = CategoryViewModel
ManageEventActivity.categoryViewModel.eOpposite = CategoryViewModel.manageEventActivity
CreateAccountActivity.registrationForm.eType = RegistrationForm
CreateAccountActivity.registrationForm.eOpposite = RegistrationForm.createAccountActivity
LoginActivity.loginService.eType = LoginService
LoginActivity.loginService.eOpposite = LoginService.loginActivity

EventRepository.organizerViewModel.eOpposite = OrganizerViewModel.eventRepo
Event.category.eOpposite = Category.events
Event.registrations.eOpposite = Registration.event
Event.organizer.eOpposite = Organizer.events
Event.eventRepository.eOpposite = EventRepository.events
Registration.participant.eOpposite = Participant.registrations
Registration.registrationRepository.eOpposite = RegistrationRepository.registrations
UserAccount.adminViewModel.eOpposite = AdminViewModel.userAccounts
OrganizerViewModel.eventRepo.eOpposite = EventRepository.organizerViewModel
RegistrationRepository.registrationViewModel.eOpposite = RegistrationViewModel.repository
RegistrationViewModel.organizerDashboardActivity.eOpposite = OrganizerDashboardActivity.registrationViewModel
Category.categoryViewModel.eOpposite = CategoryViewModel.categories
AdminViewModel.adminDashboardActivity.eOpposite = AdminDashboardActivity.adminViewModel
ParticipantViewModel.participantDashboardActivity.eOpposite = ParticipantDashboardActivity.participantViewModel
CategoryViewModel.manageCategoriesActivity.eOpposite = ManageCategoriesActivity.categoryViewModel
CategoryViewModel.manageEventActivity.eOpposite = ManageEventActivity.categoryViewModel
OrganizerViewModel.organizerDashboardActivity.eOpposite = OrganizerDashboardActivity.organizerViewModel
OrganizerViewModel.manageEventActivity.eOpposite = ManageEventActivity.organizerViewModel
LoginService.loginActivity.eOpposite = LoginActivity.loginService
RegistrationForm.createAccountActivity.eOpposite = CreateAccountActivity.registrationForm

otherClassifiers = []

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
