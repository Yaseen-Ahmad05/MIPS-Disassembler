# Module 1: I-Type Specialist (Role 1)
# Responsibilities:
# - Decode I-type instructions: addi, ori, slti, sltiu
# - Reconstruct memory operations: lw, sw, lui, sh, sb
# - Handle conditional branches: beq, bne, bltz, bgez, bgtz, blez
# - Sign/zero extension for immediates

from utils import get_reg_name, sign_extend

class ITypeDecoder:
    def __init__(self):
        pass
        
    def decode(self, binary_str, pc):
        """
        Decodes a 32-bit binary string representing an I-Type instruction.
        """
        opcode = int(binary_str[0:6], 2)
        rs = int(binary_str[6:11], 2)
        rt = int(binary_str[11:16], 2)
        imm = int(binary_str[16:32], 2)
        
        rs_name = get_reg_name(rs)
        rt_name = get_reg_name(rt)
        
        # Immediate representations
        imm_signed = sign_extend(imm)
        imm_unsigned = imm # zero-extended
        
        # Opcode mapping
        if opcode == 0x08: # addi
            return f"addi {rt_name}, {rs_name}, {imm_signed}"
        elif opcode == 0x0d: # ori
            return f"ori {rt_name}, {rs_name}, {imm_unsigned}"
        elif opcode == 0x0c: # andi (bonus)
            return f"andi {rt_name}, {rs_name}, {imm_unsigned}"
        elif opcode == 0x0a: # slti
            return f"slti {rt_name}, {rs_name}, {imm_signed}"
        elif opcode == 0x0b: # sltiu
            return f"sltiu {rt_name}, {rs_name}, {imm_signed}"
        elif opcode == 0x20: # lb (bonus)
            return f"lb {rt_name}, {imm_signed}({rs_name})"
        elif opcode == 0x23: # lw
            return f"lw {rt_name}, {imm_signed}({rs_name})"
        elif opcode == 0x2b: # sw
            return f"sw {rt_name}, {imm_signed}({rs_name})"
        elif opcode == 0x0f: # lui
            return f"lui {rt_name}, {imm_unsigned}"
        elif opcode == 0x29: # sh
            return f"sh {rt_name}, {imm_signed}({rs_name})"
        elif opcode == 0x28: # sb
            return f"sb {rt_name}, {imm_signed}({rs_name})"
        elif opcode == 0x04: # beq
            target = pc + 4 + (imm_signed << 2)
            return f"beq {rs_name}, {rt_name}, 0x{target:08x}"
        elif opcode == 0x05: # bne
            target = pc + 4 + (imm_signed << 2)
            return f"bne {rs_name}, {rt_name}, 0x{target:08x}"
        elif opcode == 0x06: # blez
            target = pc + 4 + (imm_signed << 2)
            return f"blez {rs_name}, 0x{target:08x}"
        elif opcode == 0x07: # bgtz
            target = pc + 4 + (imm_signed << 2)
            return f"bgtz {rs_name}, 0x{target:08x}"
        elif opcode == 0x01: # bltz or bgez
            target = pc + 4 + (imm_signed << 2)
            if rt == 0:
                return f"bltz {rs_name}, 0x{target:08x}"
            elif rt == 1:
                return f"bgez {rs_name}, 0x{target:08x}"
        elif opcode == 0x0e: # xori (bonus)
            return f"xori {rt_name}, {rs_name}, {imm_unsigned}"
        
        return "Unknown I-Type Instruction"
