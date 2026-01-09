import json
from Crypto.Cipher import AES as CryptoAES
from Crypto.Util.Padding import pad, unpad


def pad_key(secret_key):
    """
    Chuyển đổi secret_key (string binary) thành key 16 bytes cho AES-128
    - Chia thành từng nhóm 8 bit, chuyển thành bytes
    - Nếu < 16 bytes: pad thêm bit 0
    - Nếu > 16 bytes: lấy 16 bytes đầu
    """
    if not secret_key:
        raise ValueError("Secret key không được rỗng!")
        
    # Pad với bit 0 nếu không đủ 8 bit
    while len(secret_key) % 8 != 0:
        secret_key += '0'

    # Chuyển từng nhóm 8 bit thành byte
    key_bytes = bytes(int(secret_key[i:i+8], 2) for i in range(0, len(secret_key), 8))
    
    # Đảm bảo key_bytes có đúng 16 bytes cho AES-128
    if len(key_bytes) < 16:
        key_bytes = key_bytes + b'\x00' * (16 - len(key_bytes))  # Pad với 0x00
    else:
        key_bytes = key_bytes[:16]  # Lấy 16 bytes đầu
        
    return key_bytes

def prepare_data_bytes(temperature, humidity, dust, smoke):
    """
    Chuẩn bị dữ liệu sensor thành chuỗi bytes 16 bytes cho AES-128
    - Chuyển float thành bytes cố định (4 bytes mỗi giá trị)
    - Tổng cộng: 4 giá trị × 4 bytes = 16 bytes
    """
    import struct
    
    # Chuyển mỗi float thành 4 bytes (format 'f' = float 32-bit)
    data_bytes = struct.pack('ffff', temperature, humidity, dust, smoke)
    
    return data_bytes

def encrypt_aes(data_bytes, key_bytes):
    """
    Mã hóa dữ liệu bằng AES-128-ECB (sử dụng PyCryptodome)
    """
    try:
        # Ensure key is 16 bytes
        key_bytes = key_bytes[:16] if len(key_bytes) >= 16 else key_bytes + b'\x00' * (16 - len(key_bytes))
        
        # Ensure data is 16 bytes
        data_bytes = data_bytes[:16] if len(data_bytes) >= 16 else data_bytes + b'\x00' * (16 - len(data_bytes))
        
        cipher = CryptoAES.new(key_bytes, CryptoAES.MODE_ECB)
        ciphertext = cipher.encrypt(data_bytes)
        return ciphertext
    except Exception as e:
        print(f"Lỗi mã hóa: {e}")
        return None

def decrypt_aes(ciphertext_bytes, key_bytes):
    """
    Giải mã dữ liệu bằng AES-128-ECB (sử dụng PyCryptodome)
    """
    try:
        # Ensure key is 16 bytes
        key_bytes = key_bytes[:16] if len(key_bytes) >= 16 else key_bytes + b'\x00' * (16 - len(key_bytes))
        
        cipher = CryptoAES.new(key_bytes, CryptoAES.MODE_ECB)
        plaintext = cipher.decrypt(ciphertext_bytes)
        return plaintext
    except Exception as e:
        print(f"Lỗi giải mã: {e}")
        return None

def decode_sensor_data(data_bytes):
    """
    Giải mã dữ liệu sensor từ bytes thành 4 giá trị float
    - Chuyển bytes thành dữ liệu nhị phân (temperature, humidity, dust, smoke)
    """
    import struct
    
    if len(data_bytes) < 16:
        print("Lỗi: Dữ liệu không đủ 16 bytes")
        return None
    
    try:
        # Chuyển 16 bytes thành 4 float (format 'f' = float 32-bit)
        temperature, humidity, dust, smoke = struct.unpack('ffff', data_bytes[:16])
        
        result = {
            'temperature': round(temperature, 2),
            'humidity': round(humidity, 2),
            'dust': round(dust, 2),
            'smoke': round(smoke, 2)
        }
        return result
    except Exception as e:
        print(f"Lỗi khi giải mã dữ liệu sensor: {e}")
        return None

def save_ciphertext(ciphertext_hex):
    """Lưu ciphertext vào file stored_ciphertext.txt (append)"""
    try:
        with open('stored_ciphertext.txt', 'a', encoding='utf-8') as f:
            f.write(ciphertext_hex + '\n')
        #print(f"Ciphertext đã được lưu vào stored_ciphertext.txt")
    except Exception as e:
        print(f"Lỗi khi lưu ciphertext: {e}")

def save_secret_key(secret_key_str):
    """Lưu Bob's secret key vào file stored_key.txt (append)"""
    try:
        with open('stored_key.txt', 'a', encoding='utf-8') as f:
            f.write(secret_key_str + '\n')
        #print(f"Secret key đã được lưu vào stored_key.txt")
    except Exception as e:
        print(f"Lỗi khi lưu secret key: {e}")


def bytes_to_bits(data_bytes):
    bits = ''.join(f'{byte:08b}' for byte in data_bytes)
    return bits
