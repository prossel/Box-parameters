import adsk.core, adsk.fusion
import os
from ...lib import fusionAddInUtils as futil
from ... import config
app = adsk.core.Application.get()
ui = app.userInterface

# need to bring in the design and user params
design = adsk.fusion.Design.cast(app.activeProduct)
userParams = design.userParameters

# TODO *** Specify the command identity information. ***
CMD_ID = f'{config.COMPANY_NAME}_{config.ADDIN_NAME}_cmdDialog'
print(CMD_ID)
CMD_NAME = 'Box parameters'
CMD_Description = 'A Fusion Add-in Command with a dialog'

# Specify that the command will be promoted to the panel.
IS_PROMOTED = True

# TODO *** Define the location where the command button will be created. ***
# This is done by specifying the workspace, the tab, and the panel, and the 
# command it will be inserted beside. Not providing the command to position it
# will insert it at the end.
WORKSPACE_ID = 'FusionSolidEnvironment'
PANEL_ID = 'SolidScriptsAddinsPanel'
COMMAND_BESIDE_ID = 'ScriptsManagerCommand'

# Resource location for command icons, here we assume a sub folder in this directory named "resources".
ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources', '')

# Local list of event handlers used to maintain a reference so
# they are not released and garbage collected.
local_handlers = []

# get the user parameters
lengthParam = userParams.itemByName('xSize')
widthParam = userParams.itemByName('ySize')
heightParam = userParams.itemByName('zSize')
thicknessParam = userParams.itemByName('thickness')
targetTabWidthParam = userParams.itemByName('targetTabWidth')

# Check if any of the user parameters are missing and ask the user to create them
if lengthParam is None or widthParam is None or heightParam is None or thicknessParam is None or targetTabWidthParam is None:
    msg = 'One or more user parameters are missing. Would you like to create them?'
    if ui.messageBox(msg, 'Missing User Parameters', adsk.core.MessageBoxButtonTypes.YesNoButtonType) == adsk.core.DialogResults.DialogYes:
        if lengthParam is None:
            lengthParam = userParams.add('xSize', adsk.core.ValueInput.createByString('80 mm'), 'mm', 'Length of the box')
        if widthParam is None:
            widthParam = userParams.add('ySize', adsk.core.ValueInput.createByString('60 mm') , 'mm', 'Width of the box')
        if heightParam is None:
            heightParam = userParams.add('zSize', adsk.core.ValueInput.createByString('50 mm'), 'mm', 'Height of the box')
        if thicknessParam is None:
            thicknessParam = userParams.add('thickness', adsk.core.ValueInput.createByString('3 mm'), 'mm', 'Thickness of the material')
        if targetTabWidthParam is None:
            targetTabWidthParam = userParams.add('targetTabWidth', adsk.core.ValueInput.createByString('10 mm'), 'mm', 'Target width of the tabs')
    else:
        ui.messageBox('User parameters are missing. Exiting command.')

# Executed when add-in is run.
def start():
    # Create a command Definition.
    cmd_def = ui.commandDefinitions.addButtonDefinition(CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER)

    # Define an event handler for the command created event. It will be called when the button is clicked.
    futil.add_handler(cmd_def.commandCreated, command_created)

    # ******** Add a button into the UI so the user can run the command. ********
    # Get the target workspace the button will be created in.
    workspace = ui.workspaces.itemById(WORKSPACE_ID)

    # Get the panel the button will be created in.
    panel = workspace.toolbarPanels.itemById(PANEL_ID)

    # Create the button command control in the UI after the specified existing command.
    control = panel.controls.addCommand(cmd_def, COMMAND_BESIDE_ID, False)

    # Specify if the command is promoted to the main toolbar. 
    control.isPromoted = IS_PROMOTED


# Executed when add-in is stopped.
def stop():
    # Get the various UI elements for this command
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    command_control = panel.controls.itemById(CMD_ID)
    command_definition = ui.commandDefinitions.itemById(CMD_ID)

    # Delete the button command control
    if command_control:
        command_control.deleteMe()

    # Delete the command definition
    if command_definition:
        command_definition.deleteMe()


# Function that is called when a user clicks the corresponding button in the UI.
# This defines the contents of the command dialog and connects to the command related events.
def command_created(args: adsk.core.CommandCreatedEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Command Created Event')

    # https://help.autodesk.com/view/fusion360/ENU/?contextId=CommandInputs
    inputs = args.command.commandInputs

    # TODO Define the dialog for your command by adding different inputs to the command.

    # Create a simple text box input.
    # inputs.addTextBoxCommandInput('text_box', 'Some Text', 'Enter some text.', 1, False)

    # Create a value input field and set the default using 1 unit of the default length unit.
    # defaultLengthUnits = app.activeProduct.unitsManager.defaultLengthUnits
    # default_value = adsk.core.ValueInput.createByString('1')
    # inputs.addValueInput('value_input', 'Some Value', defaultLengthUnits, default_value)

    # create input to dislay current value
    # inputs.addTextBoxCommandInput('prev_length', 'Previous Length', lengthParam.expression, 1, True)

    # Crate a float Slider
    sliderLength = inputs.addFloatSliderCommandInput('sliderLength', 'Length', 'mm',  1, 20, False)
    sliderLength.valueOne = lengthParam.value
    
    sliderWidth = inputs.addFloatSliderCommandInput('sliderWidth', 'Width', 'mm',  1, 20, False)
    sliderWidth.valueOne = widthParam.value
    
    sliderHeight = inputs.addFloatSliderCommandInput('sliderHeight', 'Height', 'mm',  1, 20, False)
    sliderHeight.valueOne = heightParam.value
    
    sliderThickness = inputs.addFloatSliderCommandInput('sliderThickness', 'Thickness', 'mm',  0.1, 1, False)
    sliderThickness.valueOne = thicknessParam.value
    
    sliderTargetTabWidth = inputs.addFloatSliderCommandInput('sliderTargetTabWidth', 'Target tab width', 'mm',  0.1, 10, False)
    sliderTargetTabWidth.valueOne = targetTabWidthParam.value
    

    # TODO Connect to the events that are needed by this command.
    futil.add_handler(args.command.execute, command_execute, local_handlers=local_handlers)
    futil.add_handler(args.command.inputChanged, command_input_changed, local_handlers=local_handlers)
    futil.add_handler(args.command.executePreview, command_preview, local_handlers=local_handlers)
    futil.add_handler(args.command.validateInputs, command_validate_input, local_handlers=local_handlers)
    futil.add_handler(args.command.destroy, command_destroy, local_handlers=local_handlers)


# This event handler is called when the user clicks the OK button in the command dialog or 
# is immediately called after the created event not command inputs were created for the dialog.
def command_execute(args: adsk.core.CommandEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Command Execute Event')

    # TODO ******************************** Your code here ********************************

    # Get a reference to your command's inputs.
    inputs = args.command.commandInputs

    # Update the user parameter with the new value
    userParams.itemByName('xSize').expression = inputs.itemById('sliderLength').expressionOne
    userParams.itemByName('ySize').expression = inputs.itemById('sliderWidth').expressionOne
    userParams.itemByName('zSize').expression = inputs.itemById('sliderHeight').expressionOne
    userParams.itemByName('thickness').expression = inputs.itemById('sliderThickness').expressionOne
    userParams.itemByName('targetTabWidth').expression = inputs.itemById('sliderTargetTabWidth').expressionOne


# This event handler is called when the command needs to compute a new preview in the graphics window.
def command_preview(args: adsk.core.CommandEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Command Preview Event')
    inputs = args.command.commandInputs

    userParams.itemByName('xSize').expression = inputs.itemById('sliderLength').expressionOne
    userParams.itemByName('ySize').expression = inputs.itemById('sliderWidth').expressionOne
    userParams.itemByName('zSize').expression = inputs.itemById('sliderHeight').expressionOne
    userParams.itemByName('thickness').expression = inputs.itemById('sliderThickness').expressionOne
    userParams.itemByName('targetTabWidth').expression = inputs.itemById('sliderTargetTabWidth').expressionOne
    


# This event handler is called when the user changes anything in the command dialog
# allowing you to modify values of other inputs based on that change.
def command_input_changed(args: adsk.core.InputChangedEventArgs):
    changed_input = args.input
    inputs = args.inputs

    # General logging for debug.
    futil.log(f'{CMD_NAME} Input Changed Event fired from a change to {changed_input.id}')


# This event handler is called when the user interacts with any of the inputs in the dialog
# which allows you to verify that all of the inputs are valid and enables the OK button.
def command_validate_input(args: adsk.core.ValidateInputsEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Validate Input Event')

    inputs = args.inputs
    
    # Verify the validity of the input values. This controls if the OK button is enabled or not.
    valueInput = inputs.itemById('value_input')
    if valueInput.value >= 0:
        args.areInputsValid = True
    else:
        args.areInputsValid = False
        

# This event handler is called when the command terminates.
def command_destroy(args: adsk.core.CommandEventArgs):
    # General logging for debug.
    futil.log(f'{CMD_NAME} Command Destroy Event')

    global local_handlers
    local_handlers = []
