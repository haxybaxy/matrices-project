# Genotype Frequency Calculator

## Overview
This project is an application of linear algebra in genetics. It calculates the frequency of different genotypes over multiple generations using transition matrices and eigenanalysis. The application includes a graphical user interface (GUI) for user interaction and visualization of results.

## Installation

### Prerequisites
- Python 3.x installed on your system.
- pip package manager.

### Installation Steps
1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/yourusername/genotype-frequency-calculator.git
    ```

2. Navigate to the project directory:

    ```bash
    cd genotype-frequency-calculator
    ```

3. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    - On Windows:
    
        ```bash
        venv\Scripts\activate
        ```
    
    - On macOS/Linux:
    
        ```bash
        source venv/bin/activate
        ```

5. Install dependencies from the requirements folder:

    ```bash
    pip install -r requirements/requirements.txt
    ```

## Usage
1. Ensure your virtual environment is activated (if you created one).

2. Run the main script:

    ```bash
    python main.py
    ```

3. The GUI window will open. Input the initial frequencies of genotypes, select options from dropdowns, and click the "Calculate Frequencies" button to visualize the results.
