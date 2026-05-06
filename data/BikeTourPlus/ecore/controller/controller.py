from ..generated_model_layer import *
from datetime import date

class BikeTourPlusController:
	def __init__(self) -> None:
		self.btp = BikeTourPlus(startDate=None, nrWeeks=0, priceOfGuidePerWeek=0)

	def addCombo(self, name: str, discount: int) -> None:
		if not name or name.strip() == "":
			raise ValueError("The name must not be empty")

		if discount < 0:
			raise ValueError("Discount must be at least 0")

		if discount > 100:
			raise ValueError("Discount must be no more than 100")

		if any(g.name == name for g in self.btp.gear):
			raise ValueError("A piece of gear with the same name already exists")

		if any(c.name == name for c in self.btp.combos):
			raise ValueError("A combo with the same name already exists")
		combo = Combo(name=name, discount=discount)
		self.btp.combos.append(combo)

	def addGear(self, name: str, pricePerWeek: int) -> None:
		if pricePerWeek < 0:
			raise ValueError("The price per week must be greater than or equal to 0")

		if not name or name.strip() == "":
			raise ValueError("The name must not be empty")

		if any(g.name == name for g in self.btp.gear):
			raise ValueError("A piece of gear with the same name already exists")

		if any(c.name == name for c in self.btp.combos):
			raise ValueError("A combo with the same name already exists")

		gear = Gear(name=name, pricePerWeek=pricePerWeek)
		self.btp.gear.append(gear)

	def deleteCombo(self, name: str) -> None:
		combo = None
		for c in self.btp.combos:
			if c.name == name:
				combo = c
				break

		if combo is None:
			return

		for participant in self.btp.participants:
			bookedItems = list(participant.bookedItems)
			itemsToRemove = []
			for bookedItem in bookedItems:
				item = bookedItem.item
				if isinstance(item, Combo) and item.name == name:
					itemsToRemove.append(bookedItem)

			for itemToRemove in itemsToRemove:
				if itemToRemove in participant.bookedItems:
					participant.bookedItems.remove(itemToRemove)
				if itemToRemove in self.btp.bookedItems:
					self.btp.bookedItems.remove(itemToRemove)

		if combo in self.btp.combos:
			self.btp.combos.remove(combo)

	def deleteGear(self, name: str) -> None:
		gear = None
		for g in self.btp.gear:
			if g.name == name:
				gear = g
				break

		if gear is None:
			return

		for combo in self.btp.combos:
			for comboItem in combo.comboItems:
				if comboItem.gear is not None and comboItem.gear.name == name:
					raise ValueError("The piece of gear is in a combo and cannot be deleted")

		for participant in self.btp.participants:
			itemsToRemove = []
			for bookedItem in participant.bookedItems:
				item = bookedItem.item
				if isinstance(item, Gear) and item.name == name:
					itemsToRemove.append(bookedItem)
			for bi in itemsToRemove:
				if bi in participant.bookedItems:
					participant.bookedItems.remove(bi)
				if bi in self.btp.bookedItems:
					self.btp.bookedItems.remove(bi)

		if gear in self.btp.gear:
			self.btp.gear.remove(gear)

	def deleteGuide(self, email: str) -> None:
		guide = None
		for g in self.btp.guides:
			if g.email == email:
				guide = g
				break

		if guide is None:
			for p in self.btp.participants:
				if p.email == email:
					return
			if email == "manager@btp.com":
				return
			return
		for bt in list(guide.bikeTours):  # clear biketour associations before removal
			guide.bikeTours.remove(bt)
		if guide in self.btp.guides:
			self.btp.guides.remove(guide)


	def deleteParticipant(self, email: str) -> None:
		participant = None
		for p in self.btp.participants:
			if p.email == email:
				participant = p
				break

		if participant is None:
			for g in self.btp.guides:
				if g.email == email:
					return
			if email == "manager@btp.com":
				return
			return

		bookedItems = list(participant.bookedItems)
		for bi in bookedItems:
			if bi in participant.bookedItems:
				participant.bookedItems.remove(bi)
			if bi in self.btp.bookedItems:
				self.btp.bookedItems.remove(bi)

		if participant in self.btp.participants:
			self.btp.participants.remove(participant)

	def addGearOrComboToParticipant(self, name: str, email: str) -> None:
		# find participant
		participant = None
		for p in self.btp.participants:
			if p.email == email:
				participant = p
				break

		if participant is None:
			raise ValueError("The participant does not exist")

		# find gear
		item = None
		for g in self.btp.gear:
			if g.name == name:
				item = g
				break

		# find combo
		if item is None:
			for c in self.btp.combos:
				if c.name == name:
					item = c
					break

		if item is None:
			raise ValueError("The piece of gear or combo does not exist")

		for bookedItem in participant.bookedItems:
			if bookedItem.item == item:
				bookedItem.quantity = bookedItem.quantity + 1
				return

		bi = BookedItem(quantity=1, participant=participant, item=item)
		participant.bookedItems.append(bi)
		self.btp.bookedItems.append(bi)

	def addGearToCombo(self, gearName: str, comboName: str) -> None:
		# find combo
		combo = None
		for c in self.btp.combos:
			if c.name == comboName:
				combo = c
				break

		if combo is None:
			raise ValueError("The combo does not exist")

		# find gear
		gear = None
		for g in self.btp.gear:
			if g.name == gearName:
				gear = g
				break

		if gear is None:
			raise ValueError("The piece of gear does not exist")

		for item in combo.comboItems:
			if item.gear == gear:
				item.quantity = item.quantity + 1
				return
		ci = ComboItem(quantity=1, combo=combo, gear=gear)
		combo.comboItems.append(ci)
		self.btp.comboItems.append(ci)

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

		for g in self.btp.guides:
			if g.email == email:
				raise ValueError("Email already linked to a guide account")

		for p in self.btp.participants:
			if p.email == email:
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

		guide = Guide(email=email, password=password, name=name, emergencyContact=emergencyContact)
		self.btp.guides.append(guide)

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

		for g in self.btp.guides:
			if g.email == email:
				raise ValueError("Email already linked to a guide account")

		for p in self.btp.participants:
			if p.email == email:
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

		seasonWeeks = self.btp.nrWeeks
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

		participant = Participant(
			email=email,
			password=password,
			name=name,
			emergencyContact=emergencyContact,
			nrWeeks=nrWeeks,
			weekAvailableFrom=weeksAvailableFrom,
			weekAvailableUntil=weeksAvailableUntil,
			lodgeRequired=lodgeRequired,
			authorizationCode="None",
			refundedPercentageAmount=0,
			status=Status.NotAssigned,
		)
		self.btp.participants.append(participant)

	def removeGearFromCombo(self, gearName: str, comboName: str) -> None:
		combo = None
		for c in self.btp.combos:
			if c.name == comboName:
				combo = c
				break

		if combo is None:
			raise ValueError("The combo does not exist")

		itemInCombo = None
		for item in combo.comboItems:
			if item.gear is not None and item.gear.name == gearName:
				itemInCombo = item
				break

		if itemInCombo is None:
			return

		numberOfGearTypes = len(combo.comboItems)
		typesAfterRemoval = numberOfGearTypes if itemInCombo.quantity > 1 else numberOfGearTypes - 1

		if typesAfterRemoval < 2:
			raise ValueError("A combo must have at least two pieces of gear")

		if itemInCombo.quantity > 1:
			itemInCombo.quantity = itemInCombo.quantity - 1
		else:
			if itemInCombo in combo.comboItems:
				combo.comboItems.remove(itemInCombo)
			if itemInCombo in self.btp.comboItems:
				self.btp.comboItems.remove(itemInCombo)

	def removeGearOrComboFromParticipant(self, name: str, email: str) -> None:
		participant = None
		for p in self.btp.participants:
			if p.email == email:
				participant = p
				break

		if participant is None:
			raise ValueError("The participant does not exist")

		itemForParticipant = None
		for bookedItem in participant.bookedItems:
			item = bookedItem.item
			if item.name == name:
				itemForParticipant = bookedItem
				break

		if itemForParticipant is None:
			return

		if itemForParticipant.quantity > 1:
			itemForParticipant.quantity = itemForParticipant.quantity - 1
		else:
			if itemForParticipant in participant.bookedItems:
				participant.bookedItems.remove(itemForParticipant)
			if itemForParticipant in self.btp.bookedItems:
				self.btp.bookedItems.remove(itemForParticipant)

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

		if self.btp.startDate is not None:
			if startDate.year < self.btp.startDate.year:
				raise ValueError(
					"The start date cannot be from previous year or earlier"
				)

		self.btp.startDate = startDate
		self.btp.nrWeeks = nrWeeks
		self.btp.priceOfGuidePerWeek = priceOfGuidePerWeek

	def updateGear(self, oldName: str, newName: str, newPricePerWeek: int) -> None:
		gear = None
		for g in self.btp.gear:
			if g.name == oldName:
				gear = g
				break

		if gear is None:
			raise ValueError("The piece of gear does not exist")

		if newPricePerWeek < 0:
			raise ValueError("The price per week must be greater than or equal to 0")

		if not newName or newName.strip() == "":
			raise ValueError("The name must not be empty")

		for g in self.btp.gear:
			if g.name == newName and g is not gear:
				raise ValueError("A piece of gear with the same name already exists")

		for c in self.btp.combos:
			if c.name == newName:
				raise ValueError("A combo with the same name already exists")

		gear.name = newName
		gear.pricePerWeek = newPricePerWeek

	def updateCombo(self, oldName: str, newName: str, newDiscount: int) -> None:
		combo = None
		for c in self.btp.combos:
			if c.name == oldName:
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

		for g in self.btp.gear:
			if g.name == newName:
				raise ValueError("A piece of gear with the same name already exists")

		for c in self.btp.combos:
			if c.name == newName and c is not combo:
				raise ValueError("A combo with the same name already exists")

		combo.name = newName
		combo.discount = newDiscount

	def updateGuide(self, email: str, newPassword: str, newName: str, newEmergencyContact: str) -> None:
		guide = None
		for g in self.btp.guides:
			if g.email == email:
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

		guide.password = newPassword
		guide.name = newName
		guide.emergencyContact = newEmergencyContact

	def updateManager(self, password: str) -> None:
		manager = self.btp.manager

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

		manager.password = password

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
		for p in self.btp.participants:
			if p.email == email:
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

		if newNrWeeks > self.btp.nrWeeks:
			raise ValueError(
				"Number of weeks must be less than or equal to the number of biking weeks in the biking season"
			)

		if (
				newWeeksAvailableFrom < 1
				or newWeeksAvailableUntil < 1
				or newWeeksAvailableFrom > self.btp.nrWeeks
				or newWeeksAvailableUntil > self.btp.nrWeeks
		):
			raise ValueError(
				f"Available weeks must be within weeks of biking season (1-{self.btp.nrWeeks})"
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

		participant.password = newPassword
		participant.name = newName
		participant.emergencyContact = newEmergencyContact
		participant.nrWeeks = newNrWeeks
		participant.weekAvailableFrom = newWeeksAvailableFrom
		participant.weekAvailableUntil = newWeeksAvailableUntil
		participant.lodgeRequired = newLodgeRequired

	def processPay(self, email: str, code: str) -> None:
		participant = None
		for p in self.btp.participants:
			if p.email == email:
				participant = p
				break

		if participant is None:
			raise ValueError(f"Participant with email address {email} does not exist")

		status = participant.status

		if status == Status.Banned:
			raise ValueError("Cannot pay for tour because the participant is banned")
		if status == Status.Cancelled:
			raise ValueError("Cannot pay for tour because the participant has cancelled their tour")
		if status == Status.NotAssigned:
			raise ValueError("The participant has not been assigned to their tour")

		if status in [Status.Paid, Status.Started, Status.Finished]:
			raise ValueError("The participant has already paid for their tour")

		if not code or code.strip() == "":
			raise ValueError("Invalid authorization code")

		participant.authorizationCode = code
		participant.status = Status.Paid

	def processStart(self, week: int) -> None:
		startWeek = int(week)
		participantsInWeek = set()

		for tour in self.btp.bikeTours:
			if tour.startWeek == startWeek:
				for p in tour.participants:
					participantsInWeek.add(p.email)

		if not participantsInWeek:
			return

		for p in self.btp.participants:
			if p.email in participantsInWeek:
				status = p.status
				if status == Status.Started:
					raise ValueError("Cannot start tour because the participant has already started their tour")
				if status == Status.Banned:
					raise ValueError("Cannot start tour because the participant is banned")
				if status == Status.Cancelled:
					raise ValueError("Cannot start tour because the participant has cancelled their tour")
				if status == Status.Finished:
					raise ValueError("Cannot start tour because the participant has finished their tour")

		for p in self.btp.participants:
			if p.email in participantsInWeek:
				status = p.status
				if status == Status.Paid:
					p.status = Status.Started
				elif status == Status.Assigned:
					p.status = Status.Banned

	def processFinish(self, email: str) -> None:
		participant = None
		for p in self.btp.participants:
			if p.email == email:
				participant = p
				break

		if participant is None:
			raise ValueError(f"Participant with email address {email} does not exist")

		status = participant.status

		if status == Status.Banned:
			raise ValueError("Cannot finish tour because the participant is banned")
		if status == Status.Cancelled:
			raise ValueError("Cannot finish tour because the participant has cancelled their tour")
		if status == Status.Finished:
			raise ValueError("Cannot finish tour because the participant has already finished their tour")

		if status != Status.Started:
			raise ValueError("Cannot finish a tour for a participant who has not started their tour")

		participant.status = Status.Finished
		participant.refundedPercentageAmount = 0

	def createBikeTours(self):
		participants = list(self.btp.participants)
		guides = list(self.btp.guides)

		if not participants:
			return

		if not guides:
			for participant in participants:
				participant.status = Status.NotAssigned
			raise ValueError("At least one participant could not be assigned to their bike tour")

		for p in participants:
			p.status = Status.NotAssigned

		unassigned = list(participants)
		# continue after existing tours so that tour ids stay unique
		tourId = max((t.id for t in self.btp.bikeTours), default=0) + 1

		for guide in guides:
			for p in list(unassigned):
				if p.status == Status.Assigned:
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

		endWeek = startWeek + participant.nrWeeks - 1
		newTour = BikeTour(id=tourId, startWeek=startWeek, endWeek=endWeek)
		self.btp.bikeTours.append(newTour)
		newTour.guide = guide
		newTour.participants.append(participant)
		participant.status = Status.Assigned
		return True

	def _tryJoinExistingTour(self, participant):
		nrWeeks = participant.nrWeeks
		availFrom = participant.weekAvailableFrom
		availUntil = participant.weekAvailableUntil

		for tour in self.btp.bikeTours:
			tourDuration = tour.endWeek - tour.startWeek + 1

			if (tourDuration == nrWeeks and
					tour.startWeek >= availFrom and
					tour.endWeek <= availUntil):
				tour.participants.append(participant)
				participant.status = Status.Assigned
				return True

		return False

	def _findEarliestSlot(self, guide, participant):
		nrWeeks = participant.nrWeeks
		availFrom = participant.weekAvailableFrom
		availUntil = participant.weekAvailableUntil

		for start in range(availFrom, availUntil - nrWeeks + 2):
			end = start + nrWeeks - 1

			if self._guideIsFree(guide, start, end):
				return start

		return None

	def _guideIsFree(self, guide, start, end):
		for tour in self.btp.bikeTours:
			if tour.guide == guide:
				if not (end < tour.startWeek or start > tour.endWeek):
					return False
		return True

	def viewBikeTour(self, tourId):
		if tourId < 1:
			raise ValueError("Invalid bike tour id")

		for tour in self.btp.bikeTours:
			if tour.id == tourId:
				return tour
		
		raise ValueError(f"Bike tour with id {tourId} does not exist")

	def _itemsCostPerWeek(self, participant):
		total = 0.0

		for bookedItem in participant.bookedItems:
			item = bookedItem.item
			quantity = bookedItem.quantity

			if isinstance(item, Combo):
				total += self._comboCost(item, participant.lodgeRequired) * quantity
			else:
				total += item.pricePerWeek * quantity

		return total

	def _comboCost(self, combo, lodgeRequired):
		baseCost = 0

		for comboItem in combo.comboItems:
			gear = comboItem.gear
			price = gear.pricePerWeek
			quantity = comboItem.quantity
			baseCost += price * quantity

		# the combo discount only applies when a lodge is also rented
		discountPercent = combo.discount
		if lodgeRequired and discountPercent > 0:
			discounted = baseCost * (100 - discountPercent) / 100.0
			return int(discounted)

		return baseCost
