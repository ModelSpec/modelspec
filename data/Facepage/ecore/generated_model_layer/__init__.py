
from .Facepage import getEClassifier, eClassifiers
from .Facepage import name, nsURI, nsPrefix, eClass
from .Facepage import Facepage, User, Account, BusinessAccount, PersonalAccount, FriendRequest, Page, PersonalPage, AdvertisementPage, Privilege


from . import Facepage

__all__ = ['Facepage', 'User', 'Account', 'BusinessAccount', 'PersonalAccount',
           'FriendRequest', 'Page', 'PersonalPage', 'AdvertisementPage', 'Privilege']

eSubpackages = []
eSuperPackage = None
Facepage.eSubpackages = eSubpackages
Facepage.eSuperPackage = eSuperPackage

Facepage.users.eType = User
Facepage.accounts.eType = Account
Facepage.pages.eType = Page
User.account.eType = Account
User.facepage.eType = Facepage
User.facepage.eOpposite = Facepage.users
Account.user.eType = User
Account.user.eOpposite = User.account
Account.facepage.eType = Facepage
Account.facepage.eOpposite = Facepage.accounts
BusinessAccount.advertisementPages.eType = AdvertisementPage
PersonalAccount.administrator.eType = PersonalPage
PersonalAccount.privileges.eType = Privilege
PersonalAccount.senderOf.eType = FriendRequest
PersonalAccount.receiverOf.eType = FriendRequest
FriendRequest.sender.eType = PersonalAccount
FriendRequest.sender.eOpposite = PersonalAccount.senderOf
FriendRequest.receiver.eType = PersonalAccount
FriendRequest.receiver.eOpposite = PersonalAccount.receiverOf
Page.facepage.eType = Facepage
Page.facepage.eOpposite = Facepage.pages
PersonalPage.personalAccount.eType = PersonalAccount
PersonalPage.personalAccount.eOpposite = PersonalAccount.administrator
PersonalPage.privileges.eType = Privilege
AdvertisementPage.businessAccount.eType = BusinessAccount
AdvertisementPage.businessAccount.eOpposite = BusinessAccount.advertisementPages
Privilege.personalAccount.eType = PersonalAccount
Privilege.personalAccount.eOpposite = PersonalAccount.privileges
Privilege.personalPage.eType = PersonalPage
Privilege.personalPage.eOpposite = PersonalPage.privileges

otherClassifiers = []

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
