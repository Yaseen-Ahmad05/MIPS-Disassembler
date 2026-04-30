# MIPS Disassembler - Test Mapping Summary

To facilitate grading, the provided `tests/` directory contains sample binary input files mapped directly to specific features and criteria of the assignment. Each input file (e.g., `sample1.txt`) corresponds perfectly to an expected output text file (e.g., `sample1_output.txt`).

Here is a breakdown of what each test file evaluates:

### 1. `arithmetic_sample1.txt`
- **Features Tested:** R-type and I-type arithmetic instructions.
- **Criteria Evaluated:** Basic operand parsing, extraction of function codes, and distinction between signed vs unsigned addition/subtraction.

### 2. `arrays_sample1.txt`
- **Features Tested:** Array Access Pattern Reconstruction.
- **Criteria Evaluated:** The disassembler's ability to detect sequences like `sll` -> `addu` -> `lw` and automatically emit high-level comments noting the array's base and index registers.

### 3. `function_sample1.txt`
- **Features Tested:** Procedure Calls and Returns.
- **Criteria Evaluated:** Correctly processing forward `jal` jumps and assigning `func_X` labels, as well as properly tracking jump-register (`jr`) instructions.

### 4. `if_sample1.txt`
- **Features Tested:** Expanded Branch Logic (If-statements).
- **Criteria Evaluated:** Demonstrates the aggregation of `slt` + `bne`/`beq` instruction sequences into the human-readable pseudo-instructions `blt` (branch less than), `bgt` (branch greater than), and `ble` (branch less than or equal).

### 5. `jump_sample1.txt`
- **Features Tested:** Absolute Jumps.
- **Criteria Evaluated:** Correct bit-shifting of the 26-bit pseudo-absolute address field and correctly applying the upper 4 bits of the current PC.

### 6. `loops_sample1.txt`
- **Features Tested:** Loops and Backward Branches.
- **Criteria Evaluated:** Validates that branch targets pointing *behind* the current Program Counter are accurately flagged and mapped to `loop_X` labels. 

### 7. `memory_sample1.txt`
- **Features Tested:** Memory Operations.
- **Criteria Evaluated:** Accurately calculating memory offsets, and properly handling a suite of load/store variants including `lw`, `sw`, `lbu`, `lhu`, and `lui`.
