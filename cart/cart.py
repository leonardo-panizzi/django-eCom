from store.models import Product

class Cart():
	def __init__(self, request):
		self.session = request.session
		self.request = request
		cart = self.session.get('session_key') # grabs current existing session key
		if 'session_key' not in request.session: # new user case
			cart = self.session['session_key'] = {}
		self.cart = cart

	def add(self, product, quantity):
		product_id = str(product.id)
		if product_id in self.cart:
			self.cart[product_id]['quantity'] += quantity
		else:
			self.cart[product_id] = {
				'price': str(product.price),
				'quantity': quantity,
			}
		self.session.modified = True

	def __len__(self):
		return sum(item['quantity'] for item in self.cart.values())

	def cart_total(self):
		product_ids = self.cart.keys()
		products = Product.objects.filter(id__in=product_ids)
		total = 0
		for key, value in self.cart.items():
			product_id = int(key)
			quantity = int(value['quantity'])
			for product in products:
				if product.id == product_id:
					if product.is_sale:
						total += product.sale_price * quantity
					else:
						total += product.price * quantity
		return total

	def get_prods(self):
		product_ids = self.cart.keys()
		products = Product.objects.filter(id__in=product_ids)
		cart_products = []

		for product in products:
			cart_item = self.cart[str(product.id)]
			cart_products.append({
				'product': product,
				'quantity': cart_item['quantity']
			})
		return cart_products

	def get_quants(self):
		quantities = self.cart
		return quantities

	def update(self, product, quantity):
		if isinstance(product, (str, int)):
			product_id = str(product)
		else:
			product_id = str(product.id)

		if product_id in self.cart:
			self.cart[product_id]['quantity'] = quantity
			self.session.modified = True
		return self.cart

	def delete(self, product):
		product_id = str(product)
		if product_id in self.cart:
			del self.cart[product_id]

		self.session.modified = True