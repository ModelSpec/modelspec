# %% NEW FILE CreateAccountActivity BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.36.0.8268.c747da976 modeling language!
# line 139 "model.ump"
# line 272 "model.ump"
from .AppCompatActivity import AppCompatActivity

class CreateAccountActivity(AppCompatActivity):
    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #CreateAccountActivity Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    @classmethod
    def alternateConstructor(cls, aRegistrationForm):
        self = cls.__new__(cls)
        self._registrationForm = None
        super().__init__()
        if aRegistrationForm is None or not (aRegistrationForm.getCreateAccountActivity() is None) :
            raise RuntimeError ("Unable to create CreateAccountActivity due to aRegistrationForm. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        self._registrationForm = aRegistrationForm
        return self

    def __init__(self, aFirstNameForRegistrationForm, aLastNameForRegistrationForm, aUsernameForRegistrationForm, aEmailForRegistrationForm, aPhoneForRegistrationForm, aPasswordForRegistrationForm, aConfirmPasswordForRegistrationForm, aIsOrganizerForRegistrationForm, aCompanyNameForRegistrationForm):
        from .RegistrationForm import RegistrationForm
        self._registrationForm = None
        super().__init__()
        self._registrationForm = RegistrationForm.alternateConstructor(aFirstNameForRegistrationForm, aLastNameForRegistrationForm, aUsernameForRegistrationForm, aEmailForRegistrationForm, aPhoneForRegistrationForm, aPasswordForRegistrationForm, aConfirmPasswordForRegistrationForm, aIsOrganizerForRegistrationForm, aCompanyNameForRegistrationForm, self)

    #------------------------
    # INTERFACE
    #------------------------
    # Code from template association_GetOne 
    def getRegistrationForm(self):
        return self._registrationForm

    def delete(self):
        existingRegistrationForm = self._registrationForm
        self._registrationForm = None
        if not (existingRegistrationForm is None) :
            existingRegistrationForm.delete()
        super().delete()
