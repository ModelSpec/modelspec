from datetime import datetime
import uuid

from ..generated_model_layer import *

class HomeForTheElderlyController:
    def __init__(self):
        self.homeForTheElderly = HomeForTheElderly()

    def createPerson(self, name: str, birthdate: datetime) -> None:
        if not name:
            raise ValueError("The name of a person must not be empty.")
        if not birthdate:
            raise ValueError("The birthdate of a person must not be empty.")
        if birthdate.date() > datetime.now().date():
            raise ValueError("The birthdate of a person must not be in the future.")
        
        id = str(uuid.uuid4())

        person = self.homeForTheElderly.addPeople(id, name, birthdate)
        person.setRegistrationDate(datetime.today())
        person.setAbilities("")
        
        return
    
    def createProposal(self, bedNumber: int, roomNumber: int, department: str, person: str) -> None:
        if not roomNumber:
            raise ValueError("Room cannot be empty.")
        if not bedNumber:
            raise ValueError("Bed cannot be empty.")
        if not person:
            raise ValueError("Person cannot be empty.")
        
        per = Person.getWithId(person)
        if per is None:
            raise ValueError(f"Person \"{person}\" does not exist.")
        
        room = None
        dep = Department.getWithId(department)
        if dep is None:
            raise ValueError(f"Department \"{department}\" does not exist.")
        
        for r in dep.getRooms():
            if r.getRoomNumber() == roomNumber:
                room = r
                break
        
        if room is None:
            raise ValueError(f"Room {roomNumber} of department {department} does not exist.")
        
        bed = None
        for b in room.getBeds():
            if b.getBedNumber() == bedNumber:
                bed = b
                break
        
        if bed is None:
            raise ValueError(f"Bed \"bed{bedNumber}\" does not exist.")
        
        per.addProposal("waiting", False, bed)
        return

    def createStay(self, bedNumber: int, roomNumber: int, department: str, person: str, intakeDate: datetime = None) -> None:
        if not roomNumber:
            raise ValueError("Room cannot be empty.")
        if not bedNumber:
            raise ValueError("Bed cannot be empty.")
        if not person:
            raise ValueError("Person cannot be empty.")
        
        per = Person.getWithId(person)
        if per is None:
            raise ValueError(f"Person \"{person}\" does not exist.")
        
        room = None
        dep = Department.getWithId(department)
        if dep is None:
            raise ValueError(f"Department \"{department}\" does not exist.")
        
        for r in dep.getRooms():
            if r.getRoomNumber() == roomNumber:
                room = r
                break
        
        if room is None:
            raise ValueError(f"Room {roomNumber} of department {department} does not exist.")
        
        bed = None
        for b in room.getBeds():
            if b.getBedNumber() == bedNumber:
                bed = b
                break
        
        if bed is None:
            raise ValueError(f"Bed {bedNumber} of room {roomNumber} of department \"{department}\" does not exist.")
        
        if intakeDate.date() < datetime.now().date():
            raise ValueError("Intake date must be on or after the current date.")
        
        if per.numberOfProposals() == 0:
            raise ValueError(f"Cannot create stay for \"{person}\" without a proposal.")
        
        per.addStay1(intakeDate, None, bed)

        return
    
    def updateInvoice(self, person: str, invoiceDate: datetime, newOutstandingAmount: float) -> None:
        per = Person.getWithId(person)
        if per is None:
            raise ValueError(f'Person "{person}" does not exist.')

        invoice = None
        for inv in per.getInvoices():
            invDate = inv.getInvoiceDate()
            if invoiceDate.date() == invDate.date():
                invoice = inv
                break

        if invoice is None:
            raise ValueError(
                f'Invoice for person "{person}" with invoiceDate "{invoiceDate.date()}" does not exist.'
            )

        if invoice.getStatus() == "paid":
            raise ValueError("Cannot update paid invoice.")

        invoice.setOutstandingAmount(newOutstandingAmount)

        if newOutstandingAmount <= 0:
            invoice.setStatus("paid")
        else:
            invoice.setStatus("active")

        return
    
    def updatePersonAbilities(self, person: str, abilities: str) -> None:
        per = Person.getWithId(person)
        if per is None:
            raise ValueError(f'Person with ID "{person}" does not exist.')

        per.setAbilities(abilities)
        return
    
    def updateProposal(self, bedNumber: int, roomNumber: int, department: str, person: str, status: str = None, validated: bool = None, newBedNumber: int = None, newRoomNumber: int = None, newDepartment: str = None, newPerson: str = None) -> None:
        dep = Department.getWithId(department)
        if dep is None:
            raise ValueError(f'Department "{department}" does not exist.')

        room = None
        for r in dep.getRooms():
            if r.getRoomNumber() == roomNumber:
                room = r
                break
        if room is None:
            raise ValueError(f"Room {roomNumber} of department {department} does not exist.")

        bed = None
        for b in room.getBeds():
            if b.getBedNumber() == bedNumber:
                bed = b
                break
        if bed is None:
            raise ValueError(f"Bed {bedNumber} of room {roomNumber} of department \"{department}\" does not exist.")

        proposal = None
        for prop in bed.getProposals():
            if (
                prop.getBed().getBedNumber() == bedNumber
                and prop.getBed().getRoom().getRoomNumber() == roomNumber
                and prop.getBed().getRoom().getDepartment().getId() == department
                and prop.getPerson().getId() == person
            ):
                proposal = prop
                break

        if proposal is None:
            raise ValueError(f'Proposal for bed {bedNumber} of room {roomNumber} of department "{department}" to person "{person}" does not exist.')

        if status is not None:
            if status == "":
                raise ValueError("The status of a proposal must not be empty.")
            if status not in ["waiting", "accepted", "refused", "invalidated"]:
                raise ValueError("The status of a proposal must be one of: waiting, accepted, refused, invalidated.")
            proposal.setStatus(status)

        if validated is not None:
            proposal.setValidated(validated)

        if newBedNumber is not None:
            newDep = dep
            newRoom = room

            if newDepartment is not None:
                newDep = Department.getWithId(newDepartment)
                if newDep is None:
                    raise ValueError(f'Department "{newDepartment}" does not exist.')

            if newRoomNumber is not None:
                newRoom = None
                for r in newDep.getRooms():
                    if r.getRoomNumber() == newRoomNumber:
                        newRoom = r
                        break
                if newRoom is None:
                    raise ValueError(f"Room {newRoomNumber} of department {newDep.getId()} does not exist.")

            newBed = None
            for b in newRoom.getBeds():
                if b.getBedNumber() == newBedNumber:
                    newBed = b
                    break

            if newBed is None:
                raise ValueError(f'Bed {newBedNumber} of room {newRoom.getRoomNumber()} of department "{newDep.getId()}" does not exist.')

            proposal.setBed(newBed)

        if newPerson is not None:
            newPer = Person.getWithId(newPerson)
            if newPer is None:
                raise ValueError(f'Person "{newPerson}" does not exist.')
            proposal.setPerson(newPer)

        return
    
    def updateStay(self, bedNumber: int, roomNumber: int, department: str, person: str, intakeDate: datetime = None, endDate: datetime = None) -> None:
        if not roomNumber:
            raise ValueError("Room cannot be empty.")
        if not bedNumber:
            raise ValueError("Bed cannot be empty.")
        if not person:
            raise ValueError("Person cannot be empty.")
        
        per = Person.getWithId(person)
        if per is None:
            raise ValueError(f"Person \"{person}\" does not exist.")
        
        room = None
        dep = Department.getWithId(department)
        if dep is None:
            raise ValueError(f"Department \"{department}\" does not exist.")
        
        for r in dep.getRooms():
            if r.getRoomNumber() == roomNumber:
                room = r
                break
        
        if room is None:
            raise ValueError(f"Room {roomNumber} of department {department} does not exist.")
        
        bed = None
        for b in room.getBeds():
            if b.getBedNumber() == bedNumber:
                bed = b
                break
        
        if bed is None:
            raise ValueError(f"Bed {bedNumber} of room {roomNumber} of department \"{department}\" does not exist.")
        
        stay = None
        for s in bed.getStaies():
            if s.getPerson().getId() == person:
                stay = s
                break

        if stay is None:
            raise ValueError(f"Stay for person \"{person}\" and bed {bedNumber} of room {roomNumber} of department \"{department}\" does not exist.")
        
        # None means "no change"; an empty string means an empty value
        if intakeDate is not None:
            if intakeDate == "":
                raise ValueError("Intake date must not be empty.")
            if intakeDate.date() < datetime.now().date():
                raise ValueError("Intake date must be on or after the current date.")
            stay.setIntakeDate(intakeDate)

        if endDate is not None:
            stay.setEndDate(None if endDate == "" else endDate)

        return