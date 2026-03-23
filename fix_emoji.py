import re

filepath = r'd:\End-to-End Credit Card Fraud Analytics & Risk Intelligence System\app.py'

with open(filepath, 'rb') as f:
    raw = f.read()

# Find and replace the words array line containing surrogate
old = b"const words = ["
idx = raw.find(old)
if idx != -1:
    end_idx = raw.find(b"];", idx)
    if end_idx != -1:
        old_line = raw[idx:end_idx+2]
        new_line = b"const words = [String.fromCodePoint(0x1F338), 'Credit', 'Card', 'Fraud', 'Analytics'];"
        raw = raw[:idx] + new_line + raw[end_idx+2:]
        print(f"Replaced successfully")
    else:
        print("Could not find end of line")
else:
    print("Could not find target line")

with open(filepath, 'wb') as f:
    f.write(raw)

print("Fix applied!")
