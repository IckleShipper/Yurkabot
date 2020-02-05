import vk
import time

import config
import vkapi


import logging

logging.basicConfig(format=u'[%(asctime)s] - LINE:%(lineno)s - %(levelname)-8s - %(message)s', level=logging.DEBUG,
                    filename=u'mylog.log', filemode='w')

session = vk.Session()
user_token = config.user_token
vk_api = vk.API(access_token=user_token, v=5.21, session=session)


def stalk(stalk_id, stalk_time):
    liked = ['Лайки за последние сутки:']
    groups = vkapi.get_groups(stalk_id)
    group_number = 0

    for group_id in groups:
        group_number += 1
        group_id = '-%s' % group_id
        logging.info(group_id)
        percents_performed = '%s percent' % (int(group_number / len(groups) * 100))
        logging.info(percents_performed)
        try:
            vkapi.send_message(user_id='53096207', token=config.token, message=percents_performed)
        except vk.exceptions.VkAPIError:
            time.sleep(1)
        liked = vkapi.get_likes(stalk_id, group_id, liked, stalk_time)

    liked = '\n'.join(liked)
    return liked


if __name__ == '__main__':
    stalk_time = 60 * 60 * 24
    print(stalk('115938980', stalk_time))
    #print(stalk('89490983'))
    #print(vkapi.get_groups(115938980))