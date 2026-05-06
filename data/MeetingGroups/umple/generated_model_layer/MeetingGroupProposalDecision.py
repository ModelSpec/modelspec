# %% NEW FILE MeetingGroupProposalDecision BEGINS HERE %%

#PLEASE DO NOT EDIT THIS CODE
#This code was generated using the UMPLE 1.35.0.7523.c616a4dce modeling language!
# line 78 "model.ump"
# line 295 "model.ump"
import os
from enum import Enum, auto

class MeetingGroupProposalDecision():
    #------------------------
    # ENUMERATIONS
    #------------------------
    class MeetingGroupProposalDecisionCode(Enum):
        def _generate_next_value_(name, start, count, last_values):
            return name
        def __str__(self):
            return str(self.value)
        NoDecision = auto()
        Accept = auto()
        Reject = auto()

    #------------------------
    # MEMBER VARIABLES
    #------------------------
    #MeetingGroupProposalDecision Attributes
    #MeetingGroupProposalDecision Associations
    #------------------------
    # CONSTRUCTOR
    #------------------------
    def __init__(self, aRejectReason, aCode, aProposal, aAdministrator):
        self._administrator = None
        self._proposal = None
        self._code = None
        self._date = None
        self._rejectReason = None
        self._rejectReason = aRejectReason
        self._date = None
        self._code = aCode
        didAddProposal = self.setProposal(aProposal)
        if not didAddProposal :
            raise RuntimeError ("Unable to create decision due to proposal. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")
        if not self.setAdministrator(aAdministrator) :
            raise RuntimeError ("Unable to create MeetingGroupProposalDecision due to aAdministrator. See https://manual.umple.org?RE002ViolationofAssociationMultiplicity.html")

    #------------------------
    # INTERFACE
    #------------------------
    def setRejectReason(self, aRejectReason):
        wasSet = False
        self._rejectReason = aRejectReason
        wasSet = True
        return wasSet

    def setDate(self, aDate):
        wasSet = False
        self._date = aDate
        wasSet = True
        return wasSet

    def setCode(self, aCode):
        wasSet = False
        self._code = aCode
        wasSet = True
        return wasSet

    def getRejectReason(self):
        return self._rejectReason

    def getDate(self):
        return self._date

    def getCode(self):
        return self._code

    # Code from template association_GetOne
    def getProposal(self):
        return self._proposal

    # Code from template association_GetOne
    def getAdministrator(self):
        return self._administrator

    # Code from template association_SetOneToMany
    def setProposal(self, aProposal):
        wasSet = False
        if aProposal is None :
            return wasSet
        existingProposal = self._proposal
        self._proposal = aProposal
        if not (existingProposal is None) and not existingProposal == aProposal :
            existingProposal.removeDecision(self)
        self._proposal.addDecision(self)
        wasSet = True
        return wasSet

    # Code from template association_SetUnidirectionalOne
    def setAdministrator(self, aNewAdministrator):
        wasSet = False
        if not (aNewAdministrator is None) :
            self._administrator = aNewAdministrator
            wasSet = True
        return wasSet

    def delete(self):
        placeholderProposal = self._proposal
        self._proposal = None
        if not (placeholderProposal is None) :
            placeholderProposal.removeDecision(self)
        self._administrator = None

    def __str__(self):
        return str(super().__str__()) + "[" + "rejectReason" + ":" + str(self.getRejectReason()) + "]" + str(os.linesep) + "  " + "date" + "=" + str((((self.getDate().__str__().replaceAll("  ", "    ")) if not self.getDate() == self else "this") if not (self.getDate() is None) else "null")) + str(os.linesep) + "  " + "code" + "=" + str((((self.getCode().__str__().replaceAll("  ", "    ")) if not self.getCode() == self else "this") if not (self.getCode() is None) else "null")) + str(os.linesep) + "  " + "proposal = " + str(((format(id(self.getProposal()), "x")) if not (self.getProposal() is None) else "null")) + str(os.linesep) + "  " + "administrator = " + ((format(id(self.getAdministrator()), "x")) if not (self.getAdministrator() is None) else "null")
