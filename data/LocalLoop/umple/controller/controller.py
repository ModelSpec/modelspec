import uuid

from ..generated_model_layer import *

class LocalLoopController:
    def __init__(self):
        self.accounts = []
        self.events = []
        self.registrations = []
        self.categories = []
        self.roles = []

        self.eventRepository = EventRepository()
        self.registrationRepository = RegistrationRepository()
        self.adminViewModel = AdminViewModel(AdminDashboardActivity())
        self.categoryViewModel = CategoryViewModel(ManageCategoriesActivity(), ManageEventActivity(False, "", "", None))

    def createAccount(self, firstName: str, lastName: str, username: str, email: str, phoneNumber: str, password: str, confirmPassword: str, isOrganizer: bool, companyName: str) -> None:
        if not firstName:
            raise ValueError("First name must not be empty.")

        if not lastName:
            raise ValueError("Last name must not be empty.")

        if not username:
            raise ValueError("Username must not be empty.")

        if not email:
            raise ValueError("Email must not be empty.")
        
        atIndex = email.find("@")
        if atIndex == -1:
            raise ValueError("Email must contain @ symbol.")
        
        if atIndex == 0:
            raise ValueError("Email must have characters before @.")
        
        if email[atIndex:].find(".") == -1:
            raise ValueError("Email must contain a dot after @.")
        
        if email[len(email) - 1] == ".":
            raise ValueError("Email must have characters after dot.")
        
        if " " in email:
            raise ValueError("Email must not contain spaces.")
        
        for acc in self.accounts:
            if acc.getEmail() == email:
                raise ValueError("The email already exists.")
            if acc.getUsername() == username:
                raise ValueError("The username already exists.")
            
        if not password:
            raise ValueError("Password must not be empty.")
            
        if not confirmPassword:
            raise ValueError("Confirm password must not be empty.")
            
        if password != confirmPassword:
            raise ValueError("Passwords must match.")
            
        if isOrganizer and not companyName:
            raise ValueError("Company name must be provided for organizers.")
        
        id = str(uuid.uuid4())

        role = None
        if isOrganizer:
            role = Organizer(companyName)
        else:
            role = Participant()

        self.accounts.append(UserAccount(id, firstName, lastName, username, email, phoneNumber, role, self.adminViewModel))

    def createCategory(self, userId: str, name: str, description: str) -> None:
        user = None
        for u in self.accounts:
            if u.getUserID() == userId and type(u.getRole()) is Admin:
                user = u
        if user is None:
            raise ValueError("Only admin users can update categories.")
        
        if not name:
            raise ValueError("Name must not be empty.")
        
        if not description:
            raise ValueError("Description must not be empty.")
        
        id = str(uuid.uuid4())

        self.categories.append(Category(id, name, description, self.categoryViewModel))
                
    
    def createEvent(self, organizerId: str, name: str, description: str, categoryId: str, fee: float, eventStart: int, eventEnd: int, capacity: int) -> None:
        organizer = None
        for acc in self.accounts:
            if acc.getUserID() == organizerId:
                organizer = acc
                break

        if organizer is None:
            raise ValueError(f"Account with ID {organizerId} does not exist.")

        if type(organizer.getRole()) is not Organizer:
            raise ValueError("Only organizers can create events.")

        if not name:
            raise ValueError("Event name must not be empty.")

        if not description:
            raise ValueError("Event description must not be empty.")

        if fee < 0:
            raise ValueError("Fee must be 0 or a positive number.")

        if eventStart is None or eventStart == 0:
            raise ValueError("Event start time must not be empty.")

        if eventEnd is None or eventEnd == 0:
            raise ValueError("Event end time must not be empty.")

        if eventEnd <= eventStart:
            raise ValueError("Event end time must be after start time.")

        if capacity < 0:
            raise ValueError("Capacity must be 0 or a positive integer.")

        category = None
        for cat in self.categories:
            if cat.getCategoryId() == categoryId:
                category = cat
                break
        if category is None:
            raise ValueError("Category with the given ID does not exist.")

        eventId = str(uuid.uuid4())

        event = Event(eventId, organizerId, name, description, categoryId, fee, eventStart, eventEnd, capacity, category, organizer.getRole(), self.eventRepository)

        self.events.append(event)
    
    def createRegistration(self, userId: str, eventId: str, timeStamp: int) -> None:
        participant = None
        for acc in self.accounts:
            if acc.getUserID() == userId and type(acc.getRole()) is Participant:
                participant = acc
                break

        if participant is None:
            raise ValueError(f"Participant with ID {userId} does not exist.")

        targetEvent = None
        for ev in self.events:
            if ev.getEventId() == eventId:
                targetEvent = ev
                break

        if targetEvent is None:
            raise ValueError(f"Event with ID {eventId} does not exist.")

        registrationId = str(uuid.uuid4())

        registration = Registration(registrationId, eventId, participant.getUserID(), targetEvent.getOrganizerId(), "pending", timeStamp, targetEvent, participant.getRole(), self.registrationRepository)

        self.registrations.append(registration)

    def deleteAccount(self, userId: str, targetUserId: str) -> None:
        user = None
        toBeDeleted = None
        for a in self.accounts:
            if a.getUserID() == userId:
                user = a
            if a.getUserID() == targetUserId:
                toBeDeleted = a
        
        if user is None:
            raise ValueError("Account does not exist.")
        
        if toBeDeleted is None:
            raise ValueError("User account does not exist.")
        
        events = []
        registrations = []
        if type(user.getRole()) is Admin or userId == targetUserId:
            if type(toBeDeleted.getRole()) is Organizer:
                events = toBeDeleted.getRole().getEvents()
                for e in events:
                    registrations.extend(e.getRegistrations())
            if type(toBeDeleted.getRole()) is Participant:
                registrations.extend(toBeDeleted.getRole().getRegistrations())
            
            for e in events:
                self.events.remove(e)
            for r in registrations:
                self.registrations.remove(r)

            toBeDeleted.getRole().delete()

            toBeDeleted.delete()
            self.accounts.remove(toBeDeleted)
            return
    
        else:
            raise ValueError("Only admins or account owners can delete the account.")

    def deleteCategory(self, userId: str, categoryId: str) -> None:
        account = None
        for a in self.accounts:
            if a.getUserID() == userId:
                account = a

        if account is None:
            raise ValueError(f"Account with ID {userId} does not exist.")

        if type(account.getRole()) is not Admin:
            raise ValueError("Only admin users can delete categories.")

        category = None
        for c in self.categories:
            if c.getCategoryId() == categoryId:
                category = c

        if category is None:
            raise ValueError(f"Category with ID {categoryId} does not exist.")
        
        events = category.getEvents()
        registrations = []
        for e in events:
            registrations.extend(e.getRegistrations())
        
        for e in events:
            self.events.remove(e)
        for r in registrations:
            self.registrations.remove(r)

        category.delete()
        self.categories.remove(category)

    def deleteEvent(self, userId: str, eventId: str) -> None:
        account = None
        for a in self.accounts:
            if a.getUserID() == userId:
                account = a

        if account is None:
            raise ValueError(f"Account with ID {userId} does not exist.")

        if type(account.getRole()) is not Organizer:
            raise ValueError("Only organizers can delete events.")

        event = None
        for e in self.events:
            if e.getEventId() == eventId:
                event = e

        if event is None:
            raise ValueError(f"Event with ID {eventId} does not exist.")

        if event.getOrganizerId() != userId:
            raise ValueError("Only the event organizer can delete this event.")

        for r in event.getRegistrations():
            self.registrations.remove(r)

        event.delete()
        self.events.remove(event)
    
    def updateCategory(self, userId: str, categoryId: str, name: str, description: str) -> None:
        if not name:
            raise ValueError("Name must not be empty.")
        
        if not description:
            raise ValueError("Description must not be empty.")
        
        admin = None
        for a in self.accounts:
            if a.getUserID() == userId:
                admin = a
        
        if admin is None:
            raise ValueError(f"Account with ID {userId} does not exist.")
        
        if type(admin.getRole()) is not Admin:
            raise ValueError("Only admin users can update categories.")
        
        category = None
        for c in self.categories:
            if c.getCategoryId() == categoryId:
                category = c
        
        if category is None:
            raise ValueError(f"Category with ID {categoryId} does not exist.")
        
        category.setName(name)
        category.setDescription(description)

    def updateEvent(self, organizerId: str, eventId: str, name: str, description: str, categoryId: str, fee: float, eventStart: int, eventEnd: int, capacity: int) -> None:
        if not name:
            raise ValueError("Event name must not be empty.")
        
        if not description:
            raise ValueError("Event description must not be empty.")
        
        organizer = None
        for a in self.accounts:
            if a.getUserID() == organizerId:
                organizer = a

        if organizer is None:
            raise ValueError(f"Account with ID {organizerId} does not exist.")
        
        if type(organizer.getRole()) is not Organizer:
            raise ValueError("Only organizers can update events.")
        
        event = None
        for e in self.events:
            if e.getEventId() == eventId:
                event = e
        
        if event is None:
            raise ValueError(f"Event with ID {eventId} does not exist.")
        
        if event.getOrganizerId() != organizerId:
            raise ValueError("Only the event organizer can update this event.")

        if fee < 0:
            raise ValueError("Fee must be 0 or a positive number.")
        if capacity < 0:
            raise ValueError("Capacity must be 0 or a positive integer.")
        if not eventStart or eventStart == 0:
            raise ValueError("Event start time must not be empty.")
        if not eventEnd or eventEnd == 0:
            raise ValueError("Event end time must not be empty.")
        if eventStart >= eventEnd:
            raise ValueError("Event end time must be after start time.")

        category = None
        if categoryId:
            for c in self.categories:
                if c.getCategoryId() == categoryId:
                    category = c
            if category is None:
                raise ValueError("Category with the given ID does not exist.")

        event.setName(name)
        event.setDescription(description)
        event.setCategory(category)
        event.setCategoryId(categoryId)
        event.setFee(fee)
        event.setEventStart(eventStart)
        event.setEventEnd(eventEnd)
        event.setCapacity(capacity)

    def updateRegistration(self, userId: str, registrationId: str, newStatus: str) -> None:
        userExists = False
        for a in self.accounts:
            if a.getUserID() == userId:
                userExists = True
                break
        if not userExists:
            raise ValueError("Invalid user ID.")

        registration = None
        for r in self.registrations:
            if r.getRegistrationId() == registrationId:
                registration = r
        if registration is None:
            raise ValueError("Invalid registration ID.")

        if newStatus not in ["pending", "approved", "cancelled"]:
            raise ValueError("Invalid status. Must be pending, approved or cancelled.")

        currentStatus = registration.getStatus()
        if currentStatus in ["approved", "cancelled"]:
            raise ValueError(f"Cannot update registration with status '{currentStatus}'.")

        event = registration.getEvent()
        organizerId = event.getOrganizerId()
        isOwner = registration.getParticipantId() == userId
        if userId != organizerId and (not isOwner or newStatus == "approved"):
            raise ValueError(f"User {userId} is not authorized to update this registration.")

        eventId = event.getEventId()
        capacity = event.getCapacity()
        approvedCount = sum(
            1 for r in self.registrations
            if r.getEvent().getEventId() == eventId and r.getStatus() == "approved"
        )
        if newStatus == "approved" and approvedCount >= capacity:
            raise ValueError("Cannot approve registration if event is at full capacity.")

        registration.setStatus(newStatus)
