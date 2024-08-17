class InvalidPriceError(Exception):
    pass
class InvalidQuantityError(Exception):
    pass
class LoggingMixin:
    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if callable(attr):
            def wrap(*args,**kwargs):
                print(f"Calling method {name} with params {args,kwargs}")
                result = attr(*args,**kwargs)
                return result
            return wrap
        return attr

class Product:
    def __init__(self, name, price, description):
        try:
            if price <= 0:
                raise InvalidPriceError
            self.name = name
            self.price = price
            self.description = description
        except InvalidPriceError:
            print('Invalid price. EVERYTHING will crash now!!!')

    def str(self):
        return f'{self.name} - ${self.price} UAH'


class Discount:
    def apply(self, price):
        pass


class PercentageDiscount(Discount):
    def __init__(self, percentage: float | int = 0.1):
        if 0 <= percentage <= 1:
            self.percentage = percentage
        else:
            self.percentage = 0

    def apply(self, price: float | int):
        return price * (1 - self.percentage)


class FixedAmountDiscount(Discount):
    def __init__(self, amount: float | int = 0):
        if amount < 0:
            amount = 0
        self.amount = amount

    def apply(self, price: float | int):
        if price < self.amount:
            return 0
        return price - self.amount


class DiscountMixin:
    def apply_discount(self, discount: Discount):
        if hasattr(self, 'products'):
            for product in self.products:
                product.price = discount.apply(product.price)

class PaymentProcessor:
    def pay(self, amount):
        pass


class CreditCardProcessor(PaymentProcessor):
    def __init__(self, card_number, card_holder, cvv, expiry_date):
        self.card_number = card_number
        self.card_holder = card_holder
        self.cvv = cvv
        self.expiry_date = expiry_date

    def pay(self, amount):
        print(f'Paying ${amount} with credit card {self.card_number}')


class PayPalProcessor(PaymentProcessor):
    def __init__(self, email):
        self.email = email

    def pay(self, amount):
        print(f'Paying ${amount} with PayPal account {self.email}')


class BankTransferProcessor(PaymentProcessor):
    def __init__(self, account_number, account_holder):
        self.account_number = account_number
class Cart(DiscountMixin,LoggingMixin):
    def __init__(self):
        self.products = {}

    def add_product(self, product, quantity):
        try:
            if quantity <= 0:
                raise(InvalidQuantityError)
            self.products[product] = self.products.get(product, 0) + quantity
        except:
            print('Invalid quantity of the product. The script will crash now')
    def total_cost(self):
        return sum(product.price * quantity for product, quantity in self.products.items())

    def pay(self, paymentprocessor: PaymentProcessor):
        paymentprocessor.pay(self.total_cost())

    def __str__(self):
        return '\n'.join(f'{product} x {quantity} = {product.price * quantity} UAH'for product, quantity in self.products.items())


def main():
    product1 = Product('Ball', 110.00,"round")
    product2 = Product('Cube', 1000, "edgy")
    product3 = Product("Pyramid", 100.00, "spiky")

    # Creating an instance of the Cart class and adding products
    cart = Cart()
    cart.add_product(product1, 1)
    cart.add_product(product2, 2)
    cart.add_product(product3, 1)

    print(cart)
    print("Total cost:", cart.total_cost())

    # Applying different types of discounts
    percentage_discount = PercentageDiscount(0)
    fixed_amount_discount = FixedAmountDiscount(0)

    cart.apply_discount(percentage_discount)
    print(cart)
    print("Total cost after percentage discount:", cart.total_cost())

    cart.apply_discount(fixed_amount_discount)
    print(cart)
    print("Total cost after fixed amount discount:", cart.total_cost())

    credit_card_processor = CreditCardProcessor("1234-5678-9876-5432", "John Doe", "123", "12/25")
    paypal_processor = PayPalProcessor("john.doe@example.com")
    bank_transfer_processor = BankTransferProcessor("987654321", "John Doe")

    cart.pay(credit_card_processor)
    cart.pay(paypal_processor)
    cart.pay(bank_transfer_processor)

if __name__ == "__main__":
    main()