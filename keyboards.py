from telebot import types
import txt

# Simple keyboards


def menu_keyboard():
    """Mainn keyboard after start command"""
    keyboard = types.ReplyKeyboardMarkup(True, False)
    shopping = types.KeyboardButton(
        "🛍Ҳаридни Бошлаш")
    my_box_btn = types.KeyboardButton("🛒My Box")
    about_us = types.KeyboardButton("📝Our Channel")
    keyboard.add(shopping, my_box_btn)
    keyboard.add(about_us)
    return keyboard


def number_keyboard():
    keyboard = types.ReplyKeyboardMarkup(True, False)
    number = types.KeyboardButton(text='Send contact', request_contact=True)
    menu_button = types.KeyboardButton('cancel and go to menu',)
    keyboard.add(number)
    keyboard.add(menu_button)
    return keyboard


def location_keyboard():
    keyboard = types.ReplyKeyboardMarkup(True, True)
    location = types.KeyboardButton(
        text="send Location", request_location=True)
    menu_button = types.KeyboardButton('cancel and go to menu')
    keyboard.add(location)
    keyboard.add(menu_button)
    return keyboard


# Inline keyboards


def category_keyboard(categories):
    """ This function creates category list """
    key = types.InlineKeyboardMarkup()
    length = len(categories)
    for i in range(0, length, 2):
        b1 = types.InlineKeyboardButton(
            text=categories[i]['name'], callback_data=categories[i]['name'])
        try:
            b2 = types.InlineKeyboardButton(
                text=categories[i+1]['name'], callback_data=categories[i+1]['name'])
            key.add(b1, b2)
        except Exception:
            key.add(b1)
    return key


def prods_by_category(prods):
    """Returns buttons with prods in the given category"""
    key = types.InlineKeyboardMarkup()
    if len(prods) == 1:
        b = types.InlineKeyboardButton(text=prods[0], callback_data=prods[0])
        key.add(b)
    else:
        for i in range(0, len(prods), 2):
            b1 = types.InlineKeyboardButton(
                text=prods[i], callback_data=prods[i])
            try:
                b2 = types.InlineKeyboardButton(
                    text=prods[i+1], callback_data=prods[i+1])
                key.add(b1, b2)
            except Exception:
                key.add(b1)

    back_categories = types.InlineKeyboardButton(
        text='back', callback_data='back_cat')
    key.add(back_categories)
    return key


def prod_description_keyboard(prod, soum=1000, unit=1):
    """ Creates and returns the keyboard with buttons: order in sums, order in units and back to products list"""
    key = types.InlineKeyboardMarkup()
    plus_unit = types.InlineKeyboardButton(
        text="+", callback_data=f"unit_add,{prod['name']},{unit},{soum}")
    minus_unit = types.InlineKeyboardButton(
        text="-", callback_data=f"unit_sub,{prod['name']},{unit},{soum}")
    buy_in_unit = types.InlineKeyboardButton(
        text=f"Buy\n{unit} {prod['unit']}", callback_data=f"unit_buy,{prod['name']},{unit}")
    plus_soum = types.InlineKeyboardButton(
        text="+", callback_data=f"soum_add,{prod['name']},{unit},{soum}")
    minus_soum = types.InlineKeyboardButton(
        text="-", callback_data=f"soum_sub,{prod['name']},{unit},{soum}")
    buy_in_soum = types.InlineKeyboardButton(
        text=f"Buy\n{soum} Soum", callback_data=f"soum_buy,{prod['name']},{soum}")
    back_to_prods = types.InlineKeyboardButton(
        text="Back", callback_data=prod['caregory'])
    key.add(minus_unit, buy_in_unit, plus_unit)
    key.add(minus_soum, buy_in_soum, plus_soum)
    key.add(back_to_prods)
    return key


def box_actions():
    keyboard = types.InlineKeyboardMarkup()
    clear_box_btn = types.InlineKeyboardButton(
        text='Clear box', callback_data='clear')
    buy_content_btn = types.InlineKeyboardButton(
        text='Buy my box content', callback_data='buy')
    numeric_clearing_btn = types.InlineKeyboardButton(
        text='clear by number', callback_data='clear_by_number_in_box')
    back_to_start_shopping_btn = types.InlineKeyboardButton(
        text="Back to menu", callback_data='back_cat')
    keyboard.add(numeric_clearing_btn, clear_box_btn)
    keyboard.add(buy_content_btn)
    keyboard.add(back_to_start_shopping_btn)
    return keyboard


def numeric_cancell_keyboard(box):
    keyboard = types.InlineKeyboardMarkup()
    length = len(box)
    if length == 1:
        o_id = box[0]['o_id']
        p_id = box[0]['p_id']
        name = box[0]['p_name']
        num_btn = types.InlineKeyboardButton(
            text=f"❌ {name}", callback_data=f'delete_item,{p_id},{o_id},{name}')
        keyboard.add(num_btn,)
    else:
        for i in range(0, length, 2):
            o_id1 = box[i]['o_id']
            p_id1 = box[i]['p_id']
            name1 = box[i]['p_name']
            b1 = types.InlineKeyboardButton(
                text=f"❌ {name1}", callback_data=f'delete_item,{p_id1},{o_id1},{name1}')
            try:
                name2 = box[i+1]['p_name']
                o_id2 = box[i+1]['o_id']
                p_id2 = box[i+1]['p_id']
                b2 = types.InlineKeyboardButton(
                    text=f"❌ {name2}", callback_data=f'delete_item,{p_id2},{o_id2},{name2}')
                keyboard.add(b1, b2)
            except Exception:
                keyboard.add(b1)

    back_btn = types.InlineKeyboardButton(text='back', callback_data="see_box")
    keyboard.add(back_btn)
    return keyboard


def see_box_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    back_btn = types.InlineKeyboardButton(text='back', callback_data="see_box")
    keyboard.add(back_btn)
    return keyboard
