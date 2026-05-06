import pytest


@pytest.fixture
def givenController(modelingTool, mw):
    global ObligationStatus, ObligationStatusActive
    if modelingTool == "umple":
        from ..umple.controller.controller import SymboleoController
        from ..umple.generated_model_layer import (
            Contract, LegalPosition, Role, Obligation, LegalSituation, TimeInterval, TimePoint
        )
        Contract.contractsById.clear()
        LegalPosition.legalpositionsByName.clear()
        Role.rolesById.clear()
        ObligationStatus = Obligation.ObligationStatus
        ObligationStatusActive = Obligation.ObligationStatusActive
    else:
        from ..ecore.controller.controller import SymboleoController
        from ..ecore.generated_model_layer import (
            Contract, Role, Obligation, LegalSituation, TimeInterval, TimePoint,
            ObligationStatus, ObligationStatusActive
        )

    controller = SymboleoController()
    contract_raw = mw(Contract, id='contract').model
    time_interval_raw = mw(TimeInterval, start=mw(TimePoint).model, end=mw(TimePoint).model).model
    legal_situation_raw = mw(LegalSituation, time=time_interval_raw).model
    role_raw = mw(Role, id='role', contract=contract_raw).model
    controller.obligation = mw(Obligation,
        name='obligation',
        antecedent=legal_situation_raw,
        consequent=legal_situation_raw,
        contract=contract_raw,
        debtor=role_raw,
        creditor=role_raw,
        surviving=None
    ).model
    yield controller


@pytest.mark.parametrize("current_status,current_active_status,new_status,new_active_status", [
    ('Start', 'Null', 'Create', 'Null'),
    ('Start', 'Null', 'Active', 'InEffect'),
    ('Create', 'Null', 'Active', 'InEffect'),
    ('Create', 'Null', 'Discharge', 'Null'),
    ('Active', 'InEffect', 'Violation', 'Null'),
    ('Active', 'InEffect', 'Discharge', 'Null'),
    ('Active', 'InEffect', 'Fulfillment', 'Null'),
    ('Active', 'InEffect', 'UnsuccessfulTermination', 'Null'),
    ('Active', 'Suspension', 'UnsuccessfulTermination', 'Null'),
])
def testUpdateObligationStatusSuccessfully(givenController, mw, current_status, current_active_status, new_status, new_active_status):
    obligation = mw(givenController.obligation)
    obligation.setStatus(getattr(ObligationStatus, current_status))
    obligation.setStatusActive(getattr(ObligationStatusActive, current_active_status))
    givenController.updateObligationStatus(new_status)
    assert obligation.getStatus() == getattr(ObligationStatus, new_status)
    assert obligation.getStatusActive() == getattr(ObligationStatusActive, new_active_status)


@pytest.mark.parametrize("current_status,new_status", [
    ('Start', 'Discharge'),
    ('Start', 'Violation'),
    ('Start', 'Fulfillment'),
    ('Start', 'UnsuccessfulTermination'),
    ('Create', 'Start'),
    ('Create', 'Violation'),
    ('Create', 'Fulfillment'),
    ('Create', 'UnsuccessfulTermination'),
    ('Active', 'Start'),
    ('Active', 'Create'),
    ('Violation', 'Start'),
    ('Violation', 'Create'),
    ('Violation', 'Active'),
    ('Violation', 'Discharge'),
    ('Violation', 'Fulfillment'),
    ('Violation', 'UnsuccessfulTermination'),
    ('Discharge', 'Start'),
    ('Discharge', 'Create'),
    ('Discharge', 'Active'),
    ('Discharge', 'Violation'),
    ('Discharge', 'Fulfillment'),
    ('Discharge', 'UnsuccessfulTermination'),
    ('Fulfillment', 'Start'),
    ('Fulfillment', 'Create'),
    ('Fulfillment', 'Active'),
    ('Fulfillment', 'Violation'),
    ('Fulfillment', 'Discharge'),
    ('Fulfillment', 'UnsuccessfulTermination'),
    ('UnsuccessfulTermination', 'Start'),
    ('UnsuccessfulTermination', 'Create'),
    ('UnsuccessfulTermination', 'Active'),
    ('UnsuccessfulTermination', 'Violation'),
    ('UnsuccessfulTermination', 'Discharge'),
    ('UnsuccessfulTermination', 'Fulfillment'),
])
def testUpdateObligationStatusUnsuccessfullyBecauseOfObligationStatus(givenController, mw, current_status, new_status):
    obligation = mw(givenController.obligation)
    obligation.setStatus(getattr(ObligationStatus, current_status))
    with pytest.raises(ValueError) as exc_info:
        givenController.updateObligationStatus(new_status)
    assert str(exc_info.value) == f'Invalid status transition from {current_status} to {new_status}'
    assert obligation.getStatus() == getattr(ObligationStatus, current_status)


@pytest.mark.parametrize("new_status", [
    'Violation',
    'Discharge',
    'Fulfillment',
])
def testUpdateObligationStatusUnsuccessfullyBecauseObligationIsSuspended(givenController, mw, new_status):
    obligation = mw(givenController.obligation)
    obligation.setStatus(ObligationStatus.Active)
    obligation.setStatusActive(ObligationStatusActive.Suspension)
    with pytest.raises(ValueError) as exc_info:
        givenController.updateObligationStatus(new_status)
    assert str(exc_info.value) == 'Cannot change status while obligation is suspended'
    assert obligation.getStatus() == ObligationStatus.Active
