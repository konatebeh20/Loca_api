import binascii
import struct
from datetime import datetime

def decode_gt06(data):
    """Decodes GT06 protocol data into readable fields."""
    if data.startswith(b'\x78\x78'):
        data = data[2:-2]  # Remove start (0x78 0x78) and end (0x0D 0x0A) bytes

    packet_length = data[0]
    protocol_number = data[1]

    if protocol_number == 0x12:  # GPS Data Packet
        timestamp = decode_timestamp(data[2:8])
        latitude = decode_latitude(data[8:12])
        longitude = decode_longitude(data[12:16])
        speed = data[16]  # Speed in km/h
        direction = struct.unpack('>H', data[17:19])[0]  # Big-endian unsigned short

        return {
            "timestamp": timestamp,
            "latitude": latitude,
            "longitude": longitude,
            "speed": speed,
            "direction": direction
        }
    else:
        raise ValueError("Unsupported protocol number")

def decode_timestamp(timestamp_bytes):
    year = 2000 + timestamp_bytes[0]
    month, day = timestamp_bytes[1], timestamp_bytes[2]
    hour, minute, second = timestamp_bytes[3], timestamp_bytes[4], timestamp_bytes[5]
    return datetime(year, month, day, hour, minute, second).isoformat()

def decode_latitude(latitude_bytes):
    raw_lat = struct.unpack('>I', latitude_bytes)[0]
    return raw_lat / 30000 / 60  # Convert to decimal degrees

def decode_longitude(longitude_bytes):
    raw_lon = struct.unpack('>I', longitude_bytes)[0]
    return raw_lon / 30000 / 60  # Convert to decimal degrees
