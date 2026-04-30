import csv
import sys
import os
import flet as ft

# ========================
# 1. SETUP & DATA LOADING
# ========================
colors_map = {
    "Alkali Metal": "#FF9999", "Alkaline Earth": "#FFCC99",
    "Transition Metal": "#CCCCFF", "Post-Transition": "#4DBAB5",
    "Metalloid": "#99FFCC", "Halogen": "#FF99FF",
    "Noble Gas": "#99CCFF", "Lanthanide": "#FFD700",
    "Actinide": "#FFB6C1", "Nonmetal": "#CCFFCC", "Other": "#E0E0E0"
}

def resource_path(relative_path):
    try: base_path = sys._MEIPASS
    except Exception: base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

elements = {}
csv_path = resource_path("periodic_table.csv")

# DEBUG: Check if file exists
if not os.path.exists(csv_path):
    print(f"CRITICAL ERROR: File not found at {csv_path}")
else:
    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            raw_cat = row.get("Category", "Other").strip().title()
            row["Category"] = raw_cat
            num = int(row["AtomicNumber"])
            elements[num] = row

# ========================
# 2. POSITIONING LOGIC
# ========================
positions = {}
positions[1], positions[2] = (0, 0), (0, 17)
cols_p2_p3 = [0, 1, 12, 13, 14, 15, 16, 17]
for row, start in zip([1, 2], [3, 11]):
    for i, num in enumerate(range(start, start + 8)):
        positions[num] = (row, cols_p2_p3[i])
for row, start in zip([3, 4], [19, 37]):
    for col in range(18): positions[start + col] = (row, col)
positions[55], positions[56], positions[5700] = (5, 0), (5, 1), (5, 2)
for i, num in enumerate(range(72, 87)): positions[num] = (5, 3 + i)
positions[87], positions[88], positions[8900] = (6, 0), (6, 1), (6, 2)
for i, num in enumerate(range(104, 119)): positions[num] = (6, 3 + i)
for i, num in enumerate(range(57, 72)): positions[num] = (8, 2 + i)
for i, num in enumerate(range(89, 104)): positions[num] = (9, 2 + i)
for i, num in enumerate(range(57, 72)):
    positions[num] = (8, 2 + i)
# Actinides (89-103) - Row 9
# Ensure this is exactly as written
for i, num in enumerate(range(89, 104)):
    positions[num] = (9, 2 + i)

# ========================
# 3. THE FLET APP
# ========================
def main(page: ft.Page):
    page.title = "Periodic Table"
    page.bgcolor = "#111111"
    
    # 1. Detail Panel (Shows all 6 things)
    # We use a larger height here so the text doesn't overlap the table
    detail_text = ft.Text("Click an element to see details", size=16, color="white", weight="bold")
    detail_container = ft.Container(
        content=detail_text, 
        padding=20, 
        bgcolor="#333333", 
        border_radius=10,
        margin=10
    )

    def show_details(e, num):
        if not num: return
        el = elements.get(num)
        if el:
            # 1. Name/Symbol, 2. Number, 3. Mass, 4. Category, 5. Config, 6. Category (redundant check)
            detail_text.value = (
                f"1. {el['Name']} ({el['Symbol']}) | 2. Atomic #: {el['AtomicNumber']}\n"
                f"3. Mass: {el['AtomicMass']} | 4. Category: {el['Category']}\n"
                f"5. Electron Configuration: {el['ElectronConfiguration']}"
            )
            page.update()


    # 2. INCREASE THE STACK HEIGHT
    # 10 rows * 70px = 700px. We use 800px to be safe.
    table_stack = ft.Stack(width=1250, height=800)

    for num, (row, col) in positions.items():
        if num == 5700:
            txt, color, target = "57-71", colors_map["Lanthanide"], None
        elif num == 8900:
            txt, color, target = "89-103", colors_map["Actinide"], None
        elif num in elements:
            el = elements[num]
            txt, color, target = f"{num}\n{el['Symbol']}", colors_map.get(el["Category"], "white"), num
        else:
            continue

        # Using NO alignment attribute to prevent the crash
        table_stack.controls.append(
            ft.Container(
                content=ft.Text(txt, size=10, weight="bold", color="black", text_align="center"),
                bgcolor=color,
                width=60,
                height=60,
                border_radius=5,
                padding=5, # Centers the text roughly without using 'alignment'
                left=col * 65,
                top=row * 65,
                on_click=lambda e, n=target: show_details(e, n)
            )
        )


    # 3. THE SCROLLING FIX
    # We put the table in a Row (Horizontal Scroll) 
    # then put that Row in a Column (Vertical Scroll)
    page.add(
        detail_container,
        ft.Column(
            [
                ft.Row(
                    [table_stack], 
                    scroll=ft.ScrollMode.ALWAYS
                )
            ],
            scroll=ft.ScrollMode.ALWAYS,
            expand=True
        )
    )
    page.update()

ft.run(main)
