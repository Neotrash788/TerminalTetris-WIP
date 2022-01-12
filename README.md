# TerminalTetris-WIP
Logger module does not exist, it is something I made myself to help with debugging. If you want to run the code consider deleting the 'import logger statement' and any references to the file. These will be removed later.

Cannot be run in standart python terminal, it will have a tantrum due to the colours.

Plan\n
Shadow:
=====================================================
Shadow blocks can't effect any piece movement
-----------------------------------------------------
Logic.onGround has to account for shadow blocks
Logic.isTspin has to account for shadow blocks
Logic.canMove has to account for shadow blocks
Logic.validRotation has to account for shadow blocks
------------------------------------------------------
drawing shadow
------------------------------------------------------
shadow class inherits from shape class
repeat for every rotation or LR movement:
    copy origin
    move until ground (inherits from shape class)
    print the shadow pieces
keep track of each cord of a shadow cell
remove each cord if it is not lib[0]
-------------------------------------------------------
=======================================================
