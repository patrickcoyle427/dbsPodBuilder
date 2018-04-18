# dbsPodBuilder
A script to create draft pods and then export those pods to a PDF. There are two versions, dbsPodBuilder.py and dbsPodBuilderGUIVersion.py. The GUI Version is the one I suggest you use, as it is much more user friendly.

# How To Use

# Using dbsPodBuilderGUIVersion.py

WHen run, a small window will open. Clicking browse will let you search your computer for a .Tournament file you with to
use to make draft pods. After selecting a file, click create seating to build the pods for the draft. Once this is completed
successfully, a message will displayed in the window and the file will be opened.

# Using dbsPodBuilder.py
When run, dbsPodBuilder will prompt you for the path to a .tournament file created by the Konami Tournament Software 
on your computer. Just enter a prompt.  The PDF will be saved in your current 
working directory and then opened for you in your default PDF viewing software.

.Tournament files are created by the Konami Tournament Software. They are XML files that contain information about
a tournament. This script pulls player first and last names, as well as the name of the event from this XML file.

# Dependencies

reportlab = 3.4.0
PyQt5 = 5.10.1
