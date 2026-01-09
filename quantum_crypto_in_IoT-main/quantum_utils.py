import struct
import random
from typing import List


def generate_random_qubits(length: int) -> List[int]:
    """Tạo danh sách qubit ngẫu nhiên (0 hoặc 1)"""
    return [random.randint(0, 1) for _ in range(length)]

def float_to_bits(num):
    packed = struct.pack('!f', num)  # float 32-bit
    bits = ''.join(f'{b:08b}' for b in packed)
    return bits


def bits_to_float(bits):
    # Nếu bits là list hoặc bytes, chuyển thành string nhị phân
    if isinstance(bits, (list, bytes)):
        bits = ''.join(str(b) for b in bits)
    byte_array = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        byte_array.append(int(byte, 2))
    packed = bytes(byte_array)
    num = struct.unpack('!f', packed)[0]
    return num


def generate_random_bases(length: int) -> List[str]:
    """Tạo danh sách cơ sở ngẫu nhiên cho BB84 protocol"""
    return [random.choice(['+', 'x']) for _ in range(length)]


def generate_random_bits(length: int) -> List[int]:
    """Tạo danh sách bit ngẫu nhiên (0 hoặc 1)"""
    return [random.randint(0, 1) for _ in range(length)]


def generate_and_regenerate_photons(bits_list, bases):
    photons = []
    for bit, basis in zip(bits_list, bases):
        # Nếu cơ sở là "x" thì đảo bit
        if basis == "x":
            encoded_bit = 1 - bit
        else:
            encoded_bit = bit
        photons.append(encoded_bit)
    return photons

