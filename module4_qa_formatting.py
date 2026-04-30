def normalize_instruction(raw_line):
    line = raw_line.split("#", 1)[0].strip()
    if not line:
        return None

    if all(c in "01" for c in line) and len(line) == 32:
        return line

    return None
    
def read_input_file(filepath):
    instructions = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                bin_str = normalize_instruction(line)
                if bin_str:
                    instructions.append(bin_str)
                elif line.strip() and not line.strip().startswith("#"):
                    print(f"Line {line_num}: Invalid instruction format -> {line.strip()}")
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        
    return instructions

def write_output_file(assembly_lines, output_filepath):
    try:
        with open(output_filepath, 'w', encoding='utf-8') as f:
            for line in assembly_lines:
                f.write(line + "\n")
        print(f"[Success] Assembly saved to {output_filepath}")
        return True
    except Exception as e:
        print(f"Failed to write output to {output_filepath}: {str(e)}")
        return False
