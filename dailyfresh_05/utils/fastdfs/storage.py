from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.conf import settings


class FastDFSStorage(Storage):
    """自定义文件存储系统：需要把django收到的图片通过fdfs_client工具包，转存到FastDFS服务器"""

    def __init__(self, client_conf=None, server_ip=None):
        """初始化方法：主要用于接收往外界传入的参数"""

        if client_conf is None:
            client_conf = settings.CLIENT_CONF
        self.client_conf = client_conf

        if server_ip is None:
            server_ip = settings.SERVER_IP
        self.server_ip = server_ip

    def _open(self, name, mode='rb'):
        """读取文件时调用的:直接pass,因为这个类主要实现文件存储，读取不再这里"""
        pass

    def _save(self, name, content):
        """文件存储时调用的：需要把文件通过通过fdfs_client工具包，转存到FastDFS服务器"""

        # 创建fdfs客户端对象
        client = Fdfs_client(self.client_conf)

        # 获取要上传的文件的二进制信息
        file_data = content.read()

        # 调用上传文件的方法：uplaod_file_by_filename 、by_buffer
        try:
            ret = client.upload_by_buffer(file_data)
        except Exception as e:
            print(e) # 方便自己测试时查询异常
            raise

        # 判断是否上传成功
        if ret.get('Status') == 'Upload successed.':
            # 上传成功：取出file_id,储存到Django数据库表中
            file_id = ret.get('Remote file_id')
            # 通过那个模型类，发布的内容，就会自动的保存到该模型类对应的表中
            return file_id
        else:
            # 上传失败：抛出异常
            raise Exception('上传到fdfs失败')


    def exists(self, name):
        """判断要上传的文件，在django中是否存在，如果存在返回True,就不会调用save；反之，就会调用save"""
        return False

    def url(self, name):
        """会返回存储的文件的地址"""
        # return http://192.168.243.193:8888/group1/M00/00/00/wKjzwVpTPG6AekAEAALb6Vx4KgI41.jpeg
        return self.server_ip + name
