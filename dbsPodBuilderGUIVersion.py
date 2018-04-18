#!/usr/bin/python3

# TO DO: Make this work with dbsPodBuilder.py


from PyQt5.QtWidgets import (QAction, QPushButton, QFileDialog,
                             QWidget, QGridLayout, QApplication,
                             QLineEdit, QLabel)

from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

import xml.etree.ElementTree as ET

import sys, random, webbrowser, os.path

# PyQt5 - Used to build the GUI
#
# xml.etree.ElementTree - Used to read an XML file created by the Konami
#     Tournament Software. The XML file contains the names of each player
#     entered into the tournament. This script parses that XML doc to put
#     the player names into the pods.
#
# reportlab - Used for creating a PDF of the pods to be printed
#
# sys - Used with PyQt5 for exiting
#
# random - Used to shuffle the list of players for the draft pod seating.
#
# webbrowser - Used to automatically open the pdf once it's created so the user doesn't
#     have to find the file.


class Window(QWidget):

    # Parent is the QWidget class

    def __init__(self):

        super().__init__()
        # Initializes the Window object as a child of the QWidget class

        self.initUI()
        # Runs the UI

    def initUI(self):

        layout_grid = QGridLayout()
        # Creates a QGridLayout Object, which will put buttons created
        # into a grid for easier layout control
        
        layout_grid.setVerticalSpacing(2)
        # Sets the layout to have a vertical spacing of 2 pixels

        self.browse_button = QPushButton('Browse', self)
        # Creates a button that says "browse"
        
        self.browse_button.clicked.connect(self.findFile)
        # The button, when clicked, will run the findFile() method,
        # Which will open a file dialog
        
        layout_grid.addWidget(self.browse_button, 1, 0)
        # Adds browse_button to the grid layout and
        # Sets its position in the window, in this case row 1 col 0

        self.file_path_box = QLineEdit(self)
        # Creates a text line
        
        layout_grid.addWidget(self.file_path_box, 1, 1)
        # Adds this line to the grid layout at position 1, 1

        self.create_seating_button = QPushButton('Create Seating', self)
        # Adds a button that says 'Create Seating'
        
        self.create_seating_button.clicked.connect(self.createSeating)
        # Runs the createSeating() method when clicked.
        
        layout_grid.addWidget(self.create_seating_button, 2, 1)
        # Adds the 'Create Seating' button to the grid layout at position 2, 1

        self.info_text = QLabel('Click browse to search for the .tournament file you wish to create pods with.', self)

        layout_grid.addWidget(self.info_text, 4, 0, 5, 0)
        
        self.setLayout(layout_grid)
        # Sets the layout of the GUI

        self.move(300, 300)
        # Puts the window 150 pixels right and 150 pixels down when initially opened
        
        self.setWindowTitle('DBS Pod Builder')
        # Sets the name of the window
        
        self.show()
        # Displays the window

    def findFile(self):

        file_name = QFileDialog.getOpenFileName(self,
                                                'Select a .tournament File',
                                                '',
                                                'Tournament Files (*.Tournament);;All Files (*)')
        # Launches the file dialog, which will let the user browse their files for
        # a .tournament file.
        # 'Select a .tournament File' is the title of the dialog box,
        # The last option sets the filters for the window.

        self.file_path_box.setText(file_name[0])

        # Sets the file_path_box to have the name of the file. This will be used
        # by createSeating to find the correct file.

    def createSeating(self):

        def build_player_list(file_location):

            # build_player_list parses the tournament's XML file to build a list of lists
            # containing the names of each player in the tournament.

            participants = []

            tournament_file = r'{}'.format(file_location)
            
            tree = ET.parse(tournament_file)
            # Loads the XML tree to be parsed
            
            root = tree.getroot()
            # Gets the root of the tree, which in this case is <Tournament>

            for player in root.findall('.//Player'):
                # root.findall finds each instance of <Player> in the tournament file
                # . is the root of the XML tree 

                first_name = player.find('FirstName').text
                last_name = player.find('LastName').text
                # <FirstName> and <LastName> are both children of <Player>
                # player.find returns the first match for <FirstName> and <LastName>
                # in each <Player> 
                
                participants.append('{}, {}'.format(last_name, first_name))

            return participants
        
            # Participants is a list containing the names of each player in the tournament.

        def get_tournament_name(file_location):

            # get_tournament_name parses the tournament's XML file to find the name of the tournament.
            # The name is the header of the pod seating pdf

            tournament_file = r'{}'.format(file_location)

            tree = ET.parse(tournament_file)
            root = tree.getroot()
            
            tournament_name = root.find('Name').text.title()
            
            return tournament_name

            # tournament_name is a string
        
        def pod_builder(player_list):

            # Creates a list of lists (pods) that tells players where they will be sitting in
            # the tournamnet.
            
            random.shuffle(player_list)
            # Randomizes the players for the draft pod seeting.

            player_pods = []
            current_pod = []

            seat_num = 1
            # players start at seat 1 in their pods

            if len(player_list) < 4:

                self.info_text.setText('Error! Your tournament has less than 4 players!')

                # Tournaments can't be run with less than 4 players.

                return 'error'

                # if error is returned, then a pdf won't be created.

            elif len(player_list) == 6:

                # A special case. To preserve the small pod sizes, instead of having one pod of six,
                # two pods of three are made. Three is the smallest pod size that works for a draft.
                
                for player in player_list:
                
                    current_pod.append('{}. {}'.format(seat_num, player))
                    # current_pod creates a group of players.
                    
                    seat_num += 1
                    
                    if len(current_pod) == 3:
                        # When that reaches the specified number, that pod is added to the player_pods
                        # list, and then the current_pod list is cleared to be reused.
                        
                        player_pods.append(current_pod[:])
                        seat_num = 1
                        
                        current_pod.clear()

            else:

                for player in player_list:
                    
                    current_pod.append('{}. {}'.format(seat_num, player))

                    seat_num += 1
                    
                    if len(current_pod) == 4:
                        
                        player_pods.append(current_pod[:])
                        seat_num = 1
                        
                        current_pod.clear()

                current_pod_size = len(current_pod)
                # After this for statement runs, current_pod will only contain the remaining
                # players that couldn't be put into a pod of 4.
                # Current_pod_size is taken because depending on the number of remaining players,
                # different things will happen.

                if current_pod_size < 3:

                    # In the event of one or two players remaining, they are added into the first
                    # two pods here.
                    # if one remains, pod one will receive the player and will be a pod of five.
                    # if two remain, pod two will also become a pod of five.

                    for player_num in range(current_pod_size):

                        update_seating = current_pod[player_num][3:]
                        update_seating = '5. {}'.format(update_seating)
                        player_pods[player_num].append(update_seating)
                        # Changes the player's seat number to number 5 instead of what was
                        # previously assigned and then puts them into the appropriate pod.

                else:

                    player_pods.append(current_pod)
                    # If there are 3 players left, The remaining players are put into their own pod.

            return player_pods
            # player_pods is a list of lists cointaing the seating arrangement for the draft pods.

        def pdf_builder(pods_to_build, tournament_name):

            # Takes in the build pods and the tournament name to be drawn into a pdf.
            
            doc = SimpleDocTemplate("dbspods.pdf",pagesize=letter,
                                    rightMargin=72,leftMargin=72,
                                    topMargin=18,bottomMargin=18)
            # Creates the PDF file

            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
            # Gets options for writing a pdf, and sets 

            to_pdf = []
            # to_pdf is the list of everything that will be added to the file.
            # Each item is added in the order it was appended to this list.
            
            pod_num = 1
            # Pods always start at 1

            title = tournament_name
            
            to_pdf.append(Paragraph('<font size = 20>{}</font>'.format(title), styles['Title']))
            # Anything in <> won't be seen in the pdf, those are only so ReportLab knows what
            # size to make the text.

            players = pods_to_build
            # List containing lists of players (also known as pods) that comes from pod_builder()

            for group in players:
                         
                to_pdf.append(Paragraph('<font size = 20>POD {}</font>'.format(pod_num), styles['Normal']))
                to_pdf.append(Spacer(1, 15))

                for player in group:
                         
                    to_pdf.append(Paragraph('<font size = 16>{}</font>'.format(player), styles['Normal']))
                    to_pdf.append(Spacer(1, 2))

                to_pdf.append(Spacer(1, 15))

                if pod_num % 6 == 0:
                    to_pdf.append(PageBreak())
                    # Automatically creates a new page when the sixth pod is reached.
                    # Added for formatting so that a pod isn't broken up over 2 pages.

                pod_num += 1

            doc.build(to_pdf)

            # Builds and saves the pdf containing seating.

        file_location = self.file_path_box.text()

        if file_location == '':

            self.info_text.setText('Please select a file before creating seating')

            # Prevents a crash by trying to read an empty file path

        elif os.path.exists(file_location) == False:

            self.info_text.setText('File not found! Please try another file.')

            # Prevents a crash by checking to make sure the file exists.

        elif file_location.endswith('.Tournament') == False:

            self.info_text.setText('Please select a .tournament file.')

            # Prevents the program from parsing non .tournament files

        else:

            participants = build_player_list(file_location)
            tournament_name = get_tournament_name(file_location)
            player_pods = pod_builder(participants)

            if player_pods != 'error':

                # Error occurs when a pod has < 4 players.

                pdf_builder(player_pods, tournament_name)

                self.info_text.setText('Draft seating was successfully created!')
                self.file_path_box.setText('')

                if os.path.exists('dbspods.pdf'):

                    webbrowser.open('dbspods.pdf')

if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = Window()

    sys.exit(app.exec_())
