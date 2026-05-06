
from .Symboleo import getEClassifier, eClassifiers
from .Symboleo import name, nsURI, nsPrefix, eClass
from .Symboleo import Contract, Party, Role, Asset, LegalPosition, Situation, Event, TimeInterval, TimePoint, LegalSituation, Obligation, Power, ContractStatus, ContractStatusActive, ObligationStatus, ObligationStatusActive, PowerStatus, PowerStatusActive


from . import Symboleo

__all__ = ['Contract', 'Party', 'Role', 'Asset', 'LegalPosition', 'Situation', 'Event', 'TimeInterval', 'TimePoint', 'LegalSituation',
           'Obligation', 'Power', 'ContractStatus', 'ContractStatusActive', 'ObligationStatus', 'ObligationStatusActive', 'PowerStatus', 'PowerStatusActive']

eSubpackages = []
eSuperPackage = None
Symboleo.eSubpackages = eSubpackages
Symboleo.eSuperPackage = eSuperPackage

LegalPosition.trigger.eType = LegalSituation
Situation.time.eType = TimeInterval
Event.time.eType = TimePoint
TimeInterval.start.eType = TimePoint
TimeInterval.end.eType = TimePoint
Power.legalPositions.eType = LegalPosition
Contract.legalPositions.eType = LegalPosition
Contract.roles.eType = Role
Contract.parties.eType = Party
Contract.assets.eType = Asset
Contract.parentContract.eType = Contract
Contract.subContracts.eType = Contract
Contract.subContracts.eOpposite = Contract.parentContract
Contract.terminators.eType = Power
Party.contract.eType = Contract
Party.contract.eOpposite = Contract.parties
Party.roles.eType = Role
Party.assets.eType = Asset
Party.performerOf.eType = LegalPosition
Party.liableOf.eType = LegalPosition
Party.rightHolderOf.eType = LegalPosition
Role.debt.eType = LegalPosition
Role.credit.eType = LegalPosition
Role.party.eType = Party
Role.party.eOpposite = Party.roles
Role.contract.eType = Contract
Role.contract.eOpposite = Contract.roles
Asset.owners.eType = Party
Asset.owners.eOpposite = Party.assets
Asset.legalPositions.eType = LegalPosition
Asset.contract.eType = Contract
Asset.contract.eOpposite = Contract.assets
LegalPosition.performer.eType = Party
LegalPosition.performer.eOpposite = Party.performerOf
LegalPosition.liable.eType = Party
LegalPosition.liable.eOpposite = Party.liableOf
LegalPosition.rightHolder.eType = Party
LegalPosition.rightHolder.eOpposite = Party.rightHolderOf
LegalPosition.antecedent.eType = LegalSituation
LegalPosition.consequent.eType = LegalSituation
LegalPosition.contract.eType = Contract
LegalPosition.contract.eOpposite = Contract.legalPositions
LegalPosition.debtor.eType = Role
LegalPosition.debtor.eOpposite = Role.debt
LegalPosition.creditor.eType = Role
LegalPosition.creditor.eOpposite = Role.credit
LegalPosition.asset.eType = Asset
LegalPosition.asset.eOpposite = Asset.legalPositions
Situation.preEvents.eType = Event
Situation.postEvents.eType = Event
Event.postState.eType = Situation
Event.postState.eOpposite = Situation.preEvents
Event.preState.eType = Situation
Event.preState.eOpposite = Situation.postEvents
LegalSituation.antecedentOf.eType = LegalPosition
LegalSituation.antecedentOf.eOpposite = LegalPosition.antecedent
LegalSituation.consequentOf.eType = LegalPosition
LegalSituation.consequentOf.eOpposite = LegalPosition.consequent
Power.terminated.eType = Contract
Power.terminated.eOpposite = Contract.terminators

otherClassifiers = [ContractStatus, ContractStatusActive, ObligationStatus,
                    ObligationStatusActive, PowerStatus, PowerStatusActive]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
