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

        person = Person(id=id, name=name, birthdate=birthdate, registrationDate=datetime.today(), abilities="", homeForTheElderly=self.homeForTheElderly)
        self.homeForTheElderly.people.append(person)
        return
    
    def createProposal(self, bedNumber: int, roomNumber: int, department: str, person: str) -> None:
        if not roomNumber:
            raise ValueError("Room cannot be empty.")
        if not bedNumber:
            raise ValueError("Bed cannot be empty.")
        if not person:
            raise ValueError("Person cannot be empty.")
        
        per = None
        for p in self.homeForTheElderly.people:
            if p.id == person:
                per = p
                break
        if per is None:
            raise ValueError(f"Person \"{person}\" does not exist.")
        
        room = None
        dep = None
        for d in self.homeForTheElderly.departments:
            if d.id == department:
                dep = d
                break
        if dep is None:
            raise ValueError(f"Department \"{department}\" does not exist.")
        
        for r in dep.rooms:
            if r.roomNumber == roomNumber:
                room = r
                break
        
        if room is None:
            raise ValueError(f"Room {roomNumber} of department {department} does not exist.")
        
        bed = None
        for b in room.beds:
            if b.bedNumber == bedNumber:
                bed = b
                break
        
        if bed is None:
            raise ValueError(f"Bed \"bed{bedNumber}\" does not exist.")
        
        Proposal(status="waiting", validated=False, bed=bed, person=per)
        return

    def createStay(self, bedNumber: int, roomNumber: int, department: str, person: str, intakeDate: datetime = None) -> None:
        if not roomNumber:
            raise ValueError("Room cannot be empty.")
        if not bedNumber:
            raise ValueError("Bed cannot be empty.")
        if not person:
            raise ValueError("Person cannot be empty.")
        
        per = None
        for p in self.homeForTheElderly.people:
            if p.id == person:
                per = p
                break
        if per is None:
            raise ValueError(f"Person \"{person}\" does not exist.")
        
        room = None
        dep = None
        for d in self.homeForTheElderly.departments:
            if d.id == department:
                dep = d
                break
        if dep is None:
            raise ValueError(f"Department \"{department}\" does not exist.")
        
        for r in dep.rooms:
            if r.roomNumber == roomNumber:
                room = r
                break
        
        if room is None:
            raise ValueError(f"Room {roomNumber} of department {department} does not exist.")
        
        bed = None
        for b in room.beds:
            if b.bedNumber == bedNumber:
                bed = b
                break
        
        if bed is None:
            raise ValueError(f"Bed {bedNumber} of room {roomNumber} of department \"{department}\" does not exist.")
        
        if intakeDate.date() < datetime.now().date():
            raise ValueError("Intake date must be on or after the current date.")
        
        if len(per.proposals) == 0:
            raise ValueError(f"Cannot create stay for \"{person}\" without a proposal.")
        
        stay = Stay(intakeDate=intakeDate, bed=bed, person=per)
        per.staies.append(stay)

        return
    
    def updateInvoice(self, person: str, invoiceDate: datetime, newOutstandingAmount: float) -> None:
        per = None
        for p in self.homeForTheElderly.people:
            if p.id == person:
                per = p
                break
        if per is None:
            raise ValueError(f'Person "{person}" does not exist.')

        invoice = None
        for inv in per.invoices:
            invDate = inv.invoiceDate
            if invoiceDate.date() == invDate.date():
                invoice = inv
                break

        if invoice is None:
            raise ValueError(
                f'Invoice for person "{person}" with invoiceDate "{invoiceDate.date()}" does not exist.'
            )

        if invoice.status == "paid":
            raise ValueError("Cannot update paid invoice.")

        invoice.outstandingAmount = newOutstandingAmount

        if newOutstandingAmount <= 0:
            invoice.status = "paid"
        else:
            invoice.status = "active"

        return
    
    def updatePersonAbilities(self, person: str, abilities: str) -> None:
        per = None
        for p in self.homeForTheElderly.people:
            if p.id == person:
                per = p
                break
        if per is None:
            raise ValueError(f'Person with ID "{person}" does not exist.')

        per.abilities = abilities
        return
    
    def updateProposal(self, bedNumber: int, roomNumber: int, department: str, person: str, status: str = None, validated: bool = None, newBedNumber: int = None, newRoomNumber: int = None, newDepartment: str = None, newPerson: str = None) -> None:
        dep = None
        for d in self.homeForTheElderly.departments:
            if d.id == department:
                dep = d
                break
        if dep is None:
            raise ValueError(f'Department "{department}" does not exist.')

        room = None
        for r in dep.rooms:
            if r.roomNumber == roomNumber:
                room = r
                break
        if room is None:
            raise ValueError(f"Room {roomNumber} of department {department} does not exist.")

        bed = None
        for b in room.beds:
            if b.bedNumber == bedNumber:
                bed = b
                break
        if bed is None:
            raise ValueError(f"Bed {bedNumber} of room {roomNumber} of department \"{department}\" does not exist.")

        proposal = None
        for prop in bed.proposals:
            if (
                prop.bed.bedNumber == bedNumber
                and prop.bed.room.roomNumber == roomNumber
                and prop.bed.room.department.id == department
                and prop.person.id == person
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
            proposal.status = status

        if validated is not None:
            proposal.validated = validated

        if newBedNumber is not None:
            newDep = dep
            newRoom = room

            if newDepartment is not None:
                newDep = None
                for d in self.homeForTheElderly.departments:
                    if d.id == newDepartment:
                        newDep = d
                        break
                if newDep is None:
                    raise ValueError(f'Department "{newDepartment}" does not exist.')

            if newRoomNumber is not None:
                newRoom = None
                for r in dep.rooms:
                    if r.roomNumber == newRoomNumber:
                        newRoom = r
                        break
                if newRoom is None:
                    raise ValueError(f"Room {newRoomNumber} of department {newDep.id} does not exist.")
            
            if newBedNumber is not None:
                newBed = None
                for b in room.beds:
                    if b.bedNumber == newBedNumber:
                        newBed = b
                        break

            if newBed is None:
                raise ValueError(f'Bed {newBedNumber} of room {newRoom.roomNumber} of department "{newDep.id}" does not exist.')

            proposal.bed = newBed

        if newPerson is not None:
            newPer = None
            oldPer = proposal.person
            for p in self.homeForTheElderly.people:
                if p.id == newPerson:
                    newPer = p
                    break
            if newPer is None:
                raise ValueError(f'Person "{newPerson}" does not exist.')

            oldPer.proposals.remove(proposal)
            proposal.person = newPer
            newPer.proposals.append(proposal)
        return
    
    def updateStay(self, bedNumber: int, roomNumber: int, department: str, person: str, intakeDate: datetime = None, endDate: datetime = None) -> None:
        if not roomNumber:
            raise ValueError("Room cannot be empty.")
        if not bedNumber:
            raise ValueError("Bed cannot be empty.")
        if not person:
            raise ValueError("Person cannot be empty.")
        
        per = None
        for p in self.homeForTheElderly.people:
            if p.id == person:
                per = p
                break
        if per is None:
            raise ValueError(f"Person \"{person}\" does not exist.")
        
        room = None
        dep = None
        for d in self.homeForTheElderly.departments:
            if d.id == department:
                dep = d
                break
        if dep is None:
            raise ValueError(f"Department \"{department}\" does not exist.")
        
        for r in dep.rooms:
            if r.roomNumber == roomNumber:
                room = r
                break
        
        if room is None:
            raise ValueError(f"Room {roomNumber} of department {department} does not exist.")
        
        bed = None
        for b in room.beds:
            if b.bedNumber == bedNumber:
                bed = b
                break
        
        if bed is None:
            raise ValueError(f"Bed {bedNumber} of room {roomNumber} of department \"{department}\" does not exist.")
        
        stay = None
        for s in bed.staies:
            if s.person.id == person:
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
            stay.intakeDate = intakeDate

        if endDate is not None:
            stay.endDate = None if endDate == "" else endDate

        return