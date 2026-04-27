from utils import get_reg_name

def decode_rtype(binary_str):
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
    elif funct == 0x21:
        return f"addu {rd_name}, {rs_name}, {rt_name}"
    elif funct == 0x24:
        return f"and {rd_name}, {rs_name}, {rt_name}"
    elif funct == 0x08:
        return f"jr {rs_name}"
    elif funct == 0x27:
        return f"nor {rd_name}, {rs_name}, {rt_name}"
    elif funct == 0x25:
        return f"or {rd_name}, {rs_name}, {rt_name}"
    elif funct == 0x2a:
        return f"slt {rd_name}, {rs_name}, {rt_name}"
    elif funct == 0x2b:
        return f"sltu {rd_name}, {rs_name}, {rt_name}"
    elif funct == 0x00:
        return f"sll {rd_name}, {rt_name}, {shamt}"
    elif funct == 0x02:
        return f"srl {rd_name}, {rt_name}, {shamt}"
    elif funct == 0x22:
        return f"sub {rd_name}, {rs_name}, {rt_name}"
    elif funct == 0x23:
        return f"subu {rd_name}, {rs_name}, {rt_name}"
        
    return "Unknown R-Type Instruction"
