"""
Ниже — код сервиса обработки заказов интернет-магазина.
Он рабочий (в смысле — запускается и в целом делает своё дело), но давно не рефакторился: нет тестов,
 сложно тестируется из-за прямых вызовов внешних сервисов внутри бизнес-логики,
 слабая валидация, и — есть подозрение — где-то прячется логическая ошибка.

Что нужно сделать, по приоритету (если не успеете всё — лучше сделать первые пункты хорошо, чем все наспех):

1. Отрефакторить код так, чтобы его можно было протестировать без реальных вызовов отправки email и списания денег
 (подход на ваш выбор — dependency injection, моки, что угодно).
2. Написать unit-тесты (pytest), покрывающие как минимум:
успешный заказ,
 невалидный промокод,
  просроченный промокод,
   неуспешную оплату,
    невалидные входные данные (пустой список товаров, отрицательное количество товара).
3. В процессе, скорее всего, найдётся логический баг — исправить его.

4.(если останется время)
Добавить фичу: бесплатная доставка при сумме заказа (после применения скидки) от 3000 рублей и выше —
 отразить в возвращаемом результате и в тексте письма-подтверждения.
"""

from __future__ import annotations
import enum
import typing

"""
Сервис обработки заказов интернет-магазина.
"""

import datetime
from dataclasses import dataclass

def log(level, msg):
    print(f'{level}: {msg}')

class DiscountError(Exception):
    pass

class DiscountNotExist(DiscountError):
    def __init__(self, code):
        self._code = code

    def __str__(self):
        return f'Discount with {self._code} does not exist'

class DiscountIsExpired(DiscountError):
    def __init__(self, code, expires, now):
        self._code = code
        self._expires = expires
        self._now = now

    def __str__(self):
        return f'Discount with {self._code} expires {self._expires}, try to apply at {self._now}'

class PaymentNotCorrect(Exception):
    def __init__(self, payment_result: PaymentResult):
        self._payment_result = payment_result

    def __str__(self):
        return f'Payment with transaction_id {self._payment_result.transaction_id} has error'

@dataclass
class Discount:
    percent: int
    expires: datetime
    code: str

@dataclass
class OrderItem:
    name: str
    price: int
    qty: int

@dataclass
class Order:
    user: User
    items: typing.List[OrderItem]
    total: int
    transaction_id: str

@dataclass
class User:
    email: str
    card_number: str

@dataclass
class PaymentResult:
    status: str
    transaction_id: str

class PaymentStatus(enum.StrEnum):
    SUCCESS='success'
    ERROR='error'

class PaymentService:
    def charge_payment(self, card_number, amount) -> PaymentResult:
        # представим, что здесь вызов внешнего платёжного шлюза
        print(f"Charging {amount} from card {card_number}")
        return PaymentResult('success', 'tx_12345')


class EmailService:
    def send_email(self, to, subject, body):
        # представим, что здесь реальная отправка через SMTP/почтового провайдера
        print(f"EMAIL to {to}: {subject}\n{body}")


class DiscountRepository:
    def __init__(self):
        self._discounts = {}

    def init_discounts(self):
        self.add_discount(Discount(10, datetime.datetime(2026, 12, 31), code='SALE10'))
        self.add_discount(Discount(50, datetime.datetime(2025, 2025, 2025), code='SALE50'))
        self.add_discount(Discount(20, datetime.datetime(2030, 1, 1), code='VIP'))

    def add_discount(self, discount: Discount):
        self._discounts[discount.code] = discount

    def get_discount_by_code(self, code: str, now: datetime.datetime):
        try:
            _discount = self._discounts[code]
        except KeyError:
            raise DiscountNotExist(code)
        if now > _discount.expires:
            raise DiscountIsExpired(code, _discount.expires, now)
        return _discount

    def get_all_discounts(self):
        return [x for x in self._discounts.values()]

class OrderRepository:
    def __init__(self):
        self._orders = []
    def add_order(self, order: Order):
        self._orders.append(order)

class OrderService:
    def __init__(
            self,
            discount_repo: DiscountRepository,
            order_repo: OrderRepository,
            payment_service: PaymentService,
            email_service: EmailService
    ):
        self._discount_repo = discount_repo
        self._discount_repo.init_discounts()

        self._order_repo = order_repo
        self._payment_service = payment_service
        self._email_service = email_service

    def process_order(
            self,
            user: User,
            items: typing.List[OrderItem],
            date:datetime.datetime,
            discount_code = None
    ):
        total = 0
        for item in items:
            total+= item.price*item.qty
        if discount_code:
            total = self._calculate_discount(total, discount_code, date)
        payment_result = self._payment_service.charge_payment(user.card_number, total)
        if payment_result.status == PaymentStatus.ERROR:
            raise PaymentNotCorrect(payment_result)
        self._order_repo.add_order(Order(user, items, total, payment_result.transaction_id))
        self._email_service.send_email(user.email,
        "Ваш заказ оформлен",
        f"Сумма к оплате: {total} руб.")
        return total


    def _calculate_discount(self, total: int, discount_code: str, date: datetime.datetime):
        try:
            _discount = self._discount_repo.get_discount_by_code(discount_code, date)
            return total - total * _discount.percent / 100
        except DiscountError as e:
            log('ERROR', e)
            return total


DISCOUNT_CODES = {
    "SALE10": {"percent": 10, "expires": "2026-12-31"},
    "SALE50": {"percent": 50, "expires": "2025-2025-2025"},  # уже истёк
    "VIP": {"percent": 20, "expires": "2030-01-01"},
}

ORDERS_LOG = []  # имитация "базы данных" заказов


def send_email(to, subject, body):
    # представим, что здесь реальная отправка через SMTP/почтового провайдера
    print(f"EMAIL to {to}: {subject}\n{body}")


def charge_payment(card_number, amount):
    # представим, что здесь вызов внешнего платёжного шлюза
    print(f"Charging {amount} from card {card_number}")
    return {"status": "success", "transaction_id": "tx_12345"}


def process_order(user_email, card_number, items, discount_code=None):
    """
    items: список словарей вида [{"name": "Book", "price": 500, "qty": 2}, ...]
    Возвращает итоговую сумму заказа.
    """
    total = 0
    for item in items:
        total += item["price"] * item["qty"]

    if discount_code:
        discount = DISCOUNT_CODES[discount_code]
        expires = datetime.datetime.strptime(discount["expires"], "%Y-%m-%d")
        if datetime.datetime.now() < expires:
            total = total - total * discount["percent"] / 100

    payment_result = charge_payment(card_number, total)

    ORDERS_LOG.append({
        "user": user_email,
        "items": items,
        "total": total,
        "transaction_id": payment_result["transaction_id"],
    })

    send_email(
        user_email,
        "Ваш заказ оформлен",
        f"Сумма к оплате: {total} руб."
    )

    return total
