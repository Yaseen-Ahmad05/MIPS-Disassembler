

def get_registers():
    return [
        "$zero", "$at", "$v0", "$v1", "$a0", "$a1", "$a2", "$a3",
        "$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7",
        "$s0", "$s1", "$s2", "$s3", "$s4", "$s5", "$s6", "$s7",
        "$t8", "$t9", "$k0", "$k1", "$gp", "$sp", "$fp", "$ra"
    ]

def get_reg_name(reg_num):
    registers = get_registers()
    if not 0 <= reg_num < len(registers):
        raise ValueError(f"Invalid register number: {reg_num}")
    return registers[reg_num]

def sign_extend(imm_16):
    # sign extend 16-bit to integer
    if (imm_16 & 0x8000) != 0:
        return imm_16 - 0x10000
    return imm_16
