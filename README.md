# Random Password Generator

This is a Python application that generates strong, random passwords. It offers both a command-line interface (CLI) for quick password generation and a full graphical user interface (GUI) with more advanced options.

## Features

-   **Customizable Length:** Generate passwords of any desired length.
-   **Character Sets:** Choose to include any combination of:
    -   Uppercase letters (A-Z)
    -   Lowercase letters (a-z)
    -   Numbers (0-9)
    -   Symbols (!@#$...)
-   **Exclude Similar Characters:** Option to exclude visually similar characters (like 'i', 'l', '1', 'L', 'o', '0', 'O') to improve readability.
-   **Password Strength Checker:** The GUI includes a real-time password strength indicator.
-   **Dual Mode:** Run the generator in a simple CLI or a feature-rich GUI.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/AkhilRathod03/OIBSIP_Python_Task-3.git
    cd OIBSIP_Python_Task-3
    ```

2.  **Install dependencies:**
    The application will attempt to install the required dependencies automatically when you run it. You can also install them manually:
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

To start the application, run the `main.py` script from your terminal:

```bash
python main.py
```

You will be prompted to choose a mode:

-   Enter `1` for **Beginner Mode (CLI)**.
-   Enter `2` for **Advanced Mode (GUI)**.
