
from .House import getEClassifier, eClassifiers
from .House import name, nsURI, nsPrefix, eClass
from .House import Basement, ConcreteBasement, EarthBasement, House, SemiDetached, SemiDetachedWithCarport, SemiDetachedWithGarage, Carport, Garage, Company, JobLog, BMType


from . import House

__all__ = ['Basement', 'ConcreteBasement', 'EarthBasement', 'House', 'SemiDetached',
           'SemiDetachedWithCarport', 'SemiDetachedWithGarage', 'Carport', 'Garage', 'Company', 'JobLog', 'BMType']

eSubpackages = []
eSuperPackage = None
House.eSubpackages = eSubpackages
House.eSuperPackage = eSuperPackage

Basement.house.eType = House
House.basement.eType = Basement
House.basement.eOpposite = Basement.house
House.jobLogs.eType = JobLog
SemiDetachedWithCarport.carports.eType = Carport
SemiDetachedWithGarage.garage.eType = Garage
Carport.semiDetachedWithCarport.eType = SemiDetachedWithCarport
Carport.semiDetachedWithCarport.eOpposite = SemiDetachedWithCarport.carports
Garage.semiDetachedWithGarage.eType = SemiDetachedWithGarage
Garage.semiDetachedWithGarage.eOpposite = SemiDetachedWithGarage.garage
Company.jobLogs.eType = JobLog
JobLog.house.eType = House
JobLog.house.eOpposite = House.jobLogs
JobLog.company.eType = Company
JobLog.company.eOpposite = Company.jobLogs

otherClassifiers = [BMType]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
