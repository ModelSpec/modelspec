import pytest

@pytest.fixture
def controllerWithShelf(modelingTool, mw):
    if modelingTool == "umple":
        from ..umple.controller import CheECSEManagerController
        from ..umple.generated_model_layer import Shelf, ShelfLocation
        Shelf.shelfsById.clear()
        ShelfLocation.nextId = 1

    else: 
        from ..ecore.controller import CheECSEManagerController
        from ..ecore.generated_model_layer import Shelf, ShelfLocation


    controller = CheECSEManagerController()

    sh = mw(Shelf, id="A12", cheECSEManager=controller.cheECSEManager)

    for column in range(1, 6):
        mw(ShelfLocation, column=column, row=1, shelf=sh.model)

    yield controller


@pytest.mark.parametrize(
    "shelfId, nrColumns, nrRows, locationsSize",
    [("B23", 6, 2, 12), ("C45", 3, 5, 15), ("Z99", 1, 10, 10)],
)
def testAddShelfSuccess(controllerWithShelf, shelfId, nrColumns, nrRows, locationsSize, mw):
    # Act
    controllerWithShelf.addShelf(shelfId, nrColumns, nrRows)
    
    # Assert
    controllerWithShelf.cheECSEManager = mw(controllerWithShelf.cheECSEManager)
    assert controllerWithShelf.cheECSEManager.numberOfShelves() == 2

    addedShelf = None
    for sh in controllerWithShelf.cheECSEManager.getShelves():
        if sh.getId() == shelfId:
            addedShelf = sh

    assert addedShelf is not None

    locations = addedShelf.getLocations()
    assert len(locations) == locationsSize

    assert {location.getColumn() for location in locations} == set(range(1, nrColumns + 1))
    assert {location.getRow() for location in locations} == set(range(1, nrRows + 1))
    assert len({(location.getColumn(), location.getRow()) for location in locations}) == locationsSize


@pytest.mark.parametrize(
    "shelfId, nrColumns, nrRows, errorMessage",
    [
        ("A12", 6, 2, "The shelf A12 already exists."),
        ("B23", 0, 2, "Number of columns must be greater than zero."),
        ("B23", 6, 0, "Number of rows must be greater than zero."),
        ("B23", 6, 11, "Number of rows must be at the most ten."),
        ("A", 6, 2, "The id must be three characters long."),
        ("A123", 6, 2, "The id must be three characters long."),
        (" 123", 6, 2, "The first character must be a letter."),
        ("A1X", 6, 2, "The second and third characters must be digits."),
        ("AXY", 6, 2, "The second and third characters must be digits."),
        ("AX1", 6, 2, "The second and third characters must be digits."),
    ],
)
def testAddShelfInvalidInputs(controllerWithShelf, shelfId, nrColumns, nrRows, errorMessage, mw):
    # Act
    with pytest.raises(ValueError) as errorInfo:
        controllerWithShelf.addShelf(shelfId, nrColumns, nrRows)

    # Assert
    controllerWithShelf.cheECSEManager = mw(controllerWithShelf.cheECSEManager)

    assert str(errorInfo.value) == errorMessage
    assert controllerWithShelf.cheECSEManager.numberOfShelves() == 1

    addedShelf = None
    for sh in controllerWithShelf.cheECSEManager.getShelves():
        if sh.getId() == "A12":
            addedShelf = sh

    assert addedShelf is not None
    assert addedShelf.numberOfLocations() == 5