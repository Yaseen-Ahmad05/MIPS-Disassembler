# Module 4: QA, Testing & Formatting (Role 4)
# Responsibilities:
# - Error handling to prevent runtime crashes
# - Format final assembly output into readable text file
# - File reading utility

class QAManager:
    HEX_DIGITS = set("0123456789abcdefABCDEF")

    def __init__(self):
        self.errors = []

    def _normalize_instruction(self, raw_line):
        """Return a 32-bit binary string or raise ValueError."""
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            return None

        if all(c in "01" for c in line) and len(line) == 32:
            return line

        has_prefix = line.lower().startswith("0x")
        hex_part = line[2:] if has_prefix else line

        if len(hex_part) != 8:
            raise ValueError("instruction must be exactly 8 hex digits or 32 binary bits")

        if not all(c in self.HEX_DIGITS for c in hex_part):
            raise ValueError("instruction contains non-hex characters")

        return format(int(hex_part, 16), "032b")
        
    def read_input_file(self, filepath):
        """Reads hex or binary file safely"""
        instructions = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        bin_str = self._normalize_instruction(line)
                        if bin_str:
                            instructions.append(bin_str)
                    except ValueError:
                        clean_line = line.strip()
                        self.errors.append(f"Line {line_num}: Invalid instruction format -> {clean_line}")
        except FileNotFoundError:
            self.errors.append(f"File not found: {filepath}")
        except Exception as e:
            self.errors.append(f"Error reading file {filepath}: {str(e)}")
            
        return instructions

    def print_errors(self):
        """Print collected QA warnings/errors once."""
        if not self.errors:
            return

        print("--- QA Warnings/Errors ---")
        for err in self.errors:
            print(err)
        print("--------------------------\n")
        
    def format_output(self, assembly_lines, output_filepath):
        """Formats and writes output gracefully"""
        self.print_errors()
            
        try:
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write("# MIPS Disassembler Output\n")
                f.write("# Address     Instruction\n")
                f.write("-" * 40 + "\n")
                for line in assembly_lines:
                    f.write(line + "\n")
            print(f"[Success] Assembly saved to {output_filepath}")
            return True
        except Exception as e:
            print(f"[Fatal] Failed to write output to {output_filepath}: {str(e)}")
            return False
