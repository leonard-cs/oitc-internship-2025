from enum import Enum

from pydantic import BaseModel, Field


class Table(str, Enum):
    products = "Products"
    employees = "Employees"
    categories = "Categories"
    customers = "Customers"
    employee_territories = "EmployeeTerritories"
    order_details = "Order Details"
    orders = "Orders"
    region = "Region"
    shippers = "Shippers"
    suppliers = "Suppliers"
    territories = "Territories"

    @property
    def sql(self) -> str:
        if self == Table.employees:
            return """
                SELECT
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
            return """
                SELECT
                    CategoryID,
                    CategoryName,
                    Description
                FROM [{self.value}]
            """
        else:
            return f"SELECT TOP 50 * FROM [{self.value}]"


class LLMDocumentResponse(BaseModel):
    id: int | str = Field(
        ...,
        description="The id column of the row plus the table name, e.g., 'Product_1', 'Order_5', 'Employee_10'",
    )
    text: str = Field(..., description="Generated text describing the row")
    # reason: str = Field(..., description="Reason for the generated text")
