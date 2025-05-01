#!/usr/bin/env python3
"""
PDF Password Cracker

A tool to unlock password-protected PDF files using dictionary or brute-force attacks.
"""

import argparse
import os
import sys
import time
from itertools import product
from typing import List, Generator, Optional

import pikepdf
from tqdm import tqdm
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored terminal output
init()

class PDFPasswordCracker:
    """Class to handle PDF password cracking operations."""
    
    def __init__(self, pdf_path: str, output_path: Optional[str] = None):
        """
        Initialize the PDF password cracker.
        
        Args:
            pdf_path: Path to the password-protected PDF file
            output_path: Path to save the unlocked PDF (default: append "_unlocked" to original filename)
        """
        self.pdf_path = pdf_path
        
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
        if output_path:
            self.output_path = output_path
        else:
            # Create default output path by adding "_unlocked" before the extension
            base, ext = os.path.splitext(pdf_path)
            self.output_path = f"{base}_unlocked{ext}"
    
    def try_password(self, password: str) -> bool:
        """
        Try to open the PDF with the given password.
        
        Args:
            password: Password to try
            
        Returns:
            True if password worked, False otherwise
        """
        try:
            pdf = pikepdf.open(self.pdf_path, password=password)
            pdf.save(self.output_path)
            return True
        except pikepdf.PasswordError:
            return False
    
    def dictionary_attack(self, wordlist_path: str) -> bool:
        """
        Perform a dictionary attack using a wordlist file.
        
        Args:
            wordlist_path: Path to the wordlist file
            
        Returns:
            True if password was found, False otherwise
        """
        if not os.path.exists(wordlist_path):
            raise FileNotFoundError(f"Wordlist file not found: {wordlist_path}")
        
        print(f"{Fore.BLUE}[*] Starting dictionary attack...{Style.RESET_ALL}")
        
        # Count lines in file to setup progress bar
        with open(wordlist_path, 'r', errors='ignore') as f:
            total_passwords = sum(1 for _ in f)
        
        successful_password = None
        
        with open(wordlist_path, 'r', errors='ignore') as wordlist:
            for password in tqdm(wordlist, total=total_passwords, desc="Trying passwords", unit="pwd"):
                password = password.strip()
                if self.try_password(password):
                    successful_password = password
                    break
        
        if successful_password:
            print(f"{Fore.GREEN}[+] Password found: {successful_password}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[+] Unlocked PDF saved to: {self.output_path}{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}[-] Password not found in wordlist.{Style.RESET_ALL}")
            return False
    
    def generate_brute_force_passwords(self, charset: str, min_len: int, max_len: int) -> Generator[str, None, None]:
        """
        Generate passwords for brute force attack.
        
        Args:
            charset: Characters to use in brute force
            min_len: Minimum password length
            max_len: Maximum password length
            
        Yields:
            Generated passwords
        """
        for length in range(min_len, max_len + 1):
            for pwd in product(charset, repeat=length):
                yield ''.join(pwd)
    
    def brute_force_attack(self, charset: str, min_len: int, max_len: int) -> bool:
        """
        Perform a brute force attack.
        
        Args:
            charset: String of characters to use
            min_len: Minimum password length
            max_len: Maximum password length
            
        Returns:
            True if password was found, False otherwise
        """
        print(f"{Fore.BLUE}[*] Starting brute force attack...{Style.RESET_ALL}")
        print(f"{Fore.BLUE}[*] Character set: {charset}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}[*] Length range: {min_len} to {max_len}{Style.RESET_ALL}")
        
        # Calculate total combinations (for information purposes)
        total_combinations = sum(len(charset) ** i for i in range(min_len, max_len + 1))
        print(f"{Fore.YELLOW}[!] Total combinations: {total_combinations:,}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] This might take a long time depending on the password complexity.{Style.RESET_ALL}")
        
        start_time = time.time()
        tested_passwords = 0
        
        # Setup progress tracking
        pbar = tqdm(desc="Trying combinations", unit="pwd")
        
        for password in self.generate_brute_force_passwords(charset, min_len, max_len):
            tested_passwords += 1
            
            # Update progress every 100 passwords
            if tested_passwords % 100 == 0:
                pbar.update(100)
                
            if self.try_password(password):
                elapsed_time = time.time() - start_time
                pbar.close()
                print(f"{Fore.GREEN}[+] Password found: {password}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}[+] Tested {tested_passwords:,} passwords in {elapsed_time:.2f} seconds{Style.RESET_ALL}")
                print(f"{Fore.GREEN}[+] Unlocked PDF saved to: {self.output_path}{Style.RESET_ALL}")
                return True
                
        pbar.close()
        elapsed_time = time.time() - start_time
        print(f"{Fore.RED}[-] Password not found after trying {tested_passwords:,} combinations.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Attack took {elapsed_time:.2f} seconds.{Style.RESET_ALL}")
        return False


def main():
    """Main function to parse arguments and run the appropriate attack."""
    parser = argparse.ArgumentParser(description="PDF Password Cracker Tool")
    parser.add_argument("pdf_path", help="Path to the password-protected PDF file")
    parser.add_argument("-o", "--output", help="Path to save the unlocked PDF (default: append '_unlocked' to original)")
    
    attack_group = parser.add_mutually_exclusive_group(required=True)
    attack_group.add_argument("-d", "--dictionary", help="Path to wordlist file for dictionary attack")
    attack_group.add_argument("-b", "--brute-force", action="store_true", help="Perform brute force attack")
    
    # Brute force options
    brute_force_group = parser.add_argument_group("Brute Force Options")
    brute_force_group.add_argument("--charset", default="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                                   help="Character set for brute force (default: a-zA-Z0-9)")
    brute_force_group.add_argument("--min-length", type=int, default=1,
                                    help="Minimum password length for brute force (default: 1)")
    brute_force_group.add_argument("--max-length", type=int, default=4,
                                    help="Maximum password length for brute force (default: 4)")
    
    args = parser.parse_args()
    
    try:
        cracker = PDFPasswordCracker(args.pdf_path, args.output)
        
        if args.dictionary:
            success = cracker.dictionary_attack(args.dictionary)
        elif args.brute_force:
            success = cracker.brute_force_attack(args.charset, args.min_length, args.max_length)
            
        sys.exit(0 if success else 1)
            
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()