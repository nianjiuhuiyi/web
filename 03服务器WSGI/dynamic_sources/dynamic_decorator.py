import time
import pymysql
import re


now_time = time.ctime()

# 创建一个字典用于存映射关系
URL_FUNC_DICT = dict()


# 数据库链接单独写出来
def conncet_db():
    dbconnect = pymysql.connect(
            # host="192.168.2.125",
            host="192.168.125.135",
            port=3306,
            user="root",
            passwd="123456",  # (1):除了port，密码这些一定要str
            charset="utf8",
            database="my_areas"  # (2):注意这是表示用的哪一个库
        )
    return dbconnect


"这个一导包进来，带@route的行就会执行"
def route(url):
    def set_func(func):
        # (3):这里在@route时就会执行，装饰器带参数讲原理时讲过
        URL_FUNC_DICT[url] = func

        def call_func(*args, **kwargs):  # 因为一开始字典里就拿到了 func的引用，其实这下面三行可以不要的，
            return func(*args, **kwargs)  # 因为不会单独再去使用类似 register() 的单独调用，没有这三行，这样的单独调用就会报错

        return call_func

    return set_func


# 这里函数假设都是获取一些动态数据
@route("/register.py")
def register():
    return "hello world!  {}".format(now_time)


@route("/logging.py")
def logging():
    return "这是一个登录页面！ {}".format(now_time)


@route("/exiting.py")
def exiting():
    return "这是注销页面！ {}".format(now_time)


@route("/show.py")   # 用于展示画面
def show():
    """
    数据库数据查询的显示，更好的是把要查询的地方当参数传进来。
    :return:
    """
    try:  # 要检查连接容错
        dbconnect = conncet_db()
    except:
        return "<div>Error!!! 数据库连接失败，请检查密码是否正确，或数据库是否开启！</div>"

    cursor = dbconnect.cursor()
    query_sql = "select * from province;"  # 表示用的 province 这个表

    cursor.execute(query_sql)
    datas = cursor.fetchall()
    cursor.close()
    dbconnect.close()

    # 设置一个个人收藏的快速访问
    contents = "<div style='width:70px; height:25px; background:orange'><a href='collect.py'>个人收藏</a></div>"
    # 设置一个标头
    contents += """
        <tr>
            <th>district_id</th>
            <th>pid</th>
            <th>district</th>
            <th>level</th>
            <th>添加自选</th>
        </tr>
    """
    # (4):注意这里的 <a href='show/%s.py'> ，这里有个 %s 代表每个省份具体的数字   # 这每行的内容
    line = """  
        <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>
                <a href='show/%s.py'> 
                    <button style="width:70px;height:30px"><strong>收藏</strong></button>
                </a>
            </td>
        </tr>
    """
    for data in datas:
        contents += line % (data[0], data[1], data[2], data[3], data[0])

    # 使其成为比表格
    contents = "<table border='1' width='200' cellspacing='0' cellpadding='5' align='center'>" + contents + "<table/>"
    return contents


@route("/collect.py")  # 用于查看个人的收藏页面
def collect():
    try:  # 要检查连接容错
        dbconnect = conncet_db()
    except:
        return "<div>Error!!! 数据库连接失败，请检查密码是否正确，或数据库是否开启！</div>"

    cursor = dbconnect.cursor()
    query_sql = "select pid, district_id, district, level from collection;"  # 查询收藏的表

    cursor.execute(query_sql)
    datas = cursor.fetchall()
    cursor.close()
    dbconnect.close()

    contents = "<div style='width:70px; height:25px; background:orange'><a href='show.py'>展示页面</a></div>"
    # 设置一个标头
    contents += """
        <tr>
            <th>pid</th>
            <th>district_id</th>
            <th>district</th>
            <th>level</th>
            <th>备注</th>
            <th>添加自选</th>
        </tr>
    """

    # 如果没有收藏的数据，就直接返回
    if not datas:
        return contents

    line = """
        <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>我的</td>
            <td>
                <a href="collect/%s.py">
                    <button style="width:70px;height:30px"><strong>删除</strong></button>
                </a>
            </td>
        </tr>
    """
    for data in datas:
        contents += line % (data[0], data[1], data[2], data[3], data[1])

    # 使其成为比表格
    contents = "<table border='1' width='400' cellspacing='0' cellpadding='20' align='center'>" + contents + "<table/>"
    return contents


# (5):这种路由里，写的是一个正则表达式，就对应 /show/12.py  /show/15.py 这种只是后面参数不一样(点的按钮不一样)，处理逻辑都是一样的
# (6):注意点.前面的反斜杠，一定要，不然下面application函数中正则的影响很大
@route("/show/(\d+)\.py")  # 从展示的主页面收藏数据
def collect_add(ret):
    "ret是传进来的正则匹配结果(且一定是匹配到的，没配到的进不来)，ret.group(1)就是对应的各省份的district_id "
    district_id = ret.group(1)

    try:  # 要检查连接容错
        dbconnect = conncet_db()
    except:
        return "<div>Error!!! 数据库连接失败，请检查密码是否正确，或数据库是否开启！</div>"
    cursor = dbconnect.cursor()

    query_sql = "select * from province where district_id=%s;"
    # (7):注意写元祖进去，不要自己在上面.format()拼接，小心sql注入
    cursor.execute(query_sql, (district_id, ))
    query_data = cursor.fetchall()

    # 首先：判断这个收藏的id是否在数据库的范围内，若不在就没有数据，就是认为模拟的数据：
    if not query_data:
        results = "行行好，大哥手下留情，不要再攻击我们了..."
    else:
        # 其次：如果数据合法，还要判断是否已经收藏了
        # query_collect = "select district_id, district, level from collection where district_id=%s"
        query_collect = "select * from collection where district_id=%s"   # 这是个人收藏表
        cursor.execute(query_collect, (district_id,))
        query_data = cursor.fetchall()
        if query_data:
            results = "您已经收藏了，请勿重复收藏！！！"
        else:
            cursor.execute("select district_id, district, level from province where district_id=%s", (district_id, ))
            insert_data = cursor.fetchone()

            """
                注意这里这种自己拼接"insert into collection values(default, %s, '%s', %s);"的第二个%s，外面加了一对''，
            不加''就是 insert into collection values(default, 22, 山东省, 1);  # 山东省是字符串，这句是执行不了的，
            所以不要自己去拼接，像下面去自己执行
            """
            insert_sql = "insert into collection values(default, %s, %s, %s);"
            # cursor.execute(insert_sql, (insert_data[0], insert_data[1], insert_data[2]))  # 和下面是一样的
            cursor.execute(insert_sql, insert_data)
            dbconnect.commit()   # (6):一定是链接来commit
            results = "收藏成功！"

    cursor.close()
    dbconnect.close()
    results += "<div><a href='../show.py'><strong style='width:70px; height:25px'>返回展示页面</strong></a></div>"
    results += "<div><a href='../collect.py'><strong style='width:70px; height:25px'>返回收藏页面</strong></a></div>"
    return results


@route("/collect/(\d+)\.py")     # 从收藏中删除数据
def collect_del(ret):
    district_id = ret.group(1)

    try:  # 要检查连接容错
        dbconnect = conncet_db()
    except:
        return "<div>Error!!! 数据库连接失败，请检查密码是否正确，或数据库是否开启！</div>"
    cursor = dbconnect.cursor()

    query_sql = "select * from collection where district_id=%s;"
    cursor.execute(query_sql, (district_id, ))
    query_data = cursor.fetchall()

    if not query_data:
        results = "删除数据不存在，请手下留情..."
    else:
        del_sql = "delete from collection where district_id=%s;"
        cursor.execute(del_sql, (district_id, ))
        dbconnect.commit()
        results = "取消收藏成功！！！"
    cursor.close()
    dbconnect.close()

    # (8):注意：这里返回收藏页面，是以 :8899/collect.py 作为相对路径的，
    # - href=".." 就回到了 :8899/
    # - href="../collect.py"  就来到了 :8899/collect.py
    results += "<div><a href='../collect.py'><strong style='width:70px; height:25px'>返回收藏页面</strong></a></div>"
    results += "<div><a href='../show.py'><strong style='width:70px; height:25px'>返回展示页面</strong></a></div>"
    return results


# application中不能再写那么多 if else，如果有很多函数，就会写很多，不好看
def application(env: dict, start_response):
    start_response("200 OK", [("Content-Type", "text/html;charset=utf-8")])

    file_name = env["file_name"]
    # 假定以.py结尾的是访问动态资源，，若不想这样，就要有一个字典存起来对应关系，然后直接取
    if file_name.endswith(".py"):

        try:
            # (9)这是为了匹配,是@route("/show/(\d+)\.py")这个格式再把正则匹配的结果传家进去，否则是没有参数的
            # 这种一般传进来的是 /show/13.py  # 13其实就是某个省份的district_id
            match_out = re.match("/show/(\d+)\.py", file_name)
            if match_out:
                ret = URL_FUNC_DICT["/show/(\d+)\.py"]  # 这里返回的就是对应的函数引用(因为上限@路由关于这个的名字写死了的)
                return ret(match_out)
            # 这是为了匹配,是@route("/collect/(\d+)\.py"),做收藏的删除的（我这里就是直接写死了，没用去循环字典的方式了）
            match_out = re.match("/collect/(\d+)\.py", file_name)
            if match_out:
                ret = URL_FUNC_DICT["/collect/(\d+)\.py"]  # 这里返回的就是对应的函数引用(因为上限@路由关于这个的名字写死了的)
                return ret(match_out)

            # 如果都不是，那就是最简单的展示
            ret = URL_FUNC_DICT[file_name]  # 这里返回的就是对应的函数引用
            return ret()  # 这是调用函数
        except:
            return "这个页面找不到了！ 404 Not Found！"
    else:  # 否则就是访问静态资源
        try:
            # (10):一定注意，这里./static_sources这个相对路径是相对的server.py(因为是从server.py启动的)，而不是dynamic.py
            fp = open(r"./static_sources" + file_name, "r")
        except Exception:
            response_body = "这个页面找不到了！ 404 Not Found！"
        else:
            response_body = fp.read()
            fp.close()
        return response_body
