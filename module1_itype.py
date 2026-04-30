from utils import get_reg_name, sign_extend
import re

def process_pseudo_branches(assembly_lines):
    result = []
    i = 0
    while i < len(assembly_lines):
        line1 = assembly_lines[i]
        
        label_prefix1 = ""
        slt_str = line1
        if ":\n" in line1:
            parts = line1.split(":\n", 1)
            label_prefix1 = parts[0] + ":\n"
            slt_str = parts[1]
            
        slt_match = re.match(r'^slt\s+(\$\w+),\s+(\$\w+),\s+(\$\w+)$', slt_str)
        
        if slt_match and i + 1 < len(assembly_lines):
            line2 = assembly_lines[i+1]
            
            label_prefix2 = ""
            branch_str = line2
            if ":\n" in line2:
                parts = line2.split(":\n", 1)
                label_prefix2 = parts[0] + ":\n"
                branch_str = parts[1]
                
            branch_match = re.match(r'^(bne|beq)\s+(\$\w+),\s+(\$\w+),\s+(.+)$', branch_str)
            if branch_match:
                b_type, b_rs, b_rt, target = branch_match.groups()
                slt_rd, slt_rs, slt_rt = slt_match.groups()
                
                if (b_rs == slt_rd and b_rt == "$zero") or (b_rt == slt_rd and b_rs == "$zero"):
                    combined = ""
                    if b_type == "bne":
                        combined = f"blt {slt_rs}, {slt_rt}, {target}"
                    elif b_type == "beq":
                        combined = f"ble {slt_rt}, {slt_rs}, {target}"
                        
                    if combined:
                        final_label = label_prefix1 + label_prefix2
                        result.append(final_label + combined)
                        i += 2
                        continue
                        
        result.append(line1)
        i += 1
        
    return result

def decode_itype(binary_str, pc):
    opcode = int(binary_str[0:6], 2)
    rs = int(binary_str[6:11], 2)
    rt = int(binary_str[11:16], 2)
    imm = int(binary_str[16:32], 2)
    
    rs_name = get_reg_name(rs)
    rt_name = get_reg_name(rt)
    
    imm_signed = sign_extend(imm)
    imm_unsigned = imm # zero-extended
    
    if opcode == 0x08:
        return f"addi {rt_name}, {rs_name}, {imm_signed}"
    elif opcode == 0x09:
        return f"addiu {rt_name}, {rs_name}, {imm_signed}"
    elif opcode == 0x0c:
        return f"andi {rt_name}, {rs_name}, {imm_unsigned}"
    elif opcode == 0x04:
        target = pc + 4 + (imm_signed << 2)
        return f"beq {rs_name}, {rt_name}, 0x{target:08x}"
    elif opcode == 0x05:
        target = pc + 4 + (imm_signed << 2)
        return f"bne {rs_name}, {rt_name}, 0x{target:08x}"
    elif opcode == 0x24:
        return f"lbu {rt_name}, {imm_signed}({rs_name})"
    elif opcode == 0x25:
        return f"lhu {rt_name}, {imm_signed}({rs_name})"
    elif opcode == 0x0f:
        return f"lui {rt_name}, {imm_unsigned}"
    elif opcode == 0x23:
        return f"lw {rt_name}, {imm_signed}({rs_name})"
    elif opcode == 0x0d:
        return f"ori {rt_name}, {rs_name}, {imm_unsigned}"
    elif opcode == 0x0a:
        return f"slti {rt_name}, {rs_name}, {imm_signed}"
    elif opcode == 0x0b:
        return f"sltiu {rt_name}, {rs_name}, {imm_signed}"
    elif opcode == 0x28:
        return f"sb {rt_name}, {imm_signed}({rs_name})"
    elif opcode == 0x29:
        return f"sh {rt_name}, {imm_signed}({rs_name})"
    elif opcode == 0x2b:
        return f"sw {rt_name}, {imm_signed}({rs_name})"
        
    return "Unknown I-Type Instruction"
