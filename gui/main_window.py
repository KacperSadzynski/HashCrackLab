import customtkinter as ctk
import csv
from tkinter import messagebox, filedialog


# Load algorithms from CSV
def load_algorithms():
    algorithms = []
    try:
        with open("resources/assets/hash_types.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            algorithms = [(row[1], row[0]) for row in reader]  # (algorithm_name, hashcatID)
    except FileNotFoundError:
        messagebox.showerror("Error", "The hash_types.csv file was not found.")
    except UnicodeDecodeError:
        messagebox.showerror("Error", "There was an encoding issue while reading hash_types.csv.")
    return algorithms


# Function to handle typing event for the combobox
def on_typing(event, combobox, original_algorithms):
    typed_text = combobox.get().lower()

    # Filter the list based on whether it starts with the typed text (case-insensitive match)
    filtered_algorithms = [algo[0] for algo in original_algorithms if algo[0].lower().startswith(typed_text)]

    # Update the combobox's values with the filtered list
    combobox.configure(values=filtered_algorithms)

    # If no matches, reset the combobox to empty
    if not filtered_algorithms:
        combobox.set('')

    # Ensure the combobox remains focused after typing
    combobox.focus_set()


# Function to create and configure the main window
def create_window():
    root = ctk.CTk()
    root.title("HashCrackLab")
    root.geometry("800x850")
    root.config(bg="#2E3B4E")

    return root


# Attack Modes
# Attack Modes
def create_attack_mode_widgets(parent_frame):
    """
    Creates the attack mode selection widgets.
    Only the "Straight" mode is enabled by default.
    Centers the checkboxes in the parent frame.
    """
    attack_mode_label = ctk.CTkLabel(parent_frame, text="Select Attack Mode:", font=("Arial", 14, "bold"))
    attack_mode_label.pack(pady=(20, 10))

    # Dictionary of attack modes with their descriptions and IDs
    attack_modes = {
        0: "Straight",
        1: "Combination",
        3: "Brute-force",
        6: "Hybrid Wordlist + Mask",
        7: "Hybrid Mask + Wordlist",
    }

    # Frame to hold the checkboxes, centered in the parent
    attack_mode_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    attack_mode_frame.pack(pady=10, fill="both", expand=True)

    # Dictionary to store checkbox variables for each mode
    attack_mode_vars = {}

    for mode_id, description in attack_modes.items():
        var = ctk.BooleanVar(value=(mode_id == 0))  # Enable only "Straight" (ID 0) by default
        checkbox = ctk.CTkCheckBox(
            attack_mode_frame,
            text=f"{mode_id} | {description}",
            variable=var,
            state="normal" if mode_id == 0 else "disabled",  # Disable all except "Straight"
            font=("Arial", 12),
        )
        checkbox.pack(anchor="center", pady=5)  # Center-align checkboxes
        attack_mode_vars[mode_id] = var

    return attack_mode_vars


def create_widgets(root, original_algorithms):
    # Central Frame to contain all widgets
    main_frame = ctk.CTkFrame(root)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # State variables to manage enabling/disabling inputs
    input_option = ctk.StringVar(value="none")  # Default: no option selected

    # Callback function to toggle inputs
    def toggle_inputs():
        if input_option.get() == "file":
            file_button.configure(state="normal")
            file_path_entry.configure(state="normal")
            hash_entry.configure(state="disabled")
        elif input_option.get() == "hash":
            file_button.configure(state="disabled")
            file_path_entry.configure(state="disabled")
            hash_entry.configure(state="normal")
        else:
            file_button.configure(state="disabled")
            file_path_entry.configure(state="disabled")
            hash_entry.configure(state="disabled")

    # Input choice (at the top)
    toggle_frame = ctk.CTkFrame(main_frame)
    toggle_frame.pack(pady=10)

    file_toggle = ctk.CTkRadioButton(
        toggle_frame,
        text="Use File",
        variable=input_option,
        value="file",
        command=toggle_inputs,
        font=("Arial", 12),
    )
    hash_toggle = ctk.CTkRadioButton(
        toggle_frame,
        text="Enter Hash",
        variable=input_option,
        value="hash",
        command=toggle_inputs,
        font=("Arial", 12),
    )

    file_toggle.pack(side="left", padx=20)
    hash_toggle.pack(side="left", padx=20)

    # File selection section
    file_frame = ctk.CTkFrame(main_frame)
    file_frame.pack(pady=10)

    file_button = ctk.CTkButton(
        file_frame,
        text="Browse File",
        command=lambda: select_file(file_path_entry),
        font=("Arial", 12),
        width=150,
        state="disabled",
    )
    file_button.pack(side="left", padx=10)

    file_path_entry = ctk.CTkEntry(
        file_frame,
        width=300,
        placeholder_text="Selected file path",
        font=("Arial", 12),
        state="disabled",
    )
    file_path_entry.pack(side="left", padx=10)

    # Manual hash input
    hash_entry = ctk.CTkEntry(
        main_frame,
        width=300,
        placeholder_text="Enter Hash",
        font=("Arial", 12),
        state="disabled",
    )
    hash_entry.pack(pady=10)

    # Wordlist input
    wordlist_label = ctk.CTkLabel(main_frame, text="Enter Wordlist Path:", font=("Arial", 12))
    wordlist_label.pack(pady=10)

    wordlist_entry = ctk.CTkEntry(
        main_frame,
        width=300,
        placeholder_text="Wordlist path",
        font=("Arial", 12),
    )
    wordlist_entry.pack(pady=10)

    # Algorithm selection
    algorithm_label = ctk.CTkLabel(main_frame, text="Select Hash Algorithm:", font=("Arial", 12))
    algorithm_label.pack(pady=10)

    algorithm_combobox = ctk.CTkComboBox(
        main_frame, values=[algo[0] for algo in original_algorithms], width=300, font=("Arial", 12)
    )
    algorithm_combobox.set("")
    algorithm_combobox.pack(pady=10)

    algorithm_combobox.bind('<KeyRelease>', lambda event: on_typing(event, algorithm_combobox, original_algorithms))

    # Cracking mode
    attack_mode_vars = create_attack_mode_widgets(main_frame)
    mode_var = attack_mode_vars[0]

    # Start cracking button
    start_button = ctk.CTkButton(
        main_frame,
        text="Start Cracking",
        command=lambda: start_cracking(hash_entry, file_path_entry, wordlist_entry, algorithm_combobox, mode_var),
        width=300,
    )
    start_button.pack(pady=20)

    return file_path_entry, wordlist_entry, algorithm_combobox, mode_var, hash_entry


# Function to handle file selection (browse)
def select_file(file_entry):
    file_path = filedialog.askopenfilename(title="Select Hash File",
                                           filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        file_entry.delete(0, "end")
        file_entry.insert(0, file_path)


# Function to handle the cracking process (placeholder for later implementation)
def start_cracking(hash_entry, file_entry, wordlist_entry, algorithm_combobox, mode_var):
    hash_input = hash_entry.get() if hash_entry.get() else file_entry.get()
    wordlist = wordlist_entry.get()
    algorithm = algorithm_combobox.get()  # Get the selected algorithm
    mode = mode_var.get()

    if not hash_input:
        messagebox.showerror("Error", "Please provide a hash or hash file.")
        return

    messagebox.showinfo("HashcrackLab Info",
                        f"Cracking with:\nHash: {hash_input}\nAlgorithm: {algorithm}\nMode: {mode}\nWordlist: {wordlist}")


# Main function to run the GUI
def run():
    root = create_window()
    original_algorithms = load_algorithms()  # Load algorithms from the CSV file
    create_widgets(root, original_algorithms)
    root.mainloop()
