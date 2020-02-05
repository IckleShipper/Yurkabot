import vk
import time

import config
import vkapi
import stalking


session = vk.Session()
vk_api = vk.API(access_token=config.token, v=5.21, session=session)

while True:
    try:
        messages = vk_api.messages.getConversations(offset=0, count=20, filter='unread')
        if messages['count'] >= 1:
            user_id = messages['items'][0]['last_message']['from_id']
            body = messages['items'][0]['last_message']['text']
            if body.lower() == 'привет':
                vkapi.send_message(user_id=user_id, token=config.token, message='Привет, девчонки')
            elif 'коммент' in body:
                vkapi.make_a_comment()
            elif 'https://vk.com/' in body:
                vkapi.send_message(user_id=user_id, token=config.token, message='Ты че мыш')
                stalk_id = vk_api.users.get(user_ids=body[15:])[0]['id']
                stalk_time = 60 * 60 * 24
                message = stalking.stalk(stalk_id, stalk_time)
                vkapi.send_message(user_id=user_id, token=config.token, message=message)
            else:
                vkapi.send_message(user_id=user_id, token=config.token, message='Я Юрка')
        time.sleep(1)
    except vk.exceptions.VkAPIError:
        time.sleep(1)
    #except vk.exceptions.Timeout:
    #except requests.exceptions.Timeout:
        #time.sleep(15)
