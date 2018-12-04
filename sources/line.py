import re

from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    TextMessage, TextSendMessage, MessageEvent, TemplateSendMessage, ConfirmTemplate, PostbackAction, PostbackEvent,
    StickerSendMessage, FollowEvent, UnfollowEvent, StickerMessage, AudioSendMessage
)
import flask

from utils.utils import build_rich_menu, load_user_list, save_user_list, operation_handler, query_reply
from utils import app, line_bot_api, handler
import utils


@app.route('/user_list/<user_id>')
@app.route('/user_list/')
def index(user_id=None):

    if user_id is not None and user_id in utils.user_list:
        # return user's detail
        http = '<H1>{}</H1><p>'.format(user_id) + '<hr>'
        http += '<p><b>name: </b>{}</p>'.format(
            utils.user_list[user_id]['name'])
        http += '<p><b>query_table: </b>{}</p>'.format(
            utils.user_list[user_id]['query_table'])

    else:
        # return user list
        http = '<H1>User list</H1><p>' + '<hr>'

        for user, attr in utils.user_list.items():
            try:
                http += '<a href="{url}">{t}</a><br>'.format(
                    url='./{}'.format(user), t=attr['name'])
                http += '<i>user_id: {}</i>'.format(user) + '<hr>'

            except Exception:
                print('error')

    return http


@app.route('/callback', methods=['POST'])
def callback():

    signature = flask.request.headers['X-Line-Signature']
    # get request body as text
    body = flask.request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        flask.abort(400)

    return 'OK'


# handle text message
handlers = {}


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global handlers
    if event.message.type == 'text':

        user_id = event.source.user_id

        if user_id == 'Udeadbeefdeadbeefdeadbeefdeadbeef':
            line_bot_api.reply_message(event.reply_token,
                                           TextSendMessage(text='reply the webhook varification'))
            return 

        user_text = event.message.text
        query_table = utils.user_list[user_id]['query_table']

        # check if handler exist
        if user_id not in handlers:
            handlers[user_id] = operation_handler()

        op_handler = handlers[user_id]

        # logic of add, del, sel binding
        if user_text in ['{ADD}', '{DEL}', '{SEL}']:
            op_handler.control_mode = user_text[1:4]

        if op_handler.control_mode == 'ADD':
            if op_handler.control_stage is None:
                print('if op_handler.control_stage is None:')
                line_bot_api.reply_message(event.reply_token,
                                           TextSendMessage(text='請輸入「關鍵」字'))
                op_handler.control_stage = 1

            elif op_handler.control_stage == 1:
                print('elif op_handler.control_stage == 1:')
                op_handler.query = user_text
                # get bindling
                line_bot_api.reply_message(event.reply_token,
                                           TextSendMessage(text='請輸入「對應」字'))
                op_handler.control_stage = 2

            elif op_handler.control_stage == 2:
                print('elif op_handler.control_stage == 2:')
                op_handler.binding = user_text
                line_bot_api.reply_message(event.reply_token,
                                           TemplateSendMessage(
                                               alt_text='Confirm Adding',
                                               template=ConfirmTemplate(
                                                   text='確定新增對應\n {q} -> {r} 嗎？'.format(
                                                       q=op_handler.query, r=op_handler.binding),
                                                   actions=[
                                                       PostbackAction(
                                                           label='確定', data='confirm=1&act={act}'.format(act=op_handler.control_mode)),
                                                       PostbackAction(
                                                           label='取消', data='confirm=0&act={act}'.format(act=op_handler.control_mode)),
                                                   ]
                                               )
                                           ))

        elif op_handler.control_mode == 'DEL':
            if op_handler.control_stage is None:
                line_bot_api.reply_message(event.reply_token,
                                           TextSendMessage(text='請輸入「關鍵」字'))
                op_handler.control_stage = 1

            elif op_handler.control_stage == 1:
                op_handler.query = user_text
                if op_handler.query in query_table:
                    op_handler.binding = query_table[op_handler.query]
                    line_bot_api.reply_message(event.reply_token,
                                               TemplateSendMessage(
                                                   alt_text='Confirm',
                                                   template=ConfirmTemplate(
                                                       text='確定刪除對應\n {q} -> {r} 嗎？'.format(
                                                           q=op_handler.query, r=op_handler.binding),
                                                       actions=[
                                                           PostbackAction(
                                                               label='確定', data='confirm=1&act={act}'.format(act=op_handler.control_mode)),
                                                           PostbackAction(
                                                               label='取消', data='confirm=0&act={act}'.format(act=op_handler.control_mode)),
                                                       ]
                                                   )
                                               ))
                else:
                    line_bot_api.reply_message(event.reply_token,
                                               TextSendMessage(text='目前沒有這個關鍵字喔'))

                    # finish action DEL with exception, format variables
                    handlers.pop(user_id)

        elif op_handler.control_mode == 'SEL':
            resp = ''

            for q in query_table:
                resp += (q + ' -> ' + query_table[q] + '\n')

            if query_table is None:
                resp = '還沒有新增任何對應喔'

            resp.strip()

            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(text=resp))

            # postback no need, finish action SEL
            handlers.pop(user_id)

        else:
            # normal query handler
            for q in query_table:
                print('handle query: {q} -> {r}'.format(q=q, r=query_table[q]))
                query_reply(event, q, query_table[q])


@handler.add(MessageEvent, message=StickerMessage)
def handler_sticker(event):
    line_bot_api.reply_message(event.reply_token,
    StickerSendMessage(package_id='3', sticker_id='189'))


@handler.add(PostbackEvent)
def handle_postback(event):
    global handlers

    user_id = event.source.user_id
    op_handler = handlers[user_id]
    print('op_handler = handlers[user_id]')
    print(op_handler.__dict__)
    print('op_handler = handlers[user_id]')
    query_table = utils.user_list[user_id]['query_table']

    params = re.split('[=&]', event.postback.data)
    data = dict(zip(params[::2], params[1::2]))

    if data['confirm'] == '1':

        if op_handler.query is None or op_handler.binding is None:
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(text='資料錯誤，取消新增\n請重新輸入'.format(q=op_handler.query, r=op_handler.binding)))

        if data['act'] == 'ADD':
            print('ADD: {q} -> {r}'.format(q=op_handler.query,
                                           r=op_handler.binding))
            query_table[op_handler.query] = op_handler.binding
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(text='對應 {q} -> {r} 成功'.format(q=op_handler.query, r=op_handler.binding)))
        elif data['act'] == 'DEL':
            # key exist checked at stage 2 in handle_message()
            query_table.pop(op_handler.query)
            print('DEL: {q} -> {r}'.format(q=op_handler.query,
                                           r=op_handler.binding))
            line_bot_api.reply_message(event.reply_token,
                                       TextSendMessage(text='刪除 {q} -> {r} 成功'.format(q=op_handler.query, r=op_handler.binding)))

        utils.user_list[user_id]['query_table'] = query_table
        save_user_list()

        # tutorial message
        if len(query_table) == 1:
            line_bot_api.push_message(user_id, TextSendMessage(
                text='太好了！接下來只要你提到「{}」時，我就會回應你「{}」喔，趕快來試試看吧！'.format(op_handler.query, op_handler.binding)))

        handlers.pop(user_id)


@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    user_name = line_bot_api.get_profile(user_id).display_name

    line_bot_api.link_rich_menu_to_user(
        user_id, build_rich_menu(use_old=True))

    utils.user_list[user_id] = {
        "name": user_name,
        "query_table": {}
    }
    save_user_list()

    # push welcome message
    line_bot_api.push_message(user_id, TextSendMessage(
        text='Hello, {}！'.format(user_name)))
    line_bot_api.push_message(
        user_id, TextSendMessage(text='這是一個會根據您的設定，自動回應訊息的機器人'))
    line_bot_api.push_message(
        user_id, TextSendMessage(text='在選單中選擇「加入對應」加入第一個關鍵字吧'))


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    user_id = event.source.user_id

    line_bot_api.unlink_rich_menu_from_user(user_id)

    if user_id in utils.user_list:
        utils.user_list.pop(user_id)
    if user_id in handlers:
        handlers.pop(user_id)
    save_user_list()

if __name__ == '__main__':
    load_user_list()
    app.run(host='127.0.0.1', debug=True, port=3001)
