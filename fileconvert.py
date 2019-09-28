import boolean
import exprparse
import exprutility

from itertools import count
import sys
from typing import List, Sequence


class DecodeError(Exception):
    def __init__(self, line_num: int, message: str) -> None:
        self.line_num = line_num
        self.message = message

    def __str__(self) -> str:
        return "Error on line {}:\n{}".format(self.line_num, self.message)


# Converts a sequence of bits to a sequence of bytes. The bits are assumed to be ordered from high to low for each byte.
def bits_to_bytes(bits: Sequence[bool]) -> bytearray:
    res = bytearray()
    for i in range(len(bits) // 8):
        byte = 0
        for j in range(8):
            byte <<= 1
            byte |= int(bits[i * 8 + j])
        res.append(byte)
    return res


# Converts a sequence of bytes to a sequence of bits. The bits are ordered from high to low.
def bytes_to_bits(bytes_: bytes) -> List[bool]:
    res: List[bool] = []
    for byte in bytes_:
        for i in reversed(range(8)):
            bit = bool(byte & (1 << i))
            res.append(bit)
    return res


def read_bits(input_file) -> List[bool]:
    bits: List[bool] = []
    for line_count in count(1):
        line = input_file.readline()
        if not line:
            break

        line = line.strip()
        if not line:
            continue

        try:
            expr = exprparse.parse(line)
        except exprparse.InvalidSyntax as e:
            raise DecodeError(line_count, str(e))

        try:
            bit = expr.exact_value.value
        except ValueError:
            raise DecodeError(line_count, "Expression does not evaluate to a single value.")
        bits.append(bit)
    return bits


def decode(input_path: str, output_path: str) -> None:
    try:
        input_file = open(input_path, mode="r", encoding="ascii")
    except FileNotFoundError:
        print('Input file "{}" not found.'.format(input_path))
        return
    except OSError:
        print('Failed to open input file "{}".'.format(input_path))
        return

    try:
        bits = read_bits(input_file)
    except DecodeError as e:
        print(str(e))
        return
    except OSError:
        print("Failed to read line from input file.")
        return
    finally:
        try:
            input_file.close()
        except OSError:
            pass

    if len(bits) % 8 != 0:
        print("Number of input bits is not a multiple of 8.")
        return

    try:
        output_file = open(output_path, mode="xb")
    except FileExistsError:
        print('Output file "{}" already exists.'.format(output_path))
        return
    except OSError:
        print('Failed to open output file "{}".'.format(output_path))
        return

    bytes_ = bits_to_bytes(bits)

    try:
        output_file.write(bytes_)
    except OSError:
        print("Failed to write to output file.")
        return
    finally:
        try:
            output_file.close()
        except OSError:
            pass


def encode(input_path: str, output_path: str) -> None:
    try:
        input_file = open(input_path, mode="rb")
    except FileNotFoundError:
        print('Input file "{}" not found.'.format(input_path))
        return
    except OSError:
        print('Failed to open input file "{}".'.format(input_path))
        return

    try:
        bytes_: bytes = input_file.read()
    except OSError:
        print("Failed to read line from input file.")
        return
    finally:
        try:
            input_file.close()
        except OSError:
            pass

    bits = bytes_to_bits(bytes_)

    exprs = (exprutility.random_expression_with_value(4, 5, boolean.from_bool(b)) for b in bits)

    try:
        output_file = open(output_path, mode="x", encoding="ascii")
    except FileExistsError:
        print('Output file "{}" already exists.'.format(output_path))
        return
    except OSError:
        print('Failed to open output file "{}".'.format(output_path))
        return

    try:
        for expr in exprs:
            output_file.write(str(expr))
            output_file.write("\n")
    except OSError:
        print("Failed to write to output file.")
        return
    finally:
        try:
            output_file.close()
        except OSError:
            pass


if len(sys.argv) != 4:
    print("Usage: fileconvert.py decode|encode <input_file> <output_file>")
else:
    mode: str = sys.argv[1]
    mode = mode.lower()
    input_path: str = sys.argv[2]
    output_path: str = sys.argv[3]
    if mode == "decode":
        decode(input_path, output_path)
    elif mode == "encode":
        encode(input_path, output_path)
    else:
        print('Invalid mode "{}".'.format(mode))
