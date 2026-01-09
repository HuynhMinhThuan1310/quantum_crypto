import quantum_utils
import random
import struct

class Alice:
    def __init__(self):
        self.sending_data = None  # Dữ liệu nhị phân (128 bits)
        self.temperature = None
        self.humidity = None
        self.dust = None
        self.smoke = None
        self.temp_bits = None
        self.humi_bits = None
        self.dust_bits = None
        self.smoke_bits = None
        self.raw_key = None
        self.public_key = None
        self.photons = None
        self.qubits = None
        self.bases = None
        self.bob_bases = None
        print("Alice được khởi tạo!")

    def receive_and_encode_data(self, temperature, humidity, dust, smoke):
        self.temperature = temperature
        self.humidity = humidity
        self.dust = dust
        self.smoke = smoke

        # Mã hóa thành nhị phân sử dụng struct.pack (giống AES)
        data_bytes = struct.pack('ffff', temperature, humidity, dust, smoke)
        self.sending_data = ''.join(f'{byte:08b}' for byte in data_bytes)
        print(f"\nSending data (128 bits): {self.sending_data}")

    def generate_qubits(self, sending_data):
        """Tạo qubits từ dữ liệu nhị phân"""
        self.qubits = [int(bit) for bit in sending_data]
        #print(f"\nQubits được tạo từ dữ liệu: {self.qubits}")

    def create_bases(self):
        """Tạo cơ sở ngẫu nhiên cho mỗi bit dữ liệu"""
        length = len(self.qubits)
        self.bases = quantum_utils.generate_random_bases(length)
        #print(f"\nCơ sở của Alice được tạo: {self.bases}")
    
    def generate_photons(self):
        """Tạo photons dựa trên qubits và cơ sở"""
        self.photons = quantum_utils.generate_and_regenerate_photons(self.qubits, self.bases)
        #print(f"\n{len(self.photons)} photons được tạo.")
        #print(f"\nPhotons: {self.photons}")

    def generate_raw_key(self, bob_bases):
        """Tạo khóa thô dựa trên cơ sở của Alice và Bob"""
        self.raw_key = []
        for i in range(len(self.photons)):
            if self.bases[i] == bob_bases[i]:
                self.raw_key.append(int(self.photons[i]))
        #print(f"\nKhóa thô của Alice: {self.raw_key}")

    def generate_public_key(self):
        """
        Lấy 50% ngẫu nhiên của khóa thô gửi cho Bob
        (gửi dưới dạng binary string)
        """
        if len(self.raw_key) == 0:
            return ""
        
        # Số bit cần lấy (50% của khóa thô)
        part_length = max(1, len(self.raw_key) // 2)
        
        # Chọn ngẫu nhiên các vị trí từ khóa thô
        selected_positions = random.sample(range(len(self.raw_key)), part_length)
        selected_positions.sort()
        self.selected_positions = selected_positions  # Lưu vị trí để sử dụng sau
        
        # Tạo binary string từ các bit được chọn
        self.public_key = ''.join(str(self.raw_key[pos]) for pos in selected_positions)
        #print(f"\nKhóa công khai gửi cho Bob: {self.public_key}")
        return self.public_key

    def generate_secret_key(self):
        """Tạo khóa bí mật cuối cùng bằng cách loại bỏ các bit đã dùng để kiểm tra lỗi"""
        public_key_positions = set(self.selected_positions)
        self.secret_key = []
        for i in range(len(self.raw_key)):
            if i not in public_key_positions:
                self.secret_key.append(self.raw_key[i])
        #print(f"\nKhóa bí mật cuối cùng của Alice: {self.secret_key}")





        

    



    


  
