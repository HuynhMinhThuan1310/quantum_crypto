

class AES:
    """AES-128 Implementation"""
    
    # S-box: Bảng thay thế cho SubBytes
    S_BOX = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5e, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xd7, 0x4b, 0x55, 0xcf, 0x34, 0xc5, 0x84,
        0xcb, 0xb6, 0xf4, 0xf6, 0x76, 0x80, 0xff, 0x6f, 0x0d, 0x3d, 0xd3, 0x31, 0x69, 0x51, 0xd0, 0xcf,
        0x20, 0xc0, 0x33, 0x08, 0x13, 0x4a, 0x7b, 0x44, 0x82, 0xd6, 0xb0, 0x90, 0xd4, 0x2c, 0x12, 0x58,
        0x78, 0xb8, 0x50, 0xb0, 0x6d, 0x2f, 0x55, 0x2d, 0x4f, 0x87, 0x18, 0xab, 0x66, 0xb2, 0xf9, 0xd4
    ]
    
    # Inverse S-box: Bảng thay thế ngược cho InvSubBytes
    INV_S_BOX = [
        0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
        0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
        0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
        0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
        0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
        0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
        0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
        0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
        0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
        0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
        0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
        0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
        0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
        0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
    ]
    
    def __init__(self, key, plaintext):
        self.key = key
        self.plaintext = plaintext
        # Chuyển bytes plaintext thành list hex string (padding nếu cần)
        plaintext_list = list(plaintext) + [0] * (16 - len(plaintext))  # Pad với 0 nếu < 16 bytes
        plaintext_list = plaintext_list[:16]  # Lấy 16 bytes đầu
        # Tạo state 4x4 từ plaintext hex - AES dùng column-major order
        # plaintext[0,1,2,3,4,5...] -> state[0][0,1,2,3], state[1][0,1,2,3], etc.
        self.state = [
            [format(plaintext_list[i + j*4], '02x') for j in range(4)]
            for i in range(4)
        ]
        
        # Chuyển key bytes thành state 4x4 - cũng dùng column-major order
        key_list = list(key) + [0] * (16 - len(key))
        key_list = key_list[:16]
        self.key_state = [
            [format(key_list[i + j*4], '02x') for j in range(4)]
            for i in range(4)
        ]
    
        
    def _hex2int(self, hex_str):
        """Chuyển hex string thành int"""
        return int(hex_str, 16) if isinstance(hex_str, str) else hex_str
    
    def _int2hex(self, value):
        """Chuyển int thành hex string 2 ký tự"""
        return format(value & 0xff, '02x')
    
    def gmul(self, a, b):
        """Phép nhân Galois trong GF(2^8)"""
        a = self._hex2int(a) if isinstance(a, str) else a
        p = 0
        for _ in range(8):
            if b & 1:
                p ^= a
            hi_bit = a & 0x80
            a = (a << 1) & 0xff
            if hi_bit:
                a ^= 0x1b
            b >>= 1
        return p
    
    def add_round_key(self, state, round_key):
        """AddRoundKey: XOR state với round key"""
        result = [['00'] * 4 for _ in range(4)]
        # Nếu round_key là bytes, chuyển thành state 4x4
        if isinstance(round_key, bytes):
            key_list = list(round_key) + [0] * (16 - len(round_key))
            key_list = key_list[:16]
            round_key_state = [
                [format(key_list[i*4 + j], '02x') for j in range(4)]
                for i in range(4)
            ]
        else:
            round_key_state = round_key
            
        for i in range(4):
            for j in range(4):
                state_byte = self._hex2int(state[i][j])
                key_byte = self._hex2int(round_key_state[i][j])
                result[i][j] = self._int2hex(state_byte ^ key_byte)
        return result
    
    def sub_bytes(self, state):
        """SubBytes: thay thế mỗi byte sử dụng S-box"""
        result = [['00'] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                byte_val = self._hex2int(state[i][j])
                result[i][j] = self._int2hex(self.S_BOX[byte_val])
        return result
    
    def inv_sub_bytes(self, state):
        """InvSubBytes: thay thế mỗi byte sử dụng Inverse S-box"""
        result = [['00'] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                byte_val = self._hex2int(state[i][j])
                result[i][j] = self._int2hex(self.INV_S_BOX[byte_val])
        return result
    
    def shift_rows(self, state):
        """ShiftRows: dịch các hàng"""
        result = [['00'] * 4 for _ in range(4)]
        result[0] = state[0][:]
        result[1] = state[1][1:] + state[1][:1]
        result[2] = state[2][2:] + state[2][:2]
        result[3] = state[3][3:] + state[3][:3]
        return result
    
    def inv_shift_rows(self, state):
        """InvShiftRows: dịch ngược các hàng"""
        result = [['00'] * 4 for _ in range(4)]
        result[0] = state[0][:]
        result[1] = state[1][-1:] + state[1][:-1]
        result[2] = state[2][-2:] + state[2][:-2]
        result[3] = state[3][-3:] + state[3][:-3]
        return result
    
    def mix_columns(self, state):
        """MixColumns: trộn các cột"""
        result = [['00'] * 4 for _ in range(4)]
        for j in range(4):
            col = [state[i][j] for i in range(4)]
            
            result[0][j] = self._int2hex(
                self.gmul(col[0], 2) ^ self.gmul(col[1], 3) ^ 
                self._hex2int(col[2]) ^ self._hex2int(col[3])
            )
            result[1][j] = self._int2hex(
                self._hex2int(col[0]) ^ self.gmul(col[1], 2) ^ 
                self.gmul(col[2], 3) ^ self._hex2int(col[3])
            )
            result[2][j] = self._int2hex(
                self._hex2int(col[0]) ^ self._hex2int(col[1]) ^ 
                self.gmul(col[2], 2) ^ self.gmul(col[3], 3)
            )
            result[3][j] = self._int2hex(
                self.gmul(col[0], 3) ^ self._hex2int(col[1]) ^ 
                self._hex2int(col[2]) ^ self.gmul(col[3], 2)
            )
        return result
    
    def inv_mix_columns(self, state):
        """InvMixColumns: trộn ngược các cột"""
        result = [['00'] * 4 for _ in range(4)]
        for j in range(4):
            col = [state[i][j] for i in range(4)]
            
            result[0][j] = self._int2hex(
                self.gmul(col[0], 14) ^ self.gmul(col[1], 11) ^ 
                self.gmul(col[2], 13) ^ self.gmul(col[3], 9)
            )
            result[1][j] = self._int2hex(
                self.gmul(col[0], 9) ^ self.gmul(col[1], 14) ^ 
                self.gmul(col[2], 11) ^ self.gmul(col[3], 13)
            )
            result[2][j] = self._int2hex(
                self.gmul(col[0], 13) ^ self.gmul(col[1], 9) ^ 
                self.gmul(col[2], 14) ^ self.gmul(col[3], 11)
            )
            result[3][j] = self._int2hex(
                self.gmul(col[0], 11) ^ self.gmul(col[1], 13) ^ 
                self.gmul(col[2], 9) ^ self.gmul(col[3], 14)
            )
        return result
    
    def encrypt(self):
        """Mã hóa AES-128"""
        state = self.add_round_key(self.state, self.key_state)
        
        for _ in range(9):
            state = self.sub_bytes(state)
            state = self.shift_rows(state)
            state = self.mix_columns(state)
            state = self.add_round_key(state, self.key_state)
        
        state = self.sub_bytes(state)
        state = self.shift_rows(state)
        state = self.add_round_key(state, self.key_state)
        
        return state
    
    def decrypt(self, ciphertext):
        """Giải mã AES-128"""
        # Chuyển ciphertext bytes thành state 4x4 hex string - dùng column-major order
        if isinstance(ciphertext, bytes):
            cipher_list = list(ciphertext) + [0] * (16 - len(ciphertext))
            cipher_list = cipher_list[:16]
            cipher_state = [
                [format(cipher_list[i + j*4], '02x') for j in range(4)]
                for i in range(4)
            ]
        else:
            cipher_state = ciphertext
        
        state = self.add_round_key(cipher_state, self.key_state)
        
        for _ in range(9):
            state = self.inv_shift_rows(state)
            state = self.inv_sub_bytes(state)
            state = self.add_round_key(state, self.key_state)
            state = self.inv_mix_columns(state)
        
        state = self.inv_shift_rows(state)
        state = self.inv_sub_bytes(state)
        state = self.add_round_key(state, self.key_state)
        
        return state
