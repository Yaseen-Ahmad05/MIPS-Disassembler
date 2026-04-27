# Module 2: R-Type Specialist (Role 2)
# Responsibilities:
# - Extract rs, rt, rd, shamt, and funct fields.
# - Decode R-type arithmetic (add, sub, mult)
# - Decode logical (and, or, nor, not)
# - Decode shift operations (sll, srl, sra)
# - Handle 'jr' exception handler.

from utils import get_reg_name

class RTypeDecoder:
    def __init__(self):
        pass
        
    def decode(self, binary_str):
        """
        Decodes a 32-bit binary string representing an R-Type instruction.
        """
        # opcode = int(binary_str[0:6], 2) # opcode is known to be 0 for R-Type
        rs = int(binary_str[6:11], 2)
        rt = int(binary_str[11:16], 2)
        rd = int(binary_str[16:21], 2)
        shamt = int(binary_str[21:26], 2)
        funct = int(binary_str[26:32], 2)
        
        rs_name = get_reg_name(rs)
        rt_name = get_reg_name(rt)
        rd_name = get_reg_name(rd)
        
        if funct == 0x20:
            return f"add {rd_name}, {rs_name}, {rt_name}"
        elif funct == 0x21: # addu (bonus)
            return f"addu {rd_name}, {rs_name}, {rt_name}"
        elif funct == 0x22:
            return f"sub {rd_name}, {rs_name}, {rt_name}"
        elif funct == 0x18:
            return f"mult {rs_name}, {rt_name}"
        elif funct == 0x24:
            return f"and {rd_name}, {rs_name}, {rt_name}"
        elif funct == 0x25:
            return f"or {rd_name}, {rs_name}, {rt_name}"
        elif funct == 0x27:
            if rt == 0:
                return f"not {rd_name}, {rs_name}"
            return f"nor {rd_name}, {rs_name}, {rt_name}"
        elif funct == 0x00:
            return f"sll {rd_name}, {rt_name}, {shamt}"
        elif funct == 0x02:
            return f"srl {rd_name}, {rt_name}, {shamt}"
        elif funct == 0x03: # sra (bonus)
            return f"sra {rd_name}, {rt_name}, {shamt}"
        elif funct == 0x08:
            # jr exception handler
            return f"jr {rs_name}"
            
        return "Unknown R-Type Instruction"
