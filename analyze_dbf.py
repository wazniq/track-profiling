import struct
import os
import glob

def parse_dbf_header(filepath):
    try:
        with open(filepath, 'rb') as f:
            # Read the first 32 bytes
            header_data = f.read(32)
            if len(header_data) < 32:
                return "Invalid DBF file"
            
            version = header_data[0]
            num_records = struct.unpack('<I', header_data[4:8])[0]
            header_length = struct.unpack('<H', header_data[8:10])[0]
            record_length = struct.unpack('<H', header_data[10:12])[0]
            
            print(f"File: {os.path.basename(filepath)}")
            print(f"  Version: {hex(version)}")
            print(f"  Records: {num_records}")
            print(f"  Header Length: {header_length}")
            print(f"  Record Length: {record_length}")
            print("  Fields:")
            
            # Read field descriptors
            f.seek(32)
            while f.tell() < header_length - 1:
                field_data = f.read(32)
                if len(field_data) < 32:
                    break
                
                if field_data[0] == 0x0D: # End of header marker
                    break
                
                name = field_data[:11].decode('ascii', errors='ignore').strip('\x00')
                field_type = chr(field_data[11])
                length = field_data[16]
                decimal_count = field_data[17]
                
                print(f"    {name} ({field_type}, {length}.{decimal_count})")
            print("-" * 20)
            
    except Exception as e:
        print(f"Error reading {filepath}: {e}")

def main():
    dbf_files = glob.glob(r'C:\Users\Athuv\.gemini\antigravity\scratch\legacy_app\TS\*.DBF')
    for dbf_file in dbf_files:
        parse_dbf_header(dbf_file)

if __name__ == "__main__":
    main()
