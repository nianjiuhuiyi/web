import os
from pathlib import Path


# path = r"static_source"
# for root, dirs, files in os.walk(path):
#     # path文件夹下所有文件(包括子文件夹下的文件)的绝对路径
#     for name in files:
#         print(os.path.join(root, name))
#
#     # # 这里得到的都是所有递归目录的路径，所有文件的上一级目录
#     # for name in dirs:
#         # print(os.path.join(root, name), root)


path = r"a/b/123"
print(os.path.join(r"static_source", path))
print(Path("../static_source").joinpath(path))


