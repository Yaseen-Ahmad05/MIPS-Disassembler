import sys
from module3_jtype_engine import DisassemblerEngine
from module4_qa_formatting import QAManager

def print_usage():
    print("Usage: python main.py <input_file> <output_file>")
    print("Example: python main.py sample1.txt output.txt")

def main():
    print("Starting Modular MIPS Disassembler...")
    if len(sys.argv) != 3:
        print_usage()
        return 1

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    qa = QAManager()
    binary_instructions = qa.read_input_file(input_file)
    
    if not binary_instructions:
        qa.print_errors()
        print("No valid instructions found. Exiting.")
        return 1
        
    engine = DisassemblerEngine()
    assembly = engine.disassemble(binary_instructions)
    
    return 0 if qa.format_output(assembly, output_file) else 1

if __name__ == "__main__":
    sys.exit(main())
