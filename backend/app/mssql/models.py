from enum import Enum

from pydantic import BaseModel, Field


class Table(str, Enum):
    products = "Products"
    customers = "Customers"
    employee_territories = "EmployeeTerritories"
    order_details = "Order Details"
    orders = "Orders"
    region = "Region"
    shippers = "Shippers"
    suppliers = "Suppliers"
    territories = "Territories"

    def sql(self, limit: int | None = None) -> str:
        limit_str = f"TOP {limit}" if limit else ""
        return f"SELECT {limit_str} * FROM [{self.value}]"


class ImageTable(str, Enum):
    employees = "Employees"
    categories = "Categories"

    def sql_text(self, limit: int | None = None) -> str:
        limit_str = f"TOP {limit}" if limit else ""
        if self == Table.employees:
            return f"""
                SELECT {limit_str}
                    EmployeeID,
                    LastName,
                    FirstName,
                    Title,
                    TitleOfCourtesy,
                    BirthDate,
                    HireDate,
                    Address,
                    City,
                    Region,
                    PostalCode,
                    Country,
                    HomePhone,
                    Extension
                FROM [{self.value}]
            """
        elif self == Table.categories:
            return f"""
                SELECT {limit_str}
                    CategoryID,
                    CategoryName,
                    Description
                FROM [{self.value}]
            """
        else:
            raise ValueError(f"Invalid image table: {self.value}")

    def sql_image(self, limit: int | None = None) -> str:
        limit_str = f"TOP {limit}" if limit else ""
        if self == ImageTable.employees:
            return f"SELECT {limit_str} EmployeeID, Photo FROM [{self.value}]"
        elif self == ImageTable.categories:
            return f"SELECT {limit_str} CategoryID, Picture FROM [{self.value}]"
        else:
            raise ValueError(f"Invalid image table: {self.value}")


class LLMDocumentResponse(BaseModel):
    id: int | str = Field(
        ...,
        description="The id column of the row plus the table name, e.g., 'Product_1', 'Order_5', 'Employee_10'",
    )
    text: str = Field(..., description="Generated text describing the row")
    # reason: str = Field(..., description="Reason for the generated text")
