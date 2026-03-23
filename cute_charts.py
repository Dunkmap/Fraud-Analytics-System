import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace continuous scales
content = content.replace("'Reds'", "'Pinkyl'")

# Replace discrete maps
content = content.replace("{0: '#00cc00', 1: '#ff4b4b'}", "{0: '#A1E3B5', 1: '#FF9E9E'}")

# Replace Pie chart colors (Line 572 area)
content = content.replace("['#ff4b4b', '#ffa500', '#00cc00']", "['#FF9E9E', '#FFE5A3', '#A1E3B5']")

# Replace specific scatter line color
content = content.replace("color='#ff4b4b'", "color='#FF7482'")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Plotly charts successfully updated to Pastel Cute theme!")
