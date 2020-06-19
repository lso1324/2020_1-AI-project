import re
import json
import subprocess
import collections
import Tkinter as tk

def extractExtensions(answerset):

  field_pattern = re.compile(r'(\w+)\(f\((\d+),(\d+)\)(?:,([0-9]+|[a-z][a-zA-Z0-9]*|"[^"]*"))?\)')
  extensions = collections.defaultdict(lambda: set())
  for l in answerset:
    try:
      args = field_pattern.match(l).groups()
      head = args[0]
      rest = [int(args[1]), int(args[2])]
      if args[3]:
        rest.append(str(args[3]).strip('"'))

      extensions[head].add(tuple(rest))
    except:
      pass
  return extensions


class Window:

  def __init__(self,answersets):

    self.answersets = answersets
    self.selected = 0
    self.selections = range(0,len(self.answersets))
    self.root = tk.Tk()
    self.main = tk.Frame(self.root)
    self.main.pack(fill=tk.BOTH, expand=1)
    self.canvas = tk.Canvas(self.main, bg="black")
    self.canvas.pack(fill=tk.BOTH, expand=1, side=tk.BOTTOM)
    self.selector = tk.Scale(self.main, orient=tk.HORIZONTAL, showvalue=0, command=self.select)

    self.items = []
    self.updateView()

  def select(self,which):
    self.selected = int(which)
    self.updateView()

  def updateView(self):
    self.selector.config(from_=0, to=len(self.answersets)-1)


    MAXSIZE=40

    def fieldRect(x,y,offset=MAXSIZE):
      x, y = int(x), int(y)

      return (x*MAXSIZE-offset/2, y*MAXSIZE-offset/2, x*MAXSIZE+offset/2, y*MAXSIZE+offset/2)


    for i in self.items:
      self.canvas.delete(i)

    self.items = []

    ext = extractExtensions(self.answersets[self.selected])

    maxx = max(map(lambda x: x[0], ext['map']))
    maxy = max(map(lambda x: x[1], ext['map']))
    self.root.geometry("{}x{}+0+0".format((maxx+1)*MAXSIZE, (maxy+2)*MAXSIZE))

    for (x, y) in ext['map']:
      self.items.append( self.canvas.create_rectangle( * fieldRect(x,y), fill='#FFF') )
    for (x, y) in ext['pool']:
      self.items.append( self.canvas.create_rectangle( * fieldRect(x,y), fill='#444') )
    for (x, y) in ext['mark']:
      self.items.append( self.canvas.create_oval( *fieldRect(x,y,10), fill='#000') )
    for (x, y, text) in ext['text']:
      fr = fieldRect(x,y)
      self.items.append( self.canvas.create_text( (fr[0]+fr[2])/2, (fr[1]+fr[3])/2, text=str(text), fill='#000') )

def display_tk(answersets):
  w = Window(answersets)


clingo = subprocess.Popen(
  "clingo --outf=2 asp.lp {maxans}".format(maxans=100),
  shell=True, stdout=subprocess.PIPE)

clingoout, clingoerr = clingo.communicate()
del clingo
clingoout = json.loads(clingoout)
witnesses = clingoout['Call'][0]['Witnesses']

display_tk(map(lambda witness: witness['Value'], witnesses))

tk.mainloop()