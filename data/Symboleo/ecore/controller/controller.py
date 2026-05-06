from ..generated_model_layer import *


class SymboleoController:
    def __init__(self) -> None:
        self.contract = None
        self.obligation = None
        self.power = None

    def updateContractStatus(self, newStatus: str) -> None:
        current = self.contract.status
        statusEnum = getattr(ContractStatus, newStatus)

        valid_transitions = {
            ContractStatus.Form: [ContractStatus.Active],
            ContractStatus.Active: [ContractStatus.SuccessfulTermination, ContractStatus.UnsuccessfulTermination],
            ContractStatus.SuccessfulTermination: [], # terminal status
            ContractStatus.UnsuccessfulTermination: [] # terminal status
        }

        if statusEnum not in valid_transitions.get(current, []):
            raise ValueError(f'Invalid status transition from {current.name} to {statusEnum.name}')

        if (current == ContractStatus.Active and self.contract.statusActive in
            [ContractStatusActive.Suspension, ContractStatusActive.Unassign, ContractStatusActive.Rescission]):
            if statusEnum in [ContractStatus.SuccessfulTermination, ContractStatus.UnsuccessfulTermination]:
                raise ValueError(f'Cannot change status while contract active status is {self.contract.statusActive.name}')

        self.contract.status = statusEnum

        if statusEnum == ContractStatus.Active:
            self.contract.statusActive = ContractStatusActive.InEffect
        else:
            self.contract.statusActive = ContractStatusActive.Null

    def updateContractActiveStatus(self, newActiveStatus: str) -> None:
        current = self.contract.statusActive
        activeStatusEnum = getattr(ContractStatusActive, newActiveStatus)

        if self.contract.status != ContractStatus.Active:
            raise ValueError(f'Cannot set active status when contract status is {self.contract.status.name}')

        valid_transitions = {
            ContractStatusActive.InEffect: [
                ContractStatusActive.Suspension,
                ContractStatusActive.Unassign,
                ContractStatusActive.Rescission
            ],
            ContractStatusActive.Suspension: [ContractStatusActive.InEffect],
            ContractStatusActive.Unassign: [ContractStatusActive.InEffect],
            ContractStatusActive.Rescission: []
        }

        if activeStatusEnum not in valid_transitions.get(current, []):
            raise ValueError(f'Invalid active status transition from {current.name} to {activeStatusEnum.name}')

        self.contract.statusActive = activeStatusEnum

    def updateObligationStatus(self, newStatus: str) -> None:
        statusEnum = getattr(ObligationStatus, newStatus)

        if self.obligation.status == ObligationStatus.Active and self.obligation.statusActive == ObligationStatusActive.Suspension:
            if statusEnum in [ObligationStatus.Violation, ObligationStatus.Discharge, ObligationStatus.Fulfillment]:
                raise ValueError('Cannot change status while obligation is suspended')

        valid_transitions = {
            ObligationStatus.Start: [ObligationStatus.Create, ObligationStatus.Active],
            ObligationStatus.Create: [ObligationStatus.Active, ObligationStatus.Discharge],
            ObligationStatus.Active: [
                ObligationStatus.Violation,
                ObligationStatus.Discharge,
                ObligationStatus.Fulfillment,
                ObligationStatus.UnsuccessfulTermination
            ],
            ObligationStatus.Violation: [], # terminal status
            ObligationStatus.Discharge: [], # terminal status
            ObligationStatus.Fulfillment: [], # terminal status
            ObligationStatus.UnsuccessfulTermination: [] # terminal status
        }

        if statusEnum not in [s for s in valid_transitions.get(self.obligation.status, [])]:
            raise ValueError(f'Invalid status transition from {self.obligation.status.name} to {statusEnum.name}')

        self.obligation.status = statusEnum

        if statusEnum == ObligationStatus.Active:
            self.obligation.statusActive = ObligationStatusActive.InEffect
        elif (statusEnum in [
            ObligationStatus.Create,
            ObligationStatus.Start,
            ObligationStatus.Violation,
            ObligationStatus.Discharge,
            ObligationStatus.Fulfillment,
            ObligationStatus.UnsuccessfulTermination
        ]):
            self.obligation.statusActive = ObligationStatusActive.Null

    def updateObligationActiveStatus(self, newActiveStatus: str) -> None:
        activeStatusEnum = getattr(ObligationStatusActive, newActiveStatus)

        if self.obligation.status != ObligationStatus.Active:
            raise ValueError(f'Cannot set active status when obligation status is {self.obligation.status.name}')

        valid_transitions = {
            ObligationStatusActive.InEffect: [ObligationStatusActive.Suspension],
            ObligationStatusActive.Suspension: [ObligationStatusActive.InEffect]
        }

        if activeStatusEnum not in valid_transitions.get(self.obligation.statusActive, []):
            raise ValueError(f'Invalid active status transition from {self.obligation.statusActive.name} to {activeStatusEnum.name}')

        self.obligation.statusActive = activeStatusEnum

    def updatePowerStatus(self, newStatus: str) -> None:
        statusEnum = getattr(PowerStatus, newStatus)

        if self.power.status == PowerStatus.Active and self.power.statusActive == PowerStatusActive.Suspension:
            if statusEnum in [PowerStatus.UnsuccessfulTermination, PowerStatus.SuccessfulTermination]:
                raise ValueError('Cannot change status while power is suspended')

        valid_transitions = {
            PowerStatus.Start: [PowerStatus.Create, PowerStatus.Active],
            PowerStatus.Create: [PowerStatus.Active, PowerStatus.UnsuccessfulTermination],
            PowerStatus.Active: [PowerStatus.UnsuccessfulTermination, PowerStatus.SuccessfulTermination],
            PowerStatus.SuccessfulTermination: [], # terminal status
            PowerStatus.UnsuccessfulTermination: [] # terminal status
        }

        if statusEnum not in [s for s in valid_transitions.get(self.power.status, [])]:
            raise ValueError(f'Invalid status transition from {self.power.status.name} to {statusEnum.name}')

        self.power.status = statusEnum

        if statusEnum == PowerStatus.Active:
            self.power.statusActive = PowerStatusActive.InEffect
        elif statusEnum in [PowerStatus.Create, PowerStatus.Start, PowerStatus.SuccessfulTermination, PowerStatus.UnsuccessfulTermination]:
            self.power.statusActive = PowerStatusActive.Null

    def updatePowerActiveStatus(self, newActiveStatus: str) -> None:
        activeStatusEnum = getattr(PowerStatusActive, newActiveStatus)

        if self.power.status != PowerStatus.Active:
            raise ValueError(f'Cannot set active status when power status is {self.power.status.name}')

        valid_transitions = {
            PowerStatusActive.InEffect: [PowerStatusActive.Suspension],
            PowerStatusActive.Suspension: [PowerStatusActive.InEffect]
        }

        if activeStatusEnum not in valid_transitions.get(self.power.statusActive, []):
            raise ValueError(f'Invalid active status transition from {self.power.statusActive.name} to {activeStatusEnum.name}')

        self.power.statusActive = activeStatusEnum
