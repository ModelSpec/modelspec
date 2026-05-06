
from .biketourplus import getEClassifier, eClassifiers
from .biketourplus import name, nsURI, nsPrefix, eClass
from .biketourplus import BikeTourPlus, User, Manager, NamedUser, Guide, Status, Participant, BookedItem, BookableItem, Gear, Combo, ComboItem, LodgeRating, Lodge, BikeTour


from . import biketourplus

__all__ = ['BikeTourPlus', 'User', 'Manager', 'NamedUser', 'Guide', 'Status', 'Participant',
           'BookedItem', 'BookableItem', 'Gear', 'Combo', 'ComboItem', 'LodgeRating', 'Lodge', 'BikeTour']

eSubpackages = []
eSuperPackage = None
biketourplus.eSubpackages = eSubpackages
biketourplus.eSuperPackage = eSuperPackage

BikeTourPlus.manager.eType = Manager
BikeTourPlus.guides.eType = Guide
BikeTourPlus.participants.eType = Participant
BikeTourPlus.bookedItems.eType = BookedItem
BikeTourPlus.gear.eType = Gear
BikeTourPlus.combos.eType = Combo
BikeTourPlus.comboItems.eType = ComboItem
BikeTourPlus.lodges.eType = Lodge
BikeTourPlus.bikeTours.eType = BikeTour
Manager.bikeTourPlus.eType = BikeTourPlus
Manager.bikeTourPlus.eOpposite = BikeTourPlus.manager
Guide.bikeTours.eType = BikeTour
Guide.bikeTourPlus.eType = BikeTourPlus
Guide.bikeTourPlus.eOpposite = BikeTourPlus.guides
Participant.bikeTour.eType = BikeTour
Participant.bookedItems.eType = BookedItem
Participant.bikeTourPlus.eType = BikeTourPlus
Participant.bikeTourPlus.eOpposite = BikeTourPlus.participants
BookedItem.participant.eType = Participant
BookedItem.participant.eOpposite = Participant.bookedItems
BookedItem.item.eType = BookableItem
BookedItem.bikeTourPlus.eType = BikeTourPlus
BookedItem.bikeTourPlus.eOpposite = BikeTourPlus.bookedItems
BookableItem.bookedItems.eType = BookedItem
BookableItem.bookedItems.eOpposite = BookedItem.item
Gear.comboItems.eType = ComboItem
Gear.bikeTourPlus.eType = BikeTourPlus
Gear.bikeTourPlus.eOpposite = BikeTourPlus.gear
Combo.comboItems.eType = ComboItem
Combo.bikeTourPlus.eType = BikeTourPlus
Combo.bikeTourPlus.eOpposite = BikeTourPlus.combos
ComboItem.combo.eType = Combo
ComboItem.combo.eOpposite = Combo.comboItems
ComboItem.gear.eType = Gear
ComboItem.gear.eOpposite = Gear.comboItems
ComboItem.bikeTourPlus.eType = BikeTourPlus
ComboItem.bikeTourPlus.eOpposite = BikeTourPlus.comboItems
Lodge.bikeTours.eType = BikeTour
Lodge.bikeTourPlus.eType = BikeTourPlus
Lodge.bikeTourPlus.eOpposite = BikeTourPlus.lodges
BikeTour.participants.eType = Participant
BikeTour.participants.eOpposite = Participant.bikeTour
BikeTour.guide.eType = Guide
BikeTour.guide.eOpposite = Guide.bikeTours
BikeTour.lodge.eType = Lodge
BikeTour.lodge.eOpposite = Lodge.bikeTours
BikeTour.bikeTourPlus.eType = BikeTourPlus
BikeTour.bikeTourPlus.eOpposite = BikeTourPlus.bikeTours

otherClassifiers = [Status, LodgeRating]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
