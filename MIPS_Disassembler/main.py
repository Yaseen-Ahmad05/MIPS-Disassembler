import sys
from module3_jtype_engine import disassemble
from module4_qa_formatting import read_input_file, write_output_file

def print_usage():
    print("Usage: python main.py <input_file> <output_file>")
    print("Example: python main.py sample1.txt output.txt")

def main():
    print("Starting MIPS Disassembler...")
    if len(sys.argv) != 3:
        print_usage()
        return 1

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    binary_instructions = read_input_file(input_file)
    
    if not binary_instructions:
        print("No valid instructions found. Exiting.")
        return 1
        
    assembly = disassemble(binary_instructions)
    
    if write_output_file(assembly, output_file):
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
