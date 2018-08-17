import vk_api
import config
import time

token = config.token
vk = vk_api.VkApi(token=token)

while True:
    messages = vk.method('messages.getConversations', {'offset': 0, 'count': 20, 'filter': 'unread'})
    if messages['count'] >= 1:
        print('MESSAGE')
        user_id = messages['items'][0]['last_message']['from_id']
        body = messages['items'][0]['last_message']['text']
        if body.lower() == 'привет':
            #vkapi.send_message(user_id=user_id, token=config.token, message='Привет, девчонки')
            vk.method('messages.send', {'peer_id': user_id, 'message': 'Привет, девчонки'})
        #elif '!' in body:
            #vkapi.send_message(user_id=user_id, token=config.token, message='Ты че мыш')
            #stalk_id = body[:-1]
            #message = stalking.stalk(stalk_id)
            #vkapi.send_message(user_id=user_id, token=config.token, message=message)
        else:
            #vkapi.send_message(user_id=user_id, token=config.token, message='Я Юрка')
            vk.method('messages.send', {'peer_id': user_id, 'message': 'Я Юрка'})
    time.sleep(1)
