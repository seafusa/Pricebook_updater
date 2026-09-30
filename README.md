# Price Book Updater

A Windows desktop utility built to automate price book updates and simplify the process of preparing updated product pricing for Numbot label printing.

The application was created to solve a recurring business problem: manually comparing an existing price book against a new price list can be time-consuming and can result in outdated prices being used for labels.

The tool automatically identifies new products and price changes, generates an Excel file containing only the changes, backs up the existing price book, and sends the resulting Excel report by email.

The generated `.xlsx` file can then be uploaded directly into **Numbot** for label printing.

## Features

* Compare an existing price book against a new price book
* Detect newly added products
* Detect products with changed prices
* Generate an Excel file containing the changes
* Automatically back up the previous price book
* Update the existing CSV with the new price book
* Email the generated Excel file
* Simple graphical interface
* Standalone Windows executable

## How It Works

```text
Existing Price Book
        │
        ▼
   Select CSV Files
        │
        ▼
 Compare Price Books
        │
        ├── New Products
        │
        └── Price Changes
        │
        ▼
Generate Excel File
        │
        ▼
Back Up Existing Price Book
        │
        ▼
Update Price Book
        │
        ▼
Email Excel File
        │
        ▼
Upload Excel File to Numbot
        │
        ▼
Print Updated Labels
```

## Input Files

The application compares two CSV files.

Both files must contain these columns:

```text
name
barcode
price
```

### Original Price Book

The currently active price book.

### New Price Book

The newly received price book containing updated product information and prices.

## Output

The application generates an Excel file:

```text
pricing_changes_YYYY-MM-DD_HHMMSS.xlsx
```

The Excel file contains:

| Type          | name      | barcode | price |
| ------------- | --------- | ------- | ----- |
| New           | Product A | 123456  | 4.99  |
| Price Changed | Product B | 789012  | 6.49  |

This file can be uploaded directly into **Numbot** to generate labels for the affected products.

### Backup

Before replacing the existing price book, the application creates a backup:

```text
backup_YYYY-MM-DD_HHMMSS.csv
```

This provides a copy of the previous price book if it needs to be restored.

## Email

After processing the files, the application sends an email containing:

* Number of new products
* Number of price changes
* Generated Excel report

The email configuration is stored in a `.env` file.

Example:

```env
GMAIL=your_email@gmail.com
APP_PASSWORD=your_app_password
RECIPIENT=recipient@example.com
```

**Do not commit `.env` to Git.**

Add the following to `.gitignore`:

```text
.env
.venv/
__pycache__/
build/
dist/
*.spec
```

## Requirements

* Windows 10/11
* Python 3.10+
* Internet connection for email notifications
* Numbot for importing the generated Excel file and printing labels

## Python Dependencies

* `pandas` — CSV processing and comparison
* `openpyxl` — Excel file generation
* `yagmail` — email delivery
* `python-dotenv` — environment variable management
* `tkinter` — graphical user interface
* `pyinstaller` — Windows executable packaging

## Development Setup

Create a virtual environment:

```powershell
py -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
pip install pandas openpyxl yagmail python-dotenv pyinstaller
```

Verify the installation:

```powershell
python -c "import pandas, openpyxl, yagmail, dotenv, tkinter; print('All dependencies OK')"
```

## Building the Windows Executable

Build the application using PyInstaller:

```powershell
pyinstaller --onefile --windowed --name "Price Book Updater" main.py
```

The executable will be created at:

```text
dist\Price Book Updater.exe
```

## Usage

1. Open **Price Book Updater.exe**.
2. Select the current/original price book CSV.
3. Select the new price book CSV.
4. Click **Run Comparison**.
5. Confirm the update.
6. The application compares the files and identifies new products and price changes.
7. The original price book is backed up.
8. The price book is updated.
9. An Excel report is generated and emailed.
10. Upload the generated `.xlsx` file into **Numbot**.
11. Use Numbot to print the updated labels.

## Project Structure

```text
PriceBookUpdater/
│
├── price_book_updater.py
├── .env
├── original_price_book.csv
├── new_price_book.csv
├── .gitignore
├── README.md
│
└── dist/
    └── Price Book Updater.exe
```

## Purpose

This project was built as a practical business automation tool to eliminate repetitive manual price comparisons and reduce pricing errors during label updates.

Instead of manually finding every changed product, the application identifies the relevant changes and produces a ready-to-upload Excel file for Numbot.

The end result is a simple workflow:

**Compare → Backup → Update → Email → Upload to Nimbot → Print Labels**
