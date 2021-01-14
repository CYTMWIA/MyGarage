import re

def calStringWidth(text:str):
    res = 0
    for c in text:
        if (0x4E00<=ord(c)<=0x9FFF 
            or 0xFF01<=ord(c)<=0xFF60
            or c in '《》「」ー'):
            res += 2
        else:
            res += 1
    return res

class SimpleTable:
    _head = []
    '''
    _head = [
        {
            'text': str,
            'width': int
        },
        ...
    ]
    '''

    def __init__(self,headrow:list):
        self.addCols(headrow)

    def printRow(self,row,newline=True, prefix='',suffix=''):
        print(prefix, end='')

        for idx in range(len(self._head)):
            width = self._head[idx]['width']
            if idx >= len(row):
                text = ' ' * width
            else:
                text = str(row[idx])
                while calStringWidth(text) > width:
                    text = text[:-1]
                text = text + ' '*(width-calStringWidth(text))
            print(text, end='|')
        
        print(suffix, end='')
        
        if newline:
            print('')

    def printHeadRow(self):
        self.printRow([col['text'] for col in self._head])

    def printRowByDict(self,dct,*args,**kwargs):
        row = []
        for col in self._head:
            if col['text'] in dct:
                row.append(dct[col['text']])
            else:
                row.append('')
        self.printRow(row,*args,**kwargs)

    def addCol(self, headtext, width=None):
        self._head.append({
            'text': headtext,
            'width': calStringWidth(headtext) if width == None else width
        })
    
    def addCols(self,cols):
        for col in cols:
            if isinstance(col,tuple):
                self.addCol(col[0],col[1])
            else:
                self.addCol(col)

if __name__ == "__main__":
    pass