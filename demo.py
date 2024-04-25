import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Genotype Frequency Calculator')
        self.setGeometry(100, 100, 800, 600)  # Adjusted for better layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        # Create input fields
        self.input_a0 = QLineEdit()
        self.input_b0 = QLineEdit()
        self.input_c0 = QLineEdit()
        self.input_gen = QLineEdit()
        layout.addWidget(QLabel("Enter initial frequency of genotype AA:"))
        layout.addWidget(self.input_a0)
        layout.addWidget(QLabel("Enter initial frequency of genotype Aa:"))
        layout.addWidget(self.input_b0)
        layout.addWidget(QLabel("Enter initial frequency of genotype aa:"))
        layout.addWidget(self.input_c0)
        layout.addWidget(QLabel("Enter Generation for which you wanted to count:"))
        layout.addWidget(self.input_gen)

        # Dropdown for genotype pair choices
        self.combos = [QComboBox() for _ in range(3)]
        options = ["1. AA,AA", "2. Aa,Aa", "3. aa,aa", "4. Aa,AA", "5. Aa,aa", "6. AA,aa"]
        for combo in self.combos:
            combo.addItems(options)
            layout.addWidget(combo)

        # Button to calculate
        self.calculate_btn = QPushButton('Calculate Frequencies')
        self.calculate_btn.clicked.connect(self.calculate_frequencies)
        layout.addWidget(self.calculate_btn)

        # Canvas for Matplotlib
        self.canvas = FigureCanvas(plt.figure(figsize=(10, 8)))
        layout.addWidget(self.canvas)

        self.central_widget.setLayout(layout)

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
        ax3.plot(range(gen+1), frequencies)  # Include generation count in x-axis
        ax3.legend(labels)
        ax3.set_title('Changes in Genotype Distribution Over Generations')
        ax3.set_xlabel('Generation')
        ax3.set_ylabel('Frequency')

        fig.tight_layout(pad=0.1)  # Adjust layout to prevent overlap, increase pad for clearer separation
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
