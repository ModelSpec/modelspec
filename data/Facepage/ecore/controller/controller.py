from datetime import date
from ..generated_model_layer import *
from pyecore.ecore import EDate


class FacepageController:
    def __init__(self):
        self.facepage = Facepage()

    def _getUser(self, userID: int) -> User | None:
        for user in self.facepage.users:
            if user.userID == userID:
                return user
        return None

    def _getAccountOfUser(self, userID: int) -> Account | None:
        user = self._getUser(userID)
        if user is None:
            return None
        return user.account

    def _getPersonalAccountOfUser(self, userID: int) -> PersonalAccount | None:
        account = self._getAccountOfUser(userID)
        if isinstance(account, PersonalAccount):
            return account
        return None

    def _getBusinessAccountOfUser(self, userID: int) -> BusinessAccount | None:
        account = self._getAccountOfUser(userID)
        if isinstance(account, BusinessAccount):
            return account
        return None

    def _generateAccountNumber(self) -> int:
        existing = {account.accountNumber for account in self.facepage.accounts}
        next_number = len(existing) + 1
        while next_number in existing:
            next_number += 1
        return next_number

    def _getPersonalPage(self, ownerUserID: int, pageName: str) -> PersonalPage | None:
        personalAccount = self._getPersonalAccountOfUser(ownerUserID)
        if personalAccount is None:
            return None
        for page in personalAccount.administrator:
            if page.pageName == pageName:
                return page
        return None

    def _getAdvertisementPage(
        self, ownerUserID: int, pageName: str
    ) -> AdvertisementPage | None:
        businessAccount = self._getBusinessAccountOfUser(ownerUserID)
        if businessAccount is None:
            return None
        for page in businessAccount.advertisementPages:
            if page.pageName == pageName:
                return page
        return None

    def createUser(self, userID: int, name: str, email: str, dateOfBirth: date) -> None:
        if userID is None:
            raise ValueError("The userID of a user must not be empty.")

        if name is None or name.strip() == "":
            raise ValueError("The name of a user must not be empty.")

        if email is None or email.count("@") != 1:
            raise ValueError(
                'The email of a user must contain exactly one "@" character.'
            )
        _, domain = email.split("@")
        if "." not in domain:
            raise ValueError(
                'The email of a user must contain at least one "." after the "@" character.'
            )
        if email.endswith("."):
            raise ValueError('The email of a user must not end with a "." character.')

        reference_date = date.today()
        if dateOfBirth > reference_date:
            raise ValueError("The date of birth of a user must not be in the future.")

        if self._getUser(userID) is not None:
            raise ValueError(f'A user with the ID "{userID}" already exists.')

        birthDatetime = EDate.from_string(
            dateOfBirth.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        )
        created = User(userID=userID, name=name, email=email, birthDate=birthDatetime)
        self.facepage.users.append(created)

    def createPersonalAccount(self, userID: int) -> None:
        user = self._getUser(userID)
        if user is None:
            raise ValueError(f'User "{userID}" does not exist.')

        if user.account is not None:
            raise ValueError(f'A user with the ID "{userID}" already has an account.')

        account_number = self._generateAccountNumber()
        created = PersonalAccount(accountNumber=account_number, user=user)
        self.facepage.accounts.append(created)

    def createBusinessAccount(self, userID: int, companyName: str) -> None:
        user = self._getUser(userID)
        if user is None:
            raise ValueError(f'User "{userID}" does not exist.')

        if user.account is not None:
            raise ValueError(f'A user with the ID "{userID}" already has an account.')

        account_number = self._generateAccountNumber()
        created = BusinessAccount(
            accountNumber=account_number, user=user, companyName=companyName
        )
        self.facepage.accounts.append(created)

    def createPersonalPage(self, pageName: str, userID: int) -> None:
        if pageName is None or pageName.strip() == "":
            raise ValueError("The page name cannot be empty.")

        account = self._getAccountOfUser(userID)
        if account is None:
            raise ValueError(f'Personal account for user "{userID}" does not exist.')
        if not isinstance(account, PersonalAccount):
            raise ValueError("Only personal accounts can create personal pages.")

        for page in account.administrator:
            if page.pageName == pageName:
                raise ValueError(f'A page with the name "{pageName}" already exists.')

        created = PersonalPage(pageName=pageName, visits=0, personalAccount=account)
        self.facepage.pages.append(created)

    def createAdvertisementPage(self, pageName: str, userID: int) -> None:
        if pageName is None or pageName.strip() == "":
            raise ValueError("The page name cannot be empty.")

        account = self._getAccountOfUser(userID)
        if account is None:
            raise ValueError(f'Business account for user "{userID}" does not exist.')
        if not isinstance(account, BusinessAccount):
            raise ValueError("Only business accounts can create advertisement pages.")

        for page in account.advertisementPages:
            if page.pageName == pageName:
                raise ValueError(f'A page with the name "{pageName}" already exists.')

        created = AdvertisementPage(
            pageName=pageName,
            visits=0,
            bounceRate=0.0,
            clickThroughRate=0.0,
            conversionRate=0.0,
            businessAccount=account,
        )
        self.facepage.pages.append(created)

    def createFriendRequest(self, senderUserID: int, receiverUserID: int) -> None:
        if senderUserID is None:
            raise ValueError("Cannot create a friend request without a sender.")
        if receiverUserID is None:
            raise ValueError("Cannot create a friend request without a receiver.")
        if senderUserID == receiverUserID:
            raise ValueError("Cannot send a friend request to itself.")

        senderAccount = self._getAccountOfUser(senderUserID)
        receiverAccount = self._getAccountOfUser(receiverUserID)

        if not isinstance(senderAccount, PersonalAccount):
            raise ValueError("Only personal accounts can send friend requests.")
        if not isinstance(receiverAccount, PersonalAccount):
            raise ValueError("Only personal accounts can receive friend requests.")
        FriendRequest(sender=senderAccount, receiver=receiverAccount)

    def createPrivilege(
        self, privilegeType: str, pageName: str, pageOwnerUserID: int, targetUserID: int
    ) -> None:
        if privilegeType is None or privilegeType.strip() == "":
            raise ValueError("The type of privilege cannot be empty.")
        if pageName is None or pageName.strip() == "":
            raise ValueError("Page cannot be empty.")
        if pageOwnerUserID is None:
            raise ValueError("Owner of the page cannot be empty.")
        if targetUserID is None:
            raise ValueError("Target user cannot be empty.")

        pageOwner = self._getUser(pageOwnerUserID)
        if pageOwner is None:
            raise ValueError(f'User "{pageOwnerUserID}" does not exist.')

        targetUser = self._getUser(targetUserID)
        if targetUser is None:
            raise ValueError(f'User "{targetUserID}" does not exist.')

        personalPage = self._getPersonalPage(pageOwnerUserID, pageName)
        advertisementPage = self._getAdvertisementPage(pageOwnerUserID, pageName)

        if personalPage is None and advertisementPage is None:
            raise ValueError(
                f'Page "{pageName}" does not exist for user "{pageOwnerUserID}".'
            )

        if advertisementPage is not None:
            raise ValueError("Cannot grant privilege on an advertisement page.")

        targetAccount = self._getAccountOfUser(targetUserID)
        if isinstance(targetAccount, BusinessAccount):
            raise ValueError("Cannot grant privilege to a business account.")
        if not isinstance(targetAccount, PersonalAccount):
            raise ValueError(f'User "{targetUserID}" does not have a personal account.')

        if pageOwnerUserID == targetUserID:
            raise ValueError("Cannot grant privilege to the owner of the page.")
        Privilege(
            typeOfPrivilege=privilegeType,
            personalAccount=targetAccount,
            personalPage=personalPage,
        )
