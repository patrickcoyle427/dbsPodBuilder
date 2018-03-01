# dbsPodBuilder
A script to create draft pods and then export those pods to a PDF.

# How To Use
When run, dbsPodBuilder will prompt you for the path to a .tournament file created by the Konami Tournament Software 
on your computer. Just enter a prompt  The PDF will be saved in your current 
working directory and then opened for you in your default PDF viewing software.

.Tournament files are created by the Konami Tournament Software. They are XML files that contain information about
a tournament. This script pulls player first and last names, as well as the name of the event from this XML file.

# Dependencies

reportlab = 3.4.0
