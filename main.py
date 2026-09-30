import pandas as pd
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from datetime import datetime
import threading
import yagmail
from dotenv import load_dotenv

load_dotenv()

script_dir = Path(__file__).parent


def run_comparison(old_file, new_file):
    KEY = 'name'
    df_old = pd.read_csv(old_file, usecols=['name', 'barcode', 'price'])
    df_new = pd.read_csv(new_file, usecols=['name', 'barcode', 'price'])

    required = {'name', 'barcode', 'price'}
    if not required.issubset(df_old.columns):
        raise ValueError(f"Original missing columns: {required - set(df_old.columns)}")
    if not required.issubset(df_new.columns):
        raise ValueError(f"New file missing columns: {required - set(df_new.columns)}")

    merged = df_old.merge(df_new, on=KEY, how='outer', indicator=True, suffixes=('_old', '_new'))

    new_items = merged[merged['_merge'] == 'right_only']
    both = merged[merged['_merge'] == 'both']
    price_changed = both[both['price_old'] != both['price_new']]

    report_new = new_items[[KEY, 'barcode_new', 'price_new']].rename(
        columns={'barcode_new': 'barcode', 'price_new': 'price'})
    report_changed = price_changed[[KEY, 'barcode_new', 'price_new']].rename(
        columns={'barcode_new': 'barcode', 'price_new': 'price'})

    report = pd.concat([report_new, report_changed], ignore_index=True)
    report.insert(0, 'type', ['New'] * len(report_new) + ['Price Changed'] * len(price_changed))

    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    label_file = Path(old_file).parent / f'pricing_changes_{timestamp}.xlsx'
    report.to_excel(label_file, index=False)

    # Backup before overwrite
    backup_file = Path(old_file).parent / f'backup_{timestamp}.csv'
    shutil.copy2(old_file, backup_file)

    df_new.to_csv(old_file, index=False)

    GMAIL = os.environ["GMAIL"]
    APP_PASSWORD = os.environ["APP_PASSWORD"]
    RECIPIENT = os.environ["RECIPIENT"]
    yag = yagmail.SMTP(GMAIL, APP_PASSWORD)
    yag.send(
        to=RECIPIENT,
        subject=f'Price Changes - {timestamp}',
        contents=[f'{len(report_new)} new, {len(price_changed)} price changes.', str(label_file)]
    )

    return len(report_new), len(price_changed), str(label_file)


def on_run():
    old_file = old_var.get().strip()
    new_file = new_var.get().strip()

    if not old_file or not new_file:
        messagebox.showerror("Error", "Select both CSV files.")
        return

    if not messagebox.askyesno("Confirm", "Overwrite original with new data?"):
        return

    status_var.set("Running...")
    btn.config(state="disabled")

    def worker():
        try:
            n_new, n_changed, report_path = run_comparison(old_file, new_file)
            root.after(0, lambda: status_var.set(
                f"Done! {n_new} new, {n_changed} price changes.\nReport: {report_path}\nEmail sent."))
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("Error", str(e)))
        finally:
            root.after(0, lambda: btn.config(state="normal"))

    threading.Thread(target=worker, daemon=True).start()


# --- GUI ---
root = tk.Tk()
root.title("Price Book Updater")
root.geometry("520x260")
root.resizable(False, False)

tk.Label(root, text="Original Price Book:").pack(anchor="w", padx=15, pady=(15, 0))
old_var = tk.StringVar(value=str(script_dir / "original_price_book.csv"))
row1 = tk.Frame(root)
tk.Entry(row1, textvariable=old_var, width=45).pack(side="left", padx=(0, 5))
tk.Button(row1, text="Browse...", command=lambda: old_var.set(
    filedialog.askopenfilename(filetypes=[("CSV", "*.csv")]))).pack(side="left")
row1.pack(padx=15, fill="x")

tk.Label(root, text="New Price Book:").pack(anchor="w", padx=15, pady=(10, 0))
new_var = tk.StringVar(value=str(script_dir / "new_price_book.csv"))
row2 = tk.Frame(root)
tk.Entry(row2, textvariable=new_var, width=45).pack(side="left", padx=(0, 5))
tk.Button(row2, text="Browse...", command=lambda: new_var.set(
    filedialog.askopenfilename(filetypes=[("CSV", "*.csv")]))).pack(side="left")
row2.pack(padx=15, fill="x")

btn = tk.Button(root, text="Run Comparison", command=on_run, bg="#4CAF50", fg="white",
                font=("Arial", 11, "bold"))
btn.pack(pady=15)

status_var = tk.StringVar(value="Ready.")
tk.Label(root, textvariable=status_var, wraplength=490, justify="left",
         font=("Arial", 9)).pack(padx=15, pady=(0, 10))

root.mainloop()   