# うんちく 0.3.0 Stable Build 17
# By Ken Shibata
# Last Edited Sep 24, 2018
# This software is licensed under the GNU GPL 3, the GNU LGPL 3, the CC BY 4.0, or the CC BY-SA 4.0. You should have received a copy of the GNU GPL 3 in Licenses/GNU/GPL/3, the GNU LGPL 3  in Licenses/GNU/LGPL/3, the CC BY 4.0 in Licenses/CC/BY/4, the CC BY-SA 4.0 in Licenses/CC/BY-SA/4. If not visit <gnu.org> or <creativecommons.org>.


__author__ = 'Ken Shibata'
__version__ = '0.3.0-stable'
__build__ = 17
__doc__ = 'うんちく {version} (Build {build})'.format(version=__version__, build=__build__)
__license__ = ['GNU GPL 3', 'GNU LGPL 3', 'CC BY 4.0', 'CC BY-SA 4.0']

import sys

class Transpile():
    def __init__(self, PSCode, PSPath):
        self.PSError = '''エラー {Code}（{Status}）
        {Sentence}文目
        {Explanation}'''
        self.PBError = False
        self.PBDebug = False # Default: False
        self.PSCode = PSCode
        self.PLSentences = self.PSCode.split('。')
        self.PSPath = PSPath
        # Clear target file
        x = open(self.PSPath, 'w')
        x.write('')
        x.close()
        del x
        self.PSWrite = open(self.PSPath, 'a')
        self.PDObjConnect = {'書いてや':['print', 'func'], '書く':['print', 'func'], '待ってくれへん':['time.sleep', 'func'],'書いて':['print', 'func'], '書いてね':['print', 'func'], '待って':['time.sleep', 'func']}
    def run(self):
        if self.PBDebug:
            print('Info    ' + self.PSCode.replace('\n', '\nInfo    '))
        self.PSWrite.write('import random\n\n')
        PIIndent = 0
        if self.PSCode[:2] == '　　':
          self.PSCode = self.PSCode[2:]
          self.PSCode = self.PSCode.replace('\n　　', '~~end~~')
          self.PSCode = self.PSCode.replace('\n', '')
          self.PSCode = self.PSCode.replace('~~end~~', '\n　　')
          if self.PBDebug:
              print('Info    Deleted two Square Spaces @ self.PSCode[:2]')
              print('Info    Deleted all newlines in self.PSCode')
          self.PLSentences = self.PSCode.split('。')
          if self.PBDebug:
              print('Info    Updated self.PLSentence w/ latest self.PSCode')
        else:
          print(self.PSError.format(Code='1', Status = '無視', Sentence='1', Explanation = '段落が見つかりません。'))
          self.PBError = True
        for PSSentence in self.PLSentences:
            if PSSentence == '':
                # print(self.PSError.format(Code='2', Status = '無視', Sentence=self.PLSentences.index(PSSentence) + 1, Explanation = '文に内容なし。'))
                # self.PBError = True
                continue
            if self.PBDebug:
                print('Info   ', end=' ')
            if 'って' in PSSentence:
                if self.PBDebug:
                  print('って', end=' ')
                PSVerb = PSSentence.split('って')[-1]
                PSNoun = PSSentence.split('って')
                PSNoun.pop(-1)
            elif 'を' in PSSentence:
                if self.PBDebug:
                  print('を　', end=' ')
                PSVerb = PSSentence.split('を')[-1]
                PSNoun = PSSentence.split('を')
                PSNoun.pop(-1)
            elif 'と' in PSSentence:
                if self.PBDebug:
                  print('と　', end=' ')
                PSVerb = PSSentence.split('と')[-1]
                PSNoun = PSSentence.split('と')
                PSNoun.pop(-1)
            else:
                if self.PBDebug:
                  print('変数',end=' ')
                PSVerb = PSSentence
                PSNoun = ''
            PSNounRaw = PSNoun
            PSNoun = ''
            for i in PSNounRaw:
                PSNoun += str(i)
            PSNoun = PSNoun.replace('「', '\'').replace('」', '\'')
            if PSVerb.find('\n　　') == 0:
                PSLine = ''
                PIIndent -= 2
            if 'もし' in PSVerb:
                if self.PBDebug:
                  print(PIIndent, end=', ')
                PSDetails = PSVerb.split('もし')
                PSDetails.pop(0)
                PSLine = '{}if {}:\n'.format(PIIndent * ' ', PSDetails[0].replace('<', ' < ').replace('<=', ' <= ').replace('>', ' > ').replace('=>', ' =>').replace('=', ' == ').replace('! == ', ' != '))
                PIIndent += 2
            elif 'は' in PSVerb:
                if self.PBDebug:
                  print(PIIndent, end=', ')
                PSLine = PIIndent * ' ' + PSVerb.replace('は', ' = ').replace('数入力にしてえや', 'float(input())').replace('入力にしてえや', 'input()').replace('乱数にしてえや', 'random.randint(1, 5)').replace('数入力にする', 'float(input())').replace('入力にする', 'input()').replace('乱数にする', 'random.randint(1, 3)') + '\n'
            elif self.PDObjConnect[PSVerb][1] == 'func':
                if self.PBDebug:
                  print(PIIndent, end=', ')
                if '+' in PSNoun or '-' in PSNoun or '*' in PSNoun or '/' in PSNoun:
                  PSLine = PIIndent * ' ' + '{Verb}(eval(str({Noun})))\n'.format(Verb = self.PDObjConnect[PSVerb][0], Noun = PSNoun)
                else:
                  PSLine = PIIndent * ' ' + '{Verb}({Noun})\n'.format(Verb = self.PDObjConnect[PSVerb][0], Noun = PSNoun)
            if self.PBDebug:
              if PSLine == '':
                print('None')
              else:
                print(PSLine.replace('\n', ''))
            self.PSWrite.write(PSLine)
        self.PSWrite.write('# うんちく 0.2.4\n')
        if self.PBError:
          self.PSWrite.write('# エラー：あり、無視\n')
        else:
          self.PSWrite.write('# えらー：なし\n')
    def save(self):
        self.PSWrite.close()

if __name__ == '__main__':
    if False:
        pass
#     if len(sys.argv) >= 2:
#         inp = open(sys.argv[1], 'r')
    else:
        inp = open(input('? File '), 'r')
    x = Transpile(inp.read(), 'out.py')
    inp.close()
    x.run()
    if x.PBDebug:
      print('Info    Run out.py (use import stat)')
    del x, inp
    import out
