import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from module2_rtype import RTypeDecoder
from module3_jtype_engine import DisassemblerEngine
from module4_qa_formatting import QAManager


def hex_to_bin(value):
    return format(int(value, 16), "032b")


def make_r_type(rs, rt, rd, shamt, funct):
    value = (rs << 21) | (rt << 16) | (rd << 11) | (shamt << 6) | funct
    return format(value, "032b")


class QAManagerTests(unittest.TestCase):
    def test_reads_hex_binary_prefix_and_inline_comments(self):
        contents = "\n".join([
            "2008000a",
            "0x20090000 # addi $t1, $zero, 0",
            "00000001001010000100100000100000",
            "# full line comment",
            "",
        ])

        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as temp_file:
            temp_file.write(contents)
            temp_path = temp_file.name

        try:
            qa = QAManager()
            instructions = qa.read_input_file(temp_path)
        finally:
            os.remove(temp_path)

        self.assertEqual(len(instructions), 3)
        self.assertEqual(qa.errors, [])

    def test_rejects_wrong_width_instructions(self):
        qa = QAManager()

        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as temp_file:
            temp_file.write("100000000\n1010\n")
            temp_path = temp_file.name

        try:
            instructions = qa.read_input_file(temp_path)
        finally:
            os.remove(temp_path)

        self.assertEqual(instructions, [])
        self.assertEqual(len(qa.errors), 2)

    def test_missing_file_error_is_printable(self):
        qa = QAManager()
        instructions = qa.read_input_file("missing-file-for-test.txt")

        output = io.StringIO()
        with redirect_stdout(output):
            qa.print_errors()

        self.assertEqual(instructions, [])
        self.assertIn("File not found", output.getvalue())


class DecoderTests(unittest.TestCase):
    def test_sample_program_disassembles_with_labels(self):
        instructions = [
            hex_to_bin(value)
            for value in [
                "2008000a",
                "20090000",
                "01284820",
                "2108ffff",
                "1d00fffd",
                "0c100007",
                "08100009",
                "00091080",
                "03e00008",
                "afd10000",
            ]
        ]

        assembly = DisassemblerEngine().disassemble(instructions)

        self.assertEqual(assembly[0], "0x00400000:\taddi $t0, $zero, 10")
        self.assertIn("loop_1:\n0x00400008:\tadd $t1, $t1, $t0", assembly)
        self.assertIn("0x00400010:\tbgtz $t0, loop_1", assembly)
        self.assertIn("func_1:\n0x0040001c:\tsll $v0, $t1, 2", assembly)
        self.assertIn("loop_2:\n0x00400024:\tsw $s1, 0($fp)", assembly)

    def test_engine_label_state_resets_between_runs(self):
        engine = DisassemblerEngine()
        branch_to_self = hex_to_bin("1000ffff")
        addi = hex_to_bin("20080001")

        first = engine.disassemble([branch_to_self])
        second = engine.disassemble([addi])

        self.assertEqual(first[0], "loop_1:\n0x00400000:\tbeq $zero, $zero, loop_1")
        self.assertEqual(second[0], "0x00400000:\taddi $t0, $zero, 1")

    def test_external_jump_keeps_raw_address(self):
        jump_outside_loaded_program = hex_to_bin("08100009")

        assembly = DisassemblerEngine().disassemble([jump_outside_loaded_program])

        self.assertEqual(assembly[0], "0x00400000:\tj 0x00400024")

    def test_nor_zero_becomes_pseudo_not(self):
        binary = make_r_type(rs=9, rt=0, rd=8, shamt=0, funct=0x27)

        self.assertEqual(RTypeDecoder().decode(binary), "not $t0, $t1")


if __name__ == "__main__":
    unittest.main()
