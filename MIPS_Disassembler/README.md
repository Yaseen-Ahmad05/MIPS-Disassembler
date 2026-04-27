# MIPS Disassembler

This is a Python-based MIPS Disassembler designed to decode 32-bit hex or binary machine code into human-readable MIPS assembly. It is structured to simulate a 4-person team collaboration with clear module boundaries.

## Features
- **I-Type Decoding:** Parses memory, immediate, and branch instructions (e.g., `lw`, `sw`, `addi`, `andi`, `beq`, `bgtz`).
- **R-Type Decoding:** Parses arithmetic, logical, comparison, shift, multiply/divide, and jump-register instructions (e.g., `add`, `sub`, `and`, `sll`, `slt`, `jr`).
- **J-Type Engine:** Coordinates disassembly, handles jumps (`j`, `jal`), and dynamically resolves branch/jump targets to labels (e.g., `loop_1`, `func_1`).
- **QA & Formatting:** Validates exact 32-bit instructions, reports malformed input, supports inline comments, and writes formatted output.
- **Bonus Instructions:** Supports `sra` (Shift Right Arithmetic) and `xori` (Exclusive OR Immediate).
- **Automated Tests:** Includes a standard-library `unittest` suite covering parsing, labels, sample output behavior, and edge cases.

## Prerequisites
- Python 3.6 or higher.
- No external packages are required.

## How to Run

1. Navigate to the project directory:
   ```bash
   cd MIPS_Disassembler
   ```
2. Run the main script via CLI, providing the input file and desired output file:
   ```bash
   python main.py sample1.txt output.txt
   ```

## Input File Format
The input file can contain either 8-digit hex strings (with or without `0x` prefix) or 32-bit binary strings, one instruction per line. Lines starting with `#` are ignored as comments, and inline comments after `#` are also supported.

## Output
The disassembler calculates the addresses starting at `0x00400000` (standard MIPS text segment) and outputs a clean text file mapping the addresses to the reconstructed assembly instructions, including label generation.

## Testing

Run the automated tests from the project directory:

```bash
python -m unittest discover -s tests -v
```

The tests verify:
- strict input validation for hex and binary instructions
- readable QA error reporting
- sample program disassembly and label reconstruction
- label state reset across repeated engine runs
- strict real-instruction output for `nor` instead of pseudo-instruction `not`
- raw address output for jumps outside the loaded program

## Supported Instruction Coverage

| Type | Instructions |
| --- | --- |
| R-Type | `add`, `addu`, `sub`, `subu`, `mult`, `div`, `divu`, `mfhi`, `mflo`, `and`, `or`, `xor`, `nor`, `slt`, `sltu`, `sll`, `srl`, `sra`, `sllv`, `srlv`, `srav`, `jr` |
| I-Type | `addi`, `addiu`, `andi`, `ori`, `xori`, `slti`, `sltiu`, `lb`, `lbu`, `lh`, `lhu`, `lw`, `sw`, `lui`, `sh`, `sb`, `beq`, `bne`, `blez`, `bgtz`, `bltz`, `bgez` |
| J-Type | `j`, `jal` |
