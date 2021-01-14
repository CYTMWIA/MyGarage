'''
Tested:
- Symbiotic
- 千面_Melancholy
- 人间 The Lost We Lost
'''

import os
import json


ASAR = 'asar'
GAME = r"D:\home\games\SteamLibrary\steamapps\common\Symbiotic"
OUTPUT = r'D:\tmp\Symbiotic'


def ls_abs(path):
    '''
    返回 path 下所有文件（包括目录）的 绝对路径
    '''
    return list(map(os.path.abspath, [os.path.join(path, name) for name in os.listdir(path)]))


# 解包
dir_resources = os.path.join(GAME, 'resources')
paths_asar = list(filter(lambda s: s.endswith('.asar'), ls_abs(dir_resources)))
for ap in paths_asar:
    name = os.path.basename(ap)
    output = os.path.join(OUTPUT, name)
    if (os.path.exists(output)):
        print('[extract][skip]', name)
        continue

    cmd = f'{ASAR} extract "{ap}" "{output}"'
    print(f'[extract] {name} | {cmd}')
    os.system(cmd)


# 重命名文件（仅支持《人间》）
next_dirs = list(filter(lambda p: os.path.isdir(p), ls_abs(OUTPUT)))
idx = 0
while idx < len(next_dirs):
    paths = ls_abs(next_dirs[idx])
    for p in paths:
        if os.path.basename(p) == 'list.txt':
            with open(p, 'r', encoding='utf-8') as f:
                filenames_table = [l.strip().split('   ') for l in f.readlines()]

            dir_ = os.path.dirname(p)
            for row in filenames_table:
                ori_path = os.path.join(
                    dir_, os.path.basename(row[1]))  # 原始文件名
                hash_path = os.path.join(
                    dir_, os.path.basename(row[2]))  # 被打包的文件名
                if os.path.exists(hash_path):
                    print(f'[rename] {hash_path} -> {ori_path}')
                    os.rename(hash_path, ori_path)
            break
    next_dirs += list(filter(lambda p: os.path.isdir(p), paths))
    idx += 1


# 解析脚本（主要是提取文本及分支）
dir_script = os.path.join(OUTPUT ,r'main.asar\script')
paths_script = filter(lambda s: not s.endswith('.txt'), ls_abs(dir_script))
dir_text = os.path.join(OUTPUT ,r'text')
for sp in paths_script:
    print(f'[text][start] {sp}')
    with open(sp, 'r', encoding='utf-8') as f:
        script = json.load(f)

    text = []
    # text 末尾 \n 个数
    count_last_newline = lambda: len(''.join(text[-3:]))-len(''.join(text[-3:]).rstrip('\n')) if len(text) else 0
    # 确保 text 末尾有 n 个 \n
    fill_newline = lambda n: text.append('\n'*(n-count_last_newline())) if len(text) else None
    
    filename = os.path.basename(sp)
    ai = 0
    cur = ''
    notext = True
    while ai < len(script):
        action = script[ai]
        ai += 1

        # 指令
        cmd = action[0]
        # 序号，不是数组索引！可能是脚本的执行顺序（有相同序号的元素）
        idx = action[1]
        # 不明
        _ = action[2]
        # 参数
        arg = action[3] if len(action) >= 4 and isinstance(action[3], dict) else {}

        if cmd == 0: # 

            cur = 'branch_flag'
            fill_newline(2)
            text.append(arg['id']+'\n\n')

            if idx == 0 and not GAME.strip().endswith('人间 The Lost We Lost'):
                filename = arg['id'].replace('*', '')

        elif cmd == 1:
            if 'target' in arg and ai == len(script): # 下一章
                cur = 'next_chapter'
                fill_newline(2)
                text.append(arg['target']+'\n\n')

        elif cmd == 4:

            if arg[''] == 'npc':  # 切换说话对象
                cur = 'name'
                fill_newline(2)
                text.append(arg['id'])

            elif arg[''] == 'selbutton':  # 选择选项
                if cur != 'selbutton':
                    fill_newline(2)
                cur = 'selbutton'
                text.append(f'({arg["target"]}) {arg["text"]}\n')

            elif arg[''] == 'bg':  # 切换背景（转场）
                if cur != 'transition':
                    fill_newline(2)
                    text.append('_-_-_-_-_-_-_-_-\n\n')
                cur = 'transition'

        elif cmd == 5:  # 对话文字

            notext = False

            if arg['text'][0] == '「':  # 实际说出口
                if cur != 'speak':
                    fill_newline(1)
                cur = 'speak'

            else:  # 心里话
                if cur == 'speak':
                    fill_newline(2)
                elif cur != 'mind':
                    fill_newline(1)
                cur = 'mind'

            text.append(arg['text']+'\n')

        elif cmd == 50:  # 数值变化
            cur = 'value_change'
            fill_newline(2)
            text.append('< '+arg['exp']+' >\n\n')

        elif cmd == 51:  # 分支章节（IF）（注意嵌套）
            cur = 'branch'
            fill_newline(2)

            ifs = [{'branches': arg[''], 'branch_idx':0}]
            ifidx = 0
            while len(ifs):
                cur_if = ifs[ifidx]

                if cur_if['branch_idx'] >= len(cur_if['branches']):
                    ifidx -= 1
                    ifs.pop(-1)
                    continue

                bch = cur_if['branches'][cur_if['branch_idx']]
                cur_if['branch_idx'] += 1
                text.append('    '*(len(ifs)-1)+f'if {bch[0]}:\n')
                for then in bch[1]:
                    if then[0] == 51:
                        ifs.append({'branches': then[3][''], 'branch_idx': 0})
                    else:
                        if 'target' in then[3]:
                            text.append('    '*len(ifs)+then[3]['target']+'\n')

                ifidx += 1 if ifidx < len(ifs)-1 else 0

            fill_newline(2)

    if not notext:
        os.makedirs(dir_text, exist_ok=True)
        path = os.path.join(dir_text, filename+'.txt')
        print(f'[text][done] ... -> {path}')
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(text)
    else:
        print(f'[text][done] text not found')
