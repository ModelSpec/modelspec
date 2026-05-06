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


@pytest.mark.parametrize("current_active_status,new_active_status", [
    ('InEffect', 'Suspension'),
    ('Suspension', 'InEffect'),
])
def testUpdateObligationActiveStatusSuccessfully(givenController, mw, current_active_status, new_active_status):
    obligation = mw(givenController.obligation)
    obligation.setStatus(ObligationStatus.Active)
    obligation.setStatusActive(getattr(ObligationStatusActive, current_active_status))
    givenController.updateObligationActiveStatus(new_active_status)
    assert obligation.getStatusActive() == getattr(ObligationStatusActive, new_active_status)


@pytest.mark.parametrize("current_status,new_active_status", [
    ('Start', 'Suspension'),
    ('Start', 'InEffect'),
    ('Create', 'Suspension'),
    ('Create', 'InEffect'),
    ('Violation', 'Suspension'),
    ('Violation', 'InEffect'),
    ('Discharge', 'Suspension'),
    ('Discharge', 'InEffect'),
    ('Fulfillment', 'Suspension'),
    ('Fulfillment', 'InEffect'),
    ('UnsuccessfulTermination', 'Suspension'),
    ('UnsuccessfulTermination', 'InEffect'),
])
def testUpdateObligationActiveStatusUnsuccessfullyBecauseOfObligationStatus(givenController, mw, current_status, new_active_status):
    obligation = mw(givenController.obligation)
    obligation.setStatus(getattr(ObligationStatus, current_status))
    obligation.setStatusActive(ObligationStatusActive.Null)
    with pytest.raises(ValueError) as exc_info:
        givenController.updateObligationActiveStatus(new_active_status)
    assert str(exc_info.value) == f'Cannot set active status when obligation status is {current_status}'
    assert obligation.getStatusActive() == ObligationStatusActive.Null
