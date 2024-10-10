from Customer import Customer

customer = Customer("John", "Doe", "123 Main St.", "12345", "New York")
print(customer) # Output: John Doe - 123 Main St., 12345 New York
print(customer.get_first_name()) # Output: John
customer.set_first_name("Jane")
print(customer) # Output: Jane Doe - 123 Main St., 12345 New York

customer.set_first_name("") # Raises ValueError: First Name cannot be empty.