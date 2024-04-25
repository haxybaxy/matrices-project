import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from numpy.linalg import eig

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Genetic Matrix Operations Visualizer')
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.input_a0 = QLineEdit('0.5')
        self.input_b0 = QLineEdit('0.3')
        self.input_c0 = QLineEdit('0.2')
        self.input_gen = QLineEdit('10')
        layout.addWidget(QLabel("Enter initial frequencies of AA, Aa, aa:"))
        layout.addWidget(self.input_a0)
        layout.addWidget(self.input_b0)
        layout.addWidget(self.input_c0)
        layout.addWidget(QLabel("Enter number of generations:"))
        layout.addWidget(self.input_gen)

        self.combos = [QComboBox() for _ in range(3)]
        options = ["AA,AA", "Aa,Aa", "aa,aa", "Aa,AA", "Aa,aa", "AA,aa"]
        for i, combo in enumerate(self.combos):
            combo.addItems(options)
            layout.addWidget(combo)

        self.btn_calculate = QPushButton('Calculate Frequencies')
        self.btn_calculate.clicked.connect(self.calculate_frequencies)
        layout.addWidget(self.btn_calculate)

        self.canvas = FigureCanvas(plt.figure(figsize=(10, 8)))
        layout.addWidget(self.canvas)

    def calculate_frequencies(self):
        a0 = float(self.input_a0.text())
        b0 = float(self.input_b0.text())
        c0 = float(self.input_c0.text())
        gen = int(self.input_gen.text())
        initial_frequencies = np.array([a0, b0, c0])

        a = np.zeros((3, 3))
        transition_map = {0: [1, 0, 0], 1: [0.25, 0.5, 0.25], 2: [0, 0, 1], 3: [0.5, 0.5, 0], 4: [0, 1, 0], 5: [0, 0.5, 0.5]}
        for i, combo in enumerate(self.combos):
            a[:, i] = transition_map[combo.currentIndex()]

        values, vectors = eig(a)
        D = np.diag(values)
        P = vectors
        P_inv = np.linalg.inv(P)

        frequencies = [initial_frequencies]
        x = initial_frequencies[:, np.newaxis]
        for i in range(1, gen + 1):
            x = np.dot(np.linalg.matrix_power(a, i), x)
            frequencies.append(x.flatten())

        self.visualize_data(a, values, vectors, frequencies)

    def visualize_data(self, a, values, vectors, frequencies):
        fig = self.canvas.figure
        fig.clf()

        # Transition Matrix with Annotations (No Colorbar)
        ax1 = fig.add_subplot(221)
        im = ax1.matshow(a, cmap='viridis')
        for i in range(a.shape[0]):
            for j in range(a.shape[1]):
                ax1.text(j, i, f'{a[i, j]:.2f}', ha='center', va='center', color='black', fontsize=8)
        ax1.set_title('Transition Matrix A')
        ax1.set_xlabel('To State')
        ax1.set_ylabel('From State')

        ax2 = fig.add_subplot(222)
        ax2.plot(values.real, 'ro', label='Eigenvalues')
        ax2.set_title('Eigenvalues')
        ax2.legend()

        ax3 = fig.add_subplot(223)
        ax3.plot(frequencies)
        ax3.set_title('Genotype Frequencies Over Generations')
        ax3.set_xlabel('Generation')
        ax3.set_ylabel('Frequency')
        ax3.legend(['AA', 'Aa', 'aa'])

        ax4 = fig.add_subplot(224)
        ax4.quiver(np.zeros(len(vectors)), np.zeros(len(vectors)), vectors[0, :], vectors[1, :], angles='xy', scale_units='xy', scale=1)
        ax4.set_xlim(-1, 1)
        ax4.set_ylim(-1, 1)
        ax4.set_title('Eigenvectors')

        fig.tight_layout()
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
