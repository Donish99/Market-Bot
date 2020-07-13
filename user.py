import requests


class Users():
    def __init__(self):
        self.users = []
        self.user = {
            "id": 0,
            "number": '',
            "order": None,
            "long": '',
            "lat": '',
        }

    def upload_user_data(self, message):
        url = 'http://167.71.60.217:2020/users'
        user = {
            "chat_id": message.chat.id,
            "first_name": message.from_user.first_name,
            "username": message.from_user.username,
        }
        requests.post(url=url, data=user)

    def set_user_data(self, message):
        is_here = False
        for u in self.users:
            if u['id'] == message.chat.id:
                is_here = True
        if not is_here:
            self.user = {
                "id": message.chat.id,
            }
            self.users.append(self.user)

    def find_user(self, id):
        for u in self.users:
            if u['id'] == id:
                return u
        return {}

    def input_to_box(self, chat_id, product, amount):
        order = {
            'chat_id': int(chat_id),
            'product': int(product['id']),
            'amount': float(amount),
        }
        requests.post(url='http://167.71.60.217:2020/order', data=order)

    def set_box(self, id, box):
        user = self.find_user(id)
        user["order"] = box

    def get_user_box(self, id):
        url = 'http://167.71.60.217:2020/order?chat_id='+str(id)
        r = requests.get(url=url)
        r = r.json()
        if r['status'] == 404:
            return []
        r = r['results']
        r = r['list']
        self.set_box(id, r[0])
        return r[0]

    def get_box_details(self, id, prods):
        user = self.find_user(id)
        ordered_products = user["order"]
        count = 0
        text = 'Your order(s)\n'
        unit = ''
        for prod in ordered_products:
            for p in prods:
                if p['name'] == prod['p_name']:
                    unit = p['unit']
            count += 1
            text += f"{count}. {prod['p_name'].upper()}\n  Price per unit - {prod['p_price']}\n  You have ordered - {prod['amount']} {unit}\n\n"
        return text

    def get_local_box(self, id):
        user = self.find_user(id)
        return user["order"]

    def clear_box_locally(self, id):
        user = self.find_user(id)
        del user["order"]

    def clear_all_box_content(self, id):
        order = self.get_local_box(id)
        if not order:
            return False
        data = {
            "order_id": order[0]['o_id'],
        }
        url = 'http://167.71.60.217:2020/order/clear'
        r = requests.post(url=url, data=data)
        r = r.json()
        self.clear_box_locally(id)
        if r['status'] == 200:
            return True
        return False

    def delete_item(self, p_id, o_id, user_id):
        # Deleting_item_locally
        user = self.find_user(user_id)
        box = user['order']
        index_of_box = 0
        for item in box:
            if item["p_id"] == int(p_id):
                del box[index_of_box]
                break
            index_of_box += 1
        # Deleting item from server
        url = 'http://167.71.60.217:2020/order/clear/item'
        body = {
            "order_id": o_id,
            "product_id": p_id,
        }
        r = requests.post(url=url, data=body)
        r = r.json()
        if r['status'] == 200:
            return True
        return False

    def set_contact(self, id, contact):
        user = self.find_user(id)
        user['number'] = contact

    def set_location(self, id, long, lat):
        user = self.find_user(id)
        user["long"] = long
        user["lat"] = lat

    def confirm_order(self, id):
        url = "http://167.71.60.217:2020/order/confirm"
        try:
            user = self.find_user(id)
            order = user['order']
            order = order[0]
            order_id = order["o_id"]
            data = {
                "order_id": order_id,
                "contact": user['number'],
                "lat": user["lat"],
                "long": user["long"],
            }
            r = requests.post(url=url, data=data)
            r = r.json()
            print(r)
            if r['status'] == 200:
                return True
        except Exception:
            print("Crash in gettin user data")
            return False
