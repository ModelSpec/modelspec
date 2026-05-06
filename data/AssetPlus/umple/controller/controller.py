from datetime import date
from typing import List
from ..generated_model_layer import *

class AssetPlusController:
    def __init__(self) -> None:
        self.assetPlus = AssetPlus()
        
    # helper methods

    def _get_asset_type(self, name: str) -> AssetType | None:
        for at in self.assetPlus.getAssetTypes():
            if at.getName() == name:
                return at
        return None

    def _get_specific_asset(self, asset_number: int) -> SpecificAsset | None:
        for sa in self.assetPlus.getSpecificAssets():
            if sa.getAssetNumber() == asset_number:
                return sa
        return None

    def _get_ticket(self, ticket_id: int) -> MaintenanceTicket | None:
        for t in self.assetPlus.getMaintenanceTickets():
            if t.getId() == ticket_id:
                return t
        return None

    def _get_user(self, email: str) -> User | None:
        m = self.assetPlus.getManager()
        if m is not None and m.getEmail() == email:
            return m
        for e in self.assetPlus.getEmployees():
            if e.getEmail() == email:
                return e
        for g in self.assetPlus.getGuests():
            if g.getEmail() == email:
                return g
        return None

    def _is_string_valid(self, value: str, subject: str, cannot_or_must_not: str) -> None:
        if value is None or value == "":
            raise ValueError(f"The {subject} {cannot_or_must_not} be empty")

    def _is_description_empty(self, value: str) -> None:
        if value is None or value == "":
            raise ValueError("Ticket description cannot be empty")

    def _is_greater_than_zero(self, number: int, error: str) -> None:
        if number <= 0:
            raise ValueError(error)

    def _is_greater_or_equal_zero(self, number: int, subject: str) -> None:
        if number < 0:
            raise ValueError(f"Error: the number from {subject} must be greater than or equal to 0.\n")

    def _is_existing_asset_type(self, name: str) -> None:
        if self._get_asset_type(name) is None:
            raise ValueError("The asset type does not exist")


    def _is_existing_user(self, email: str, subject: str) -> None:
        if email == "manager@ap.com":
            return
        user = self._get_user(email)
        if user is None or (subject == "hotel staff" and isinstance(user, Guest)):
            if subject == "hotel staff":
                raise ValueError("Hotel staff does not exist")
            if subject == "ticket raiser":
                raise ValueError("The ticket raiser does not exist")
            raise ValueError("Error: user not found")

    def _delete_ticket(self, ticket: MaintenanceTicket) -> None:
        # the generated MaintenanceTicket.delete() fails on tickets that still have notes or images
        for note in ticket.getTicketNotes():
            note.delete()
        for img in ticket.getTicketImages():
            img.delete()
        ticket.delete()

    def _is_existing_ticket(self, ticket_id: int) -> None:
        if self._get_ticket(ticket_id) is None:
            raise ValueError("Ticket does not exist")

    def _is_valid_image_url(self, url: str) -> None:
        if url is None or url == "":
            return
        if not (url.startswith("http://") or url.startswith("https://")):
            raise ValueError("Image URL must start with http:// or https://")

    def _has_space(self, value: str) -> bool:
        return any(c.isspace() for c in value) if value else False

    def _valid_email(self, value: str) -> bool:
        if not value or self._has_space(value) or value.count("@") != 1:
            return False
        local, domain = value.split("@")
        if not local or not domain:
            return False
        parts = domain.split(".")
        if len(parts) != 2 or not parts[0] or not parts[1]:
            return False
        return True
    
    # main controllers
    
    def updateManager(self, email: str, new_password: str) -> None:
        m = self.assetPlus.getManager()
        if m is None or m.getEmail() != email:
            raise ValueError("Invalid manager")
        if not new_password:
            raise ValueError("Password cannot be empty")
        if len(new_password) < 4:
            raise ValueError("Password must be at least four characters long")
        if not any(c in "!#$" for c in new_password):
            raise ValueError("Password must contain one character out of !#$")
        if new_password.upper() == new_password:
            raise ValueError("Password must contain one lower-case character")
        if new_password.lower() == new_password:
            raise ValueError("Password must contain one upper-case character")
        m.setPassword(new_password)

    def registerEmployee(self, email: str, password: str, name: str, phone: str) -> None:
        if not email:
            raise ValueError("Email cannot be empty")
        if email.lower() == "manager@ap.com":
            raise ValueError("Email cannot be manager@ap.com")
        if self._get_user(email) is not None:
            raise ValueError("Email already linked to an employee account")
        if self._has_space(email):
            raise ValueError("Email must not contain any spaces")
        if not self._valid_email(email):
            raise ValueError("Invalid email")
        if not email.endswith("@ap.com"):
            raise ValueError("Email domain must be @ap.com")
        if not password:
            raise ValueError("Password cannot be empty")
        self.assetPlus.addEmployee(email, name, password, phone)

    def updateEmployee(self, email: str, new_password: str, new_name: str, new_phone: str) -> None:
        u = self._get_user(email)
        if u is None or not isinstance(u, Employee):
            raise ValueError("Employee does not exist")
        if not new_password:
            raise ValueError("Password cannot be empty")
        u.setPassword(new_password)
        u.setName(new_name)
        u.setPhoneNumber(new_phone)

    def deleteEmployee(self, email: str) -> None:
        u = self._get_user(email)
        if isinstance(u, Employee):
            for t in u.getMaintenanceTasks():
                self._delete_ticket(t)
            for t in u.getRaisedTickets():
                self._delete_ticket(t)
            u.delete()

    def registerGuest(self, email: str, password: str, name: str, phone: str) -> None:
        if not email:
            raise ValueError("Email cannot be empty")
        if email.lower() == "manager@ap.com":
            raise ValueError("Email cannot be manager@ap.com")
        if self._get_user(email) is not None:
            raise ValueError("Email already linked to a guest account")
        if email.endswith("@ap.com"):
            raise ValueError("Email domain cannot be @ap.com")
        if self._has_space(email):
            raise ValueError("Email must not contain any spaces")
        if not self._valid_email(email):
            raise ValueError("Invalid email")
        if not password:
            raise ValueError("Password cannot be empty")
        self.assetPlus.addGuest(email, name, password, phone)

    def updateGuest(self, email: str, new_password: str, new_name: str, new_phone: str) -> None:
        if self._get_user(email) is None:
            raise ValueError("Guest does not exist")
        if not new_password:
            raise ValueError("Password cannot be empty")
        u = self._get_user(email)
        if u is None or not isinstance(u, Guest):
            raise ValueError("Guest does not exist")
        u.setPassword(new_password)
        u.setName(new_name)
        u.setPhoneNumber(new_phone)

    def deleteGuest(self, email: str) -> None:
        u = self._get_user(email)
        if isinstance(u, Guest):
            for t in u.getRaisedTickets():
                self._delete_ticket(t)
            u.delete()

    def addAssetType(self, name: str, expected_life_span: int, image_url: str = None) -> None:
        self._is_string_valid(name, "name", "must not")
        self._is_greater_than_zero(expected_life_span, "The expected life span must be greater than 0 days")
        if self._get_asset_type(name) is not None:
            raise ValueError("The asset type already exists")
        self._is_valid_image_url(image_url)
        at = self.assetPlus.addAssetType(name, expected_life_span)
        if image_url:
            at.setImage(image_url)

    def updateAssetType(self, old_name: str, new_name: str, new_span: int, new_image_url: str = None) -> None:
        self._is_string_valid(new_name, "name", "must not")
        self._is_greater_than_zero(new_span, "The expected life span must be greater than 0 days")
        old = self._get_asset_type(old_name)
        if old is None:
            raise ValueError("The asset type does not exist")
        if old_name != new_name and self._get_asset_type(new_name) is not None:
            raise ValueError("The asset type already exists")
        self._is_valid_image_url(new_image_url)
        old.setName(new_name)
        old.setExpectedLifeSpan(new_span)
        old.setImage(new_image_url or "")

    def deleteAssetType(self, name: str) -> None:
        self._is_string_valid(name, "name", "must not")
        at = self._get_asset_type(name)
        if at is not None:
            for a in at.getSpecificAssets():
                self.deleteAsset(a.getAssetNumber())
            at.delete()

    def addAsset(self, asset_number: int, asset_type_name: str, purchase_date: date, floor_number: int, room_number: int) -> None:
        self._is_greater_or_equal_zero(asset_number, "assetNumber")
        if asset_number < 1:
            raise ValueError("The asset number shall not be less than 1")
        if floor_number < 0:
            raise ValueError("The floor number shall not be less than 0")
        if room_number < -1:
            raise ValueError("The room number shall not be less than -1")
        self._is_existing_asset_type(asset_type_name)
        if self._get_specific_asset(asset_number) is not None:
            raise ValueError("The asset number already exists")
        at = self._get_asset_type(asset_type_name)
        self.assetPlus.addSpecificAsset(asset_number, floor_number, room_number, purchase_date, at)

    def updateAsset(self, asset_number: int, new_asset_type_name: str, new_purchase_date: date, new_floor_number: int, new_room_number: int) -> None:
        a = self._get_specific_asset(asset_number)
        if a is None:
            raise ValueError(f"Asset with asset number {asset_number} does not exist")
        if new_floor_number < 0:
            raise ValueError("The floor number shall not be less than 0")
        if new_room_number < -1:
            raise ValueError("The room number shall not be less than -1")
        at = self._get_asset_type(new_asset_type_name)
        if at is None:
            raise ValueError("The asset type does not exist")
        a.setAssetType(at)
        a.setPurchaseDate(new_purchase_date)
        a.setFloorNumber(new_floor_number)
        a.setRoomNumber(new_room_number)

    def deleteAsset(self, asset_number: int) -> None:
        a = self._get_specific_asset(asset_number)
        if a is not None:
            for t in a.getMaintenanceTickets():
                self._delete_ticket(t)
            a.delete()
        return None

    def addMaintenanceTicket(self, id: int, ticket_raiser: str, raised_on: date, description: str, asset_number: int) -> None:
        self._is_greater_or_equal_zero(id, "Ticket id")
        if self._get_ticket(id) is not None:
            raise ValueError("Ticket id already exists")
        self._is_description_empty(description)
        self._is_string_valid(ticket_raiser, "Email", "cannot")
        self._is_existing_user(ticket_raiser, "ticket raiser")
        asset = None
        if asset_number is not None:
            asset = self._get_specific_asset(int(asset_number))
            if asset is None:
                raise ValueError("The asset does not exist")
        raiser = self._get_user(ticket_raiser)
        if raiser is None:
            raise ValueError("The ticket raiser does not exist")
        t = self.assetPlus.addMaintenanceTicket(id, raised_on, description, raiser)
        if asset is not None:
            t.setAsset(asset)

    def updateMaintenanceTicket(self, id: int, ticketRaiserEmail: str, raisedOnDate: date, description: str, assetNumber: int):
        ticket = None
        for t in self.assetPlus.getMaintenanceTickets():
            if t.getId() == id:
                ticket = t
                break
        if ticket is None:
            raise ValueError("The maintenance ticket does not exist")
        raiser = None
        m = self.assetPlus.getManager()
        if m is not None and m.getEmail() == ticketRaiserEmail:
            raiser = m
        if raiser is None:
            for e in self.assetPlus.getEmployees():
                if e.getEmail() == ticketRaiserEmail:
                    raiser = e
                    break
        if raiser is None:
            for g in self.assetPlus.getGuests():
                if g.getEmail() == ticketRaiserEmail:
                    raiser = g
                    break
        if raiser is None:
            raise ValueError("The ticket raiser does not exist")
        if description is None or str(description) == "":
            raise ValueError("Ticket description cannot be empty")
        asset = None
        if assetNumber is not None:
            for a in self.assetPlus.getSpecificAssets():
                if a.getAssetNumber() == assetNumber:
                    asset = a
                    break
            if asset is None:
                raise ValueError("The asset does not exist")
        ticket.setTicketRaiser(raiser)
        ticket.setRaisedOnDate(raisedOnDate)
        ticket.setDescription(description)
        if assetNumber is None:
            ticket.setAsset(None)
        else:
            ticket.setAsset(asset)
        return None

    def deleteMaintenanceTicket(self, id: int) -> None:
            ticket = self._get_ticket(id)
            if ticket is None:
                return None
            self._delete_ticket(ticket)
            return None

    def addTicketImage(self, ticket_id: int, image_url: str) -> None:
        self._is_greater_or_equal_zero(ticket_id, "ticketID")

        if image_url is None or image_url == "":
            raise ValueError("Image URL cannot be empty")

        self._is_valid_image_url(image_url)

        t = self._get_ticket(ticket_id)
        if t is None:
            raise ValueError("Ticket does not exist")

        for img in t.getTicketImages():
            if img.getImageURL() == image_url:
                raise ValueError("Image already exists for the ticket")

        t.addTicketImage(image_url)
        return None

    def deleteTicketImage(self, ticket_id: int, image_url: str) -> None:
        self._is_greater_or_equal_zero(ticket_id, "ticketID")
        self._is_string_valid(image_url, "imageURL", "cannot")

        t = self._get_ticket(ticket_id)
        if t is None:
            return None

        for img in list(t.getTicketImages()):
            if img.getImageURL() == image_url:
                img.delete()
                return None
        return None
    
    def addMaintenanceNote(self, ticket_id: int, note_taker: str, added_on: date, description: str) -> None:
        self._is_description_empty(description)
        self._is_existing_ticket(ticket_id)
        if note_taker == "":
            raise ValueError("The Email cannot be empty")
        self._is_existing_user(note_taker, "hotel staff")
        t = self._get_ticket(ticket_id)
        staff = self._get_user(note_taker)
        if t is None:
            raise ValueError("Ticket does not exist")
        if staff is None:
            raise ValueError("Hotel staff does not exist")
        staff.addMaintenanceNote(added_on, description, t)

    def updateMaintenanceNote(self, ticket_id: int, note_index: int, new_taker: str, new_date: date, new_description: str) -> None:
        self._is_description_empty(new_description)
        self._is_existing_ticket(ticket_id)
        self._is_existing_user(new_taker, "hotel staff")
        t = self._get_ticket(ticket_id)
        if t is None:
            raise ValueError("Ticket does not exist")
        notes = list(t.getTicketNotes())
        if note_index < 0:
            raise ValueError("Note does not exist")
        try:
            note = notes[note_index]
        except Exception:
            raise ValueError("Note does not exist")
        staff = self._get_user(new_taker)
        if staff is None:
            raise ValueError("Hotel staff does not exist")
        note.setDate(new_date)
        note.setDescription(new_description)
        note.setNoteTaker(staff)

    def deleteMaintenanceNote(self, ticket_id: int, note_index: int) -> None:
        t = self._get_ticket(ticket_id)
        if t is None or note_index < 0:
            return None
        try:
            notes = list(t.getTicketNotes())
            note = notes[note_index]
            note.delete()
        except Exception:
            pass
        return None

    def viewStatusOfMaintenanceTickets(self) -> List[TOMaintenanceTicket]:
        result: List[TOMaintenanceTicket] = []
        for t in self.assetPlus.getMaintenanceTickets():
            raiser = t.getTicketRaiser()
            raised_by_email = raiser.getEmail() if raiser is not None else None
            status = None
            if hasattr(t, "getStatus"):
                status = t.getStatus()
            fixed_by_email = None
            if hasattr(t, "getFixedBy"):
                fb = t.getFixedBy()
                if fb is not None and hasattr(fb, "getEmail"):
                    fixed_by_email = fb.getEmail()
            time_to_resolve = None
            if hasattr(t, "getTimeToResolve"):
                time_to_resolve = t.getTimeToResolve()
            priority = None
            if hasattr(t, "getPriority"):
                priority = t.getPriority()
            approval_required = None
            if hasattr(t, "getApprovalRequired"):
                approval_required = t.getApprovalRequired()
            asset_name = None
            expected_life_span = None
            purchase_date = None
            floor_number = None
            room_number = None
            a = t.getAsset() if hasattr(t, "getAsset") else None
            if a is not None:
                at = a.getAssetType() if hasattr(a, "getAssetType") else None
                asset_name = at.getName() if at is not None and hasattr(at, "getName") else None
                expected_life_span = at.getExpectedLifeSpan() if at is not None and hasattr(at, "getExpectedLifeSpan") else None
                if hasattr(a, "getPurchaseDate"):
                    purchase_date = a.getPurchaseDate()
                if hasattr(a, "getFloorNumber"):
                    floor_number = a.getFloorNumber()
                if hasattr(a, "getRoomNumber"):
                    room_number = a.getRoomNumber()
            to_ticket = TOMaintenanceTicket(
                t.getId(),
                t.getRaisedOnDate(),
                t.getDescription(),
                raised_by_email,
                status,
                fixed_by_email,
                time_to_resolve,
                priority,
                approval_required,
                asset_name,
                expected_life_span,
                purchase_date,
                floor_number,
                room_number
            )
            for img in t.getTicketImages():
                to_ticket._imageURLs.append(img.getImageURL())
            for note in t.getTicketNotes():
                to_ticket._noteDates.append(note.getDate())
                to_ticket._noteDescriptions.append(note.getDescription())
                nt = note.getNoteTaker()
                to_ticket._noteTakerEmails.append(nt.getEmail() if nt is not None else None)
            result.append(to_ticket)
        return result