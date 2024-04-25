import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QDialog, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QKeyEvent
from PyQt5.QtCore import Qt


class ImagePopup(QDialog):
    def __init__(self, parent=None):
        super(ImagePopup, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Flower Image')
        self.setGeometry(300, 300, 300, 300)  # Adjust size as needed
        self.setModal(True)  # Make the dialog modal

        layout = QVBoxLayout(self)

        # Load and display the image
        pixmap = QPixmap('surprise.png')
        image_label = QLabel(self)
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)
        image_label.resize(300, 300)  # Adjust size to fit the dialog
        layout.addWidget(image_label)

        # Thank you text label
        thank_you_label = QLabel("For You, Professor Ignacio <3", self)
        thank_you_label.setAlignment(Qt.AlignCenter)  # Center the text
        layout.addWidget(thank_you_label)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Genotype Frequency Calculator')
        self.setGeometry(100, 100, 1000, 600)  # Adjusted for better layout
        self.backgroundPixmap = QPixmap('background.jpg')

        # Set the pixmap as the background of a QLabel
        self.backgroundLabel = QLabel(self)
        self.backgroundLabel.setPixmap(self.backgroundPixmap)
        self.backgroundLabel.setScaledContents(True)  # Scale the image to fill the widget
        self.backgroundLabel.resize(self.size())  # Resize the label to fill the window

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create a main layout for the central widget
        main_layout = QHBoxLayout(self.central_widget)

        # Create a layout for the input widgets
        input_layout = QVBoxLayout()

        # Create input fields
        self.input_a0 = QLineEdit()
        self.input_b0 = QLineEdit()
        self.input_c0 = QLineEdit()
        self.input_gen = QLineEdit()
        input_layout.addWidget(QLabel("Enter initial frequency of genotype AA:"))
        input_layout.addWidget(self.input_a0)
        input_layout.addWidget(QLabel("Enter initial frequency of genotype Aa:"))
        input_layout.addWidget(self.input_b0)
        input_layout.addWidget(QLabel("Enter initial frequency of genotype aa:"))
        input_layout.addWidget(self.input_c0)
        input_layout.addWidget(QLabel("Enter Generation for which you wanted to count:"))
        input_layout.addWidget(self.input_gen)

        # Dropdown for genotype pair choices
        self.combos = [QComboBox() for _ in range(3)]
        options = ["1. AA,AA", "2. Aa,Aa", "3. aa,aa", "4. Aa,AA", "5. Aa,aa", "6. AA,aa"]
        for combo in self.combos:
            combo.addItems(options)
            input_layout.addWidget(combo)

        # Button to calculate
        self.calculate_btn = QPushButton('Calculate Frequencies')
        self.calculate_btn.clicked.connect(self.calculate_frequencies)
        input_layout.addWidget(self.calculate_btn)

        # Add input layout to the main layout
        main_layout.addLayout(input_layout)

        # Create a layout for the Matplotlib canvas
        plot_layout = QVBoxLayout()

        # Canvas for Matplotlib
        self.canvas = FigureCanvas(plt.figure(figsize=(8, 6)))
        plot_layout.addWidget(self.canvas)

        # Add plot layout to the main layout
        main_layout.addLayout(plot_layout)

        # Add main layout to the central widget
        self.central_widget.setLayout(main_layout)

        # Create a layout for the side panel
        side_panel_layout = QVBoxLayout()

        # Label for the side panel
        side_panel_label = QLabel("Transition Matrix and Eigenvalues/Eigenvectors")
        side_panel_label.setAlignment(Qt.AlignCenter)
        side_panel_layout.addWidget(side_panel_label)

        # Placeholder for displaying transition matrix, eigenvalues, and eigenvectors
        self.side_panel_widget = QLabel("Placeholder for Transition Matrix and Eigenvalues/Eigenvectors")
        self.side_panel_widget.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        side_panel_layout.addWidget(self.side_panel_widget)

        # Add side panel layout to the main layout
        main_layout.addLayout(side_panel_layout)

    def resizeEvent(self, event):
        # Ensure the background resizes correctly
        self.backgroundLabel.resize(self.size())
        super(MainWindow, self).resizeEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_F1:  # You can change the key as needed
            self.showImagePopup()

    def showImagePopup(self):
        # Create and show the popup dialog with the image
        popup = ImagePopup(self)
        popup.exec_()  # Show the dialog window

    def calculate_frequencies(self):
        # Read inputs
        a0 = float(self.input_a0.text())
        b0 = float(self.input_b0.text())
        c0 = float(self.input_c0.text())
        gen = int(self.input_gen.text())

        # Initial frequencies
        initial_frequencies = np.array([a0, b0, c0])

        # Setup the matrix
        a = np.zeros((3, 3))
        for i, combo in enumerate(self.combos):
            x = int(combo.currentText()[0])
            if x == 1:
                a[:, i] = [1, 0, 0]
            elif x == 2:
                a[:, i] = [0.25, 0.5, 0.25]
            elif x == 3:
                a[:, i] = [0, 0, 1]
            elif x == 4:
                a[:, i] = [0.5, 0.5, 0]
            elif x == 5:
                a[:, i] = [0, 1, 0]
            elif x == 6:
                a[:, i] = [0, 0.5, 0.5]

        # Eigenvalues and eigenvectors
        eig_values = np.linalg.eigvals(a)
        P = np.linalg.eig(a)[1]
        D = np.diag(eig_values)
        P_inv = np.linalg.inv(P)

        # Track changes in frequencies
        frequencies = [initial_frequencies]
        x = initial_frequencies[:, np.newaxis]
        for i in range(gen):
            N = np.linalg.matrix_power(D, i + 1)
            f = np.dot(P, np.dot(N, P_inv))
            x = np.dot(f, x)
            frequencies.append(x.flatten())

        # Plotting the pie charts and line graph
        fig = self.canvas.figure
        fig.clear()
        # Place the pie charts in the first row, occupying a larger portion of the figure
        ax1 = fig.add_subplot(221)  # First pie chart in the top left, but larger
        ax2 = fig.add_subplot(222)  # Second pie chart in the top right, but larger
        # Place the line graph in the second row, spanning the entire row
        ax3 = fig.add_subplot(212)  # Line graph across the bottom, less height

        labels = ['AA', 'Aa', 'aa']

        # Initial pie chart
        ax1.pie(initial_frequencies, labels=labels, autopct='%1.1f%%')
        ax1.set_title('Initial Distribution')

        # Final pie chart
        ax2.pie(frequencies[-1], labels=labels, autopct='%1.1f%%')
        ax2.set_title(f'Distribution After {gen} Generations')

        # Line graph for changes over generations
        ax3.plot(range(gen + 1), frequencies)  # Include generation count in x-axis
        ax3.legend(labels)
        ax3.set_title('Changes in Genotype Distribution Over Generations')
        ax3.set_xlabel('Generation')
        ax3.set_ylabel('Frequency')

        fig.tight_layout(pad=0.1)  # Adjust layout to prevent overlap, increase pad for clearer separation
        self.canvas.draw()

        # Display transition matrix, eigenvalues, and eigenvectors in the side panel
        side_panel_text = f"Transition Matrix:\n{a}\n\nEigenvalues:\n{eig_values}\n\nEigenvectors:\n{P}"
        self.side_panel_widget.setText(side_panel_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
