"""Definition of meta model 'Facepage'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'Facepage'
nsURI = 'Facepage'
nsPrefix = ''

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)


class Facepage(EObject, metaclass=MetaEClass):

    users = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    accounts = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)
    pages = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)

    def __init__(self, *, users=None, accounts=None, pages=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if users:
            self.users.extend(users)

        if accounts:
            self.accounts.extend(accounts)

        if pages:
            self.pages.extend(pages)


class User(EObject, metaclass=MetaEClass):

    userID = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    email = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    birthDate = EAttribute(eType=EDate, unique=True, derived=False, changeable=True)
    account = EReference(ordered=True, unique=True, containment=False, derived=False)
    facepage = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, userID=None, name=None, email=None, birthDate=None, account=None, facepage=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if userID is not None:
            self.userID = userID

        if name is not None:
            self.name = name

        if email is not None:
            self.email = email

        if birthDate is not None:
            self.birthDate = birthDate

        if account is not None:
            self.account = account

        if facepage is not None:
            self.facepage = facepage


@abstract
class Account(EObject, metaclass=MetaEClass):

    accountNumber = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    user = EReference(ordered=True, unique=True, containment=False, derived=False)
    facepage = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, accountNumber=None, user=None, facepage=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if accountNumber is not None:
            self.accountNumber = accountNumber

        if user is not None:
            self.user = user

        if facepage is not None:
            self.facepage = facepage


class FriendRequest(EObject, metaclass=MetaEClass):

    sender = EReference(ordered=True, unique=True, containment=False, derived=False)
    receiver = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, sender=None, receiver=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if sender is not None:
            self.sender = sender

        if receiver is not None:
            self.receiver = receiver


@abstract
class Page(EObject, metaclass=MetaEClass):

    pageName = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    visits = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    facepage = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, pageName=None, visits=None, facepage=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if pageName is not None:
            self.pageName = pageName

        if visits is not None:
            self.visits = visits

        if facepage is not None:
            self.facepage = facepage


class Privilege(EObject, metaclass=MetaEClass):

    typeOfPrivilege = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    personalAccount = EReference(ordered=True, unique=True, containment=False, derived=False)
    personalPage = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, typeOfPrivilege=None, personalAccount=None, personalPage=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if typeOfPrivilege is not None:
            self.typeOfPrivilege = typeOfPrivilege

        if personalAccount is not None:
            self.personalAccount = personalAccount

        if personalPage is not None:
            self.personalPage = personalPage


class BusinessAccount(Account):

    companyName = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    advertisementPages = EReference(ordered=True, unique=True,
                                    containment=False, derived=False, upper=-1)

    def __init__(self, *, companyName=None, advertisementPages=None, **kwargs):

        super().__init__(**kwargs)

        if companyName is not None:
            self.companyName = companyName

        if advertisementPages:
            self.advertisementPages.extend(advertisementPages)


class PersonalAccount(Account):

    administrator = EReference(ordered=True, unique=True,
                               containment=False, derived=False, upper=-1)
    privileges = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    senderOf = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)
    receiverOf = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)

    def __init__(self, *, administrator=None, privileges=None, senderOf=None, receiverOf=None, **kwargs):

        super().__init__(**kwargs)

        if administrator:
            self.administrator.extend(administrator)

        if privileges:
            self.privileges.extend(privileges)

        if senderOf:
            self.senderOf.extend(senderOf)

        if receiverOf:
            self.receiverOf.extend(receiverOf)


class PersonalPage(Page):

    personalAccount = EReference(ordered=True, unique=True, containment=False, derived=False)
    privileges = EReference(ordered=True, unique=True, containment=False, derived=False, upper=-1)

    def __init__(self, *, personalAccount=None, privileges=None, **kwargs):

        super().__init__(**kwargs)

        if personalAccount is not None:
            self.personalAccount = personalAccount

        if privileges:
            self.privileges.extend(privileges)


class AdvertisementPage(Page):

    bounceRate = EAttribute(eType=EDouble, unique=True, derived=False, changeable=True)
    clickThroughRate = EAttribute(eType=EDouble, unique=True, derived=False, changeable=True)
    conversionRate = EAttribute(eType=EDouble, unique=True, derived=False, changeable=True)
    businessAccount = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, bounceRate=None, clickThroughRate=None, conversionRate=None, businessAccount=None, **kwargs):

        super().__init__(**kwargs)

        if bounceRate is not None:
            self.bounceRate = bounceRate

        if clickThroughRate is not None:
            self.clickThroughRate = clickThroughRate

        if conversionRate is not None:
            self.conversionRate = conversionRate

        if businessAccount is not None:
            self.businessAccount = businessAccount
