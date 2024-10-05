# from faker import Faker

# fake = Faker()

# def mock_payment():
#     return {
#         'payment_id': fake.uuid4(),
#         'amount': fake.random_number(digits=5),
#         'currency': 'hjbvdsbdbh',
#         'status': fake.random_element(elements=('created', 'completed', 'failed')),
#         'transaction_date': fake.date_time_this_year()
#     }

# # Generate mock payment data
# payment = mock_payment()
# print(payment)

import stripe
stripe.api_key = "sk_test_51Q6AImP3SbJ6TZaO5WUnvcqMyg3gvD6xEhIAUc4IlVSuNWZukveRJKYHL57ogBamy4uPXvm8RqDQZ5C1XycMVAoL00OzuQkNtj"

payment_intent = stripe.PaymentIntent.create(
  amount=500,
  currency="gbp",
  payment_method="pm_card_visa",
)

print(payment_intent)