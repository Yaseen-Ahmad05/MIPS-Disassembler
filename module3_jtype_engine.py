from module1_itype import decode_itype, process_pseudo_branches
from module2_rtype import decode_rtype
import re

BRANCH_OPCODES = {0x04, 0x05} # beq, bne

def branch_target(binary_str, pc):
    imm = int(binary_str[16:32], 2)
    if (imm & 0x8000) != 0:
        imm = imm - 0x10000
    return pc + 4 + (imm << 2)

def jump_target(binary_str, pc):
    address = int(binary_str[6:32], 2)
    pc_upper = (pc + 4) & 0xf0000000
    return pc_upper | (address << 2)
    
def decode_jtype(binary_str, pc):
    opcode = int(binary_str[0:6], 2)
    target = jump_target(binary_str, pc)
    
    if opcode == 0x02: # j
        return f"j 0x{target:08x}", target
    elif opcode == 0x03: # jal
        return f"jal 0x{target:08x}", target
        
    return "Unknown J-Type", None

def analyze_pass1(binary_instructions, base_address):
    labels = {}
    label_counter = 1
    func_counter = 1
    
    valid_addresses = {
        base_address + (index * 4)
        for index in range(len(binary_instructions))
    }

    pc = base_address
    for bin_str in binary_instructions:
        opcode = int(bin_str[0:6], 2)
        if opcode == 0x00: # R-type
            pass
        elif opcode in [0x02, 0x03]: # J-Type
            target = jump_target(bin_str, pc)
            if target in valid_addresses and target not in labels:
                if target < pc:
                    labels[target] = f"loop_{label_counter}"
                    label_counter += 1
                elif opcode == 0x03 and target > pc:
                    labels[target] = f"func_{func_counter}"
                    func_counter += 1
                else:
                    labels[target] = f"label_{label_counter}"
                    label_counter += 1
        else: # I-Type
            if opcode in BRANCH_OPCODES:
                target = branch_target(bin_str, pc)
                if target in valid_addresses and target not in labels:
                    if target < pc:
                        labels[target] = f"loop_{label_counter}"
                        label_counter += 1
                    else:
                        labels[target] = f"label_{label_counter}"
                        label_counter += 1
        pc += 4
        
    return labels

def process_array_accesses(assembly_lines):
    for i in range(2, len(assembly_lines)):
        def get_inst(line):
            if ":\n" in line:
                return line.split(":\n", 1)[1]
            return line
            
        inst1 = get_inst(assembly_lines[i-2])
        inst2 = get_inst(assembly_lines[i-1])
        inst3 = get_inst(assembly_lines[i])
        
        sll_match = re.match(r'^sll\s+(\$\w+),\s+(\$\w+),\s+2$', inst1)
        addu_match = re.match(r'^addu\s+(\$\w+),\s+(\$\w+),\s+(\$\w+)$', inst2)
        lw_match = re.match(r'^lw\s+(\$\w+),\s+(-?\d+)\((\$\w+)\)$', inst3)
        
        if sll_match and addu_match and lw_match:
            sll_rd, sll_rt = sll_match.groups()
            addu_rd, addu_rs, addu_rt = addu_match.groups()
            lw_rt, lw_imm, lw_rs = lw_match.groups()
            
            if sll_rd == addu_rd and addu_rd == lw_rs:
                base_reg = None
                if addu_rs == sll_rd:
                    base_reg = addu_rt
                elif addu_rt == sll_rd:
                    base_reg = addu_rs
                    
                if base_reg:
                    assembly_lines[i] += f" # Array access: base {base_reg}, index {sll_rt}"
                    
    return assembly_lines

def disassemble(binary_instructions, base_address=0x00400000):
    labels = analyze_pass1(binary_instructions, base_address)
    
    assembly = []
    pc = base_address
    for bin_str in binary_instructions:
        opcode = int(bin_str[0:6], 2)
        
        label_prefix = ""
        if pc in labels:
            label_prefix = f"{labels[pc]}:\n"
            
        if opcode == 0x00:
            asm_str = decode_rtype(bin_str)
        elif opcode in [0x02, 0x03]:
            asm_str, target = decode_jtype(bin_str, pc)
            if target in labels:
                asm_str = f"{asm_str.split(' ')[0]} {labels[target]}"
        else:
            asm_str = decode_itype(bin_str, pc)
            if opcode in BRANCH_OPCODES:
                target_addr = branch_target(bin_str, pc)
                if target_addr in labels:
                    target_hex = f"0x{target_addr:08x}"
                    asm_str = asm_str.replace(target_hex, labels[target_addr])

        line = asm_str
        if label_prefix:
            line = label_prefix + line
            
        assembly.append(line)
        pc += 4
        
    assembly = process_array_accesses(assembly)
    assembly = process_pseudo_branches(assembly)
    
    return assembly
