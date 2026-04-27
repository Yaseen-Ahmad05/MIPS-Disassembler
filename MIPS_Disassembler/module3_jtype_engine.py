# Module 3: J-Type & System Engine Architect (Role 3)
# Responsibilities:
# - File I/O loop to read 32-bit hex/binary codes
# - Primary 6-bit opcode dispatcher
# - Jump Decoding: j, jal
# - High-Level Reconstruction: Identify Functions, Loops, Array initializations

from module1_itype import ITypeDecoder
from module2_rtype import RTypeDecoder

class DisassemblerEngine:
    BRANCH_OPCODES = {0x01, 0x04, 0x05, 0x06, 0x07}

    def __init__(self):
        self.itype_decoder = ITypeDecoder()
        self.rtype_decoder = RTypeDecoder()
        self.base_address = 0x00400000
        self._reset_labels()

    def _reset_labels(self):
        self.labels = {} # address -> label_name
        self.label_counter = 1
        self.func_counter = 1

    def _add_label(self, target, is_function=False):
        if target in self.labels:
            return

        if is_function:
            self.labels[target] = f"func_{self.func_counter}"
            self.func_counter += 1
        else:
            self.labels[target] = f"loop_{self.label_counter}"
            self.label_counter += 1

    def _branch_target(self, binary_str, pc):
        imm = int(binary_str[16:32], 2)
        if (imm & 0x8000) != 0:
            imm = imm - 0x10000
        return pc + 4 + (imm << 2)

    def _jump_target(self, binary_str, pc):
        address = int(binary_str[6:32], 2)
        pc_upper = (pc + 4) & 0xf0000000
        return pc_upper | (address << 2)
        
    def decode_jtype(self, binary_str, pc):
        opcode = int(binary_str[0:6], 2)
        target = self._jump_target(binary_str, pc)
        
        if opcode == 0x02: # j
            return f"j 0x{target:08x}", target
        elif opcode == 0x03: # jal
            return f"jal 0x{target:08x}", target
            
        return "Unknown J-Type", None

    def analyze_pass1(self, binary_instructions):
        """First pass to find branch and jump targets for labels"""
        self._reset_labels()
        valid_addresses = {
            self.base_address + (index * 4)
            for index in range(len(binary_instructions))
        }

        pc = self.base_address
        for bin_str in binary_instructions:
            opcode = int(bin_str[0:6], 2)
            if opcode == 0x00: # R-type
                pass # jr is R-type
            elif opcode in [0x02, 0x03]: # J-Type
                target = self._jump_target(bin_str, pc)
                if target in valid_addresses:
                    self._add_label(target, is_function=(opcode == 0x03))
            else: # I-Type
                # Check for branches
                if opcode in self.BRANCH_OPCODES:
                    target = self._branch_target(bin_str, pc)
                    if target in valid_addresses:
                        self._add_label(target)
            pc += 4

    def disassemble(self, binary_instructions):
        """Second pass to generate assembly with labels"""
        binary_instructions = list(binary_instructions)
        self.analyze_pass1(binary_instructions)
        
        assembly = []
        pc = self.base_address
        for bin_str in binary_instructions:
            opcode = int(bin_str[0:6], 2)
            
            label_prefix = ""
            if pc in self.labels:
                label_prefix = f"{self.labels[pc]}:\n"
                
            if opcode == 0x00:
                asm_str = self.rtype_decoder.decode(bin_str)
            elif opcode in [0x02, 0x03]:
                asm_str, target = self.decode_jtype(bin_str, pc)
                if target in self.labels:
                    # Replace address with label
                    asm_str = f"{asm_str.split(' ')[0]} {self.labels[target]}"
            else:
                asm_str = self.itype_decoder.decode(bin_str, pc)
                # If branch, replace target with label
                if opcode in self.BRANCH_OPCODES:
                    target_addr = self._branch_target(bin_str, pc)
                    if target_addr in self.labels:
                        target_hex = f"0x{target_addr:08x}"
                        asm_str = asm_str.replace(target_hex, self.labels[target_addr])

            line = f"0x{pc:08x}:\t{asm_str}"
            if label_prefix:
                line = label_prefix + line
                
            assembly.append(line)
            pc += 4
            
        return assembly
