
from .AssetPlus import getEClassifier, eClassifiers
from .AssetPlus import name, nsURI, nsPrefix, eClass
from .AssetPlus import AssetPlus, User, HotelStaff, Guest, Employee, Manager, MaintenanceTicket, MaintenanceNote, TicketImage, SpecificAsset, AssetType, TOMaintenanceNote, TOUser, TOGuest, TOHotelStaff, TOEmployee, TOManager, TOAssetType, TOSpecificAsset, TOMaintenanceTicket, TimeEstimate, PriorityLevel


from . import AssetPlus

__all__ = ['AssetPlus', 'User', 'HotelStaff', 'Guest', 'Employee', 'Manager', 'MaintenanceTicket', 'MaintenanceNote', 'TicketImage', 'SpecificAsset', 'AssetType',
           'TOMaintenanceNote', 'TOUser', 'TOGuest', 'TOHotelStaff', 'TOEmployee', 'TOManager', 'TOAssetType', 'TOSpecificAsset', 'TOMaintenanceTicket', 'TimeEstimate', 'PriorityLevel']

eSubpackages = []
eSuperPackage = None
AssetPlus.eSubpackages = eSubpackages
AssetPlus.eSuperPackage = eSuperPackage

TOSpecificAsset.assetType.eType = TOAssetType
AssetPlus.employees.eType = Employee
AssetPlus.guests.eType = Guest
AssetPlus.manager.eType = Manager
AssetPlus.maintenanceTickets.eType = MaintenanceTicket
AssetPlus.assetTypes.eType = AssetType
AssetPlus.specificAssets.eType = SpecificAsset
User.raisedTickets.eType = MaintenanceTicket
HotelStaff.maintenanceNotes.eType = MaintenanceNote
HotelStaff.maintenanceTasks.eType = MaintenanceTicket
Guest.assetPlus.eType = AssetPlus
Guest.assetPlus.eOpposite = AssetPlus.guests
Employee.assetPlus.eType = AssetPlus
Employee.assetPlus.eOpposite = AssetPlus.employees
Manager.ticketsForApproval.eType = MaintenanceTicket
Manager.assetPlus.eType = AssetPlus
Manager.assetPlus.eOpposite = AssetPlus.manager
MaintenanceTicket.ticketRaiser.eType = User
MaintenanceTicket.ticketRaiser.eOpposite = User.raisedTickets
MaintenanceTicket.ticketFixer.eType = HotelStaff
MaintenanceTicket.ticketFixer.eOpposite = HotelStaff.maintenanceTasks
MaintenanceTicket.fixApprover.eType = Manager
MaintenanceTicket.fixApprover.eOpposite = Manager.ticketsForApproval
MaintenanceTicket.ticketNotes.eType = MaintenanceNote
MaintenanceTicket.ticketImages.eType = TicketImage
MaintenanceTicket.asset.eType = SpecificAsset
MaintenanceTicket.assetPlus.eType = AssetPlus
MaintenanceTicket.assetPlus.eOpposite = AssetPlus.maintenanceTickets
MaintenanceNote.noteTaker.eType = HotelStaff
MaintenanceNote.noteTaker.eOpposite = HotelStaff.maintenanceNotes
MaintenanceNote.ticket.eType = MaintenanceTicket
MaintenanceNote.ticket.eOpposite = MaintenanceTicket.ticketNotes
TicketImage.ticket.eType = MaintenanceTicket
TicketImage.ticket.eOpposite = MaintenanceTicket.ticketImages
SpecificAsset.maintenanceTickets.eType = MaintenanceTicket
SpecificAsset.maintenanceTickets.eOpposite = MaintenanceTicket.asset
SpecificAsset.assetType.eType = AssetType
SpecificAsset.assetPlus.eType = AssetPlus
SpecificAsset.assetPlus.eOpposite = AssetPlus.specificAssets
AssetType.specificAssets.eType = SpecificAsset
AssetType.specificAssets.eOpposite = SpecificAsset.assetType
AssetType.assetPlus.eType = AssetPlus
AssetType.assetPlus.eOpposite = AssetPlus.assetTypes

otherClassifiers = [TimeEstimate, PriorityLevel]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
