# Menumaker
Menumaker is just Luma Pictures' [automatic creation of menu items script](http://www.nukepedia.com/python/ui/auto-creation-of-menu-items-for-gizmos-menupy) with a few neat additions!  It creates a home for all your gizmos on startup so new gizmos can be simply dropped in the correct folder and Nuke will do the rest!  The days of hardcoding paths are over!

- Menubar icon support (credit: Piotr Borowsk on Nukepedia)
- .gizmo _and_ .nk support (because lets be honest, .gizmo files sorta stink!) (credit: [MatthewVerr](https://github.com/MatthewVerr))
- Drag and drop installation!  No more typing in your paths to a python script.

### Installation

If you do not have a custom `menu.py` or `init.py` in your root .nuke directory you can drag the `Gizmos` folder as well as `init.py` and `menu.py` into your .nuke folder located in your user home folder.

If you do have a custom `menu.py` and `init.py` in your root .nuke directory append the following line to the end of both: `nuke.pluginAddPath('Gizmos/')`

Start Nuke!

### Usage

Menumaker by default includes a folder inside the Gizmos folder called HWTools.  This is the root folder in which your gizmos will be placed, feel free to rename it and replace the icon!  Menumaker will automatically add PNG icon images to folders, Nuke files and gizmos with the same name as their corresponding file.  Folder icons must be placed inside the folder, gizmo icons must be in the same directory as the gizmo and also named the same thing.

### Contributing

PRs welcome!  I am by no means a Python wizard and I appreciate anyone who wishes to contribute!  This has been tested on Windows and while I see no reason why it shouldn't work on MacOS or Linux I haven't been able to give it a shot over there yet.  Let me know if it works for you!
