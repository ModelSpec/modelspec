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


@pytest.mark.parametrize("current_active_status,new_active_status", [
    ('InEffect', 'Suspension'),
    ('Suspension', 'InEffect'),
])
def testUpdatePowerActiveStatusSuccessfully(givenController, mw, current_active_status, new_active_status):
    power = mw(givenController.power)
    power.setStatus(PowerStatus.Active)
    power.setStatusActive(getattr(PowerStatusActive, current_active_status))
    givenController.updatePowerActiveStatus(new_active_status)
    assert power.getStatusActive() == getattr(PowerStatusActive, new_active_status)


@pytest.mark.parametrize("current_status,new_active_status", [
    ('Start', 'InEffect'),
    ('Start', 'Suspension'),
    ('Create', 'InEffect'),
    ('Create', 'Suspension'),
    ('UnsuccessfulTermination', 'InEffect'),
    ('UnsuccessfulTermination', 'Suspension'),
    ('SuccessfulTermination', 'InEffect'),
    ('SuccessfulTermination', 'Suspension'),
])
def testUpdatePowerActiveStatusUnsuccessfully(givenController, mw, current_status, new_active_status):
    power = mw(givenController.power)
    power.setStatus(getattr(PowerStatus, current_status))
    power.setStatusActive(PowerStatusActive.Null)
    with pytest.raises(ValueError) as exc_info:
        givenController.updatePowerActiveStatus(new_active_status)
    assert str(exc_info.value) == f'Cannot set active status when power status is {current_status}'
    assert power.getStatusActive() == PowerStatusActive.Null
