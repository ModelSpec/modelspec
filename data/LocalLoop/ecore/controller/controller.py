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
        self.adminViewModel = AdminViewModel(adminDashboardActivity=AdminDashboardActivity())
        self.categoryViewModel = CategoryViewModel(manageCategoriesActivity=ManageCategoriesActivity(), manageEventActivity=ManageEventActivity(isEditMode=False, organizerId="", selectedCategoryId="", eventToEdit=None))

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
            if acc.email == email:
                raise ValueError("The email already exists.")
            if acc.username == username:
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
            role = Organizer(companyName=companyName)
        else:
            role = Participant()

        self.accounts.append(UserAccount(userID=id, firstName=firstName, lastName=lastName, username=username, email=email, phoneNumber=phoneNumber, role=role, adminViewModel=self.adminViewModel))

    def createCategory(self, userId: str, name: str, description: str) -> None:
        user = None
        for u in self.accounts:
            if u.userID == userId and type(u.role) is Admin:
                user = u
        if user is None:
            raise ValueError("Only admin users can update categories.")
        
        if not name:
            raise ValueError("Name must not be empty.")
        
        if not description:
            raise ValueError("Description must not be empty.")
        
        id = str(uuid.uuid4())

        self.categories.append(Category(categoryId=id, name=name, description=description, categoryViewModel=self.categoryViewModel))
                
    
    def createEvent(self, organizerId: str, name: str, description: str, categoryId: str, fee: float, eventStart: int, eventEnd: int, capacity: int) -> None:
        organizer = None
        for acc in self.accounts:
            if acc.userID == organizerId:
                organizer = acc
                break

        if organizer is None:
            raise ValueError(f"Account with ID {organizerId} does not exist.")

        if type(organizer.role) is not Organizer:
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
            if cat.categoryId == categoryId:
                category = cat
                break
        if category is None:
            raise ValueError("Category with the given ID does not exist.")

        eventId = str(uuid.uuid4())

        event = Event(eventId=eventId, organizerId=organizerId, name=name, description=description, categoryId=categoryId, fee=fee, eventStart=eventStart, eventEnd=eventEnd, capacity=capacity, category=category, organizer=organizer.role, eventRepository=self.eventRepository)

        self.events.append(event)
    
    def createRegistration(self, userId: str, eventId: str, timeStamp: int) -> None:
        participant = None
        for acc in self.accounts:
            if acc.userID == userId and type(acc.role) is Participant:
                participant = acc
                break

        if participant is None:
            raise ValueError(f"Participant with ID {userId} does not exist.")

        targetEvent = None
        for ev in self.events:
            if ev.eventId == eventId:
                targetEvent = ev
                break

        if targetEvent is None:
            raise ValueError(f"Event with ID {eventId} does not exist.")

        registrationId = str(uuid.uuid4())

        registration = Registration(registrationId=registrationId, eventId=eventId, participantId=participant.userID, organizerId=targetEvent.organizerId, status="pending", timestamp=timeStamp, event=targetEvent, participant=participant.role, registrationRepository=self.registrationRepository)

        self.registrations.append(registration)

    def deleteAccount(self, userId: str, targetUserId: str) -> None:
        user = None
        toBeDeleted = None
        for a in self.accounts:
            if a.userID == userId:
                user = a
            if a.userID == targetUserId:
                toBeDeleted = a
        
        if user is None:
            raise ValueError("Account does not exist.")
        
        if toBeDeleted is None:
            raise ValueError("User account does not exist.")
        
        events = []
        registrations = []
        if type(user.role) is Admin or userId == targetUserId:
            if type(toBeDeleted.role) is Organizer:
                events = toBeDeleted.role.events
                for e in events:
                    registrations.extend(e.registrations)
            if type(toBeDeleted.role) is Participant:
                registrations.extend(toBeDeleted.role.registrations)
            
            for e in list(events):
                self.events.remove(e)
            for r in registrations:
                self.registrations.remove(r)

            if type(toBeDeleted.role) is Organizer:
                toBeDeleted.role.events.clear()

            toBeDeleted.adminViewModel = None
            self.accounts.remove(toBeDeleted)
            return
    
        else:
            raise ValueError("Only admins or account owners can delete the account.")

    def deleteCategory(self, userId: str, categoryId: str) -> None:
        account = None
        for a in self.accounts:
            if a.userID == userId:
                account = a

        if account is None:
            raise ValueError(f"Account with ID {userId} does not exist.")

        if type(account.role) is not Admin:
            raise ValueError("Only admin users can delete categories.")

        category = None
        for c in self.categories:
            if c.categoryId == categoryId:
                category = c

        if category is None:
            raise ValueError(f"Category with ID {categoryId} does not exist.")
        
        events = category.events
        registrations = []
        for e in events:
            registrations.extend(e.registrations)
        
        for e in  list(events):
            self.events.remove(e)
        for r in registrations:
            self.registrations.remove(r)

        self.categories.remove(category)
        category.events.clear() 
        category.categoryViewModel = None

    def deleteEvent(self, userId: str, eventId: str) -> None:
        account = None
        for a in self.accounts:
            if a.userID == userId:
                account = a

        if account is None:
            raise ValueError(f"Account with ID {userId} does not exist.")

        if type(account.role) is not Organizer:
            raise ValueError("Only organizers can delete events.")

        event = None
        for e in self.events:
            if e.eventId == eventId:
                event = e

        if event is None:
            raise ValueError(f"Event with ID {eventId} does not exist.")

        if event.organizer != account.role:
            raise ValueError("Only the event organizer can delete this event.")

        for r in event.registrations:
            self.registrations.remove(r)

        self.events.remove(event)
        event.category = None
        event.registrations.clear()
        event.organizer = None
        event.eventRepository = None

    
    def updateCategory(self, userId: str, categoryId: str, name: str, description: str) -> None:
        if not name:
            raise ValueError("Name must not be empty.")
        
        if not description:
            raise ValueError("Description must not be empty.")
        
        admin = None
        for a in self.accounts:
            if a.userID == userId:
                admin = a
        
        if admin is None:
            raise ValueError(f"Account with ID {userId} does not exist.")
        
        if type(admin.role) is not Admin:
            raise ValueError("Only admin users can update categories.")
        
        category = None
        for c in self.categories:
            if c.categoryId == categoryId:
                category = c
        
        if category is None:
            raise ValueError(f"Category with ID {categoryId} does not exist.")
        
        category.name = name
        category.description = description

    def updateEvent(self, organizerId: str, eventId: str, name: str, description: str, categoryId: str, fee: float, eventStart: int, eventEnd: int, capacity: int) -> None:
        if not name:
            raise ValueError("Event name must not be empty.")
        
        if not description:
            raise ValueError("Event description must not be empty.")
        
        organizer = None
        for a in self.accounts:
            if a.userID == organizerId:
                organizer = a

        if organizer is None:
            raise ValueError(f"Account with ID {organizerId} does not exist.")
        
        if type(organizer.role) is not Organizer:
            raise ValueError("Only organizers can update events.")
        
        event = None
        for e in self.events:
            if e.eventId == eventId:
                event = e
        
        if event is None:
            raise ValueError(f"Event with ID {eventId} does not exist.")
        
        if event.organizerId != organizerId:
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
                if c.categoryId == categoryId:
                    category = c
            if category is None:
                raise ValueError("Category with the given ID does not exist.")

        event.name = name
        event.description = description
        event.category = category
        event.categoryId = categoryId
        event.fee = fee
        event.eventStart = eventStart
        event.eventEnd = eventEnd
        event.capacity = capacity

    def updateRegistration(self, userId: str, registrationId: str, newStatus: str) -> None:
        account = None
        for a in self.accounts:
            if a.userID == userId:
                account = a
                break
        if account is None:
            raise ValueError("Invalid user ID.")

        registration = None
        for r in self.registrations:
            if r.registrationId == registrationId:
                registration = r
        if registration is None:
            raise ValueError("Invalid registration ID.")

        if newStatus not in ["pending", "approved", "cancelled"]:
            raise ValueError("Invalid status. Must be pending, approved or cancelled.")

        currentStatus = registration.status
        if currentStatus in ["approved", "cancelled"]:
            raise ValueError(f"Cannot update registration with status '{currentStatus}'.")

        event = registration.event
        isOrganizer = event.organizerId == userId
        isOwner = registration.participantId == userId

        if not isOrganizer and (not isOwner or newStatus == "approved"):
            raise ValueError(f"User {userId} is not authorized to update this registration.")

        capacity = event.capacity
        eventId = event.eventId
        approvedCount = sum(
            1 for r in self.registrations
            if r.event.eventId == eventId and r.status == "approved"
        )
        if newStatus == "approved" and approvedCount >= capacity:
            raise ValueError("Cannot approve registration if event is at full capacity.")

        registration.status = newStatus
