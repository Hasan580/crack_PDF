#!/usr/bin/env python3
"""
PDF Password Cracker GUI

A simple graphical interface for the PDF password cracking tool.
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from pdf_password_cracker import PDFPasswordCracker

class PDFPasswordCrackerGUI:
    """GUI wrapper for the PDF Password Cracker tool."""
    
    def __init__(self, root):
        """
        Initialize the GUI.
        
        Args:
            root: The tkinter root window
        """
        self.root = root
        self.root.title("PDF Password Cracker")
        self.root.geometry("600x520")  # Slightly taller to accommodate new button
        self.root.resizable(True, True)
        
        # Set up the main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="PDF File", padding="10")
        file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.pdf_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.pdf_path_var, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="Browse", command=self.browse_pdf).pack(side=tk.RIGHT, padx=5)
        
        # Output file
        output_frame = ttk.LabelFrame(main_frame, text="Output File (Optional)", padding="10")
        output_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.output_path_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_path_var, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Browse", command=self.browse_output).pack(side=tk.RIGHT, padx=5)
        
        # Quick Crack Button - NEW FEATURE
        crack_button_frame = ttk.Frame(main_frame)
        crack_button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        self.crack_button = ttk.Button(
            crack_button_frame, 
            text="CRACK PDF", 
            command=self.quick_crack,
            style="Accent.TButton"
        )
        self.crack_button.pack(fill=tk.X, ipady=10)
        
        # Create a style for the button
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 12, "bold"))
        
        # Attack type selection
        attack_frame = ttk.LabelFrame(main_frame, text="Attack Method", padding="10")
        attack_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.attack_type = tk.StringVar(value="dictionary")
        ttk.Radiobutton(attack_frame, text="Dictionary Attack", variable=self.attack_type, 
                        value="dictionary", command=self.toggle_attack_options).pack(anchor=tk.W, padx=5, pady=2)
        ttk.Radiobutton(attack_frame, text="Brute Force Attack", variable=self.attack_type, 
                        value="brute_force", command=self.toggle_attack_options).pack(anchor=tk.W, padx=5, pady=2)
        
        # Dictionary attack options
        self.dict_frame = ttk.LabelFrame(main_frame, text="Dictionary Attack Options", padding="10")
        self.dict_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.wordlist_path_var = tk.StringVar()
        ttk.Entry(self.dict_frame, textvariable=self.wordlist_path_var, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(self.dict_frame, text="Browse", command=self.browse_wordlist).pack(side=tk.RIGHT, padx=5)
        
        # Brute force attack options
        self.bf_frame = ttk.LabelFrame(main_frame, text="Brute Force Attack Options", padding="10")
        # Initially hidden
        
        charset_frame = ttk.Frame(self.bf_frame)
        charset_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(charset_frame, text="Character Set:").pack(side=tk.LEFT, padx=5)
        
        self.charset_var = tk.StringVar(value="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        ttk.Entry(charset_frame, textvariable=self.charset_var, width=40).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Preset buttons
        preset_frame = ttk.Frame(self.bf_frame)
        preset_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(preset_frame, text="Digits", command=lambda: self.charset_var.set("0123456789")).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_frame, text="Lower", command=lambda: self.charset_var.set("abcdefghijklmnopqrstuvwxyz")).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_frame, text="Upper", command=lambda: self.charset_var.set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_frame, text="Alpha", command=lambda: self.charset_var.set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")).pack(side=tk.LEFT, padx=2)
        ttk.Button(preset_frame, text="Alphanumeric", command=lambda: self.charset_var.set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")).pack(side=tk.LEFT, padx=2)
        
        length_frame = ttk.Frame(self.bf_frame)
        length_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(length_frame, text="Min Length:").pack(side=tk.LEFT, padx=5)
        self.min_length_var = tk.IntVar(value=1)
        ttk.Spinbox(length_frame, from_=1, to=10, textvariable=self.min_length_var, width=5).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(length_frame, text="Max Length:").pack(side=tk.LEFT, padx=5)
        self.max_length_var = tk.IntVar(value=4)
        ttk.Spinbox(length_frame, from_=1, to=10, textvariable=self.max_length_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.progress_var = tk.StringVar(value="Ready")
        ttk.Label(progress_frame, textvariable=self.progress_var).pack(anchor=tk.W, padx=5, pady=2)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode="indeterminate")
        self.progress_bar.pack(fill=tk.X, padx=5, pady=5)
        
        # Results text area
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.results_text = tk.Text(results_frame, wrap=tk.WORD, height=10)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(self.results_text, command=self.results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.config(yscrollcommand=scrollbar.set)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        ttk.Button(button_frame, text="Start Attack", command=self.start_attack).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=root.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Initial state
        self.toggle_attack_options()
        
        # Create a simple built-in dictionary for common passwords
        self._create_common_passwords_dict()
    
    def _create_common_passwords_dict(self):
        """Create a built-in dictionary of common passwords for quick cracking."""
        self.common_passwords = [
            # Empty password
            "",
            # Common PDF passwords
            "password", "1234", "admin", "12345", "123456", "adobe", 
            "qwerty", "abc123", "111111", "123abc", "admin123",
            # Single digits
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
            # Months and seasons
            "january", "february", "march", "april", "may", "june", "july",
            "august", "september", "october", "november", "december",
            "winter", "spring", "summer", "fall", "autumn",
            # Years
            "2020", "2021", "2022", "2023", "2024", "2025"
        ]
    
    def quick_crack(self):
        """Start a quick password cracking process with built-in password list."""
        # Input validation
        pdf_path = self.pdf_path_var.get().strip()
        if not pdf_path:
            messagebox.showerror("Error", "Please select a PDF file.")
            return
        
        if not os.path.exists(pdf_path):
            messagebox.showerror("Error", "PDF file does not exist.")
            return
        
        # Disable the crack button during the operation
        self.crack_button.configure(state="disabled", text="Cracking...")
        
        # Clear and initialize progress
        self.clear_results()
        self.progress_var.set("Running quick crack...")
        self.progress_bar.start()
        
        # Start quick crack in a separate thread
        threading.Thread(target=self._run_quick_crack, daemon=True).start()
    
    def _run_quick_crack(self):
        """Run the quick crack in a background thread."""
        try:
            pdf_path = self.pdf_path_var.get().strip()
            output_path = self.output_path_var.get().strip() or None
            
            self.log_message("🔐 QUICK CRACK STARTED 🔐")
            self.log_message(f"Attempting to crack PDF: {pdf_path}")
            if output_path:
                self.log_message(f"Unlocked PDF will be saved to: {output_path}")
            else:
                # Create default output path
                base, ext = os.path.splitext(pdf_path)
                output_path = f"{base}_unlocked{ext}"
                self.output_path_var.set(output_path)
                self.log_message(f"Unlocked PDF will be saved to: {output_path}")
            
            cracker = PDFPasswordCracker(pdf_path, output_path)
            
            self.log_message("Trying common passwords first...")
            success = False
            
            # Try common passwords first
            for password in self.common_passwords:
                self.log_message(f"Trying: {password or '(empty password)'}")
                if cracker.try_password(password):
                    self.log_message(f"✅ SUCCESS! Password found: {password or '(empty password)'}")
                    self.log_message(f"✅ PDF unlocked and saved to: {output_path}")
                    self.progress_var.set(f"Password found: {password or '(empty password)'}")
                    success = True
                    break
            
            # If common passwords didn't work, try brute force with digits only (very quick)
            if not success:
                self.log_message("Common passwords failed. Trying digits (0-9)...")
                charset = "0123456789"
                min_len = 1
                max_len = 4  # Keep this small for speed
                
                # Redirect stdout/stderr to capture progress output
                original_stdout = sys.stdout
                original_stderr = sys.stderr
                
                class StdoutRedirector:
                    def __init__(self, text_widget):
                        self.text_widget = text_widget
                    
                    def write(self, string):
                        self.text_widget.insert(tk.END, string)
                        self.text_widget.see(tk.END)
                        self.text_widget.update()
                    
                    def flush(self):
                        pass
                
                sys.stdout = StdoutRedirector(self.results_text)
                sys.stderr = StdoutRedirector(self.results_text)
                
                try:
                    success = cracker.brute_force_attack(charset, min_len, max_len)
                finally:
                    # Restore stdout/stderr
                    sys.stdout = original_stdout
                    sys.stderr = original_stderr
            
            if not success:
                self.log_message("❌ Quick crack failed. Try the advanced options below.")
                self.progress_var.set("Quick crack failed. Try advanced options.")
        
        except Exception as e:
            self.log_message(f"Error: {str(e)}")
            self.progress_var.set("Error occurred during quick crack.")
        
        finally:
            # Re-enable the crack button
            self.crack_button.configure(state="normal", text="CRACK PDF")
            self.progress_bar.stop()
    
    def browse_pdf(self):
        """Open file dialog to select a PDF file."""
        file_path = filedialog.askopenfilename(
            title="Select PDF File",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        if file_path:
            self.pdf_path_var.set(file_path)
            
            # Auto-generate output path
            base, ext = os.path.splitext(file_path)
            self.output_path_var.set(f"{base}_unlocked{ext}")
    
    def browse_output(self):
        """Open file dialog to select output file location."""
        file_path = filedialog.asksaveasfilename(
            title="Save Unlocked PDF As",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")],
            defaultextension=".pdf"
        )
        if file_path:
            self.output_path_var.set(file_path)
    
    def browse_wordlist(self):
        """Open file dialog to select a wordlist file."""
        file_path = filedialog.askopenfilename(
            title="Select Wordlist File",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            self.wordlist_path_var.set(file_path)
    
    def toggle_attack_options(self):
        """Show/hide attack options based on selected attack type."""
        if self.attack_type.get() == "dictionary":
            self.bf_frame.pack_forget()
            self.dict_frame.pack(fill=tk.X, padx=5, pady=5)
        else:
            self.dict_frame.pack_forget()
            self.bf_frame.pack(fill=tk.X, padx=5, pady=5)
    
    def log_message(self, message):
        """Add message to results text area."""
        self.results_text.insert(tk.END, message + "\n")
        self.results_text.see(tk.END)
    
    def clear_results(self):
        """Clear the results text area."""
        self.results_text.delete(1.0, tk.END)
    
    def start_attack(self):
        """Start the password cracking attack in a separate thread."""
        # Input validation
        pdf_path = self.pdf_path_var.get().strip()
        if not pdf_path:
            messagebox.showerror("Error", "Please select a PDF file.")
            return
        
        if not os.path.exists(pdf_path):
            messagebox.showerror("Error", "PDF file does not exist.")
            return
        
        output_path = self.output_path_var.get().strip() or None
        
        attack_type = self.attack_type.get()
        if attack_type == "dictionary":
            wordlist_path = self.wordlist_path_var.get().strip()
            if not wordlist_path:
                messagebox.showerror("Error", "Please select a wordlist file.")
                return
            
            if not os.path.exists(wordlist_path):
                messagebox.showerror("Error", "Wordlist file does not exist.")
                return
        else:  # brute force
            charset = self.charset_var.get()
            if not charset:
                messagebox.showerror("Error", "Character set cannot be empty.")
                return
            
            min_length = self.min_length_var.get()
            max_length = self.max_length_var.get()
            
            if min_length > max_length:
                messagebox.showerror("Error", "Minimum length cannot be greater than maximum length.")
                return
        
        # Disable UI during attack
        for widget in self.root.winfo_children():
            try:
                widget.configure(state="disabled")
            except:
                pass
        
        # Clear and initialize progress
        self.clear_results()
        self.progress_var.set("Running attack...")
        self.progress_bar.start()
        
        # Start attack in a separate thread
        threading.Thread(target=self._run_attack, daemon=True).start()
    
    def _run_attack(self):
        """Run the attack in a background thread."""
        try:
            pdf_path = self.pdf_path_var.get().strip()
            output_path = self.output_path_var.get().strip() or None
            
            self.log_message(f"Attempting to crack PDF: {pdf_path}")
            if output_path:
                self.log_message(f"Unlocked PDF will be saved to: {output_path}")
            
            cracker = PDFPasswordCracker(pdf_path, output_path)
            
            attack_type = self.attack_type.get()
            success = False
            
            if attack_type == "dictionary":
                wordlist_path = self.wordlist_path_var.get().strip()
                self.log_message(f"Starting dictionary attack using wordlist: {wordlist_path}")
                
                # Redirect stdout/stderr to capture progress output
                original_stdout = sys.stdout
                original_stderr = sys.stderr
                
                class StdoutRedirector:
                    def __init__(self, text_widget):
                        self.text_widget = text_widget
                    
                    def write(self, string):
                        self.text_widget.insert(tk.END, string)
                        self.text_widget.see(tk.END)
                        self.text_widget.update()
                    
                    def flush(self):
                        pass
                
                sys.stdout = StdoutRedirector(self.results_text)
                sys.stderr = StdoutRedirector(self.results_text)
                
                try:
                    success = cracker.dictionary_attack(wordlist_path)
                finally:
                    # Restore stdout/stderr
                    sys.stdout = original_stdout
                    sys.stderr = original_stderr
                
            else:  # brute force
                charset = self.charset_var.get()
                min_length = self.min_length_var.get()
                max_length = self.max_length_var.get()
                
                self.log_message(f"Starting brute force attack with character set: {charset}")
                self.log_message(f"Length range: {min_length} to {max_length}")
                
                # Redirect stdout/stderr to capture progress output
                original_stdout = sys.stdout
                original_stderr = sys.stderr
                
                class StdoutRedirector:
                    def __init__(self, text_widget):
                        self.text_widget = text_widget
                    
                    def write(self, string):
                        self.text_widget.insert(tk.END, string)
                        self.text_widget.see(tk.END)
                        self.text_widget.update()
                    
                    def flush(self):
                        pass
                
                sys.stdout = StdoutRedirector(self.results_text)
                sys.stderr = StdoutRedirector(self.results_text)
                
                try:
                    success = cracker.brute_force_attack(charset, min_length, max_length)
                finally:
                    # Restore stdout/stderr
                    sys.stdout = original_stdout
                    sys.stderr = original_stderr
            
            if success:
                self.progress_var.set("Password found! PDF unlocked successfully.")
            else:
                self.progress_var.set("Attack completed. Password not found.")
        
        except Exception as e:
            self.log_message(f"Error: {str(e)}")
            self.progress_var.set("Error occurred during attack.")
        
        finally:
            # Re-enable UI elements
            for widget in self.root.winfo_children():
                try:
                    widget.configure(state="normal")
                except:
                    pass
            
            self.progress_bar.stop()


def main():
    """Main function to start the GUI application."""
    root = tk.Tk()
    app = PDFPasswordCrackerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()