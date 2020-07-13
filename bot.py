import telebot
import keyboards
import utils
import txt
from telebot import types
from utils import MainClass
from user import Users
import config

users = Users()
data_instance = MainClass()
bot = telebot.TeleBot(config.token)
data_instance.init_or_refresh_data()
box_photo = config.box_photo
main_photo = config.main_photo


@bot.message_handler(commands=['start'])
def start_handler(message):
    # utils.get_user_data(message)
    users.set_user_data(message)
    users.upload_user_data(message)
    key = keyboards.menu_keyboard()
    text = txt.wellcome_txt
    bot.send_message(chat_id=message.chat.id, text=text,
                     reply_markup=key, parse_mode="HTML")


@bot.message_handler(regexp="🛍Ҳаридни Бошлаш")
def start_shopping(message):
    users.set_user_data(message)
    data_instance.init_or_refresh_data()
    keyboard = keyboards.category_keyboard(data_instance.categories)
    caption = txt.category
    bot.send_photo(chat_id=message.chat.id, photo=main_photo,
                   caption=caption, reply_markup=keyboard, parse_mode="HTML")


@bot.message_handler(regexp="🛒My Box")
def my_box_handler(message):
    print(message.chat.id)
    users.set_user_data(message)
    box = users.get_user_box(message.chat.id)
    if not box:
        keyboard = keyboards.category_keyboard(data_instance.categories)
        text = "Your Box is Empty"
        bot.send_photo(chat_id=message.chat.id, photo=main_photo,
                       caption=text, reply_markup=keyboard)
    else:
        keyboard = keyboards.box_actions()
        text = users.get_box_details(
            message.chat.id, data_instance.products_with_details)
        bot.send_photo(chat_id=message.chat.id, photo=box_photo,
                       caption=text, reply_markup=keyboard)


@bot.message_handler(regexp="📝Our Channel")
def about_us(message):
    keyboard = types.InlineKeyboardMarkup()
    channel_button = types.InlineKeyboardButton(
        text='Our telegram channel', url='https://t.me/joinchat/AAAAAFRiQUxgbnx5JsRHBQ')
    keyboard.add(channel_button)
    bot.send_message(text="To learn more about us please click the link below",
                     chat_id=message.chat.id, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in data_instance.get_category_names())
def category_handler(call):
    print(call.data)
    prods = data_instance.get_prods_in_given_category(call.data)
    key = keyboards.prods_by_category(prods)
    caption = call.data.upper()
    try:
        bot.edit_message_media(media=types.InputMediaPhoto(main_photo, caption=caption),
                               chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=key)
    except Exception:
        pass


@bot.callback_query_handler(func=lambda call: call.data == 'back_cat')
def back_cat_handling(call):
    print(call.data)
    keyboard = keyboards.category_keyboard(data_instance.categories)
    caption = 'Choose the category'
    try:
        bot.edit_message_media(media=types.InputMediaPhoto(main_photo, caption=caption),
                               chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=keyboard)
    except Exception:
        pass


@bot.callback_query_handler(func=lambda call: call.data in data_instance.get_product_names())
def product_handling(call):
    print(call.data)
    product = data_instance.get_product_details(call.data)
    key = keyboards.prod_description_keyboard(product)
    caption = f"{product['name']}\nUnit - {product['unit']}\nPrice - {product['price']}"
    try:
        bot.edit_message_media(media=types.InputMediaPhoto(product['image'], caption=caption), chat_id=call.from_user.id,
                               message_id=call.message.message_id, reply_markup=key)
    except Exception:
        pass


@bot.callback_query_handler(func=lambda call: call.data[0:8] == "unit_add")
def unit_adding_handler(call):
    print(call.data)
    call_result = call.data.split(',')
    product = data_instance.get_product_details(call_result[1])
    unit_amount = call_result[2]
    soum_amount = call_result[3]
    unit_amount = int(unit_amount) + 1
    key = keyboards.prod_description_keyboard(
        product, soum_amount, unit_amount)
    try:
        bot.edit_message_reply_markup(
            chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=key)
    except Exception:
        pass


@bot.callback_query_handler(func=lambda call: call.data[0:8] == "unit_sub")
def unit_subtracting_handler(call):
    print(call.data)
    call_result = call.data.split(',')
    product = data_instance.get_product_details(call_result[1])
    unit_amount = call_result[2]
    soum_amount = call_result[3]
    if int(unit_amount) <= 1:
        pass
    else:
        unit_amount = int(unit_amount) - 1
        key = keyboards.prod_description_keyboard(
            product, soum_amount, unit_amount)
        try:
            bot.edit_message_reply_markup(
                chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=key)
        except Exception:
            pass


@bot.callback_query_handler(func=lambda call: call.data[0:8] == "soum_add")
def soum_adding_handler(call):
    print(call.data)
    call_result = call.data.split(',')
    product = data_instance.get_product_details(call_result[1])
    unit_amount = call_result[2]
    soum_amount = call_result[3]
    soum_amount = int(soum_amount) + 1000
    key = keyboards.prod_description_keyboard(
        product, soum_amount, unit_amount)
    try:
        bot.edit_message_reply_markup(
            chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=key)
    except Exception:
        pass


@bot.callback_query_handler(func=lambda call: call.data[0:8] == "soum_sub")
def soum_subtracting_handler(call):
    print(call.data)
    call_result = call.data.split(',')
    product = data_instance.get_product_details(call_result[1])
    unit_amount = call_result[2]
    soum_amount = call_result[3]
    if int(soum_amount) <= 1000:
        pass
    else:
        soum_amount = int(soum_amount) - 1000
        key = keyboards.prod_description_keyboard(
            product, soum_amount, unit_amount)
        try:
            bot.edit_message_reply_markup(
                chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=key)
        except Exception:
            pass


@bot.callback_query_handler(func=lambda call: call.data[0:8] == "unit_buy")
def unit_buy_handler(call):
    print(call.data)
    call_result = call.data.split(",")
    product = data_instance.get_product_details(call_result[1])
    unit_amount = call_result[2]
    user_id = call.from_user.id
    caption = f"You have added {product['name']} succesifully to your box\n\nPlease choose the category"
    users.input_to_box(chat_id=user_id, product=product, amount=unit_amount)
    key = keyboards.category_keyboard(data_instance.categories)
    try:
        bot.edit_message_media(media=types.InputMediaPhoto(main_photo, caption=caption),
                               chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=key)
    except Exception:
        pass


@bot.callback_query_handler(func=lambda call: call.data[0:8] == "soum_buy")
def soum_buy_handler(call):
    print(call.data)
    call_result = call.data.split(",")
    product = data_instance.get_product_details(call_result[1])
    soum_amount = call_result[2]
    unit_amount = float(soum_amount)/product['price']
    user_id = call.from_user.id
    caption = f"You have added {product['name']} succesifully to your box\n\nPlease choose the category"
    users.input_to_box(chat_id=user_id, product=product, amount=unit_amount)
    key = keyboards.category_keyboard(data_instance.categories)
    try:
        bot.edit_message_media(media=types.InputMediaPhoto(main_photo, caption=caption),
                               chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=key)
    except Exception:
        pass


@bot.callback_query_handler(func=lambda call: call.data == "clear")
def clear_box_handler(call):
    keyboard = keyboards.category_keyboard(data_instance.categories)
    is_cleared = users.clear_all_box_content(call.from_user.id)
    if is_cleared:
        caption = 'Your box has been cleared'
    else:
        caption = 'The box is already empty'
    try:
        bot.edit_message_caption(caption=caption, chat_id=call.from_user.id,
                                 message_id=call.message.message_id, reply_markup=keyboard)
    except Exception:
        pass


@bot.callback_query_handler(func=lambda call: call.data == 'clear_by_number_in_box')
def numeric_clearing_handler(call):
    box = users.get_local_box(call.from_user.id)
    keyboard = keyboards.numeric_cancell_keyboard(box)
    caption = "Please select the product that you want to remove"
    try:
        bot.edit_message_caption(caption=caption, chat_id=call.from_user.id,
                                 message_id=call.message.message_id, reply_markup=keyboard)
    except Exception:
        pass


@bot.callback_query_handler(func=lambda call: call.data == "see_box")
def see_box_handler(call):
    keyboard = keyboards.box_actions()
    caption = users.get_box_details(
        call.from_user.id, data_instance.products_with_details)
    if not users.get_local_box(call.from_user.id):
        caption = "Your box is empty"
        keyboard = keyboards.category_keyboard(data_instance.categories)
        try:
            bot.edit_message_caption(caption=caption, chat_id=call.from_user.id,
                                     message_id=call.message.message_id, reply_markup=keyboard)
        except Exception:
            pass
    else:
        try:
            bot.edit_message_media(media=types.InputMediaPhoto(box_photo, caption=caption), chat_id=call.from_user.id,
                                   message_id=call.message.message_id, reply_markup=keyboard)
        except Exception:
            pass


@bot.callback_query_handler(func=lambda call: call.data[:11] == "delete_item")
def delete_item_handler(call):
    call_result = call.data.split(',')
    p_id = call_result[1]
    o_id = call_result[2]
    is_deleted = users.delete_item(p_id, o_id, call.from_user.id)
    if is_deleted:
        box = users.get_local_box(call.from_user.id)
        if not box:
            keyboard = keyboards.category_keyboard(data_instance.categories)
            caption = "Your box is empty please choose products"
            try:
                bot.edit_message_caption(caption=caption, chat_id=call.from_user.id,
                                         message_id=call.message.message_id, reply_markup=keyboard)
            except Exception:
                pass

        else:
            keyboard = keyboards.numeric_cancell_keyboard(box)
            try:
                bot.edit_message_reply_markup(
                    chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=keyboard)
            except Exception:
                pass


@bot.message_handler(regexp="cancel and go to menu")
def cancel_handler(message):
    data_instance.init_or_refresh_data()
    key = keyboards.menu_keyboard()
    text = "Wellcome to ou shop to sturt shopping please press appropriate button"  # Text package
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=key)


@bot.callback_query_handler(func=lambda call: call.data == "buy")
def buy_handler(call):
    keyboard = keyboards.number_keyboard()
    bot.send_message(text='Send us Contact number',
                     chat_id=call.from_user.id, reply_markup=keyboard)


@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    print(type(message.contact.phone_number))
    users.set_contact(message.chat.id, message.contact.phone_number)
    keyboard = keyboards.location_keyboard()
    text = "Please send us location"
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def location_handler(message):
    print(message.location)
    users.set_location(
        message.chat.id, message.location.longitude, message.location.latitude)
    is_confirmed = users.confirm_order(message.chat.id)
    if is_confirmed:
        text = "Your order is confirmed we will contact you soon\n\n\n"
        text += users.get_box_details(
            message.chat.id, data_instance.products_with_details)
        bot.send_message(chat_id=message.chat.id, text=text)
        keyboard = keyboards.menu_keyboard()
        bot.send_message(
            message.chat.id, text="Press start shopping", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, text="Your data might be lost for long waiting olease try again",
                         reply_markup=keyboards.menu_keyboard())


bot.polling()
