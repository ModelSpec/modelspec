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


@pytest.mark.parametrize("current_status,new_status", [
    ('Form', 'Active'),
    ('Active', 'SuccessfulTermination'),
    ('Active', 'UnsuccessfulTermination'),
])
def testUpdateContractStatusSuccessfully(givenController, mw, current_status, new_status):
    contract = mw(givenController.contract)
    contract.setStatus(getattr(ContractStatus, current_status))
    givenController.updateContractStatus(new_status)
    assert contract.getStatus() == getattr(ContractStatus, new_status)


@pytest.mark.parametrize("current_status,new_status", [
    ('Form', 'SuccessfulTermination'),
    ('Form', 'UnsuccessfulTermination'),
    ('Active', 'Form'),
    ('SuccessfulTermination', 'Form'),
    ('SuccessfulTermination', 'Active'),
    ('SuccessfulTermination', 'UnsuccessfulTermination'),
    ('UnsuccessfulTermination', 'Form'),
    ('UnsuccessfulTermination', 'Active'),
    ('UnsuccessfulTermination', 'SuccessfulTermination'),
])
def testUpdateContractStatusUnsuccessfullyBecauseOfContractStatus(givenController, mw, current_status, new_status):
    contract = mw(givenController.contract)
    contract.setStatus(getattr(ContractStatus, current_status))
    with pytest.raises(ValueError) as exc_info:
        givenController.updateContractStatus(new_status)
    assert str(exc_info.value) == f'Invalid status transition from {current_status} to {new_status}'
    assert contract.getStatus() == getattr(ContractStatus, current_status)


@pytest.mark.parametrize("current_active_status,new_status", [
    ('Suspension', 'SuccessfulTermination'),
    ('Suspension', 'UnsuccessfulTermination'),
    ('Unassign', 'SuccessfulTermination'),
    ('Unassign', 'UnsuccessfulTermination'),
    ('Rescission', 'SuccessfulTermination'),
    ('Rescission', 'UnsuccessfulTermination'),
])
def testUpdateContractStatusUnsuccessfullyBecauseOfContractActiveStatus(givenController, mw, current_active_status, new_status):
    contract = mw(givenController.contract)
    contract.setStatus(ContractStatus.Active)
    contract.setStatusActive(getattr(ContractStatusActive, current_active_status))
    with pytest.raises(ValueError) as exc_info:
        givenController.updateContractStatus(new_status)
    assert str(exc_info.value) == f'Cannot change status while contract active status is {current_active_status}'
    assert contract.getStatus() == ContractStatus.Active
