import sys
import math

class Gates:
    SIGNAL = {"_": False, "-": True}
    REV_SIGNAL = {False: "_", True: "-"}

    @classmethod
    def and_gate(cls, in1: bool, in2: bool) -> bool:
        return in1 and in2
    @classmethod
    def or_gate(cls, in1: bool, in2: bool) -> bool:
        return in1 or in2
    @classmethod
    def xor_gate(cls, in1: bool, in2: bool) -> bool:
        return in1 ^ in2
    @classmethod
    def nand_gate(cls, in1: bool, in2: bool) -> bool:
        return not cls.and_gate(in1, in2)
    @classmethod
    def nor_gate(cls, in1: bool, in2: bool) -> bool:
        return not cls.or_gate(in1, in2)
    @classmethod
    def nxor_gate(cls, in1: bool, in2: bool) -> bool:
        return not cls.xor_gate(in1, in2)

    @classmethod
    def gate(cls, _type:str, in1: bool, in2: bool) -> bool:
        gates = {
            "AND": cls.and_gate,
            "OR": cls.or_gate,
            "XOR": cls.xor_gate,
            "NAND": cls.nand_gate,
            "NOR": cls.nor_gate,
            "NXOR": cls.nxor_gate,
        }
        return gates[_type](in1, in2)

n = int(input())
m = int(input())
signals = dict()
for i in range(n):
    input_name, input_signal = input().split()
    signals[input_name] = [Gates.SIGNAL[i] for i in input_signal]

out_signals = []
for i in range(m):
    output_name, _type, input_name_1, input_name_2 = input().split()
    out_signals.append((
        output_name,
        [Gates.gate(_type, in1, in2) for in1, in2 in zip(signals[input_name_1], signals[input_name_2])]
    ))


for name, signal in out_signals:
    s = ''.join([Gates.REV_SIGNAL[x] for x in signal])
    print(f"{name} {s}")
