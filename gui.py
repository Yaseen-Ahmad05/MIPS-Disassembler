import tkinter as tk
from tkinter import filedialog, messagebox
import os

from module3_jtype_engine import disassemble
from module4_qa_formatting import read_input_file, write_output_file

class DisassemblerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MIPS Disassembler")
        self.root.geometry("500x200")
        self.root.resizable(False, False)
        
        # Configure grid to stretch the middle column
        self.root.columnconfigure(1, weight=1)
        
        # Input Frame elements
        tk.Label(root, text="Input File:").grid(row=0, column=0, padx=10, pady=20, sticky="e")
        self.input_var = tk.StringVar()
        self.input_entry = tk.Entry(root, textvariable=self.input_var)
        self.input_entry.grid(row=0, column=1, sticky="we", pady=20)
        tk.Button(root, text="Browse", command=self.browse_input).grid(row=0, column=2, padx=10, pady=20)
        
        # Output Frame elements
        tk.Label(root, text="Output File:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.output_var = tk.StringVar()
        self.output_entry = tk.Entry(root, textvariable=self.output_var)
        self.output_entry.grid(row=1, column=1, sticky="we", pady=5)
        tk.Button(root, text="Browse", command=self.browse_output).grid(row=1, column=2, padx=10, pady=5)
        
        # Process Button
        self.process_btn = tk.Button(root, text="Process", command=self.process, width=15)
        self.process_btn.grid(row=2, column=0, columnspan=3, pady=30)
        
    def browse_input(self):
        filename = filedialog.askopenfilename(
            title="Select Input Binary File",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if filename:
            self.input_var.set(filename)
            
    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            title="Select Output Location",
            defaultextension=".txt",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if filename:
            self.output_var.set(filename)
            
    def process(self):
        input_path = self.input_var.get().strip()
        output_path = self.output_var.get().strip()
        
        if not input_path:
            messagebox.showwarning("Warning", "Please select an input file.")
            return
            
        if not output_path:
            messagebox.showwarning("Warning", "Please select an output file.")
            return
            
        if not os.path.exists(input_path):
            messagebox.showerror("Error", f"Input file not found: {input_path}")
            return
            
        # Parse the input file
        binary_instructions = read_input_file(input_path)
        
        if not binary_instructions:
            messagebox.showerror("Error", "No valid instructions found in the input file.")
            return
            
        try:
            # Handle the base_address=0x00400000 default correctly
            assembly = disassemble(binary_instructions, base_address=0x00400000)
            
            # Write to the destination
            success = write_output_file(assembly, output_path)
            
            if success:
                messagebox.showinfo("Success", f"[Success] Assembly saved to {output_path}")
            else:
                messagebox.showerror("Error", "Failed to write output to the specified location.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during disassembly:\n{str(e)}")

def main():
    root = tk.Tk()
    app = DisassemblerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
