import pytest


@pytest.fixture
def givenController(modelingTool, mw):
    global PowerStatus, PowerStatusActive
    if modelingTool == "umple":
        from ..umple.controller.controller import SymboleoController
        from ..umple.generated_model_layer import (
            Contract, LegalPosition, Role, Power, LegalSituation, TimeInterval, TimePoint
        )
        Contract.contractsById.clear()
        LegalPosition.legalpositionsByName.clear()
        Role.rolesById.clear()
        PowerStatus = Power.PowerStatus
        PowerStatusActive = Power.PowerStatusActive
    else:
        from ..ecore.controller.controller import SymboleoController
        from ..ecore.generated_model_layer import (
            Contract, Role, Power, LegalSituation, TimeInterval, TimePoint,
            PowerStatus, PowerStatusActive
        )

    controller = SymboleoController()
    contract_raw = mw(Contract, id='contract').model
    time_interval_raw = mw(TimeInterval, start=mw(TimePoint).model, end=mw(TimePoint).model).model
    legal_situation_raw = mw(LegalSituation, time=time_interval_raw).model
    role_raw = mw(Role, id='role', contract=contract_raw).model
    controller.power = mw(Power,
        name='power',
        antecedent=legal_situation_raw,
        consequent=legal_situation_raw,
        contract=contract_raw,
        debtor=role_raw,
        creditor=role_raw
    ).model
    yield controller


@pytest.mark.parametrize("current_status,current_active_status,new_status,new_active_status", [
    ('Start', 'Null', 'Create', 'Null'),
    ('Start', 'Null', 'Active', 'InEffect'),
    ('Create', 'Null', 'Active', 'InEffect'),
    ('Create', 'Null', 'UnsuccessfulTermination', 'Null'),
    ('Active', 'InEffect', 'UnsuccessfulTermination', 'Null'),
    ('Active', 'InEffect', 'SuccessfulTermination', 'Null'),
])
def testUpdatePowerStatusSuccessfully(givenController, mw, current_status, current_active_status, new_status, new_active_status):
    power = mw(givenController.power)
    power.setStatus(getattr(PowerStatus, current_status))
    power.setStatusActive(getattr(PowerStatusActive, current_active_status))
    givenController.updatePowerStatus(new_status)
    assert power.getStatus() == getattr(PowerStatus, new_status)
    assert power.getStatusActive() == getattr(PowerStatusActive, new_active_status)


@pytest.mark.parametrize("current_status,new_status", [
    ('Start', 'UnsuccessfulTermination'),
    ('Start', 'SuccessfulTermination'),
    ('Create', 'Start'),
    ('Create', 'SuccessfulTermination'),
    ('Active', 'Start'),
    ('Active', 'Create'),
    ('UnsuccessfulTermination', 'Start'),
    ('UnsuccessfulTermination', 'Create'),
    ('UnsuccessfulTermination', 'Active'),
    ('UnsuccessfulTermination', 'SuccessfulTermination'),
    ('SuccessfulTermination', 'Start'),
    ('SuccessfulTermination', 'Create'),
    ('SuccessfulTermination', 'Active'),
    ('SuccessfulTermination', 'UnsuccessfulTermination'),
])
def testUpdatePowerStatusUnsuccessfullyBecauseOfPowerStatus(givenController, mw, current_status, new_status):
    power = mw(givenController.power)
    power.setStatus(getattr(PowerStatus, current_status))
    with pytest.raises(ValueError) as exc_info:
        givenController.updatePowerStatus(new_status)
    assert str(exc_info.value) == f'Invalid status transition from {current_status} to {new_status}'
    assert power.getStatus() == getattr(PowerStatus, current_status)


@pytest.mark.parametrize("new_status", [
    'UnsuccessfulTermination',
    'SuccessfulTermination',
])
def testUpdatePowerStatusUnsuccessfullyBecausePowerIsSuspended(givenController, mw, new_status):
    power = mw(givenController.power)
    power.setStatus(PowerStatus.Active)
    power.setStatusActive(PowerStatusActive.Suspension)
    with pytest.raises(ValueError) as exc_info:
        givenController.updatePowerStatus(new_status)
    assert str(exc_info.value) == 'Cannot change status while power is suspended'
    assert power.getStatus() == PowerStatus.Active
