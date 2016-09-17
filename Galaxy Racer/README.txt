			  Galaxy Racer (README.TXT)
=============================================================================
Version: 1.0, Stable Release
Contracted by Cognitive Thought Media
Created by Celestial Software | Q1 2016
Team Members: George Weng, Nathan Leba, William Jeang, Anshuman Kumar

How To Install and Play
-----------------------
To install the game, extract the zip file, containing the iExpress installer for
GalaxyRacer. Execute the installer. Specify the directory in which the contents will be
extracted to. From there, the game can be executed by clicking on the GalaxyRacer.exe file
in the folder "Galaxy Racer". 
WARNING: Any tampering and tampering with source files may result in errors. Be cautious
in opening and reading any files.

Bug Fixes | Additions
---------------------
v.1.0.0
   - implemented in-game tutorial
   - improved high score formatting
   - created constellation thumbnails for each level
   - changed button and start up aesthetics
   - enabled rotating the nebula

v.0.9.1
   - added three loggers (SystemEvents, CrashReports, SystemErrors), global loggers
   - added sounds for buttons and music
   - updated graphics for the finish line (nebula), stage select screen, and high score screen
   - added an icon
   - enlarged and moved the timer to the top right of the screen

v.0.9.0
   - incorporated high score functionality
       - three initials for name (arcade-esque feel)
       - save updated high score values
       - display high score values after completing a level
       - placed high score buttons in the stage select menu
   - added pause menu functionality

v.0.8.2
   - enabled rotating the ship
   - changed collision logic to better match the shape of the sprites

Documentation
-------------
The documentation for this game is located in the "docs" folder. Includes the user manual and data flow diagram.

Logs
----
Located in the logs folder; contains three files.
System Events - records the time and descriptions of normal events that should occur throughout the game.
System Errors - records errors that prohibit the game from working correctly but does not crash the game.
Crash Reports - records the time of events that crash the game.

Source Code
-----------
Located in the src folder. Contains all .py files 

Level Creator
------------------------------
LevelCreator for GalaxyRacer:

Move camera with [WASD] and [Left Click] to create stars
Press [E] to switch the size of the stars
Press [R] to place the ship start position
Press [T] to place the nebula position
Only the most recently placed ship/nebula will be saved
When finished press [ESC]

Saves star coordinates to GalaxyRacer/levels/newtrack?.txt

Contact Us
----------
If you happen to encounter any errors, please email us at racergalaxy2016@gmail.com - do not actually email
