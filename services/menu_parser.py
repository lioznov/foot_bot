from docx import Document
import re

def parse_docx_menu(file_path: str) -> list[tuple[str,float]]:
    doc = Document(file_path)
    menu_items = []

    for table in doc.tables:
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            if len(cells) >= 2:
                dish_name = cells[0]
                price_text = cells[1]
                if "наименование" in dish_name.lower() or "блюдо" in dish_name.lower():
                    continue
                price_digits = re.findall(r'\d+', price_text)
                if dish_name and price_digits:
                    price = float(price_digits[0])
                    menu_items.append((dish_name, price))
    return menu_items