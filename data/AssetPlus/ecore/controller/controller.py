from datetime import date
from typing import List, Optional
from pyecore.ecore import EDate

from ..generated_model_layer import *

class AssetPlusController:

    def __init__(self) -> None:
        self.assetPlus = AssetPlus()

    @staticmethod
    def _to_edate(d: date):
        return EDate.from_string(d.strftime('%Y-%m-%dT%H:%M:%S.%f%z'))

    def _get_asset_type(self, name: str) -> Optional[AssetType]:
        for at in list(self.assetPlus.assetTypes):
            if getattr(at, "name", None) == name:
                return at
        return None

    def _get_specific_asset(self, asset_number: int) -> Optional[SpecificAsset]:
        for sa in list(self.assetPlus.specificAssets):
            if getattr(sa, "assetNumber", None) == asset_number:
                return sa
        return None

    def _get_ticket(self, ticket_id: int) -> Optional[MaintenanceTicket]:
        for t in list(self.assetPlus.maintenanceTickets):
            if getattr(t, "id", None) == ticket_id:
                return t
        return None

    def _get_user(self, email: str) -> Optional[User]:
        if self.assetPlus.manager and self.assetPlus.manager.email == email:
            return self.assetPlus.manager
        for e in list(self.assetPlus.employees):
            if e.email == email:
                return e
        for g in list(self.assetPlus.guests):
            if g.email == email:
                return g
        return None

    @staticmethod
    def _is_string_valid(value: Optional[str], subject: str, cannot_or_must_not: str) -> None:
        if value is None or value == "":
            raise ValueError(f"The {subject} {cannot_or_must_not} be empty")

    @staticmethod
    def _is_description_empty(value: Optional[str]) -> None:
        if value is None or value == "":
            raise ValueError("Ticket description cannot be empty")

    @staticmethod
    def _is_greater_than_zero(number: int, error: str) -> None:
        if number <= 0:
            raise ValueError(error)

    @staticmethod
    def _is_greater_or_equal_zero(number: int, subject: str) -> None:
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

    def _is_existing_ticket(self, ticket_id: int) -> None:
        if self._get_ticket(ticket_id) is None:
            raise ValueError("Ticket does not exist")

    @staticmethod
    def _is_valid_image_url(url: Optional[str]) -> None:
        if url is None or url == "":
            return
        if not (url.startswith("http://") or url.startswith("https://")):
            raise ValueError("Image URL must start with http:// or https://")

    @staticmethod
    def _has_space(s: Optional[str]) -> bool:
        return any(c.isspace() for c in s) if s else False

    @staticmethod
    def _valid_email(email: Optional[str]) -> bool:
        if not email or AssetPlusController._has_space(email) or email.count("@") != 1:
            return False
        local, domain = email.split("@")
        if not local or not domain:
            return False
        parts = domain.split(".")
        if len(parts) != 2 or not parts[0] or not parts[1]:
            return False
        return True

    def updateManager(self, email: str, newPassword: str) -> None:
        m = self.assetPlus.manager
        if not m or m.email != email:
            raise ValueError("Invalid manager")
        if not newPassword:
            raise ValueError("Password cannot be empty")
        if len(newPassword) < 4:
            raise ValueError("Password must be at least four characters long")
        if not any(c in "!#$" for c in newPassword):
            raise ValueError("Password must contain one character out of !#$")
        if newPassword.upper() == newPassword:
            raise ValueError("Password must contain one lower-case character")
        if newPassword.lower() == newPassword:
            raise ValueError("Password must contain one upper-case character")
        m.password = newPassword

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

        e = Employee(email=email, name=name, password=password, phoneNumber=phone)
        self.assetPlus.employees.append(e)

    def updateEmployee(self, email: str, newPassword: str, newName: str, newPhone: str) -> None:
        u = self._get_user(email)
        if u is None or not isinstance(u, Employee):
            raise ValueError("Employee does not exist")
        if not newPassword:
            raise ValueError("Password cannot be empty")
        u.password = newPassword
        u.name = newName
        u.phoneNumber = newPhone

    def deleteEmployee(self, email: str) -> None:
        u = self._get_user(email)
        if isinstance(u, Employee):
            for note in list(u.maintenanceNotes):
                note.delete()
            for t in list(u.maintenanceTasks):
                t.delete()
            for t in list(u.raisedTickets):
                t.delete()
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

        g = Guest(email=email, name=name, password=password, phoneNumber=phone)
        self.assetPlus.guests.append(g)

    def updateGuest(self, email: str, newPassword: str, newName: str, newPhone: str) -> None:
        if self._get_user(email) is None:
            raise ValueError("Guest does not exist")
        if not newPassword:
            raise ValueError("Password cannot be empty")
        u = self._get_user(email)
        if u is None or not isinstance(u, Guest):
            raise ValueError("Guest does not exist")
        u.password = newPassword
        u.name = newName
        u.phoneNumber = newPhone

    def deleteGuest(self, email: str) -> None:
        u = self._get_user(email)
        if isinstance(u, Guest):
            for t in list(u.raisedTickets):
                t.delete()
            u.delete()

    def addAssetType(self, name: str, expectedLifeSpan: int, imageUrl: str = None) -> None:
        self._is_string_valid(name, "name", "must not")
        self._is_greater_than_zero(expectedLifeSpan, "The expected life span must be greater than 0 days")
        if self._get_asset_type(name) is not None:
            raise ValueError("The asset type already exists")
        self._is_valid_image_url(imageUrl)

        at = AssetType(name=name, expectedLifeSpan=expectedLifeSpan)
        if imageUrl:
            at.image = imageUrl
        self.assetPlus.assetTypes.append(at)

    def updateAssetType(self, oldName: str, newName: str, newSpan: int, newImageUrl: str = None) -> None:
        self._is_string_valid(newName, "name", "must not")
        self._is_greater_than_zero(newSpan, "The expected life span must be greater than 0 days")
        old = self._get_asset_type(oldName)
        if old is None:
            raise ValueError("The asset type does not exist")
        if oldName != newName and self._get_asset_type(newName) is not None:
            raise ValueError("The asset type already exists")
        self._is_valid_image_url(newImageUrl)
        old.name = newName
        old.expectedLifeSpan = newSpan
        old.image = newImageUrl or ""

    def deleteAssetType(self, name: str) -> None:
        self._is_string_valid(name, "name", "must not")
        at = self._get_asset_type(name)
        if at is not None:
            for a in list(at.specificAssets):
                self.deleteAsset(a.assetNumber)
            at.delete()


    def addAsset(self, assetNumber: int, assetTypeName: str, purchaseDate: date, floorNumber: int, roomNumber: int) -> None:
        if assetNumber < 0:
            raise ValueError("Error: the number from assetNumber must be greater than or equal to 0.\n")
        if assetNumber < 1:
            raise ValueError("The asset number shall not be less than 1")
        if floorNumber < 0:
            raise ValueError("The floor number shall not be less than 0")
        if roomNumber < -1:
            raise ValueError("The room number shall not be less than -1")
        self._is_existing_asset_type(assetTypeName)
        if self._get_specific_asset(assetNumber) is not None:
            raise ValueError("The asset number already exists")
        at = self._get_asset_type(assetTypeName)
        asset = SpecificAsset(
            assetNumber=assetNumber,
            floorNumber=floorNumber,
            roomNumber=roomNumber,
            purchaseDate=self._to_edate(purchaseDate),
            assetType=at,
        )
        self.assetPlus.specificAssets.append(asset)

    def updateAsset(self, assetNumber: int, newAssetTypeName: str, newPurchaseDate: date, newFloorNumber: int, newRoomNumber: int) -> None:
        a = self._get_specific_asset(assetNumber)
        if a is None:
            raise ValueError(f"Asset with asset number {assetNumber} does not exist")
        if newFloorNumber < 0:
            raise ValueError("The floor number shall not be less than 0")
        if newRoomNumber < -1:
            raise ValueError("The room number shall not be less than -1")
        at = self._get_asset_type(newAssetTypeName)
        if at is None:
            raise ValueError("The asset type does not exist")
        a.assetType = at
        a.purchaseDate = self._to_edate(newPurchaseDate)
        a.floorNumber = newFloorNumber
        a.roomNumber = newRoomNumber

    def deleteAsset(self, asset_number: int) -> None:
        a = self._get_specific_asset(asset_number)
        if a is not None:
            for t in list(a.maintenanceTickets):
                t.delete()
            a.delete()
        return None


    def addMaintenanceTicket(self, id: int, ticketRaiser: str, raisedOn: date, description: str, assetNumber: int) -> None:
        if id < 0:
            raise ValueError("Error: the number from Ticket id must be greater than or equal to 0.\n")
        if self._get_ticket(id) is not None:
            raise ValueError("Ticket id already exists")
        self._is_description_empty(description)
        self._is_string_valid(ticketRaiser, "Email", "cannot")
        self._is_existing_user(ticketRaiser, "ticket raiser")
        asset = None
        if assetNumber is not None:
            asset = self._get_specific_asset(int(assetNumber))
            if asset is None:
                raise ValueError("The asset does not exist")
        raiser = self._get_user(ticketRaiser)
        t = MaintenanceTicket(id=id, raisedOnDate=self._to_edate(raisedOn), description=description, ticketRaiser=raiser, asset=asset)
        self.assetPlus.maintenanceTickets.append(t)

    def updateMaintenanceTicket(self, id: int, ticketRaiserEmail: str, raisedOnDate: date, description: str, assetNumber: int):
        ticket = self._get_ticket(id)
        if ticket is None:
            raise ValueError("The maintenance ticket does not exist")
        raiser = self._get_user(ticketRaiserEmail)
        if raiser is None:
            raise ValueError("The ticket raiser does not exist")
        if description is None or str(description) == "":
            raise ValueError("Ticket description cannot be empty")
        asset = None
        if assetNumber is not None:
            asset = self._get_specific_asset(int(assetNumber))
            if asset is None:
                raise ValueError("The asset does not exist")
        ticket.ticketRaiser = raiser
        ticket.raisedOnDate = self._to_edate(raisedOnDate)
        ticket.description = description
        if assetNumber is None:
            ticket.asset = None
        else:
            ticket.asset = asset
        return None

    def deleteMaintenanceTicket(self, id: int) -> None:
        ticket = self._get_ticket(id)
        if ticket is None:
            return None
        ticket.delete()
        return None

    def addTicketImage(self, ticketId: int, imageUrl: str) -> None:
        self._is_greater_or_equal_zero(ticketId, "ticketID")
        if imageUrl is None or imageUrl == "":
            raise ValueError("Image URL cannot be empty")
        self._is_valid_image_url(imageUrl)
        t = self._get_ticket(ticketId)
        if t is None:
            raise ValueError("Ticket does not exist")
        for img in list(t.ticketImages):
            if img.imageURL == imageUrl:
                raise ValueError("Image already exists for the ticket")
        ti = TicketImage(imageURL=imageUrl, ticket=t)
        t.ticketImages.append(ti)
        return None

    def deleteTicketImage(self, ticketId: int, imageUrl: str) -> None:
        self._is_greater_or_equal_zero(ticketId, "ticketID")
        self._is_string_valid(imageUrl, "imageURL", "cannot")
        t = self._get_ticket(ticketId)
        if t is None:
            return None
        for img in list(t.ticketImages):
            if img.imageURL == imageUrl:
                try:
                    t.ticketImages.remove(img)
                except ValueError:
                    pass
                return None
        return None

    def addMaintenanceNote(self, ticketId: int, noteTaker: str, addedOn: date, description: str) -> None:
        self._is_description_empty(description)
        self._is_existing_ticket(ticketId)
        if noteTaker == "":
            raise ValueError("The Email cannot be empty")
        self._is_existing_user(noteTaker, "hotel staff")
        t = self._get_ticket(ticketId)
        staff = self._get_user(noteTaker)
        if t is None:
            raise ValueError("Ticket does not exist")
        if staff is None:
            raise ValueError("Hotel staff does not exist")
        note = MaintenanceNote(date=self._to_edate(addedOn), description=description, noteTaker=staff, ticket=t)
        t.ticketNotes.append(note)

    def updateMaintenanceNote(self, ticketId: int, noteIndex: int, newTaker: str, newDate: date, newDescription: str) -> None:
        self._is_description_empty(newDescription)
        self._is_existing_ticket(ticketId)
        self._is_existing_user(newTaker, "hotel staff")
        t = self._get_ticket(ticketId)
        if t is None:
            raise ValueError("Ticket does not exist")
        if noteIndex < 0:
            raise ValueError("Note does not exist")
        try:
            note = t.ticketNotes[noteIndex]
        except Exception:
            raise ValueError("Note does not exist")
        staff = self._get_user(newTaker)
        if staff is None:
            raise ValueError("Hotel staff does not exist")
        note.date = self._to_edate(newDate)
        note.description = newDescription
        note.noteTaker = staff

    def deleteMaintenanceNote(self, ticketId: int, noteIndex: int) -> None:
        t = self._get_ticket(ticketId)
        if t is None or noteIndex < 0:
            return None
        try:
            notes = list(t.ticketNotes)
            note = notes[noteIndex]
            note.delete()
        except Exception:
            pass
        return None

    def viewStatusOfMaintenanceTickets(self) -> List[TOMaintenanceTicket]:
        result: List[TOMaintenanceTicket] = []
        for t in list(self.assetPlus.maintenanceTickets):
            raiser = t.ticketRaiser if hasattr(t, "ticketRaiser") else None
            raisedByEmail = raiser.email if raiser is not None else None
            status = getattr(t, "status", None)
            fixedByEmail = None
            fixer = getattr(t, "ticketFixer", None)
            if fixer is not None and hasattr(fixer, "email"):
                fixedByEmail = fixer.email
            timeToResolve = t.timeToResolve if t.eIsSet("timeToResolve") else None
            priority = t.priority if t.eIsSet("priority") else None
            approvalRequired = getattr(t, "approvalRequired", None)
            assetName = None
            expectedLifeSpan = None
            purchaseDate = None
            floorNumber = None
            roomNumber = None
            asset = getattr(t, "asset", None)
            if asset is not None:
                at = getattr(asset, "assetType", None)
                assetName = at.name if at is not None else None
                expectedLifeSpan = at.expectedLifeSpan if at is not None else None
                purchaseDate = getattr(asset, "purchaseDate", None)
                floorNumber = getattr(asset, "floorNumber", None)
                roomNumber = getattr(asset, "roomNumber", None)
            to_ticket = TOMaintenanceTicket(
                id=t.id,
                raisedOnDate=t.raisedOnDate,
                description=t.description,
                raisedByEmail=raisedByEmail,
                status=status,
                fixedByEmail=fixedByEmail,
                timeToResolve=timeToResolve,
                priority=priority,
                approvalRequired=approvalRequired if approvalRequired is not None else False,
                assetName=assetName,
                expectedLifeSpanInDays=expectedLifeSpan if expectedLifeSpan is not None else 0,
                purchaseDate=purchaseDate,
                floorNumber=floorNumber if floorNumber is not None else 0,
                roomNumber=roomNumber if roomNumber is not None else 0,
            )
            for img in list(t.ticketImages):
                to_ticket.imageURLs.append(img.imageURL)
            for note in list(t.ticketNotes):
                to_ticket.noteDates.append(note.date)
                to_ticket.noteDescriptions.append(note.description)
                nt = note.noteTaker
                to_ticket.noteTakerEmails.append(nt.email if nt is not None else None)
            result.append(to_ticket)
        return result
