# Box parameters

An add-in for Autodesk Fusion 360 that provides custom parameters dialog optimized for the parametric box tutorial by Pierre Rossel, but can be used with any design using the same set of parameters. 

See this tutorial for an example: [Tutoriel Fusion 360 : Créer une boîte paramétrique par découpe laser avec assemblages à queue droite](https://youtu.be/77HIIhUTk6w).

## Features

<!-- image box_parameters_demo.png -->
![Box parameters Demo](commands/commandDialog/resources/box_parameters_demo.png)

- Slider bars to intuitively adjust the parameters (click, drag or scroll)
- Compatible with the parameter box tutorial of this video: <https://www.youtube.com/watch?v=77HIIhUTk6w>
- Compatible with any Fusion 360 drawing that has the same parameter names, even if they are not all used
- The plug-in can create the missing parameters in existing or new design

## Installation

1. Download the source code from the [latest release](https://github.com/prossel/Box-parameters/releases/latest) and extract the archive
2. Rename to folder to `Box-parameter`
3. To permanently install the add-in copy the source code to `C:\Users\%Username%\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\AddIns` on Windows or 
`~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/Box parameters` on Mac.

4. OR to open it from its existing location go to **UTILITIES** toolbar tab > **ADD-INS** > **Add-Ins** tab > Green **+** button and locate the folder

## Running

1. Go to **UTILITIES** toolbar tab > **ADD-INS** > **Add-Ins** tab
2. Click **Box Parameters** in the list to highlight
3. Select **Run on Startup** (Optional)
4. Click **Run**
5. Click on the icon in the plugins panel
6. A window will load
7. If any of the required parameters are missing the plug-in can add them for you.

## Using the Add-in

- Drag a slider left/right, use a mouse scroll wheel or click left/right of the slider to change the value
- Click OK to keep the changes or Cancel to revert to previous values

## Limitations

- Current version only works with specific parameter names. It can be used with any file that has at least these parameters names configured in mm, however the plug-in can create them for you when some are missing:
  - xSize
  - ySize
  - zSize
  - thickness
  - targetTabWidth
- Sliders limits are hard coded
