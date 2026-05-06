from ..generated_model_layer.BikeTourPlus import BikeTourPlus
from ..generated_model_layer.BikeTour import BikeTour
from ..generated_model_layer.Combo import Combo
from ..generated_model_layer.Gear import Gear
from ..generated_model_layer.BookedItem import BookedItem
from ..generated_model_layer.ComboItem import ComboItem
from ..generated_model_layer.Participant import Participant
from datetime import date

class BikeTourPlusController:
    def __init__(self) -> None:
        self.btp = BikeTourPlus(None, 0, 0)

    def addCombo(self, name: str, discount: int) -> None:
        if not name or name.strip() == "":
            raise ValueError("The name must not be empty")

        if discount < 0:
            raise ValueError("Discount must be at least 0")

        if discount > 100:
            raise ValueError("Discount must be no more than 100")

        if any(g.getName() == name for g in self.btp.getGear()):
            raise ValueError("A piece of gear with the same name already exists")

        if any(c.getName() == name for c in self.btp.getCombos()):
            raise ValueError("A combo with the same name already exists")

        self.btp.addCombo(name, discount)

    def addGear(self, name: str, pricePerWeek: int) -> None:
        if pricePerWeek < 0:
            raise ValueError("The price per week must be greater than or equal to 0")

        if not name or name.strip() == "":
            raise ValueError("The name must not be empty")

        if any(g.getName() == name for g in self.btp.getGear()):
            raise ValueError("A piece of gear with the same name already exists")

        if any(c.getName() == name for c in self.btp.getCombos()):
            raise ValueError("A combo with the same name already exists")

        self.btp.addGear(name, pricePerWeek)

    def deleteCombo(self, name: str) -> None:
        combo = None
        for c in self.btp.getCombos():
            if c.getName() == name:
                combo = c
                break

        if combo is None:
            return

        for participant in self.btp.getParticipants():
            bookedItems = participant.getBookedItems()
            itemsToRemove = []
            for bookedItem in bookedItems:
                item = bookedItem.getItem()
                if isinstance(item, Combo) and item.getName() == name:
                    itemsToRemove.append(bookedItem)

            for itemToRemove in itemsToRemove:
                participant.removeBookedItem(itemToRemove)

        self.btp.removeCombo(combo)
        combo.delete()

    def deleteGear(self, name: str) -> None:
        gear = None
        for g in self.btp.getGear():
            if g.getName() == name:
                gear = g
                break

        if gear is None:
            return

        for combo in self.btp.getCombos():
            for comboItem in combo.getComboItems():
                if comboItem.getGear().getName() == name:
                    raise ValueError("The piece of gear is in a combo and cannot be deleted")

        for participant in self.btp.getParticipants():
            itemsToRemove = []
            for bookedItem in participant.getBookedItems():
                item = bookedItem.getItem()
                if isinstance(item, Gear) and item.getName() == name:
                    itemsToRemove.append(bookedItem)
            for bi in itemsToRemove:
                participant.removeBookedItem(bi)

        self.btp.removeGear(gear)
        gear.delete()

    def deleteGuide(self, email: str) -> None:
        guide = None
        for g in self.btp.getGuides():
            if g.getEmail() == email:
                guide = g
                break

        if guide is None:
            for p in self.btp.getParticipants():
                if p.getEmail() == email:
                    return
            if email == "manager@btp.com":
                return
            return

        guide.delete()

    def deleteParticipant(self, email: str) -> None:
        participant = None
        for p in self.btp.getParticipants():
            if p.getEmail() == email:
                participant = p
                break

        if participant is None:
            for g in self.btp.getGuides():
                if g.getEmail() == email:
                    return
            if email == "manager@btp.com":
                return
            return

        bookedItems = list(participant.getBookedItems())
        for bi in bookedItems:
            participant.removeBookedItem(bi)

        participant.delete()

    def addGearOrComboToParticipant(self, name: str, email: str) -> None:
        # find participant
        participant = None
        for p in self.btp.getParticipants():
            if p.getEmail() == email:
                participant = p
                break

        if participant is None:
            raise ValueError("The participant does not exist")

        # find gear
        item = None
        for g in self.btp.getGear():
            if g.getName() == name:
                item = g
                break

        # find combo
        if item is None:
            for c in self.btp.getCombos():
                if c.getName() == name:
                    item = c
                    break

        if item is None:
            raise ValueError("The piece of gear or combo does not exist")

        for bookedItem in participant.getBookedItems():
            if bookedItem.getItem() == item:
                bookedItem.setQuantity(bookedItem.getQuantity() + 1)
                return
        participant.addBookedItem(1, self.btp, item)

    def addGearToCombo(self, gearName: str, comboName: str) -> None:
        # find combo
        combo = None
        for c in self.btp.getCombos():
            if c.getName() == comboName:
                combo = c
                break

        if combo is None:
            raise ValueError("The combo does not exist")

        # find gear
        gear = None
        for g in self.btp.getGear():
            if g.getName() == gearName:
                gear = g
                break

        if gear is None:
            raise ValueError("The piece of gear does not exist")

        for item in combo.getComboItems():
            if item.getGear() == gear:
                item.setQuantity(item.getQuantity() + 1)
                return
        combo.addComboItem(1, self.btp, gear)


    def registerGuide(self, email: str, password: str, name: str, emergencyContact: str) -> None:
        if not email or email.strip() == "":
            raise ValueError("Email cannot be empty")

        if not password or password.strip() == "":
            raise ValueError("Password cannot be empty")

        if not name or name.strip() == "":
            raise ValueError("Name cannot be empty")

        if not emergencyContact or emergencyContact.strip() == "":
            raise ValueError("Emergency contact cannot be empty")

        if " " in email:
            raise ValueError("Email must not contain any spaces")

        if email == "manager@btp.com":
            raise ValueError("Email cannot be manager@btp.com")

        for g in self.btp.getGuides():
            if g.getEmail() == email:
                raise ValueError("Email already linked to a guide account")

        for p in self.btp.getParticipants():
            if p.getEmail() == email:
                raise ValueError("Email already linked to a participant account")

        if email.count("@") != 1:
            raise ValueError("Invalid email")

        username, domainPart = email.split("@")

        invalidEmail = (
                not username or
                not domainPart or
                "." not in domainPart or
                domainPart.startswith(".") or
                domainPart.endswith(".")
        )

        if invalidEmail:
            raise ValueError("Invalid email")

        # create guide
        self.btp.addGuide(email, password, name, emergencyContact)

    def registerParticipant(
        self,
        email: str,
        password: str,
        name: str,
        emergencyContact: str,
        nrWeeks: int,
        weeksAvailableFrom: int,
        weeksAvailableUntil: int,
        lodgeRequired: bool
    ) -> None:
        if not email or email.strip() == "":
            raise ValueError("Email cannot be empty")

        if not password or password.strip() == "":
            raise ValueError("Password cannot be empty")

        if not name or name.strip() == "":
            raise ValueError("Name cannot be empty")

        if not emergencyContact or emergencyContact.strip() == "":
            raise ValueError("Emergency contact cannot be empty")

        if " " in email:
            raise ValueError("Email must not contain any spaces")

        if email == "manager@btp.com":
            raise ValueError("Email cannot be manager@btp.com")

        for g in self.btp.getGuides():
            if g.getEmail() == email:
                raise ValueError("Email already linked to a guide account")

        for p in self.btp.getParticipants():
            if p.getEmail() == email:
                raise ValueError("Email already linked to a participant account")

        if email.count("@") != 1:
            raise ValueError("Invalid email")

        username, domainPart = email.split("@")
        invalidEmail = (
            not username or
            not domainPart or
            "." not in domainPart or
            domainPart.startswith(".") or
            domainPart.endswith(".")
        )
        if invalidEmail:
            raise ValueError("Invalid email")

        if nrWeeks <= 0:
            raise ValueError("Number of weeks must be greater than zero")

        seasonWeeks = self.btp.getNrWeeks()
        if nrWeeks > seasonWeeks:
            raise ValueError(
                "Number of weeks must be less than or equal to the number of biking weeks in the biking season"
            )

        if (
                weeksAvailableFrom < 1 or
                weeksAvailableFrom > seasonWeeks or
                weeksAvailableUntil < 1 or
                weeksAvailableUntil > seasonWeeks
        ):
            raise ValueError(
                f"Available weeks must be within weeks of biking season (1-{seasonWeeks})"
            )
        if weeksAvailableFrom > weeksAvailableUntil:
            raise ValueError(
                "Week from which one is available must be less than or equal to the week until which one is available"
            )

        availableWeeks = weeksAvailableUntil - weeksAvailableFrom + 1
        if nrWeeks > availableWeeks:
            raise ValueError(
                "Number of weeks must be less than or equal to the number of available weeks"
            )

        self.btp.addParticipant(
            email,
            password,
            name,
            emergencyContact,
            nrWeeks,
            weeksAvailableFrom,
            weeksAvailableUntil,
            lodgeRequired,
            "None",
            0
        )

    def removeGearFromCombo(self, gearName: str, comboName: str) -> None:
        combo = None
        for c in self.btp.getCombos():
            if c.getName() == comboName:
                combo = c
                break

        if combo is None:
            raise ValueError("The combo does not exist")

        itemInCombo = None
        for item in combo.getComboItems():
            if item.getGear().getName() == gearName:
                itemInCombo = item
                break

        if itemInCombo is None:
            return

        numberOfGearTypes = len(combo.getComboItems())

        typesAfterRemoval = numberOfGearTypes if itemInCombo.getQuantity() > 1 else numberOfGearTypes - 1

        if typesAfterRemoval < 2:
            raise ValueError("A combo must have at least two pieces of gear")

        if itemInCombo.getQuantity() > 1:
            itemInCombo.setQuantity(itemInCombo.getQuantity() - 1)
        else:
            itemInCombo.delete()

    def removeGearOrComboFromParticipant(self, name: str, email: str) -> None:
        participant = None
        for p in self.btp.getParticipants():
            if p.getEmail() == email:
                participant = p
                break

        if participant is None:
            raise ValueError("The participant does not exist")

        itemForParticipant = None
        for bookedItem in participant.getBookedItems():
            item = bookedItem.getItem()
            if item.getName() == name:
                itemForParticipant = bookedItem
                break

        if itemForParticipant is None:
            return

        if itemForParticipant.getQuantity() > 1:
            itemForParticipant.setQuantity(itemForParticipant.getQuantity() - 1)
        else:
            itemForParticipant.delete()

    def updateBikeTourPlus(
            self,
            startDate: date,
            nrWeeks: int,
            priceOfGuidePerWeek: int,
    ) -> None:
        if nrWeeks < 0:
            raise ValueError(
                "The number of riding weeks must be greater than or equal to zero"
            )

        if priceOfGuidePerWeek < 0:
            raise ValueError(
                "The price of guide per week must be greater than or equal to zero"
            )

        if self.btp.getStartDate() is not None:
            if startDate.year < self.btp.getStartDate().year:
                raise ValueError(
                    "The start date cannot be from previous year or earlier"
                )

        self.btp.setStartDate(startDate)
        self.btp.setNrWeeks(nrWeeks)
        self.btp.setPriceOfGuidePerWeek(priceOfGuidePerWeek)

    def updateGear(self, oldName: str, newName: str, newPricePerWeek: int) -> None:
        gear = None
        for g in self.btp.getGear():
            if g.getName() == oldName:
                gear = g
                break

        if gear is None:
            raise ValueError("The piece of gear does not exist")

        if newPricePerWeek < 0:
            raise ValueError("The price per week must be greater than or equal to 0")

        if not newName or newName.strip() == "":
            raise ValueError("The name must not be empty")

        for g in self.btp.getGear():
            if g.getName() == newName and g is not gear:
                raise ValueError("A piece of gear with the same name already exists")

        for c in self.btp.getCombos():
            if c.getName() == newName:
                raise ValueError("A combo with the same name already exists")

        gear.setName(newName)
        gear.setPricePerWeek(newPricePerWeek)

    def updateCombo(self, oldName: str, newName: str, newDiscount: int) -> None:
        combo = None
        for c in self.btp.getCombos():
            if c.getName() == oldName:
                combo = c
                break

        if combo is None:
            raise ValueError("The combo does not exist")

        if newDiscount < 0:
            raise ValueError("Discount must be at least 0")

        if newDiscount > 100:
            raise ValueError("Discount must be no more than 100")

        if not newName or newName.strip() == "":
            raise ValueError("The name must not be empty")

        for g in self.btp.getGear():
            if g.getName() == newName:
                raise ValueError("A piece of gear with the same name already exists")

        for c in self.btp.getCombos():
            if c.getName() == newName and c is not combo:
                raise ValueError("A combo with the same name already exists")

        combo.setName(newName)
        combo.setDiscount(newDiscount)

    def updateGuide(self, email: str, newPassword: str, newName: str, newEmergencyContact: str) -> None:
        guide = None
        for g in self.btp.getGuides():
            if g.getEmail() == email:
                guide = g
                break

        if guide is None:
            raise ValueError("The guide account does not exist")

        if not newPassword or newPassword.strip() == "":
            raise ValueError("Password cannot be empty")

        if not newName or newName.strip() == "":
            raise ValueError("Name cannot be empty")

        if not newEmergencyContact or newEmergencyContact.strip() == "":
            raise ValueError("Emergency contact cannot be empty")

        guide.setPassword(newPassword)
        guide.setName(newName)
        guide.setEmergencyContact(newEmergencyContact)

    def updateManager(self, password: str) -> None:
        manager = self.btp.getManager()

        if manager is None:
            raise ValueError("Manager does not exist")

        if not password or password.strip() == "":
            raise ValueError("Password cannot be empty")

        if len(password) < 4:
            raise ValueError("Password must be at least four characters long")

        if not any(ch in "!#$" for ch in password):
            raise ValueError("Password must contain one character out of !#$")

        if not any(ch.islower() for ch in password):
            raise ValueError("Password must contain one lower-case character")

        if not any(ch.isupper() for ch in password):
            raise ValueError("Password must contain one upper-case character")

        manager.setPassword(password)

    def updateParticipant(
            self,
            email: str,
            newPassword: str,
            newName: str,
            newEmergencyContact: str,
            newNrWeeks: int,
            newWeeksAvailableFrom: int,
            newWeeksAvailableUntil: int,
            newLodgeRequired: bool,
    ) -> None:
        participant = None
        for p in self.btp.getParticipants():
            if p.getEmail() == email:
                participant = p
                break

        if participant is None:
            raise ValueError("The participant account does not exist")

        if not newPassword or newPassword.strip() == "":
            raise ValueError("Password cannot be empty")

        if not newName or newName.strip() == "":
            raise ValueError("Name cannot be empty")

        if not newEmergencyContact or newEmergencyContact.strip() == "":
            raise ValueError("Emergency contact cannot be empty")

        if newNrWeeks <= 0:
            raise ValueError("Number of weeks must be greater than zero")

        if newNrWeeks > self.btp.getNrWeeks():
            raise ValueError(
                "Number of weeks must be less than or equal to the number of biking weeks in the biking season"
            )

        if (
                newWeeksAvailableFrom < 1
                or newWeeksAvailableUntil < 1
                or newWeeksAvailableFrom > self.btp.getNrWeeks()
                or newWeeksAvailableUntil > self.btp.getNrWeeks()
        ):
            raise ValueError(
                f"Available weeks must be within weeks of biking season (1-{self.btp.getNrWeeks()})"
            )

        if newWeeksAvailableFrom > newWeeksAvailableUntil:
            raise ValueError(
                "Week from which one is available must be less than or equal to the week until which one is available"
            )

        availableWeeks = (
                newWeeksAvailableUntil - newWeeksAvailableFrom + 1
        )
        if newNrWeeks > availableWeeks:
            raise ValueError(
                "Number of weeks must be less than or equal to the number of available weeks"
            )

        participant.setPassword(newPassword)
        participant.setName(newName)
        participant.setEmergencyContact(newEmergencyContact)
        participant.setNrWeeks(newNrWeeks)
        participant.setWeekAvailableFrom(newWeeksAvailableFrom)
        participant.setWeekAvailableUntil(newWeeksAvailableUntil)
        participant.setLodgeRequired(newLodgeRequired)

    def processPay(self, email: str, code: str) -> None:
        participant = None
        for p in self.btp.getParticipants():
            if p.getEmail() == email:
                participant = p
                break

        if participant is None:
            raise ValueError(f"Participant with email address {email} does not exist")

        status = participant.getStatus()

        if status == Participant.Status.Banned:
            raise ValueError("Cannot pay for tour because the participant is banned")
        if status == Participant.Status.Cancelled:
            raise ValueError("Cannot pay for tour because the participant has cancelled their tour")
        if status == Participant.Status.NotAssigned:
            raise ValueError("The participant has not been assigned to their tour")

        if status in [Participant.Status.Paid, Participant.Status.Started, Participant.Status.Finished]:
            raise ValueError("The participant has already paid for their tour")

        if not code or code.strip() == "":
            raise ValueError("Invalid authorization code")

        participant.setAuthorizationCode(code)
        participant.setStatus(Participant.Status.Paid)

    def processStart(self, week: int) -> None:
        startWeek = int(week)
        participantsInWeek = set()

        for tour in self.btp.getBikeTours():
            if tour.getStartWeek() == startWeek:
                for p in tour.getParticipants():
                    participantsInWeek.add(p.getEmail())

        if not participantsInWeek:
            return

        for p in self.btp.getParticipants():
            if p.getEmail() in participantsInWeek:
                status = p.getStatus()
                if status == Participant.Status.Started:
                    raise ValueError("Cannot start tour because the participant has already started their tour")
                if status == Participant.Status.Banned:
                    raise ValueError("Cannot start tour because the participant is banned")
                if status == Participant.Status.Cancelled:
                    raise ValueError("Cannot start tour because the participant has cancelled their tour")
                if status == Participant.Status.Finished:
                    raise ValueError("Cannot start tour because the participant has finished their tour")

        for p in self.btp.getParticipants():
            if p.getEmail() in participantsInWeek:
                status = p.getStatus()
                if status == Participant.Status.Paid:
                    p.setStatus(Participant.Status.Started)
                elif status == Participant.Status.Assigned:
                    p.setStatus(Participant.Status.Banned)

    def processFinish(self, email: str) -> None:
        participant = None
        for p in self.btp.getParticipants():
            if p.getEmail() == email:
                participant = p
                break

        if participant is None:
            raise ValueError(f"Participant with email address {email} does not exist")

        status = participant.getStatus()

        if status == Participant.Status.Banned:
            raise ValueError("Cannot finish tour because the participant is banned")
        if status == Participant.Status.Cancelled:
            raise ValueError("Cannot finish tour because the participant has cancelled their tour")
        if status == Participant.Status.Finished:
            raise ValueError("Cannot finish tour because the participant has already finished their tour")

        if status != Participant.Status.Started:
            raise ValueError("Cannot finish a tour for a participant who has not started their tour")

        participant.setStatus(Participant.Status.Finished)
        participant.setRefundedPercentageAmount(0)

    def createBikeTours(self):
        participants = list(self.btp.getParticipants())
        guides = list(self.btp.getGuides())

        if not participants:
            return

        if not guides:
            for participant in participants:
                participant.setStatus(Participant.Status.NotAssigned)
            raise ValueError("At least one participant could not be assigned to their bike tour")

        for p in participants:
            p.setStatus(Participant.Status.NotAssigned)

        unassigned = list(participants)
        # continue after existing tours so that tour ids stay unique
        tourId = max((t.getId() for t in self.btp.getBikeTours()), default=0) + 1

        for guide in guides:
            for p in list(unassigned):
                if p.getStatus() == Participant.Status.Assigned:
                    unassigned.remove(p)
                    continue

                if self._tryJoinExistingTour(p):
                    unassigned.remove(p)
                    continue

                if self._createNewTourWithGuide(p, guide, tourId):
                    unassigned.remove(p)
                    tourId += 1

        for p in list(unassigned):
            if self._tryJoinExistingTour(p):
                unassigned.remove(p)

        if unassigned:
            raise ValueError("At least one participant could not be assigned to their bike tour")

    def _createNewTourWithGuide(self, participant, guide, tourId):
        startWeek = self._findEarliestSlot(guide, participant)
        if startWeek is None:
            return False

        endWeek = startWeek + participant.getNrWeeks() - 1
        self.btp.addBikeTour(tourId, startWeek, endWeek, guide)

        newTour = BikeTour.getWithId(tourId)
        newTour.addParticipant(participant)
        participant.setStatus(Participant.Status.Assigned)
        return True

    def _tryJoinExistingTour(self, participant):
        nrWeeks = participant.getNrWeeks()
        availFrom = participant.getWeekAvailableFrom()
        availUntil = participant.getWeekAvailableUntil()

        for tour in self.btp.getBikeTours():
            tourDuration = tour.getEndWeek() - tour.getStartWeek() + 1

            if (tourDuration == nrWeeks and
                    tour.getStartWeek() >= availFrom and
                    tour.getEndWeek() <= availUntil):
                tour.addParticipant(participant)
                participant.setStatus(Participant.Status.Assigned)
                return True

        return False


    def _findEarliestSlot(self, guide, participant):
        nrWeeks = participant.getNrWeeks()
        availFrom = participant.getWeekAvailableFrom()
        availUntil = participant.getWeekAvailableUntil()

        for start in range(availFrom, availUntil - nrWeeks + 2):
            end = start + nrWeeks - 1

            if self._guideIsFree(guide, start, end):
                return start

        return None

    def _guideIsFree(self, guide, start, end):
        for tour in self.btp.getBikeTours():
            if tour.getGuide() == guide:
                if not (end < tour.getStartWeek() or start > tour.getEndWeek()):
                    return False
        return True

    def viewBikeTour(self, tourId):
        if tourId < 1:
            raise ValueError("Invalid bike tour id")

        tour = BikeTour.getWithId(tourId)
        if tour is None:
            raise ValueError(f"Bike tour with id {tourId} does not exist")
        
        return tour

    def _itemsCostPerWeek(self, participant):
        total = 0.0

        for bookedItem in participant.getBookedItems():
            item = bookedItem.getItem()
            quantity = bookedItem.getQuantity()

            if isinstance(item, Combo):
                total += self._comboCost(item, participant.getLodgeRequired()) * quantity
            else:
                total += item.getPricePerWeek() * quantity

        return total

    def _comboCost(self, combo, lodgeRequired):
        baseCost = 0

        for comboItem in combo.getComboItems():
            gear = comboItem.getGear()
            price = gear.getPricePerWeek()
            quantity = comboItem.getQuantity()
            baseCost += price * quantity

        # the combo discount only applies when a lodge is also rented
        discountPercent = combo.getDiscount()
        if lodgeRequired and discountPercent > 0:
            discounted = baseCost * (100 - discountPercent) / 100.0
            return int(discounted)

        return baseCost
