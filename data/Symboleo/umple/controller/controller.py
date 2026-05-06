from ..generated_model_layer import *


class SymboleoController:
    def __init__(self) -> None:
        self.contract = None
        self.obligation = None
        self.power = None

    def updateContractStatus(self, newStatus: str) -> None:
        current = self.contract.getStatus()
        statusEnum = getattr(Contract.ContractStatus, newStatus)

        valid_transitions = {
            Contract.ContractStatus.Form: [Contract.ContractStatus.Active],
            Contract.ContractStatus.Active: [Contract.ContractStatus.SuccessfulTermination, Contract.ContractStatus.UnsuccessfulTermination],
            Contract.ContractStatus.SuccessfulTermination: [], # terminal status
            Contract.ContractStatus.UnsuccessfulTermination: [] # terminal status
        }

        if statusEnum not in valid_transitions.get(current, []):
            raise ValueError(f'Invalid status transition from {current} to {statusEnum}')

        if (current == Contract.ContractStatus.Active and self.contract.getStatusActive() in
            [Contract.ContractStatusActive.Suspension, Contract.ContractStatusActive.Unassign, Contract.ContractStatusActive.Rescission]):
            if statusEnum in [Contract.ContractStatus.SuccessfulTermination, Contract.ContractStatus.UnsuccessfulTermination]:
                raise ValueError(f'Cannot change status while contract active status is {self.contract.getStatusActive()}')

        self.contract.setStatus(statusEnum)

        if statusEnum == Contract.ContractStatus.Active:
            self.contract.setStatusActive(Contract.ContractStatusActive.InEffect)
        else:
            self.contract.setStatusActive(Contract.ContractStatusActive.Null)

    def updateContractActiveStatus(self, newActiveStatus: str) -> None:
        current = self.contract.getStatusActive()
        activeStatusEnum = getattr(Contract.ContractStatusActive, newActiveStatus)

        if self.contract.getStatus() != Contract.ContractStatus.Active:
            raise ValueError(f'Cannot set active status when contract status is {self.contract.getStatus()}')

        valid_transitions = {
            Contract.ContractStatusActive.InEffect: [
                Contract.ContractStatusActive.Suspension,
                Contract.ContractStatusActive.Unassign,
                Contract.ContractStatusActive.Rescission
            ],
            Contract.ContractStatusActive.Suspension: [Contract.ContractStatusActive.InEffect],
            Contract.ContractStatusActive.Unassign: [Contract.ContractStatusActive.InEffect],
            Contract.ContractStatusActive.Rescission: []
        }

        if activeStatusEnum not in valid_transitions.get(current, []):
            raise ValueError(f'Invalid active status transition from {current} to {activeStatusEnum}')

        self.contract.setStatusActive(activeStatusEnum)

    def updateObligationStatus(self, newStatus: str) -> None:
        statusEnum = getattr(Obligation.ObligationStatus, newStatus)

        if self.obligation.getStatus() == Obligation.ObligationStatus.Active and self.obligation.getStatusActive() == Obligation.ObligationStatusActive.Suspension:
            if statusEnum in [Obligation.ObligationStatus.Violation, Obligation.ObligationStatus.Discharge, Obligation.ObligationStatus.Fulfillment]:
                raise ValueError('Cannot change status while obligation is suspended')

        valid_transitions = {
            Obligation.ObligationStatus.Start: [Obligation.ObligationStatus.Create, Obligation.ObligationStatus.Active],
            Obligation.ObligationStatus.Create: [Obligation.ObligationStatus.Active, Obligation.ObligationStatus.Discharge],
            Obligation.ObligationStatus.Active: [
                Obligation.ObligationStatus.Violation,
                Obligation.ObligationStatus.Discharge,
                Obligation.ObligationStatus.Fulfillment,
                Obligation.ObligationStatus.UnsuccessfulTermination
            ],
            Obligation.ObligationStatus.Violation: [], # terminal status
            Obligation.ObligationStatus.Discharge: [], # terminal status
            Obligation.ObligationStatus.Fulfillment: [], # terminal status
            Obligation.ObligationStatus.UnsuccessfulTermination: [] # terminal status
        }

        if statusEnum not in valid_transitions.get(self.obligation.getStatus(), []):
            raise ValueError(f'Invalid status transition from {self.obligation.getStatus()} to {statusEnum}')

        self.obligation.setStatus(statusEnum)

        if statusEnum == Obligation.ObligationStatus.Active:
            self.obligation.setStatusActive(Obligation.ObligationStatusActive.InEffect)
        elif statusEnum in [
            Obligation.ObligationStatus.Create,
            Obligation.ObligationStatus.Start,
            Obligation.ObligationStatus.Violation,
            Obligation.ObligationStatus.Discharge,
            Obligation.ObligationStatus.Fulfillment,
            Obligation.ObligationStatus.UnsuccessfulTermination
        ]:
            self.obligation.setStatusActive(Obligation.ObligationStatusActive.Null)

    def updateObligationActiveStatus(self, newActiveStatus: str) -> None:
        activeStatusEnum = getattr(Obligation.ObligationStatusActive, newActiveStatus)

        if self.obligation.getStatus() != Obligation.ObligationStatus.Active:
            raise ValueError(f'Cannot set active status when obligation status is {self.obligation.getStatus()}')

        valid_transitions = {
            Obligation.ObligationStatusActive.InEffect: [Obligation.ObligationStatusActive.Suspension],
            Obligation.ObligationStatusActive.Suspension: [Obligation.ObligationStatusActive.InEffect]
        }

        if activeStatusEnum not in valid_transitions.get(self.obligation.getStatusActive(), []):
            raise ValueError(f'Invalid active status transition from {self.obligation.getStatusActive()} to {activeStatusEnum}')

        self.obligation.setStatusActive(activeStatusEnum)

    def updatePowerStatus(self, newStatus: str) -> None:
        statusEnum = getattr(Power.PowerStatus, newStatus)

        if self.power.getStatus() == Power.PowerStatus.Active and self.power.getStatusActive() == Power.PowerStatusActive.Suspension:
            if statusEnum in [Power.PowerStatus.UnsuccessfulTermination, Power.PowerStatus.SuccessfulTermination]:
                raise ValueError('Cannot change status while power is suspended')

        valid_transitions = {
            Power.PowerStatus.Start: [Power.PowerStatus.Create, Power.PowerStatus.Active],
            Power.PowerStatus.Create: [Power.PowerStatus.Active, Power.PowerStatus.UnsuccessfulTermination],
            Power.PowerStatus.Active: [Power.PowerStatus.UnsuccessfulTermination, Power.PowerStatus.SuccessfulTermination],
            Power.PowerStatus.SuccessfulTermination: [], # terminal status
            Power.PowerStatus.UnsuccessfulTermination: [] # terminal status
        }

        if statusEnum not in valid_transitions.get(self.power.getStatus(), []):
            raise ValueError(f'Invalid status transition from {self.power.getStatus()} to {statusEnum}')

        self.power.setStatus(statusEnum)

        if statusEnum == Power.PowerStatus.Active:
            self.power.setStatusActive(Power.PowerStatusActive.InEffect)
        elif statusEnum in [Power.PowerStatus.Create, Power.PowerStatus.Start, Power.PowerStatus.SuccessfulTermination, Power.PowerStatus.UnsuccessfulTermination]:
            self.power.setStatusActive(Power.PowerStatusActive.Null)

    def updatePowerActiveStatus(self, newActiveStatus: str) -> None:
        activeStatusEnum = getattr(Power.PowerStatusActive, newActiveStatus)

        if self.power.getStatus() != Power.PowerStatus.Active:
            raise ValueError(f'Cannot set active status when power status is {self.power.getStatus()}')

        valid_transitions = {
            Power.PowerStatusActive.InEffect: [Power.PowerStatusActive.Suspension],
            Power.PowerStatusActive.Suspension: [Power.PowerStatusActive.InEffect]
        }

        if activeStatusEnum not in valid_transitions.get(self.power.getStatusActive(), []):
            raise ValueError(f'Invalid active status transition from {self.power.getStatusActive()} to {activeStatusEnum}')

        self.power.setStatusActive(activeStatusEnum)
