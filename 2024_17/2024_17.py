import sys
from common.utils import run


def line_to_reg_value(line: str) -> int:
    return int(line.split(":")[1].strip())


def run_program(init_reg_a: int, init_reg_b: int, init_reg_c: int, program: list[int]) -> list[int]:
    state = {"a": init_reg_a, "b": init_reg_b, "c": init_reg_c, "instr_p": 0, "output": []}

    def combo_operand(op: int, state) -> int:
        if op <= 3:
            return op
        elif op == 4:
            return state["a"]
        elif op == 5:
            return state["b"]
        elif op == 6:
            return state["c"]
        else:
            raise "Invalid op"

    def adv(op: int, state: dict[str, int]):
        # The adv instruction (opcode 0) performs division.
        # The numerator is the value in the A register.
        # The denominator is found by raising 2 to the power of the instruction's combo operand.
        # (So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.)
        # The result of the division operation is truncated to an integer and then written to the A register.
        state["a"] = int(state["a"] / (2 ** combo_operand(op, state)))
        return True

    def bxl(op: int, state: dict[str, int]):
        # The bxl instruction (opcode 1) calculates the bitwise XOR of register B
        # and the instruction's literal operand, then stores the result in register B.
        state["b"] = state["b"] ^ op
        return True

    def bst(op: int, state: dict[str, int]):
        # The bst instruction (opcode 2) calculates the value of its combo operand modulo 8
        # (thereby keeping only its lowest 3 bits), then writes that value to the B register.
        state["b"] = combo_operand(op, state) % 8
        return True

    def jnz(op: int, state: dict[str, int]):
        # The jnz instruction (opcode 3) does nothing if the A register is 0.
        # However, if the A register is not zero, it jumps by setting the instruction pointer to the value of its literal operand;
        # if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.
        if state["a"] == 0:
            return True
        state["instr_p"] = op
        return False

    def bxc(op: int, state: dict[str, int]):
        # The bxc instruction (opcode 4) calculates the bitwise XOR of register B and register C
        # then stores the result in register B.
        # (For legacy reasons, this instruction reads an operand but ignores it.)
        state["b"] = state["b"] ^ state["c"]
        return True

    def out(op: int, state: dict[str, int]):
        # The out instruction (opcode 5) calculates the value of its combo operand modulo 8,
        # then outputs that value. (If a program outputs multiple values, they are separated by commas.)
        state["output"].append(combo_operand(op, state) % 8)
        return True

    def bdv(op: int, state: dict[str, int]):
        # The bdv instruction (opcode 6) works exactly like the adv instruction
        # except that the result is stored in the B register.
        # (The numerator is still read from the A register.)
        state["b"] = int(state["a"] / (2 ** combo_operand(op, state)))
        return True

    def cdv(op: int, state: dict[str, int]):
        # The cdv instruction (opcode 7) works exactly like the adv instruction
        # except that the result is stored in the C register.
        # (The numerator is still read from the A register.)
        state["c"] = int(state["a"] / (2 ** combo_operand(op, state)))
        return True

    def get_operation(opcode: int):
        return {0: adv, 1: bxl, 2: bst, 3: jnz, 4: bxc, 5: out, 6: bdv, 7: cdv}[opcode]

    try:
        while state["instr_p"] <= (len(program) - 2):
            operation = get_operation(program[state["instr_p"]])
            operand = program[state["instr_p"] + 1]
            should_jump = operation(operand, state)
            if should_jump:
                state["instr_p"] += 2
    except Exception as ex:
        print(ex)

    return state["output"]


def solution_2024_17_A(filename: str) -> str:
    with open(filename) as file:
        lines = list(file)
    reg_a = line_to_reg_value(lines[0])
    reg_b = line_to_reg_value(lines[1])
    reg_c = line_to_reg_value(lines[2])

    program = [int(num.strip()) for num in lines[4].split(":")[1].split(",")]
    output = run_program(reg_a, reg_b, reg_c, program)

    return ",".join([str(i) for i in output])


# Our input Program: 2,4,1,1,7,5,4,4,1,4,0,3,5,5,3,0
# our program outputs reg_b%8 repeatedly while reg_a != 0
# 2,4 - reg_b=reg_a%8
# 1,1 - reg_b=reg_b^1
# 7,5 - reg_c = reg_a/(2**reg_b)
# 4,4 - reg_b = reg_b^reg_c
# 1,4 - reg_b = reg_b^4
# 0,3 - reg_a = reg_a/(2**3)

# So reg each iteration
# 2,4 - reg_b=A%8
# 1,1 - reg_b=(A%8)^1
# 7,5 - reg_c = int((A%8)/(2**((A%8)^1)))
# 4,4 - reg_b = ((A%8)^1)^(int((A%8)/(2**((A%8)^1))))
# 1,4 - reg_b = ((((A%8)^1)^(int((A%8)/(2**((A%8)^1)))))^4)

# initial reg_b=A%8 means the value output cycles by 8 each time

# So our program needs to output 16 numbers to have output match the program
# So starting val of reg_8 needs to be divisible by 8, 16 times
# So final numerator must be 1 <= N < 8

#  i.e  A / 8^15 = N where 1 <= N < 8
# So A=8**15 * N where 1 <= N < 8
# So just out of range is A=8**15*8=281474976710656
# So highest poss reg_a=281474976710655
# Running for our input 281474976710655 gives
#  [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2]

# 1. >>> int(281474976710655/8)
# 35184372088831
# 2. >>> int(35184372088831/8)
# 4398046511103
# 3. >>> int(4398046511103/8)
# 549755813887
# 4. >>> int(549755813887/8)
# 68719476735
# 5. >>> int(68719476735/8)
# 8589934591
# 6. >>> int(8589934591/8)
# 1073741823
# 7. >>> int(1073741823/8)
# 134217727
# 8. >>> int(134217727/8)
# 16777215
# 9. >>> int(16777215/8)
# 2097151
# 10. >>> int(2097151/8)
# 262143
# 11. >>> int(262143/8)
# 32767
# 12. >>> int(32767/8)
# 4095
# 13. >>> int(4095/8)
# 511
# 14. >>> int(511/8)
# 63
# 15. >>> int(63/8)
# 7
# 16. >>> int(7/8)
# 0


# 2,4 - reg_b=reg_a%8
# 1,1 - reg_b=(reg_a%8)^1
# 7,5 - reg_c = int(reg_a/(2**((reg_a%8)^1)))
# 4,4 - reg_b = ((reg_a%8)^1)^(int(reg_a/(2**((reg_a%8)^1))))
# 1,4 - reg_b = (((reg_a%8)^1)^(int(reg_a/(2**((reg_a%8)^1)))))^4

# So first in program is a 2 so we want
# (((A%8)^1)^(int(A/(2**((A%8)^1)))))^4 = 2
# ((A%8)^1)^(int(A/(2**((A%8)^1)))) = 2^4
# ((A%8)^1)^(int(A/(2**((A%8)^1)))) = 6
# int(A/(2**((A%8)^1)) = 6^((A%8)^1)
#

# So for each A as it decrease we output ((A%8)^1)^(A/(2**(A%8)^1))^4
# So we want an A s.t ((A%8)^1)^(A/(2**(A%8)^1))^4 = 2
#                     ((int(A/8)%8)^1)^(int(A/16)/(2**(int(A/8)%8)^1))^4 = 4
#                     ((int(A/64)%8)^1)^(int(A/64)/(2**(int(A/64)%8)^1))^4 = 1
# etc


def solution_2024_17_B(filename: str) -> str:
    with open(filename) as file:
        lines = list(file)

    reg_b = line_to_reg_value(lines[1])
    reg_c = line_to_reg_value(lines[2])

    program = [int(num.strip()) for num in lines[4].split(":")[1].split(",")]

    #
    #          j        i                     0,1                            4,6,7
    # reg_a = ((5 << (3*15)) + (6 << (3*14))) + (0 << (3*13)) + (1 << (3*12)) + (6 << (3*11)) # etc
    # Need to try all combos where there are multiple possibilities.
    # Try them in asc order so we match the lowest one first

    def find_quine_input(program: list[int], candidate_reg_val: int, i: int):
        candidates = []
        for j in range(0, 8):
            add = j << (3 * i)
            new_reg_a = candidate_reg_val + add
            output = run_program(new_reg_a, reg_b, reg_c, program)
            if output == program:
                return new_reg_a
            elif len(output) == len(program) and output[i] == program[i] and i > 0:
                candidates.append(find_quine_input(program, new_reg_a, i - 1))
        results = [candidate for candidate in candidates if candidate is not None]
        valid_results = [result for result in results if run_program(result, reg_b, reg_c, program) == program]
        if len(valid_results) > 0:
            return min(valid_results)
        else:
            return None

    return find_quine_input(program, 0, len(program) - 1)


def test_solution_2024_17_A():
    assert (
        solution_2024_17_A("./2024_17/test_input.txt") == "4,6,3,5,6,3,5,2,1,0"
    )  # Replace with expected output for the test case


# def test_final_solution_2024_17_A():
#    assert solution_2024_17_A('./2024_17/input.txt') == 0 # Replace with solution when known


def test_solution_2024_17_B():
    assert solution_2024_17_B("./2024_17/test_input_b.txt") == 117440  # Replace with expected output for the test case


# def test_final_solution_2024_17_B():
#    assert solution_2024_17_B('./2024_17/input.txt') == 0 # Replace with solution when known

if __name__ == "__main__":
    run("2024_17", sys.argv[1], solution_2024_17_A, solution_2024_17_B)
