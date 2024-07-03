import os
import sys
from PyQt5.QtWidgets import QApplication, QCheckBox , QPushButton, QFileDialog, QComboBox, QScrollArea, QWidget, QLabel, QVBoxLayout, QStackedLayout, QLineEdit, QSpacerItem, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal

from PyQt5.QtGui import QFont, QIcon
import qpageview
from pdf2image import convert_from_path
import tempfile


class DropArea(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Document Here \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 5px solid #CCCCCC;  /* Lighter color */
                border-radius: 10px;     /* Rounded corners */
                background-color: #ddd;  /* Light background */
                font-size: 20px;  /* Bigger font size */
                font-weight: bold;  /* Make the font bold */
                font-style: italic;  /* Make the font italic */
                color: #333;  /* Darker text color */
            }
        ''')
        
        
class ImageLabel(qpageview.View):
    def __init__(self):
        super().__init__()

    def set_image(self, file_path):
        self.loadImages([file_path])
        self.setViewMode(qpageview.FitBoth)
        
class AppDemo(QWidget):
    imageDropped = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DocScan")
        self.setWindowIcon(QIcon(r"C:\Users\C.C\Downloads\icon.jfif"))
        self.resize(1300, 900)
        self.setAcceptDrops(True)

        mainLayout = QHBoxLayout() # Create a QHBoxLayout for the main layout

        # Create a QVBoxLayout for the left area
        leftLayout = QVBoxLayout()

        # Create a font
        self.font = QFont()
        self.font.setPointSize(10)  # Increase the font size
        self.font.setBold(True)  # Make the font bold


        # Create the drop-down list 
        self.documentTypeCombo = QComboBox()
        self.documentTypeCombo.addItems(["Choose Document Type", "Invoice", "Identity Document", "Other (Unrecognizable Document)"])
        self.documentTypeCombo.setFont(self.font)
        self.documentTypeCombo.setFixedSize(630, 50)

        # Connect the drop down list signal to the changeFields method
        self.documentTypeCombo.currentIndexChanged.connect(self.changeFields)

        leftLayout.addWidget(self.documentTypeCombo)

        # Create the form layout with labels and fields 
        self.formLayout = QVBoxLayout()  
        self.formLayout.setAlignment(Qt.AlignCenter)

        # Create different sets of labels and fields for each item in the dropdown list
        self.invoiceFields = self.createInvoiceFields()
        self.idFields = self.createIdFields()

        # Style the combo box
        self.documentTypeCombo.setStyleSheet("""
            QComboBox {
                border: 1px solid #cccccc; /* Default border color */
                border-radius: 4px; /* Rounded corners */
                padding: 5px 10px 5px 5px; /* Padding for text and dropdown arrow */
            }

            QComboBox::drop-down {
                border: 0px; /* This seems to replace the whole arrow of the combo box */
            }

            /* Define a new custom arrow icon for the combo box */
            QComboBox::down-arrow{
                height: 20px;
                right: 10px;
            }

            QComboBox::hover{
            border-color: #cccccc; /* Border color on hover (unchanged) */
            background-color: #e0e0e0; /* Background color on hover (light grey) */
            }

        """)



        # Add the form layout to the left layout
        leftLayout.addLayout(self.formLayout)

        # Creating a Box for the buttons
        buttonLayout = QHBoxLayout()

        # Create the choose a document button
        self.button = QPushButton("Choose Document")
        self.button.setFont(self.font)


        self.button.clicked.connect(self.clicked)  # Connect the button to the clicked method
        # leftLayout.addWidget(self.button)

        # Create the switch button for backend mode
        self.switch_button = QPushButton("Use Solution Locally", self)
        self.switch_button.setFont(self.font)
        self.switch_button.setCheckable(True) # Default to local execution
        # setting calling method by button
        self.switch_button.clicked.connect(self.changeColor)


        # Add buttons to the horizontal layout with a spacer between them
        buttonLayout.addWidget(self.button)
        buttonLayout.addSpacing(20)  # Add space between the buttons (20 pixels)
        buttonLayout.addWidget(self.switch_button)

        # Add the horizontal layout to the left layout
        leftLayout.addLayout(buttonLayout)


        # Add the left layout to the main layout
        mainLayout.addLayout(leftLayout)

        # Add a spacer to create a gap
        mainLayout.addItem(QSpacerItem(100, 50, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.scrollArea = QScrollArea()  # Create a QScrollArea
        self.scrollArea.setWidgetResizable(True)  # Allow the widget to resize
        self.scrollArea.setMinimumWidth(600)  # Set a minimum width

        self.stackedLayout = QStackedLayout()

        self.dropArea = DropArea()
        self.photoViewer = ImageLabel()

        self.stackedLayout.addWidget(self.dropArea)
        self.stackedLayout.addWidget(self.photoViewer)

        self.scrollArea.setLayout(self.stackedLayout)

        

        mainLayout.addWidget(self.scrollArea)  # Add the QScrollArea to the layout

        self.setLayout(mainLayout)

    def changeColor(self):
        # if button is checked
        if self.switch_button.isChecked():
            self.switch_button.setStyleSheet('''
                QLabel{
                    border: 5px solid #CCCCCC;  /* Lighter color */
                    border-radius: 10px;     /* Rounded corners */
                    background-color: #ddd;  /* Light background */
                    font-size: 20px;  /* Bigger font size */
                    font-weight: bold;  /* Make the font bold */
                    font-style: italic;  /* Make the font italic */
                    color: #333;  /* Darker text color */
                }
            ''')
            self.switch_button.setStyleSheet('''
                QPushButton{
                    border-radius: 100px;     /* Rounded corners */
                }
            ''')
            
            # self.switch_button.setStyleSheet('background-color: red; color: white;')
        else:
            self.switch_button.setStyleSheet('''
                QLabel{
                    border: 5px solid #CCCCCC;  /* Lighter color */
                    border-radius: 10px;     /* Rounded corners */
                    background-color: #ddd;  /* Light background */
                    font-size: 20px;  /* Bigger font size */
                    font-weight: bold;  /* Make the font bold */
                    font-style: italic;  /* Make the font italic */
                    color: #333;  /* Darker text color */
                }
            ''')
            self.switch_button.setStyleSheet('''
                QPushButton{
                    border-radius: 100px;     /* Rounded corners */
                }
            ''')

            

    def createInvoiceFields(self):
        fields = {}

        label = QLabel("Sender :", font=self.font)
        fields['sender_label'] = label
        fields['invoice_sender'] = QLineEdit()
        fields['invoice_sender'].setFont(self.font)

        label = QLabel("Number :", font=self.font)
        fields['invoice_number_label'] = label
        fields['invoice_number'] = QLineEdit()
        fields['invoice_number'].setFont(self.font)

        label = QLabel("Date :", font=self.font)
        fields['invoice_date_label'] = label
        fields['invoice_date'] = QLineEdit()
        fields['invoice_date'].setFont(self.font)

        label = QLabel("Total Amount :", font=self.font)
        fields['total_amount_label'] = label
        fields['total_amount'] = QLineEdit()
        fields['total_amount'].setFont(self.font)

        label = QLabel("Currency :", font=self.font)
        fields['currency_label'] = label
        fields['currency'] = QLineEdit()
        fields['currency'].setFont(self.font)

        return fields

    def createIdFields(self):
        fields = {}

        label = QLabel("ID Number :", font=self.font)
        fields['id_number_label'] = label
        fields['id_number'] = QLineEdit()
        fields['id_number'].setFont(self.font)

        label = QLabel("Full Name :", font=self.font)
        fields['full_name_label'] = label
        fields['full_name'] = QLineEdit()
        fields['full_name'].setFont(self.font)

        label = QLabel("Nationality :", font=self.font)
        fields['nationality_label'] = label
        fields['nationality'] = QLineEdit()
        fields['nationality'].setFont(self.font)

        label = QLabel("Date of Birth :", font=self.font)
        fields['dob_label'] = label
        fields['date_of_birth'] = QLineEdit()
        fields['date_of_birth'].setFont(self.font)

        label = QLabel("Gender :", font=self.font)
        fields['gender_label'] = label
        fields['gender'] = QLineEdit()
        fields['gender'].setFont(self.font)

        return fields

    def changeFields(self, index):
        # Clear the form layout
        for i in reversed(range(self.formLayout.count())):
            self.formLayout.itemAt(i).widget().setParent(None)
        
        print(index, type(index))

        # Add the appropriate fields to the form layout
        if index == 0 or index == 3 or index == "Other": # Choose Document Type / Other
            placeholder = QWidget()
            placeholder.setFixedHeight(200)  # Adjust this value as needed > Keep drop list top left after intial choice
            self.formLayout.addWidget(placeholder)
            if index == "Other":
                self.documentTypeCombo.setCurrentIndex(3)

        elif index == 1 or index == "Invoice":  # Invoice
            self.documentTypeCombo.setCurrentIndex(1)

            for field in self.invoiceFields:
                self.formLayout.addWidget(self.invoiceFields[field])

        elif index == 2 or index == "Identity Document":  # ID
            self.documentTypeCombo.setCurrentIndex(2)
            for field in self.idFields:
                self.formLayout.addWidget(self.idFields[field])



    # Update the fields with the data extracted
    def update_fields(self, data):
        print(data)
        if data:  # Check if data is valid

            # Get the current document type
            doc_type = self.documentTypeCombo.currentText().lower()
            print(doc_type)
            
            if doc_type == "identity document":
                doc_type = "id"

            # Get the fields for the current document type
            fields = getattr(self, f'{doc_type}Fields')
            print(fields)
            # Update the fields
            for field_name, field_value in data.items():
                print(field_name, field_value, fields[field_name])
                
                if field_name in fields:
                    fields[field_name].setText(str(field_value))
                    print(field_name, field_value, fields[field_name])
        else:
            # Clear the fields or display an error message if necessary
            print("Invalid data / Another doc is being processed. Please wait...")

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(file_path) # Call set_image to display the image
            event.accept()
            print(file_path)
            self.imageDropped.emit(file_path)
            # a = self.imageDropped.emit(file_path)
            # print(a)
        else:
            event.ignore()

    # Open a file dialog when the button is clicked and display the document
    def clicked(self):
            file = QFileDialog.getOpenFileName(self, 'File Dialog', '', 'All Files (*);; Python Files (*.py);; PDF Files (*.pdf);; Image Files (*.jpg *.png *.jpeg *.tif *.jfif)')
            # Alternatively, you can use this file_path , _ = QFileDialog.getOpenFileName() etc.. 
            # cuz getOpenFileName returns a tuple where the 1st element is the file path
            file_path = file[0]
            
            if file:
                self.set_image(file_path)
                print(file_path)
                self.imageDropped.emit(file_path)

    def set_image(self, file_path):
        # Convert PDF to image if the file is a PDF
        if file_path.lower().endswith('.pdf'):
            images = convert_from_path(file_path)
            temp_dir = tempfile.mkdtemp()
            file_path = os.path.join(temp_dir, 'output.jpg')
            # Save the first page of the PDF as an image
            images[0].save(file_path, 'JPEG')


        # Set the image in the photoViewer
        self.photoViewer.set_image(file_path)
        self.stackedLayout.setCurrentWidget(self.photoViewer)

if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create the QApplication object

    demo = AppDemo()  # Create an instance of your AppDemo class
    demo.show()       # Display the main window

    sys.exit(app.exec_())  # Start the event loop