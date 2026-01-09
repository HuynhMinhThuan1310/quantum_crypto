import quantum_utils

class Eve:
    def __init__(self):
        self.photons = []
        self.bases = []
        self.send_photons = []
        print("Eve được khởi tạo!")

    def intercept_photons(self, photons):
        """Eve chặn các photon truyền từ Alice đến Bob"""
        self.photons = photons
        print(f"\nEve chặn {len(photons)} photons từ Alice.")

    def create_bases(self):
        """Tạo cơ sở ngẫu nhiên cho mỗi photon chặn được"""
        self.bases = quantum_utils.generate_random_bases(len(self.photons))
        #print(f"\nCơ sở của Eve được tạo: {self.bases}")
    
    def resend_photons(self, alice_bases_ao):
        for i in range(len(self.photons)):
            # Nếu cơ sở của Eve khác với cơ sở của Alice, đo ngẫu nhiên
            if self.bases[i] != alice_bases_ao[i]:
                self.send_photons.append(quantum_utils.generate_random_bits(1)[0])
            else:
                self.send_photons.append(self.photons[i])  # Giả sử đo đúng
        return self.send_photons