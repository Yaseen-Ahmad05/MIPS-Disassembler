# Technical Documentation

## Overview
This MIPS Disassembler takes 32-bit machine code instructions, extracts the binary fields, and reconstructs the assembly syntax.

## Decoding Process

### 1. File Parsing (QA Module)
The input file is read line-by-line. Blank lines and comments are ignored, including inline comments after `#`. Valid instructions must be either:
- exactly 8 hexadecimal digits, with or without a `0x` prefix
- exactly 32 binary bits

Hexadecimal strings are parsed into integers using `int(line, 16)`, then formatted into a strictly 32-bit binary string with `format(value, "032b")`. Invalid widths and non-hex characters are collected as QA errors instead of crashing the program.

### 2. Opcode Extraction (Engine Module)
The first 6 bits `[0:6]` of the 32-bit binary string represent the **opcode**.
- `0x00`: Instruction is R-Type. Dispatched to the R-Type decoder.
- `0x02`, `0x03`: Instruction is J-Type (`j`, `jal`). Handled directly by the engine.
- Other: Instruction is I-Type. Dispatched to the I-Type decoder.

### 3. Bit-Masking and Shifting

While Python handles string slicing naturally (e.g., `rs = int(binary_str[6:11], 2)`), it simulates hardware bit-shifting.

#### R-Type Bit-Fields:
```
Opcode (6) | rs (5) | rt (5) | rd (5) | shamt (5) | funct (6)
```

#### I-Type Bit-Fields:
```
Opcode (6) | rs (5) | rt (5) | immediate (16)
```
**Immediate Sign Extension:**
The 16-bit immediate can be signed or unsigned. For signed operations (like `addi` or `lw`), we must sign-extend it to 32 bits.
Algorithm: Check if the 16th bit (0x8000) is set. If so, subtract `0x10000` (65536) to compute the correct negative integer representation in Python.

#### J-Type Address Calculation:
The 26-bit pseudo-absolute address must be converted to a full 32-bit absolute address:
1. Extract the `address` field (bits 6:32).
2. Shift left by 2 (`address << 2`).
3. Take the upper 4 bits of the current `PC + 4` (`(pc + 4) & 0xf0000000`).
4. Bitwise OR the two values to get the target absolute address.

### 4. Branch Target Calculation (I-Type)
Branches use PC-relative addressing.
1. The 16-bit immediate is sign-extended.
2. It is shifted left by 2 (`imm_signed << 2`).
3. Added to `PC + 4`.

### 5. Label Reconstruction (Engine Module)
The engine executes a two-pass algorithm:
1. **Pass 1:** It iterates through all instructions to identify branch targets (using PC-relative calculation) and jump targets (using pseudo-absolute calculation). It logs in-program targets into a dictionary and assigns them `loop_X` or `func_X` labels.
2. **Pass 2:** It generates the assembly strings. When it encounters a branch/jump, it replaces the raw hex address with the corresponding string label from the dictionary. It also prepends the label to the line matching the target address.

External targets are left as raw addresses so the output does not reference labels that are never defined.

### 6. Error Handling and Repeatability
The QA module records malformed input lines and missing files, then prints a readable warning block. The disassembler engine resets label state before each run, so one engine object can safely disassemble multiple instruction lists without leaking old labels into new output.

### 7. Automated Test Strategy
The `tests/test_disassembler.py` suite uses Python's built-in `unittest` module. It covers:
- accepted input forms: hex, `0x` hex, binary, blank lines, full-line comments, and inline comments
- rejected malformed instruction widths
- missing-file error reporting
- exact sample program output behavior
- label-state reset between repeated disassemblies
- external jump target handling
- strict `nor` output rather than pseudo-instruction substitution
