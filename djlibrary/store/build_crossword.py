from PIL import Image, ImageDraw, ImageFont
from random import randint

class Crossword(object):
    def __init__(self):
        self.W = 15
        self.H = 15
        self.C = 200
        self.used = [[0 for i in range(self.H*2)] for j in range(self.W*2)]
        self.img = Image.new("RGB", (self.W*2*self.C, self.H*2*self.C), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.img)
        self.words = []
        self.letters = [[] for i in range(33)]
        self.font = ImageFont.load_default().font

    def add_rect(self, x, y):
        self.draw.rectangle((self.W*self.C + x*self.C, self.H*self.C + y*self.C, self.W*self.C + (x + 1)*self.C, self.H*self.C + (y + 1)*self.C), outline=(0, 0, 0))

    def add_word(self, word):
        if not len(self.words):
            clr = (randint(0, 255), randint(0, 255), randint(0, 255))
            self.draw.polygon([(self.W*self.C, self.H*self.C), (self.W*self.C, (1 + self.H)*self.C), ((self.W + 0.5)*self.C, (self.H + 0.5)*self.C)], fill=clr)
            #self.draw.text((0, 0),str(len(self.words)),(0,0,0), font=self.font)
            for x1 in range(len(word)):
                self.used[x1][0] = word[x1]
                self.add_rect(x1, 0)
                self.letters[ord(word[x1]) - ord('а')].append((x1, 0, 0))
            self.draw.text((self.W, self.H),str(len(self.words)),(0,0,0), font=self.font)
            self.words.append(word)
            return True
        else:
            for i, ch in enumerate(word):
                for x, y, f in self.letters[ord(ch) - ord('а')]:
                    if f:
                        tmp = 0
                        for x1 in range(x - i, x + len(word) - i):
                            if self.used[x1][y] and self.used[x1][y] != word[x1 - x + i]:
                                tmp = 1
                        if tmp:
                            continue
                        #self.draw.text((self.W + (x - i)*self.C, self.H + y*self.C),str(len(self.words)),(0,0,0), font=self.font)
                        for x1 in range(x - i, x + len(word) - i):
                            #print(x1, y)
                            self.used[x1][y] = word[x1 - x + i]
                            self.add_rect(x1, y)
                            self.letters[ord(word[x1 - x + i]) - ord('а')].append((x1, y, not f))
                        clr = (randint(0, 255), randint(0, 255), randint(0, 255))
                        self.draw.polygon([((self.W + x - i)*self.C, (y + self.H)*self.C), ((self.W + x - i)*self.C, (y + 1 + self.H)*self.C), ((self.W + x - i + 0.5)*self.C, (y + self.H + 0.5)*self.C)], fill=clr)
                    else:
                        tmp = 0
                        for y1 in range(y - i, y + len(word) - i):
                            if self.used[x][y1] and self.used[x][y1] != word[y1 - y + i]:
                                tmp = 1
                        if tmp:
                            continue
                        #self.draw.text((self.W + x*self.C, self.H + (y - i)*self.C),str(len(self.words)),(0,0,0), font=self.font)
                        for y1 in range(y - i, y + len(word) - i):
                            #print(x, y1)
                            self.used[x][y1] = word[y1 - y + i]
                            self.add_rect(x, y1)
                            self.letters[ord(word[y1 - y + i]) - ord('а')].append((x, y1, not f))
                        clr = (randint(0, 255), randint(0, 255), randint(0, 255))
                        self.draw.polygon([((self.W + x)*self.C, (y - i + self.H)*self.C), ((self.W + x + 1)*self.C, (y - i + self.H)*self.C), ((self.W + x + 0.5)*self.C, (y - i + self.H + 0.5)*self.C)], fill=clr)
                    self.words.append(word)
                    return True
        return False

    def build(self, inp_words):
        while len(inp_words):
            idx = randint(0, len(inp_words) - 1)
            if (self.add_word(inp_words[idx])):
                del inp_words[idx]
cw = Crossword()
cw.build(["карамзин", "окурок","олик", "трамвай", "петух"])
cw.img.show()
