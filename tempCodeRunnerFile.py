import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def get_eigenvalues(matrix):
    return np.linalg.eigvals(matrix)

def get_eigenvectors(matrix):
    return np.linalg.eig(matrix)[1]

def matrix_inverse(matrix):
    return np.linalg.inv(matrix)

def diagonal_matrix(values):
    return np.diag(values)

def matrix_multiplication(A, B):
    return np.dot(A, B)

class FlowerGenotypeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flower Genotype Frequency Simulator")
        self.geometry("600x600")

        # Entry for generation count
        tk.Label(self, text="Enter Generation for which you wanted to count:").pack(pady=(10, 0))
        self.entry_gen = tk.Entry(self)
        self.entry_gen.pack()

        # Entry for AA genotype frequency
        tk.Label(self, text="Enter initial frequency of genotype AA:").pack(pady=(10, 0))
        self.entry_aa = tk.Entry(self)
        self.entry_aa.pack()

        # Entry for Aa genotype frequency
        tk.Label(self, text="Enter initial frequency of genotype Aa:").pack(pady=(10, 0))
        self.entry_aA = tk.Entry(self)
        self.entry_aA.pack()

        # Entry for aa genotype frequency
        tk.Label(self, text="Enter initial frequency of genotype aa:").pack(pady=(10, 0))
        self.entry_aa_low = tk.Entry(self)
        self.entry_aa_low.pack()

        # Button to calculate frequencies
        tk.Button(self, text="Calculate", command=self.perform_calculation).pack(pady=(20, 10))

        # Area to plot the pie chart
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def perform_calculation(self):
        try:
            gen = int(self.entry_gen.get())
            a_0 = float(self.entry_aa.get())
            b_0 = float(self.entry_aA.get())
            c_0 = float(self.entry_aa_low.get())

            # Hardcoded genotype matrix for simplification, you can adjust this based on actual input
            a = np.array([[1, 0.5, 0], [0, 0.5, 1], [0, 0, 1]])

            eig_values = get_eigenvalues(a)
            P = get_eigenvectors(a)
            D = diagonal_matrix(eig_values)
            N = np.linalg.matrix_power(D, gen)
            P_inv = matrix_inverse(P)
            f = matrix_multiplication(N, P_inv)
            f = matrix_multiplication(P, f)

            x = np.array([[a_0], [b_0], [c_0]])
            ans = matrix_multiplication(f, x)

            # Update plot
            self.ax.clear()
            labels = ['AA', 'Aa', 'aa']
            sizes = [ans[0, 0], ans[1, 0], ans[2, 0]]
            self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
            self.ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = FlowerGenotypeGUI()
    app.mainloop()
