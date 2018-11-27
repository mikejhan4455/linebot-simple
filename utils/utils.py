import os
import json
import inspect

from linebot.models import (
    RichMenu, RichMenuSize, MessageAction, RichMenuArea, RichMenuBounds, TextSendMessage
)
import utils


class operation_handler:

    def __init__(self):
        self.op_target = ''
        self.control_stage = None  # stage=1, enter 'query', stage=2, enter 'binding'
        self.control_mode = None  # ADD or DEL
        self.query, self.binding = None, None


def load_user_list():
    if 'user-list.json' not in os.listdir('.'):
        os.system('touch user-list.json')

    with open('user-list.json', 'r') as file:
        try:
            utils.user_list = json.load(file)
        except json.decoder.JSONDecodeError:
            utils.user_list = {}
            save_user_list()

    print('LOAD user list successful')


def save_user_list():
    with open('user-list.json', 'w') as file:
        file.write(json.dumps(utils.user_list))

    print('SAVE user list successful')


def query_reply(event, query, binding):

    if query in event.message.text:
        utils.line_bot_api.reply_message(event.reply_token,
                                         TextSendMessage(text=binding))


def build_rich_menu(use_old=False):

    # del old menus
    if not use_old:
        rich_menu_list = utils.line_bot_api.get_rich_menu_list()
        for rich_menu in rich_menu_list:
            print('del: {id}'.format(id=rich_menu.rich_menu_id))
            utils.line_bot_api.delete_rich_menu(rich_menu.rich_menu_id)

        # create new one
        rich_menu_to_create = RichMenu(
            size=RichMenuSize(width=2500, height=1686),
            selected=False,
            name="control",
            chat_bar_text="控制選項",
            areas=[
                RichMenuArea(
                    bounds=RichMenuBounds(x=970, y=2, width=1530, height=558),
                    action=MessageAction(label='add query', text='{ADD}')),
                RichMenuArea(
                    bounds=RichMenuBounds(
                        x=970, y=563, width=1530, height=558),
                    action=MessageAction(label='delete query', text='{DEL}')),
                RichMenuArea(
                    bounds=RichMenuBounds(
                        x=970, y=1127, width=1530, height=558),
                    action=MessageAction(label='delete query', text='{SEL}'))]
        )
        rich_menu_id = utils.line_bot_api.create_rich_menu(
            rich_menu=rich_menu_to_create)

        print('rich_menu_id: {id}'.format(id=rich_menu_id))

        with open('./assets/rich-menu-image.jpg', 'rb') as f:
            utils.line_bot_api.set_rich_menu_image(
                rich_menu_id, 'image/jpeg', f)

    else:
        # reuse old rich menu
        rich_menu_id = 'richmenu-f72203c3d17a6f3eca7b3df839561bbf'

    return rich_menu_id
