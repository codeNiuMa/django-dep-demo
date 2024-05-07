import hashlib
import random
from datetime import datetime
from time import sleep

from django.conf import settings
from django.test import TestCase
from pymysql import Connection


# random.seed(2024)


# Create your tests here.


def shengcheng_num():
    # INSERT INTO dj1.app02_prettynum (mobile, price, level, status)
    # VALUES ('15155980544', 50, 3, 1);
    num_list = [15722073289, 18615190982, 19670712167, 19866194005, 16696589751, 18864249501, 13380215088, 13246233931,
                17565127789, 13653112034, 19048883930, 13815852037, 17691828085, 18040645744, 15562469934, 15187965458,
                19939383765, 19154421832, 17522839348, 14992553276, 19742640710, 15297210165, 19016737837, 13975551532,
                15847751625, 18226910073, 18520841988, 19184939345, 15178816752, 18623382767, 17877878423, 18794915822,
                13370348893, 15147013335, 17876132122, 13668692918, 15893827920, 17564946916, 18676376246, 13321962817,
                13577703600, 17746976635, 13629133638, 13742150239, 17826909474, 15992693143, 18583837594, 15692692607,
                13491761777, 15382708484, 18397371353, 19792680942, 18841925002, 13154882258, 15751461235, 17766231857,
                13451340854, 19757253565, 19913660297, 18897011145, 17632671222, 14761010068, 17394899430, 18249814440,
                19195747544, 15568815455, 17513660818, 18467630356, 19843871737, 19145087788, 13922895785, 13181426490,
                17325564657, 13323814962, 15860196521, 15823608054, 16627422768, 17735538005, 18686017002, 15893362670,
                14794773911, 19963827789, 13072802139, 19770636735, 18836672997, 15011263904, 15185174764, 14575914074,
                14510102494, 17334499700, 15687397190, 19718574053, 19032694349, 13935465322, 19371208450, 19660421984,
                13698854271, 19661957884, 13626011196, 15620359151, 18119239231, 14561537015, 18978563094, 19777506785,
                19881231311, 19974176340, 19326849899, 17515871844, 18162018561, 18728177263, 18050840017, 18069800612,
                15872445284, 13255508254, 18789698032, 18682838761, 19363155692, 17578191655, 13825564493, 19933244726,
                13554360070, 13233064387, 19576765220, 17382547773, 19515665444, 16639334438, 17728983146, 13713152134,
                13762754969, 13341646713, 14551888987, 17727773879, 19781747884, 19549282140, 17385424600, 19588953689,
                19950249372, 18645508913, 14524875260, 14547841879, 13923022911, 17396183186, 19717889348, 18757019037,
                19829949903, 19761714447, 13473161914, 17735003103, 17324970617, 18779807917, 15178966462, 18035868471,
                18630279235, 18025956867, 15868856976, 19774419090, 15924235833, 19722322363, 19166512968, 18713328318,
                17522659571, 15064727756, 19141152261, 17274319064, 18348730256, 18490069281, 16624984765, 18220612121,
                15394483663, 13688646392, 15623568784, 18216378940, 19359729243, 17752986176, 13396183702, 13663540243,
                18717620938, 14746927767, 15023122357, 13624921450, 18861809107, 15625183085, 18118600094, 13556832942,
                19769221194, 13251564008, 17555498583, 13459443187, 19625312475, 13375912940, 15195378118, 15349732970,
                18185789843, 18738167645, 19049769346, 15742254915, 13960860131, 15033642813, 18837335984, 13879836800]

    # 生成随机数
    price = random.randint(10, 100)
    price_list = []
    level = random.randint(1, 4)
    level_list = []
    status = random.randint(1, 2)
    status_list = []

    for _ in range(200):
        price_list.append(random.randint(10, 100))
        level_list.append(random.randint(1, 4))
        status_list.append(random.randint(1, 2))

    for i in range(100, 200):
        print(
            f'INSERT INTO dj1.app02_prettynum (mobile, price, level, status) VALUES ({num_list[i]}, {price_list[i]}, {level_list[i]}, {status_list[i]});')


def shengcheng_order():
    cnt = 7

    conn = Connection(host='localhost',
                      port=3306,
                      user='root',
                      password='123456',
                      autocommit=True
                      )

    # print(conn.get_server_info())  # 获取服务器信息8.0.36
    cursor = conn.cursor()
    conn.select_db('dj1')

    # cursor.execute('create table test_pymysql(id int);')
    for i in range(100):
        h, m, s = (random.randint(0, 23)), (random.randint(0, 59)), (random.randint(0, 59))
        rnd_oid = datetime.now().strftime("%Y%m%d") + f'{h:02d}{m:02d}{s:02d}' + str(random.randint(10000, 99999))

        def rndChar():
            # 定义字符的ASCII码范围
            ascii_ranges = [
                (48, 57),  # 数字 0-9
                (65, 90),  # 大写字母 A-Z
                (97, 122),  # 小写字母 a-z
            ]
            # 随机选择一个范围
            chosen_range = random.choice(ascii_ranges)

            # 在选定的范围内随机选择一个字符并返回
            return chr(random.randint(chosen_range[0], chosen_range[1]))

        title = 'order_'
        for _ in range(6):
            title += rndChar()
        price = random.randint(10, 300)
        status = random.randint(1, 2)
        user_id = random.randint(1, 4)
        print(f"INSERT INTO dj1.app02_order (id, oid, title, price, status, user_id) VALUES ({cnt}, {rnd_oid},'{title}', {price}, {status}, {user_id});")
        cursor.execute(
            f"INSERT INTO dj1.app02_order (id, oid, title, price, status, user_id) VALUES ({cnt}, {rnd_oid},'{title}', {price}, {status}, {user_id});")

        sleep(0.5)
        cnt+=1

    conn.close()


def md5(input_string):
    m = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))

    # 更新md5对象内容，可以多次update，这里一次性完成
    m.update(input_string.encode('utf-8'))

    # 获取16进制格式的MD5值
    return m.hexdigest()


def check_code(width=120, height=40, length=4, font_size=20):
    code = []
    from PIL import Image, ImageDraw
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndChar():
        # 定义字符的ASCII码范围
        ascii_ranges = [
            (48, 57),  # 数字 0-9
            (65, 90),  # 大写字母 A-Z
            (97, 122),  # 小写字母 a-z
        ]
        # 随机选择一个范围
        chosen_range = random.choice(ascii_ranges)

        # 在选定的范围内随机选择一个字符并返回
        return chr(random.randint(chosen_range[0], chosen_range[1]))

    def rndColor():
        # 随机颜色，不用255因为有点浅
        return (random.randint(0, 200), random.randint(0, 200), random.randint(0, 200))

    # 绘制字符
    for i in range(length):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 3)
        w = i * width / length + random.randint(-2, 5)
        draw.text(xy=(w, h), text=char, fill=rndColor(), font_size=30)

    # 绘制干扰像素点
    for _ in range(40):
        x, y = random.randint(0, width), random.randint(0, height)
        draw.point(xy=(x, y), fill=(0, 0, 0))

    # 绘制干扰圈
    for _ in range(30):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc(xy=(x, y, x + 5, y + 5), start=random.randint(0, 180), end=random.randint(180, 360), fill=rndColor())

    # 绘制干扰线
    for i in range(5):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        draw.line(xy=(x1, y1, x2, y2), fill=rndColor())

    # img.save(r'F:\Code\PythonCode\djangoProject\app02\static\img\code.png')
    return img, ''.join(code)


if __name__ == '__main__':
    # shengcheng_order()
    # print(datetime.now().strftime('%Y%m%d'))
    pass
