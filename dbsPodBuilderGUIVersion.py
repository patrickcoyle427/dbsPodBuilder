#!/usr/bin/python3

# TO DO: Make this work with dbsPodBuilder.py


from PyQt5.QtWidgets import (QAction, QPushButton, QFileDialog,
                             QWidget, QGridLayout, QApplication,
                             QLineEdit)


import sys

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
        
        self.setLayout(layout_grid)
        # Sets the layout of the GUI

        self.move(150, 150)
        # Puts the window 150 pixels right and 150 pixels down when initially opened
        
        self.setWindowTitle('DBS Pod Builder')
        # Sets the name of the window
        
        self.show()
        # Displays the window

    def findFile(self):

        file_name = QFileDialog.getOpenFileName(self,
                                                'Select a .tournament File',
                                                '/home',
                                                'Tournament Files (*.tournament);;All Files (*)')
        # Launches the file dialog, which will let the user browse their files for
        # a .tournament file.
        # 'Select a .tournament File' is the title of the dialog box,
        # /home sets the directory the dialog starts in
        # The last option sets the filters for the window.

        self.file_path_box.setText(file_name)

    def createSeating(self):

        pass

if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = Window()

    sys.exit(app.exec_())
