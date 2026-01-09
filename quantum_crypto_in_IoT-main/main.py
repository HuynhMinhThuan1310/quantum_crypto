from alice import Alice
from bob import Bob
from eve import Eve
from read_IoT_sensor import read_sensor_input
import aes_utils



def main():

    alice = Alice()
    bob = Bob()
    eve = Eve()

    #Đọc dữ liệu từ cảm biến IoT
    sensor_data = read_sensor_input()
    
    if sensor_data is None:
        print("Không thể đọc dữ liệu sensor!")
        return
    
    temperature = sensor_data['temperature']
    humidity = sensor_data['humidity']
    dust = sensor_data['dust']
    smoke = sensor_data['smoke']
    kiem_tra = sensor_data['eve_check']



    #Phần 1: Tạo khóa raw_key bằng giao thức BB84

    alice.receive_and_encode_data(temperature, humidity, dust, smoke)
    sending_data = alice.sending_data

    alice.generate_qubits(sending_data)
    alice.create_bases()
    alice.generate_photons()

    sending_photons = alice.photons
    alice_bases_ao = alice.bases

    if kiem_tra:
        eve.intercept_photons(sending_photons)
        eve.create_bases()
        sending_photons = eve.resend_photons(alice_bases_ao)
        print("\nEve đã can thiệp vào kênh truyền!")
    
    bob.receive_photons(sending_photons)
    bob.create_bases()
    bob.measure_photons(alice_bases_ao)

    alice.generate_raw_key(bob.bases)  # Bob gửi cơ sở của mình cho Alice
    bob.generate_raw_key(alice.bases)  # Alice gửi cơ sở của mình cho Bob
    alice.generate_public_key()
    bob.public_key = alice.public_key  # Bob nhận public_key từ Alice
    bob.check_error_rate(alice.public_key, alice.selected_positions)  # Bob cần biết vị trí
    alice.generate_secret_key()
    bob.generate_secret_key()

    alice_secret_key_str = ''.join(map(str, alice.secret_key))
    bob_secret_key_str = ''.join(map(str, bob.secret_key))
    alice_public_key_str = ''.join(map(str, alice.public_key))
    bob_public_key_str = ''.join(map(str, bob.public_key))
    alice_raw_key_str = ''.join(map(str, alice.raw_key))
    bob_raw_key_str = ''.join(map(str, bob.raw_key))
    alice_bases_str = ''.join(map(str, alice.bases))
    bob_bases_str = ''.join(map(str, bob.bases))
    alice_photons_str = ''.join(map(str, alice.photons))
    bob_photons_str = ''.join(map(str, bob.measure_photon))

    print(f"\n--- Kết quả QKD ---")
    print(f"\nPhotons của Alice gửi đi: {alice_photons_str}")
    print(f"\nPhotons của Bob đo được: {bob_photons_str}")
    print(f"\nCơ sở của Alice: {alice_bases_str}")
    print(f"\nCơ sở của Bob: {bob_bases_str}")
    print(f"\nKhóa thô của Alice: {alice_raw_key_str}")
    print(f"\nKhóa thô của Bob: {bob_raw_key_str}")
    print(f"\nKhóa công khai của Alice: {alice_public_key_str}")
    print(f"\nKhóa công khai của Bob: {bob_public_key_str}")
    print(f"\nTỷ lệ lỗi giữa Alice và Bob: {bob.error_rate*100:.2f}%")
    print(f"\nKhóa bí mật cuối cùng của Alice: {alice_secret_key_str}")
    print(f"\nKhóa bí mật cuối cùng của Bob: {bob_secret_key_str}")
    print("-------------------")



    #Phần 2: Mã hóa dữ liệu sensor bằng AES với khóa từ QKD
    key_bytes = aes_utils.pad_key(alice_secret_key_str)
    data_bytes = aes_utils.prepare_data_bytes(temperature, humidity, dust, smoke)
    print(f"\nKhóa bí mật chuẩn bị để mã hóa (secret key): {key_bytes.hex()}")
    print(f"\nDữ liệu sensor chuẩn bị để mã hóa (plaintext): {data_bytes.hex()}")

    # Mã hóa bằng AES chuẩn
    ciphertext = aes_utils.encrypt_aes(data_bytes, key_bytes)
    print(f"\nDữ liệu sensor sau khi mã hóa (ciphertext hex): {ciphertext.hex()}")
    aes_utils.save_ciphertext(ciphertext.hex())
    aes_utils.save_secret_key(bob_secret_key_str)



    #Phần 3: Giải mã dữ liệu sensor bằng AES với khóa từ QKD
    # Giả sử Bob nhận được ciphertext và sử dụng khóa bí mật của mình để giải
    key_bytes_bob = aes_utils.pad_key(bob_secret_key_str)
    
    # Giải mã bằng AES chuẩn
    decrypted_data_bytes = aes_utils.decrypt_aes(ciphertext, key_bytes_bob)
    print(f"\nDữ liệu sensor sau khi giải mã (plaintext): {decrypted_data_bytes.hex()}")
    
    # So sánh dữ liệu
    print(f"\n--- So sánh dữ liệu ---")
    print(f"Dữ liệu trước AES:  {data_bytes.hex()}")
    print(f"Dữ liệu sau AES: {decrypted_data_bytes.hex()}")
    print(f"Giống nhau:   {data_bytes.hex() == decrypted_data_bytes.hex()}")
    
    # In dữ liệu dạng nhị phân để so sánh với sending_data
    receiving_data = aes_utils.bytes_to_bits(decrypted_data_bytes)
    print(f"\n--- So sánh dữ liệu nhị phân ---")
    print(f"Sending data  (128 bits): {sending_data}")
    print(f"Receiving data (128 bits): {receiving_data}")
    print(f"Nhị phân giống nhau: {sending_data == receiving_data}")

    
    # Giải mã dữ liệu sensor từ bytes thành dữ liệu thô
    decrypted_sensor_data = aes_utils.decode_sensor_data(decrypted_data_bytes)
    if decrypted_sensor_data:
        print(f"\n Dữ liệu sensor sau khi giải mã:")
        print(f"  - Temperature: {decrypted_sensor_data['temperature']}°C")
        print(f"  - Humidity: {decrypted_sensor_data['humidity']}%")
        print(f"  - Dust: {decrypted_sensor_data['dust']} µg/m³")
        print(f"  - Smoke: {decrypted_sensor_data['smoke']} ppm")


if __name__ == "__main__":
    main()