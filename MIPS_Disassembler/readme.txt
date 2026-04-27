MIPS Disassembler
=================

This is a Python-based MIPS Disassembler designed to decode 32-bit hex or binary machine code into human-readable MIPS assembly. It is structured as a simple, easy-to-understand project using standard Python functions.

Features
--------
- I-Type Decoding: Parses memory, immediate, and branch instructions.
- R-Type Decoding: Parses arithmetic, logical, comparison, and shift instructions.
- J-Type Engine: Handles jumps (j, jal) and resolves branch/jump targets to labels (e.g., loop_1, func_1) using a simple 2-pass algorithm.
- Formatting: Validates 32-bit instructions, ignores comments, and writes clean formatted output.

Supported Instructions
----------------------
The disassembler supports the following exact instruction set:
- R-Type: add, addu, and, jr, nor, or, slt, sltu, sll, srl, sub, subu
- I-Type: addi, addiu, andi, beq, bne, lbu, lhu, lui, lw, ori, slti, sltiu, sb, sh, sw
- J-Type: j, jal

Prerequisites
-------------
- Python 3.6 or higher.
- No external packages are required.

How to Run
----------
1. Navigate to the project directory:
   cd MIPS_Disassembler

2. Run the main script via CLI, providing the input file and desired output file:
   python main.py sample1.txt output.txt

Input File Format
-----------------
The input file must contain exactly 32-bit binary strings, one instruction per line. Lines starting with # are ignored as comments, and inline comments after # are also supported. Hexadecimal format is not supported.

Output
------
The disassembler calculates the addresses starting at 0x00400000 (standard MIPS text segment) and outputs a clean text file mapping the addresses to the reconstructed assembly instructions, including label generation.

Testing
-------
To make grading easy, there is a "tests" folder containing specific binary sample files for each of the grading criteria, along with their expected outputs.

You can test a file manually against the disassembler like so:
   python main.py tests/arithmetic_sample1.txt my_output.txt
