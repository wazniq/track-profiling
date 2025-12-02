import re
import sys

def extract_strings(filename, min_len=4):
    with open(filename, errors='ignore') as f:
        # Read as binary to avoid encoding issues, then decode what we can
        try:
            with open(filename, 'rb') as f:
                content = f.read()
                # Find sequences of printable characters
                # 32-126 are standard printable ASCII
                regex = b"[\x20-\x7E]{" + str(min_len).encode() + b",}"
                matches = re.findall(regex, content)
                
                print(f"Strings found in {filename}:")
                for match in matches[:50]: # Print first 50 matches
                    print(match.decode('ascii'))
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    extract_strings(r'C:\Users\Athuv\.gemini\antigravity\scratch\legacy_app\TS\TSMANUAL.DOC')
