from . import Utils

class BasicMarket3rd:
    session = Utils.getMaskedRequestsSession()
    def walkItems(self, query_string):
        '''根据查询字符串创建一个生成器, 返回对象是单个饰品及其信息
        '''
        pass