import re


from . import BasicMarket3rd
from . import Item3rd

class C5game(BasicMarket3rd.BasicMarket3rd):
    def walkItems(self, query_string):
        try:
            page = int(re.search(r'page=(\d+)',query_string)[1])
        except Exception:
            page = 1
        
        while True:
            rsp = self.session.get(f'https://www.c5game.com/{query_string}&page={page}')
            itemurls = ['https://www.c5game.com' + p for p in re.findall(r'<li class="selling">.*?<a href="(.*?)">',rsp.text,re.DOTALL)]
            for iu in itemurls:
                pass


            page += 1

        pass
    
    pass

if __name__ == "__main__":
    pass