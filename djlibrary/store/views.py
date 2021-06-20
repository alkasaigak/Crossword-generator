from django.shortcuts import render, redirect
from django.views import generic
from PIL import Image, ImageDraw, ImageFont
from random import randint
import requests

cw_amount = 2

def get_meaning(word):
    try:
        content = requests.get(f'https://ru.wiktionary.org/wiki/{word}')
        unparsed = content.text.split('<span class="mw-headline" id="Значение">Значение</span>')[1].split('</li>')[0]
        print(unparsed)
        ans = ""
        cnt = 0
        for ch in unparsed:
            cnt += ch == '"'
            if not cnt % 2 and (ch in ' ,.?!' or (ord('а') <= ord(ch) and ord(ch) <= ord('я'))):
                ans += ch
        return f"{' '.join(ans.split()).replace('править', '')} ({word})"
    except:
        return f"({word})"
    
    
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
        self.font = ImageFont.load_default()

    def add_rect(self, x, y):
        self.draw.rectangle((self.W*self.C + x*self.C, self.H*self.C + y*self.C, self.W*self.C + (x + 1)*self.C, self.H*self.C + (y + 1)*self.C), outline=(0, 0, 0))

    def add_word(self, word):
        if not len(self.words):
            clr = (randint(100, 255), randint(100, 255), randint(100, 255))
            self.draw.polygon([(self.W*self.C, self.H*self.C), (self.W*self.C, (1 + self.H)*self.C), ((self.W + 0.5)*self.C, (self.H + 0.5)*self.C)], fill=clr)
            #self.draw.text((0, 0),str(len(self.words)),(0,0,0), font=self.font)
            for x1 in range(len(word)):
                self.used[x1][0] = word[x1]
                self.add_rect(x1, 0)
                self.letters[ord(word[x1]) - ord('а')].append((x1, 0, 0))
            self.draw.text((self.W, self.H),str(len(self.words)),(0,0,0), font=self.font)
            self.words.append([get_meaning(word), f"rgb{str(clr)}"])
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
                        clr = (randint(100, 255), randint(100, 255), randint(100, 255))
                        self.draw.polygon([((self.W + x - i)*self.C, (y + self.H)*self.C), ((self.W + x - i)*self.C, (y + 1 + self.H)*self.C), ((self.W + x - i + 0.5)*self.C, (y + self.H + 0.5)*self.C)], fill=clr)
                        self.draw.text(((self.W + x - i + 0.5)*self.C, (y + self.H + 0.5)*self.C),(0,0,0), font=self.font)
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
                        clr = (randint(100, 255), randint(100, 255), randint(100, 255))
                        self.draw.polygon([((self.W + x)*self.C, (y - i + self.H)*self.C), ((self.W + x + 1)*self.C, (y - i + self.H)*self.C), ((self.W + x + 0.5)*self.C, (y - i + self.H + 0.5)*self.C)], fill=clr)
                    self.words.append([get_meaning(word), f"rgb{str(clr)}"])
                    return True
        return False

    def build(self, inp_words):
        global cw_amount
        i = 0
        while len(inp_words) > 1 and i < 1000:
            print(i, inp_words)
            idx = randint(1, len(inp_words) - 1)
            if (self.add_word(inp_words[idx])):
                del inp_words[idx]
            i += 1
        cw_amount += 1
        self.img.save(f'static/media/out{cw_amount}.png');

from .forms import (
    BookFormset
)
from .models import Book, Author


def create_book_normal(request):
    global cw_amount
    template_name = 'store/create_normal.html'
    heading_message = 'Введите слова'
    if request.method == 'GET':
        formset = BookFormset(request.GET or None)
    elif request.method == 'POST':
        formset = BookFormset(request.POST)
        if formset.is_valid():
            arr = []
            arr.append('')
            cw = Crossword()
            for form in formset:
                name = form.cleaned_data.get('name')
                # save book instance
                if name:
                    arr.append(str(name))
                    Book(name=name).save()
            arr1 = arr
            cw.build(arr)
            print(arr)
            return render(request, 'store/list.html', context={'words': cw.words, 'fname': f'media/out{cw_amount}.png'})

    return render(request, template_name, {
        'formset': formset,
        'heading': heading_message,
    })


class BookListView(generic.ListView):

    model = Book
    context_object_name = 'books'
    template_name = 'store/list.html'
