import time
import random

from parser import RdoParser
from excel_controller import ExcelController


def save_current_row(row):
    with open("current_row.txt", "w") as f:
        f.write(str(row))

def get_current_row():
    with open("current_row.txt") as f:
        return int(f.read())


def main():
    parser: RdoParser = RdoParser()

    excelController = ExcelController("RDO.xlsx", get_current_row())
    max_row = excelController.max_row

    while excelController.row <= max_row:
        art = str(excelController.sheet[f"A{excelController.row}"].value).replace(",", "")
        print(excelController.row, art)

        link = parser.get_part_link(art)
        if(not link):
            excelController.row += 1
            continue

        data = parser.get_page_data(link, art)

        excelController.sheet[f"B{excelController.row}"] = data["models"] or ""
        excelController.sheet[f"C{excelController.row}"] = "" if data["img"] else "Пусто"

        excelController.save_document()

        save_current_row(excelController.row)

        excelController.row += 1

    # excelController.sheet["C5"] = "Пусто"
    # for i in range(619, 1578):
    #     img_link = excelController.sheet[f"C{i}"].value
    #     if(img_link != "Пусто"): continue

    #     art = str(excelController.sheet[f"A{i}"].value).replace(",", "")
    #     print(i, art)

    #     link = parser.get_part_link(art)
    #     if(not link):
    #         continue

    #     data = parser.get_page_data(link, art)

    #     excelController.sheet[f"B{i}"] = data["models"] or ""
    #     excelController.sheet[f"C{i}"] = "" if data["img"] else "Пусто"

    #     excelController.save_document()

if __name__ == "__main__":
    main()