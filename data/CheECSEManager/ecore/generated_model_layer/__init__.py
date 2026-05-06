
from .cheecsemanager import getEClassifier, eClassifiers
from .cheecsemanager import name, nsURI, nsPrefix, eClass
from .cheecsemanager import CheECSEManager, User, FacilityManager, Farmer, WholesaleCompany, Shelf, ShelfLocation, CheeseWheel, Transaction, Purchase, Order, Robot, LogEntry, MaturationPeriod, TOFarmer, TOWholesaleCompany, TOShelf, TOCheeseWheel


from . import cheecsemanager

__all__ = ['CheECSEManager', 'User', 'FacilityManager', 'Farmer', 'WholesaleCompany', 'Shelf', 'ShelfLocation', 'CheeseWheel',
           'Transaction', 'Purchase', 'Order', 'Robot', 'LogEntry', 'MaturationPeriod', 'TOFarmer', 'TOWholesaleCompany', 'TOShelf', 'TOCheeseWheel']

eSubpackages = []
eSuperPackage = None
cheecsemanager.eSubpackages = eSubpackages
cheecsemanager.eSuperPackage = eSuperPackage

CheECSEManager.manager.eType = FacilityManager
CheECSEManager.farmers.eType = Farmer
CheECSEManager.shelves.eType = Shelf
CheECSEManager.cheeseWheels.eType = CheeseWheel
CheECSEManager.transactions.eType = Transaction
CheECSEManager.companies.eType = WholesaleCompany
CheECSEManager.robot.eType = Robot
FacilityManager.cheECSEManager.eType = CheECSEManager
FacilityManager.cheECSEManager.eOpposite = CheECSEManager.manager
Farmer.cheECSEManager.eType = CheECSEManager
Farmer.cheECSEManager.eOpposite = CheECSEManager.farmers
Farmer.purchases.eType = Purchase
WholesaleCompany.cheECSEManager.eType = CheECSEManager
WholesaleCompany.cheECSEManager.eOpposite = CheECSEManager.companies
WholesaleCompany.orders.eType = Order
Shelf.robot.eType = Robot
Shelf.cheECSEManager.eType = CheECSEManager
Shelf.cheECSEManager.eOpposite = CheECSEManager.shelves
Shelf.locations.eType = ShelfLocation
ShelfLocation.cheeseWheel.eType = CheeseWheel
ShelfLocation.shelf.eType = Shelf
ShelfLocation.shelf.eOpposite = Shelf.locations
CheeseWheel.robot.eType = Robot
CheeseWheel.cheECSEManager.eType = CheECSEManager
CheeseWheel.cheECSEManager.eOpposite = CheECSEManager.cheeseWheels
CheeseWheel.purchase.eType = Purchase
CheeseWheel.location.eType = ShelfLocation
CheeseWheel.location.eOpposite = ShelfLocation.cheeseWheel
CheeseWheel.order.eType = Order
Transaction.cheECSEManager.eType = CheECSEManager
Transaction.cheECSEManager.eOpposite = CheECSEManager.transactions
Purchase.cheeseWheels.eType = CheeseWheel
Purchase.cheeseWheels.eOpposite = CheeseWheel.purchase
Purchase.farmer.eType = Farmer
Purchase.farmer.eOpposite = Farmer.purchases
Order.cheeseWheels.eType = CheeseWheel
Order.cheeseWheels.eOpposite = CheeseWheel.order
Order.company.eType = WholesaleCompany
Order.company.eOpposite = WholesaleCompany.orders
Robot.cheECSEManager.eType = CheECSEManager
Robot.cheECSEManager.eOpposite = CheECSEManager.robot
Robot.currentShelf.eType = Shelf
Robot.currentShelf.eOpposite = Shelf.robot
Robot.currentCheeseWheel.eType = CheeseWheel
Robot.currentCheeseWheel.eOpposite = CheeseWheel.robot
Robot.log.eType = LogEntry
LogEntry.robot.eType = Robot
LogEntry.robot.eOpposite = Robot.log

otherClassifiers = [MaturationPeriod]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
