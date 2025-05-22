
🗂️ FILESYSTEM SIMULATION

A console-based simulation of a Unix-like file system, developed as part of the Advanced Programming course at the Faculty of Mathematics and Computer Science.

🏛️ UNIVERSITY
Amir Kabir University of Technology

👨‍🏫 INSTRUCTOR
Dr. Ghorbanali

👨‍💻 CODERS
- Sariye Hosseini
- Mohammadjavad Hosseini

🗓️ TERM
Spring 1404

📘 PROJECT DESCRIPTION
This project simulates a mini Unix-style file system with essential functionalities such as creation, deletion, navigation, and editing of directories and `.txt` files.

The implementation follows Object-Oriented Programming (OOP) principles with a strong focus on:
- Clean Code
- Extensibility
- Command-line Interaction

🛠️ FEATURES

📁 DIRECTORY OPERATIONS
- mkdir <path> <folder_name> — Create a new directory.
- rm <path> — Remove a directory.
- cd <path> — Change to a specific directory.
- cd .. — Navigate to the parent directory.
- ls — List all files and folders in the current directory.

📄 FILE OPERATIONS
- touch <path> <file_name>.txt — Create a new .txt file.
- rm <path> — Delete a file.
- nwfiletxt <path> — Overwrite the contents of a file.
- appendtxt <path> — Append text to the end of a file.
- editline <path> <line> <text> — Edit a specific line in a file.
- deline <path> <line> — Delete a specific line in a file.
- cat <path> — Display the contents of a file.

📦 FILE/FOLDER MANAGEMENT
- mv <source_path> <destination_path> — Move a file or folder to a new location.
- cp <source_path> <destination_path> — Create a deep copy of a file or folder.
- rename <path> <new_name> — Rename a file or folder.

📋 EVALUATION CRITERIA

✅ VERSION CONTROL
- Use of Git with regular, meaningful commits throughout development.

✅ TEAM COLLABORATION
- Active participation from all group members (if applicable).

✅ OOP PRINCIPLES
- Use of at least 3 distinct classes.
- Clean, organized, and maintainable code structure.

✅ FUNCTIONAL COMPLETENESS
- Full and correct implementation of all required commands.

✅ PATH MANAGEMENT
- Proper handling of absolute and relative paths.
- Clear error messages for invalid paths (e.g., "Path not found").
