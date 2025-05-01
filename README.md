# PDF Password Cracker

this tool allow you to open any pdf with password by cracking the password and edit your pdf as you want 

## Features

- **Dictionary Attack**: Try passwords from a wordlist file
- **Brute Force Attack**: Try all possible combinations of characters
- **Command Line Interface**: For automation and scripting
- **Graphical User Interface**: For ease of use
- **Progress Tracking**: Shows progress during the attack
- **Colored Output**: For better readability

## Requirements

- Python 3.6+
- Required packages (install using `pip install -r requirements.txt`):
  - pikepdf: For PDF manipulation
  - tqdm: For progress bars
  - colorama: For colored terminal output

## Installation

1. Clone or download this repository
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

The tool can be used from the command line for automation and scripting:

```
python pdf_password_cracker.py [options] <pdf_file>
```

#### Options:

- `-o, --output`: Path to save the unlocked PDF (default: append '_unlocked' to original filename)
- `-d, --dictionary`: Path to wordlist file for dictionary attack
- `-b, --brute-force`: Perform brute force attack
- `--charset`: Character set for brute force (default: a-zA-Z0-9)
- `--min-length`: Minimum password length for brute force (default: 1)
- `--max-length`: Maximum password length for brute force (default: 4)

#### Examples:

Dictionary attack using a wordlist:
```
python pdf_password_cracker.py -d wordlist.txt secure.pdf
```

Brute force attack with default settings:
```
python pdf_password_cracker.py -b secure.pdf
```

Brute force attack with custom settings:
```
python pdf_password_cracker.py -b --charset "0123456789" --min-length 4 --max-length 6 secure.pdf
```

### Graphical User Interface

For easier use, the tool provides a graphical interface:

```
python pdf_password_cracker_gui.py
```

The GUI allows you to:
- Select PDF files using a file browser
- Choose the attack method (dictionary or brute force)
- Configure attack parameters
- Track progress visually
- See real-time results

## Creating a Wordlist

For dictionary attacks, you need a wordlist (a text file with one password per line). You can:

1. Create your own based on potential passwords
2. Download common password lists from security websites
3. Use specialized tools to generate wordlists

## Performance Considerations

- Brute force attacks can take a very long time for longer passwords
- The time required increases exponentially with password length
- For better performance, try dictionary attacks first
- If using brute force, start with smaller character sets and shorter lengths

## Security and Legal Notice

This tool is provided for educational and legitimate purposes only, such as:
- Recovering your own PDF passwords
- Security testing with explicit permission

Never use this tool to access PDFs you don't have permission to unlock. Unauthorized access to protected documents may violate laws in your jurisdiction.

## Limitations

- The tool can only recover "user" passwords, not "owner" passwords
- Success depends on the complexity of the password
- Very long or complex passwords may be impractical to crack

## License

This project is available for personal and educational use only.
