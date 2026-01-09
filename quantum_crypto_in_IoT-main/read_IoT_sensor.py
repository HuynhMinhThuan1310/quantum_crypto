#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Config module - Cấu hình đọc dữ liệu sensor từ file
"""

import json

def read_sensor_input():
    """
    Đọc dữ liệu từ file sensor_input.txt
    
    File input có định dạng JSON:
    {
        "temperature": float,
        "humidity": float,
        "dust": float,
        "smoke": float,
        "eve_check": boolean (True nếu có Eve chặn)
    }
    
    Returns:
        dict: Dữ liệu sensor hoặc None nếu có lỗi
    """
    try:
        with open('sensor_input.txt', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Kiểm tra các key cần thiết
        required_keys = ['temperature', 'humidity', 'dust', 'smoke', 'eve_check']
        for key in required_keys:
            if key not in data:
                print(f"Lỗi: Thiếu key '{key}' trong file sensor_input.txt")
                return None
        
        return data
    
    except FileNotFoundError:
        print("Lỗi: Không tìm thấy file 'sensor_input.txt'")
        return None
    except json.JSONDecodeError:
        print("Lỗi: File 'sensor_input.txt' không phải định dạng JSON hợp lệ")
        return None
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
        return None
