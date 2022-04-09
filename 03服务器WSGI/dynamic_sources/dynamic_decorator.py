import time
import pymysql

now_time = time.ctime()

# 创建一个字典用于存映射关系
URL_FUNC_DICT = dict()

"这个一导包进来，带@route的行就会执行"


def route(url):
    def set_func(func):
        URL_FUNC_DICT[url] = func  # 这里在@route时就会执行，装饰器带参数讲原理时讲过

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


@route("/show.py")
def show():
    """
    数据库数据查询的显示，更好的是把要查询的地方当参数传进来。
    :return:
    """
    dbconnect = pymysql.connect(
        host="192.168.2.125",
        port=3306,
        user="root",
        passwd="123456",  # 除了port，密码这些一定要str
        charset="utf8",
        database="my_areas"
    )
    cursor = dbconnect.cursor()
    # 这里的 "四川省" 可以换成其它的，也可以换成市,比如 “广安”
    query_sql = "select * from areas as province inner join areas as city on province.district_id=city.pid " \
                "having province.district_id=(select district_id from areas where district='成都');"

    cursor.execute(query_sql)
    datas = cursor.fetchall()
    cursor.close()
    dbconnect.close()

    # 设置一个标头
    contents = """
        <tr>
            <th>district_id</th>
            <th>pid</th>
            <th>district</th>
            <th>level</th>
            <th>%district_id(1)</th>
            <th>%pid(1)</th>
            <th>district(1)</th>
            <th>level(1)</th>
            <th>添加自选</th>
        </tr>
    """
    # 这每行的内容
    line = """
        <tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>
                <input type='button' value='添加'>
            </td>
        </tr>
    """
    for data in datas:
        contents += line % (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7])

    # 使其成为比表格
    contents = "<table border='1' width='200' cellspacing='0' cellpadding='5' align='center'>" + contents + "<table/>"
    return contents


# application中不能再写那么多 if else，如果有很多函数，就会写很多，不好看
def application(env: dict, start_response):
    start_response("200 OK", [("Content-Type", "text/html;charset=utf-8")])

    file_name = env["file_name"]
    # 假定以.py结尾的是访问动态资源，，若不想这样，就要有一个字典存起来对应关系，然后直接取
    if file_name.endswith(".py"):
        try:
            ret = URL_FUNC_DICT[file_name]  # 这里返回的就是对应的函数引用
            return ret()  # 这是调用函数
        except:
            return "这个页面找不到了！ 404 Not Found！"
    else:  # 否则就是访问静态资源
        try:
            # 一定注意，这里./static_sources这个相对路径是相对的server.py(因为是从server.py启动的)，而不是dynamic.py
            fp = open(r"./static_sources" + file_name, "r")
        except Exception:
            response_body = "这个页面找不到了！ 404 Not Found！"
        else:
            response_body = fp.read()
            fp.close()
        return response_body


