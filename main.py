
import subprocess
import sys
import os

# --- Dependency Installation ---
def install_dependencies():
    """Checks and installs dependencies from requirements.txt."""
    try:
        print("Checking for required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies are up to date.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        print("Please try to install the dependencies manually by running:")
        print(f"{sys.executable} -m pip install -r requirements.txt")
        sys.exit(1)
    except FileNotFoundError:
        print("pip is not installed or not in the system's PATH. Please install pip.")
        sys.exit(1)

# --- CLI Mode ---
def run_cli():
    """Runs the command-line interface for password generation."""
    # Late import to avoid loading heavy GUI libs for CLI mode
    import password_logic

    print("\n--- Random Password Generator (CLI Mode) ---")
    
    # Get password length
    while True:
        try:
            length = int(input("Enter desired password length (e.g., 16): "))
            if length > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Get character types
    use_upper = input("Include uppercase letters? (y/n): ").lower() == 'y'
    use_lower = input("Include lowercase letters? (y/n): ").lower() == 'y'
    use_numbers = input("Include numbers? (y/n): ").lower() == 'y'
    use_symbols = input("Include symbols? (y/n): ").lower() == 'y'

    # Generate password
    password, error = password_logic.generate_password(
        length=length,
        use_upper=use_upper,
        use_lower=use_lower,
        use_numbers=use_numbers,
        use_symbols=use_symbols,
        exclude_similar=False # Not an option in simple CLI
    )

    if error:
        print(f"\nError: {error}")
    else:
        print(f"\nGenerated Password: {password}")

# --- Main Execution ---
if __name__ == "__main__":
    # Set working directory to the script's location to ensure assets are found
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    install_dependencies()

    while True:
        print("\nChoose your mode:")
        print("1. Beginner Mode (CLI)")
        print("2. Advanced Mode (GUI)")
        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            run_cli()
            break
        elif choice == '2':
            print("Launching GUI...")
            try:
                # Late import to ensure dependencies are installed first
                import gui_app
                gui_app.run_gui()
            except ImportError as e:
                print(f"\n--- ERROR ---")
                print(f"Failed to import GUI components: {e}")
                print("Please ensure PySide6 is installed correctly.")
                print(f"You can try running: pip install PySide6")
                print("-------------")
                sys.exit(1)
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
