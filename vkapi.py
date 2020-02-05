import vk
import time

import stalking
import config


session = vk.Session()
user_token = config.user_token
vk_api = vk.API(access_token=user_token, v=5.21, session=session)

api = vk.API(session, v=5.21)


def send_message(user_id, token, message):
    while True:
        try:
            api.messages.send(access_token=token, user_id=str(user_id), message=message)
            break
        except vk.exceptions.VkAPIError:
            time.sleep(1)


def get_groups(user_id):
    return vk_api.groups.get(user_id=user_id)['items']


def get_link(post):
    return 'https://vk.com/wall%s_%s' % (post['owner_id'], post['id'])


def check_like(user_id, group_id, post_id):
    return vk_api.likes.isLiked(user_id=user_id, type='post', owner_id=group_id, item_id=post_id)['liked']


def get_likes(stalk_id, group_id, liked, stalk_time):
    need_to_repeat, offset = 1, 0
    while need_to_repeat == 1:
        while True:
            try:
                need_to_repeat, liked_new = vk_execute(time.time(), offset, stalk_id, group_id, stalk_time)
                liked = liked + liked_new
                offset += 24
                break
            except vk.exceptions.VkAPIError:
                time.sleep(1)
    return liked



def vk_execute(current_time, offset, user_id, group_id, stalk_time):
    return vk_api.execute(code=
                          'var liked_new = [];'
    'var user_id = '+str(user_id)+';'
    'var group_id = '+str(group_id)+';'
    'var posts = API.wall.get({"owner_id":group_id,"count": 24,"offset":'+str(offset)+'})["items"];'
    'if (posts.length>0){'
        'var i = 0;'
        'var like = 0;'
        'if (posts[i]["is_pinned"]==1){'
        'i=i+1;'
        '}'
        'while (('+str(int(current_time))+' - posts[i]["date"]) < '+str(stalk_time)+') {'
            'var post_id = posts[i]["id"];'
            'like = API.likes.isLiked({"user_id":user_id, "type":"post", "owner_id":group_id, "item_id":post_id})["liked"];'
            'if (like==1) {'
            'liked_new.push("https://vk.com/wall"+group_id+"_"+post_id);'
            '}'
            'i = i+1;'
            'if (i==24){'
            'return [1,liked_new];'
            '};'
        '};'
    '};'
    'return [0, liked_new];')


#это еще не работает
def make_a_comment():
    while True:
        try:
            stalk_time = 60 * 60
            stalk_id = '89490983'
            message = stalking.stalk(stalk_id, stalk_time)
            vk_api.photos.createComment(owner_id='-166864638', album_id='254031876', photo_id='456239031',
                                        message='Лайки за последние сутки: %s' % message)
            break
        except vk.exceptions.VkAPIError:
            time.sleep(1)

if __name__ == "__main__":
    vk_api.photos.createComment(owner_id='-166864638', album_id='254031876', photo_id='456239031',
                                message="Ура коммент")
    make_a_comment()