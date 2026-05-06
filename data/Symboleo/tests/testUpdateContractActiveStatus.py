import pytest


@pytest.fixture
def givenController(modelingTool, mw):
    global ContractStatus, ContractStatusActive
    if modelingTool == "umple":
        from ..umple.controller.controller import SymboleoController
        from ..umple.generated_model_layer import Contract, LegalPosition, Role
        Contract.contractsById.clear()
        LegalPosition.legalpositionsByName.clear()
        Role.rolesById.clear()
        ContractStatus = Contract.ContractStatus
        ContractStatusActive = Contract.ContractStatusActive
    else:
        from ..ecore.controller.controller import SymboleoController
        from ..ecore.generated_model_layer import Contract, ContractStatus, ContractStatusActive

    controller = SymboleoController()
    controller.contract = mw(Contract, id='contract').model
    yield controller


@pytest.mark.parametrize("current_active_status,new_active_status", [
    ('InEffect', 'Suspension'),
    ('InEffect', 'Unassign'),
    ('InEffect', 'Rescission'),
    ('Suspension', 'InEffect'),
    ('Unassign', 'InEffect'),
])
def testUpdateContractActiveStatusSuccessfully(givenController, mw, current_active_status, new_active_status):
    contract = mw(givenController.contract)
    contract.setStatus(ContractStatus.Active)
    contract.setStatusActive(getattr(ContractStatusActive, current_active_status))
    givenController.updateContractActiveStatus(new_active_status)
    assert contract.getStatusActive() == getattr(ContractStatusActive, new_active_status)


@pytest.mark.parametrize("current_status,new_active_status", [
    ('Form', 'InEffect'),
    ('Form', 'Suspension'),
    ('Form', 'Unassign'),
    ('Form', 'Rescission'),
    ('SuccessfulTermination', 'InEffect'),
    ('SuccessfulTermination', 'Suspension'),
    ('SuccessfulTermination', 'Unassign'),
    ('SuccessfulTermination', 'Rescission'),
    ('UnsuccessfulTermination', 'InEffect'),
    ('UnsuccessfulTermination', 'Suspension'),
    ('UnsuccessfulTermination', 'Unassign'),
    ('UnsuccessfulTermination', 'Rescission'),
])
def testUpdateContractActiveStatusUnsuccessfullyBecauseOfContractStatus(givenController, mw, current_status, new_active_status):
    contract = mw(givenController.contract)
    contract.setStatus(getattr(ContractStatus, current_status))
    contract.setStatusActive(ContractStatusActive.Null)
    with pytest.raises(ValueError) as exc_info:
        givenController.updateContractActiveStatus(new_active_status)
    assert str(exc_info.value) == f'Cannot set active status when contract status is {current_status}'
    assert contract.getStatusActive() == ContractStatusActive.Null


@pytest.mark.parametrize("current_active_status,new_active_status", [
    ('Suspension', 'Unassign'),
    ('Suspension', 'Rescission'),
    ('Unassign', 'Suspension'),
    ('Unassign', 'Rescission'),
    ('Rescission', 'InEffect'),
    ('Rescission', 'Suspension'),
    ('Rescission', 'Unassign'),
])
def testUpdateContractActiveStatusUnsuccessfullyBecauseOfContractActiveStatus(givenController, mw, current_active_status, new_active_status):
    contract = mw(givenController.contract)
    contract.setStatus(ContractStatus.Active)
    contract.setStatusActive(getattr(ContractStatusActive, current_active_status))
    with pytest.raises(ValueError) as exc_info:
        givenController.updateContractActiveStatus(new_active_status)
    assert str(exc_info.value) == f'Invalid active status transition from {current_active_status} to {new_active_status}'
    assert contract.getStatusActive() == getattr(ContractStatusActive, current_active_status)
