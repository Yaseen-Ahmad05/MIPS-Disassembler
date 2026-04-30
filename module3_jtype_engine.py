from module1_itype import decode_itype
from module2_rtype import decode_rtype

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
                if opcode == 0x03:
                    labels[target] = f"func_{func_counter}"
                    func_counter += 1
                else:
                    labels[target] = f"loop_{label_counter}"
                    label_counter += 1
        else: # I-Type
            if opcode in BRANCH_OPCODES:
                target = branch_target(bin_str, pc)
                if target in valid_addresses and target not in labels:
                    labels[target] = f"loop_{label_counter}"
                    label_counter += 1
        pc += 4
        
    return labels

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
        
    return assembly
