import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QDialog, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QKeyEvent
from PyQt5.QtCore import Qt
from mpl_toolkits.mplot3d import Axes3D


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
        self.setGeometry(100, 100, 1200, 600)  # Adjusted size to better fit new layout
        self.backgroundPixmap = QPixmap('background.jpg')

        # Set the pixmap as the background of a QLabel
        self.backgroundLabel = QLabel(self)
        self.backgroundLabel.setPixmap(self.backgroundPixmap)
        self.backgroundLabel.setScaledContents(True)  # Scale the image to fill the widget
        self.backgroundLabel.resize(self.size())  # Resize the label to fill the window



        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);")  # Semi-transparent white background for the widget

        main_layout = QHBoxLayout(self.central_widget)  # Main layout now horizontal

        # Create form layout for input controls
        form_layout = QVBoxLayout()

        # Input fields and labels
        form_layout.addWidget(QLabel("Enter initial frequency of genotype AA:"))
        self.input_a0 = QLineEdit('0.5')
        form_layout.addWidget(self.input_a0)

        form_layout.addWidget(QLabel("Enter initial frequency of genotype Aa:"))
        self.input_b0 = QLineEdit('0.3')
        form_layout.addWidget(self.input_b0)

        form_layout.addWidget(QLabel("Enter initial frequency of genotype aa:"))
        self.input_c0 = QLineEdit('0.2')
        form_layout.addWidget(self.input_c0)

        form_layout.addWidget(QLabel("Enter Generation for which you wanted to count:"))
        self.input_gen = QLineEdit('10')
        form_layout.addWidget(self.input_gen)


        # Dropdown for genotype pair choices
        self.combos = [QComboBox() for _ in range(3)]
        options = ["1. AA,AA", "2. Aa,Aa", "3. aa,aa", "4. Aa,AA", "5. Aa,aa", "6. AA,aa"]
        for combo in self.combos:
            combo.addItems(options)
            form_layout.addWidget(combo)

        # Button to calculate
        self.calculate_btn = QPushButton('Calculate Frequencies')
        self.calculate_btn.clicked.connect(self.calculate_frequencies)
        form_layout.addWidget(self.calculate_btn)

        # Add form layout to the main layout
        main_layout.addLayout(form_layout)

        # Create graph layout for matplotlib canvas
        graph_layout = QVBoxLayout()
        self.canvas = FigureCanvas(plt.figure(figsize=(10, 8)))
        graph_layout.addWidget(self.canvas)

        # Add graph layout to the main layout
        main_layout.addLayout(graph_layout)

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
        eig_values, P = np.linalg.eig(a)
        P_inv = np.linalg.inv(P)

        # Track changes in frequencies
        frequencies = [initial_frequencies]
        x = initial_frequencies[:, np.newaxis]
        for i in range(gen):
            x = np.dot(a, x)
            frequencies.append(x.flatten())

        # Plotting the pie charts, line graph, and vector plots
        fig = self.canvas.figure
        fig.clear()
        ax1 = fig.add_subplot(331)  # First pie chart in the top left
        ax2 = fig.add_subplot(332)  # Second pie chart in the top center
        ax3 = fig.add_subplot(333)  # Line graph
        ax4 = fig.add_subplot(334)  # Transition matrix
        ax5 = fig.add_subplot(335)  # Eigenvalues
        ax6 = fig.add_subplot(336,projection = '3d')  # Eigenvectors (vector plot)

        labels = ['AA', 'Aa', 'aa']

        # Initial pie chart
        ax1.pie(initial_frequencies, labels=labels, autopct='%1.1f%%')
        ax1.set_title('Initial Distribution')

        # Final pie chart
        ax2.pie(frequencies[-1], labels=labels, autopct='%1.1f%%')
        ax2.set_title(f'Distribution After {gen} Generations')

        # Line graph for changes over generations
        ax3.plot(range(gen+1), frequencies)
        ax3.legend(labels)
        ax3.set_title('Changes Over Generations')

        # Transition matrix
        rotated_a = np.rot90(a, k=1)
        cax = ax4.imshow(rotated_a, interpolation='nearest', origin = 'lower')
    # Annotate each cell with the numeric value
        for i in range(rotated_a.shape[0]):
            for j in range(rotated_a.shape[1]):
                ax4.text(j, i, f'{rotated_a[i, j]:.2f}', ha='center', va='center', color='white')
        ax4.set_title('Transition Matrix')


        # Eigenvalues
        ax5.plot(eig_values.real, eig_values.imag, 'ro')
        for idx, eig in enumerate(eig_values):
            # dominant_index = np.argmax(np.abs(P[:, idx]))  # Find index of max magnitude in each eigenvector column
            # genotype_label = labels[dominant_index]  # Match to genotype
            # Annotate eigenvalue with index, value, and dominant genotype with smaller font size
            ax5.annotate(f'{idx+1}: {eig:.2f}',
                        (eig.real, eig.imag),
                        textcoords="offset points",
                        xytext=(5, 10),
                        ha='center',
                        fontsize=8)  # Smaller font size
        ax5.set_title('Eigenvalues')
        ax5.grid(True)

        # Eigenvector vector plot
        # Eigenvector vector plot
         # Change subplot index as needed
        origin = [0, 0, 0]  # Origin point for the vectors
    # Plot each eigenvector
        for i in range(len(P)):
            # Eigenvectors are columns in P, so we plot each column as a vector
            ax6.quiver(*origin, P[0, i].real, P[1, i].real, P[2, i].real, color='b', arrow_length_ratio=0.1)
        ax6.set_xlim([-1, 1])
        ax6.set_ylim([-1, 1])
        ax6.set_zlim([-1, 1])
        ax6.set_xlabel('aa')
        ax6.set_ylabel('Aa')
        ax6.set_zlabel('AA')
        ax6.set_title('Eigenvectors in 3D')

        fig.tight_layout(pad=0.2)  # Adjust layout to prevent overlap
        fig.subplots_adjust(top=0.75,hspace=0.5)
        self.canvas.draw()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())