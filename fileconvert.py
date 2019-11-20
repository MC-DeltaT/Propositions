import boolean
import exprparse
import exprutility

from contextlib import ExitStack
from io import TextIOBase
import sys
from typing import Iterator, List

import numpy
from tqdm import tqdm


class DecodeError(Exception):
    def __init__(self, line_num: int, message: str) -> None:
        self.line_num = line_num
        self.message = message

    def __str__(self) -> str:
        return f"Error on line {self.line_num}:\n{self.message}"


# Converts bits to a byte.
def bits_to_byte(b7: bool, b6: bool, b5: bool, b4: bool, b3: bool, b2: bool, b1: bool, b0: bool) -> int:
    return b0 | int(b1) << 1 | int(b2) << 2 | int(b3) << 3 | int(b4) << 4 | int(b5) << 5 | int(b6) << 6 | int(b7) << 7


# Lazily converts a sequence of bytes to a sequence of bits. The bits are ordered from high to low.
def bytes_to_bits(bytes_: bytes) -> Iterator[bool]:
    for byte in bytes_:
        for i in reversed(range(8)):
            bit = bool(byte & (1 << i))
            yield bit


# Lazily decodes encoded lines into bytes.
def decode_lines(lines) -> Iterator[int]:
    assert len(lines) % 8 == 0
    bits = numpy.empty(8, dtype=bool)
    j = 0
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            raise DecodeError(i, "Line must not be blank.")
        try:
            expr = exprparse.parse(line)
        except exprparse.InvalidSyntax as e:
            raise DecodeError(i, str(e))
        try:
            bit = expr.exact_value.value
        except ValueError:
            raise DecodeError(i, "Expression does not evaluate to a single value.")

        bits[j] = bit
        if j == 7:
            yield bits_to_byte(*bits)
            j = 0
        else:
            j += 1


def decode(input_path: str, output_path: str) -> None:
    with ExitStack() as context:
        try:
            input_file: TextIOBase = context.enter_context(open(input_path, mode="r", encoding="ascii"))
        except FileNotFoundError:
            print(f'Input file "{input_path}" not found.')
            return
        except OSError:
            print(f'Failed to open input file "{input_path}".')
            return

        print("Reading input...", end="")
        try:
            lines: List[str] = list(input_file)
        except OSError:
            print("\nFailed to read from input file.")
            return
        print(" done")

    if len(lines) % 8 != 0:
        print("Number of input bits is not a multiple of 8.")
        return

    print("Decoding...")
    with ExitStack() as context:
        try:
            output_file = context.enter_context(open(output_path, mode="xb"))
        except FileExistsError:
            print(f'Output file "{output_path}" already exists.')
            return
        except OSError:
            print(f'Failed to open output file "{output_path}".')
            return

        try:
            for byte in decode_lines(tqdm(lines, unit="b")):
                output_file.write(bytes((byte,)))
        except DecodeError as e:
            print(str(e))
            return
        except OSError:
            print("Failed to write to output file.")
            return


def encode(input_path: str, output_path: str) -> None:
    with ExitStack() as context:
        try:
            input_file = context.enter_context(open(input_path, mode="rb"))
        except FileNotFoundError:
            print(f'Input file "{input_path}" not found.')
            return
        except OSError:
            print(f'Failed to open input file "{input_path}".')
            return

        print("Reading input...", end="")
        try:
            data: bytes = input_file.read()
        except OSError:
            print("\nFailed to read from input file.")
            return
        print(" done")

    bits = bytes_to_bits(data)
    exprs = (exprutility.random_expression_with_value(4, 5, boolean.from_bool(b)) for b in bits)

    print("Encoding...")
    with ExitStack() as context:
        try:
            output_file = context.enter_context(open(output_path, mode="x", encoding="ascii"))
        except FileExistsError:
            print(f'Output file "{output_path}" already exists.')
            return
        except OSError:
            print(f'Failed to open output file "{output_path}".')
            return

        try:
            for expr in tqdm(exprs, total=len(data) * 8, unit="b"):
                output_file.write(f"{expr}\n")
        except OSError:
            print("Failed to write to output file.")
            return


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
        print(f'Invalid mode "{mode}".')
