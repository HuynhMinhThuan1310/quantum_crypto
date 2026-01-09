import quantum_utils

class Bob:
    def __init__(self):
        self.photons = [] # Danh sách photon nhận được
        self.bases = []
        self.alice_bases = []  # Sẽ nhận sau, qua classical channel
        self.temperature = None
        self.humidity = None 
        self.dust = None
        self.smoke = None
        self.received_data = None # Dữ liệu nhận được sau khi giải mã (128 bits)
        self.measure_photon = []    # Kết quả đo photon
        self.raw_key = []
        self.public_key = []
        self.secret_key = []
        self.error_rate = None
        print("Bob được khởi tạo!")
    
    def receive_photons(self, photons):
        """Bob nhận photons từ Alice (qua quantum channel)"""
        self.photons = photons
        #print(f"\nBob nhận {len(photons)} photons từ Alice qua QUANTUM CHANNEL")
        #print(f"\nPhotons Bob nhận được: {self.photons}")
    
    def create_bases(self):
        """Tạo cơ sở ngẫu nhiên cho mỗi photon nhận được"""
        length = len(self.photons)
        self.bases = quantum_utils.generate_random_bases(length)
        #print(f"\nCơ sở của Bob được tạo: {self.bases}")
    
    def measure_photons(self,alice_bases_ao):
        """Đo các photon dựa trên cơ sở của Bob và lưu kết quả"""
        self.alice_bases = alice_bases_ao
        self.measure_photon = []
        for photon, bob_basis in zip(self.photons, self.bases):
            # Nếu cơ sở của Bob khác với cơ sở của Alice, đo ngẫu nhiên
            if bob_basis != self.alice_bases[len(self.measure_photon)]:
                measured_bit = quantum_utils.generate_random_bits(1)[0]
            else:
                measured_bit = photon  # Giả sử đo đúng
            self.measure_photon.append(measured_bit)
        #print(f"\nPhoton Bob đo được: {self.measure_photon}")

    def generate_raw_key(self, alice_bases):
        """Tạo khóa thô dựa trên cơ sở của Alice và Bob"""
        self.raw_key = []
        for i in range(len(self.measure_photon)):
            if self.bases[i] == alice_bases[i]:
                self.raw_key.append(self.measure_photon[i])
        #print(f"\nKhóa thô của Bob: {self.raw_key}")
        
    def check_error_rate(self, public_key_str, selected_positions):
        """So sánh phần khóa chung nhận từ Alice để kiểm tra lỗi"""
        mismatches = 0
        for i, position in enumerate(selected_positions):
            if i < len(public_key_str) and position < len(self.raw_key):
                if int(public_key_str[i]) != self.raw_key[position]:
                    mismatches += 1
        self.error_rate = mismatches / len(selected_positions) if len(selected_positions) > 0 else 0
        self.public_key_positions = set(selected_positions)  # Lưu vị trí để generate_secret_key
        #print(f"\nSố bit không khớp: {mismatches} trên tổng số {len(selected_positions)} bit được so sánh.")
    
    def generate_secret_key(self):
        """Tạo khóa bí mật cuối cùng bằng cách loại bỏ các bit đã dùng để kiểm tra lỗi"""
        for i in range(len(self.raw_key)):
            if i not in self.public_key_positions:
                self.secret_key.append(self.raw_key[i])
        #print(f"\nKhóa bí mật cuối cùng của Bob: {self.secret_key}")
    
    

        