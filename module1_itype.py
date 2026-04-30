from utils import get_reg_name, sign_extend

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
