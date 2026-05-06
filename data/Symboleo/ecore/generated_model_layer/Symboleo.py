"""Definition of meta model 'Symboleo'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'Symboleo'
nsURI = 'Symboleo'
nsPrefix = ''

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)
ContractStatus = EEnum('ContractStatus', literals=[
                       'Form', 'Active', 'SuccessfulTermination', 'UnsuccessfulTermination'])

ContractStatusActive = EEnum('ContractStatusActive', literals=[
                             'Null', 'InEffect', 'Suspension', 'Unassign', 'Rescission'])

ObligationStatus = EEnum('ObligationStatus', literals=[
                         'Start', 'Create', 'Active', 'Violation', 'Discharge', 'Fulfillment', 'UnsuccessfulTermination'])

ObligationStatusActive = EEnum('ObligationStatusActive', literals=[
                               'Null', 'InEffect', 'Suspension'])

PowerStatus = EEnum('PowerStatus', literals=[
                    'Start', 'Create', 'Active', 'SuccessfulTermination', 'UnsuccessfulTermination'])

PowerStatusActive = EEnum('PowerStatusActive', literals=['Null', 'InEffect', 'Suspension'])


class Contract(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    status = EAttribute(eType=ContractStatus, unique=True, derived=False,
                        changeable=True, default_value=None)
    statusActive = EAttribute(eType=ContractStatusActive, unique=True,
                              derived=False, changeable=True, default_value=None)
    legalPositions = EReference(ordered=True, unique=True,
                                containment=True, derived=False, upper=-1)
    roles = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    parties = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    assets = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    parentContract = EReference(ordered=True, unique=True, containment=False, derived=False)
    subContracts = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    terminators = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)

    def __init__(self, *, id=None, legalPositions=None, roles=None, parties=None, assets=None, parentContract=None, subContracts=None, terminators=None, status=None, statusActive=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if status is not None:
            self.status = status

        if statusActive is not None:
            self.statusActive = statusActive

        if legalPositions:
            self.legalPositions.extend(legalPositions)

        if roles:
            self.roles.extend(roles)

        if parties:
            self.parties.extend(parties)

        if assets:
            self.assets.extend(assets)

        if parentContract is not None:
            self.parentContract = parentContract

        if subContracts:
            self.subContracts.extend(subContracts)

        if terminators:
            self.terminators.extend(terminators)


class Party(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    contract = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    roles = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    assets = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    performerOf = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    liableOf = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    rightHolderOf = EReference(ordered=True, unique=True,
                               containment=False, derived=False, upper=-1)

    def __init__(self, *, id=None, contract=None, roles=None, assets=None, performerOf=None, liableOf=None, rightHolderOf=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if contract:
            self.contract.extend(contract)

        if roles:
            self.roles.extend(roles)

        if assets:
            self.assets.extend(assets)

        if performerOf:
            self.performerOf.extend(performerOf)

        if liableOf:
            self.liableOf.extend(liableOf)

        if rightHolderOf:
            self.rightHolderOf.extend(rightHolderOf)


class Role(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    debt = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    credit = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    party = EReference(ordered=True, unique=True, containment=False, derived=False)
    contract = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, id=None, debt=None, credit=None, party=None, contract=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if debt:
            self.debt.extend(debt)

        if credit:
            self.credit.extend(credit)

        if party is not None:
            self.party = party

        if contract is not None:
            self.contract = contract


class Asset(EObject, metaclass=MetaEClass):

    id = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    owners = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    legalPositions = EReference(ordered=True, unique=True,
                                containment=False, derived=False, upper=-1)
    contract = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, id=None, owners=None, legalPositions=None, contract=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if id is not None:
            self.id = id

        if owners:
            self.owners.extend(owners)

        if legalPositions:
            self.legalPositions.extend(legalPositions)

        if contract is not None:
            self.contract = contract


@abstract
class LegalPosition(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    performer = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    liable = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    rightHolder = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    antecedent = EReference(ordered=True, unique=True, containment=False, derived=False)
    consequent = EReference(ordered=True, unique=True, containment=False, derived=False)
    trigger = EReference(ordered=True, unique=True, containment=False, derived=False)
    contract = EReference(ordered=True, unique=True, containment=False, derived=False)
    debtor = EReference(ordered=True, unique=True, containment=False, derived=False)
    creditor = EReference(ordered=True, unique=True, containment=False, derived=False)
    asset = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, name=None, performer=None, liable=None, rightHolder=None, antecedent=None, consequent=None, trigger=None, contract=None, debtor=None, creditor=None, asset=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if performer:
            self.performer.extend(performer)

        if liable:
            self.liable.extend(liable)

        if rightHolder:
            self.rightHolder.extend(rightHolder)

        if antecedent is not None:
            self.antecedent = antecedent

        if consequent is not None:
            self.consequent = consequent

        if trigger is not None:
            self.trigger = trigger

        if contract is not None:
            self.contract = contract

        if debtor is not None:
            self.debtor = debtor

        if creditor is not None:
            self.creditor = creditor

        if asset is not None:
            self.asset = asset


class Situation(EObject, metaclass=MetaEClass):

    preEvents = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    postEvents = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    time = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, preEvents=None, postEvents=None, time=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if preEvents:
            self.preEvents.extend(preEvents)

        if postEvents:
            self.postEvents.extend(postEvents)

        if time is not None:
            self.time = time


class Event(EObject, metaclass=MetaEClass):

    time = EReference(ordered=True, unique=True, containment=False, derived=False)
    postState = EReference(ordered=True, unique=True, containment=False, derived=False)
    preState = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, time=None, postState=None, preState=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if time is not None:
            self.time = time

        if postState is not None:
            self.postState = postState

        if preState is not None:
            self.preState = preState


class TimeInterval(EObject, metaclass=MetaEClass):

    start = EReference(ordered=True, unique=True, containment=False, derived=False)
    end = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, start=None, end=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if start is not None:
            self.start = start

        if end is not None:
            self.end = end


class TimePoint(EObject, metaclass=MetaEClass):

    def __init__(self):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class LegalSituation(Situation):

    antecedentOf = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    consequentOf = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)

    def __init__(self, *, antecedentOf=None, consequentOf=None, **kwargs):

        super().__init__(**kwargs)

        if antecedentOf:
            self.antecedentOf.extend(antecedentOf)

        if consequentOf:
            self.consequentOf.extend(consequentOf)


class Obligation(LegalPosition):

    surviving = EAttribute(eType=EBoolean, unique=True, derived=False, changeable=True)
    status = EAttribute(eType=ObligationStatus, unique=True,
                        derived=False, changeable=True, default_value=None)
    statusActive = EAttribute(eType=ObligationStatusActive, unique=True,
                              derived=False, changeable=True, default_value=None)

    def __init__(self, *, surviving=None, status=None, statusActive=None, **kwargs):

        super().__init__(**kwargs)

        if surviving is not None:
            self.surviving = surviving

        if status is not None:
            self.status = status

        if statusActive is not None:
            self.statusActive = statusActive


class Power(LegalPosition):

    status = EAttribute(eType=PowerStatus, unique=True, derived=False,
                        changeable=True, default_value=None)
    statusActive = EAttribute(eType=PowerStatusActive, unique=True,
                              derived=False, changeable=True, default_value=None)
    terminated = EReference(ordered=True, unique=True, containment=False, derived=False)
    legalPositions = EReference(ordered=True, unique=True,
                                containment=False, derived=False, upper=-1)

    def __init__(self, *, terminated=None, legalPositions=None, status=None, statusActive=None, **kwargs):

        super().__init__(**kwargs)

        if status is not None:
            self.status = status

        if statusActive is not None:
            self.statusActive = statusActive

        if terminated is not None:
            self.terminated = terminated

        if legalPositions:
            self.legalPositions.extend(legalPositions)
