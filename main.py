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
    _instances = []

    def __init__(self, name, price, description):
        try:
            if price <= 0:
                raise InvalidPriceError
            self.name = name
            self.price = price
            self.description = description
            Product._instances.append(self)
        except InvalidPriceError:
            print('Invalid price. EVERYTHING will crash now!!!')

    @classmethod
    def get_product_by_name(cls, name):
        for instance in cls._instances:
            if instance.name.lower() == name.lower():
                return instance
        return None
    @classmethod
    def print_all_instances(cls):
        # Iterate over all instances and format their attributes
        instance_strs = []
        for instance in cls._instances:
            instance_str = f"'{instance.name}' Price: {instance.price}UAH '{instance.description}'"
            instance_strs.append(instance_str)
        return "\n".join(instance_strs)

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


class Cart(DiscountMixin):
    def __init__(self):
        self.products = {}

    def add_product(self, product_name, quantity):
        product = Product.get_product_by_name(product_name)
        try:
            if quantity <= 0:
                raise InvalidQuantityError
            self.products[product] = self.products.get(product, 0) + quantity
        except:
            print('Invalid quantity of the product. The script will crash now')

    @staticmethod
    def get_cart_instance(cart_name, cart1, cart2, merged_cart):
        if cart_name.lower() == 'cart1':
            return cart1
        elif cart_name.lower() == 'cart2':
            return cart2
        elif cart_name.lower() == 'mergedcart':
            return merged_cart
        else:
            print("Invalid cart name")
            return None

    def merge(self,cart1,cart2):
        self.products = {key: cart1.products.get(key,0)+cart2.products.get(key,0) for key in set(cart1.products)|set(cart2.products)}
    def total_cost(self):
        return sum(product.price * quantity for product, quantity in self.products.items())

    def pay(self, paymentprocessor: PaymentProcessor):
        paymentprocessor.pay(self.total_cost())

    def __str__(self):
        return '\n'.join(f'{product.name} x {quantity} = {product.price * quantity} UAH'for product, quantity in self.products.items())


def main():
    ball = Product('Ball', 110.00,"round")
    cube = Product('Cube', 1000, "edgy")
    pyramid = Product("Pyramid", 100.00, "spiky")

    # Creating an instance of the Cart class and adding products
    cinstance1 = Cart()
    cinstance2 = Cart()
    merged_cart = Cart()
    print(Product.print_all_instances())
    while True:
        cart_name = input('Enter the cart name (Cart1, Cart2, or MergedCart): ').strip()
        operator = input('Enter the operator (+ for add, += for merge): ').strip()
        selected_cart = Cart.get_cart_instance(cart_name, cinstance1, cinstance2, merged_cart)
        if not selected_cart:
            continue
        if operator == '+':
            product_name = input('Enter the product name to add: ').strip()
            quantity = int(input('Enter the quantity: ').strip())
            selected_cart.add_product(product_name, quantity)
        elif operator == '+=':
            cart_to_merge_name = input('Enter the name of the cart to merge with: ').strip()
            cart_to_merge = Cart.get_cart_instance(cart_to_merge_name, cinstance1, cinstance2, merged_cart)
            if cart_to_merge:
                merged_cart.merge(selected_cart, cart_to_merge)



    # Applying different types of discounts
    percentage_discount = PercentageDiscount(0)
    fixed_amount_discount = FixedAmountDiscount(0)

    cinstance1.apply_discount(percentage_discount)
    print(cinstance1)
    print("Total cost after percentage discount:", cinstance1.total_cost())

    cinstance1.apply_discount(fixed_amount_discount)
    print(cinstance1)
    print("Total cost after fixed amount discount:", cinstance1.total_cost())


main()
