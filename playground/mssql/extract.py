from employees import (
    export_employee_photo_s,
    export_employee_sentence_s,
    export_employees_csv,
    export_employees_sentences,
)

from products import (
    export_product_sentence_s,
    export_products_csv,
    export_products_sentences,
)
from utils import extract_table


if __name__ == "__main__":
    table = "Products"
    table_df = extract_table(table)
    export_products_csv(table, table_df)
    export_products_sentences(table, table_df)
    export_product_sentence_s(table, table_df)

    table = "Employees"
    table_df = extract_table(table)
    export_employees_csv(table, table_df)
    export_employees_sentences(table, table_df)
    export_employee_sentence_s(table, table_df)
    export_employee_photo_s(table)
