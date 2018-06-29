from tkinter import* 
from tkinter.simpledialog import askstring
from tkinter.filedialog   import asksaveasfilename
from tkinter.messagebox import askokcancel
root=Tk()
root.title("TEXT EDITOR")

class Quitter(Frame):
    
    def __init__(self, parent=None):          

        Frame.__init__(self, parent)
        self.pack()
        widget = Button(self, padx=15,pady=15,font=("arial",15),text='Quit', command=self.quit)
        widget.pack(expand=YES, fill=BOTH, side=LEFT)

    def quit(self):

        ans = askokcancel(' EXIT', "Press OK To Quit")
        if ans: Frame.quit(self)


class ScrolledText(Frame):
    
    def __init__(self, parent=None, text='', file=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)               
        self.makewidgets()
        self.settext(text, file)
        
    def makewidgets(self):
        sbar = Scrollbar(self)
        text = Text(self, relief=SUNKEN)
        sbar.config(command=text.yview)                  
        text.config(yscrollcommand=sbar.set)           
        sbar.pack(side=RIGHT, fill=Y)                   
        text.pack(side=LEFT, expand=YES, fill=BOTH)     
        self.text = text
        
    def settext(self, text='', file=None):
        if file: 
            text = open(file, 'r').read()
        self.text.delete('1.0', END)                   
        self.text.insert('1.0', text)                  
        self.text.mark_set(INSERT, '1.0')              
        self.text.focus()

    def gettext(self):                               
        return self.text.get('1.0', END+'-1c')         



class SimpleEditor(ScrolledText):
    
    def __init__(self, parent=None, file=None): 
        frm = Frame(parent)
        frm.pack(fill=X)
        Button(frm, padx=15,pady=15,font=("arial",15),text='Save',  command=self.onSave).pack(side=LEFT)
        Button(frm, padx=15,pady=15,font=("arial",15),text='Cut',   command=self.onCut).pack(side=LEFT)
        Button(frm, padx=15,pady=15,font=("arial",15),text='Copy',  command=self.onCopy).pack(side=LEFT)
        Button(frm, padx=15,pady=15,font=("arial",15),text='Paste', command=self.onPaste).pack(side=LEFT)
        Button(frm, padx=15,pady=15,font=("arial",15),text='Find', command=self.onFind).pack(side=LEFT)
        Quitter(frm).pack(side=LEFT)
        ScrolledText.__init__(self, parent, file=file) 
        self.text.config(font=('TIMESNEWROMAN', 25, 'normal'))

    def onSave(self):
        filename = asksaveasfilename()
        if filename:
            alltext = self.gettext()                      
            open(filename, 'w').write(alltext)

    def onCut(self):
        text = self.text.get(SEL_FIRST, SEL_LAST)        
        self.text.delete(SEL_FIRST, SEL_LAST)            
        self.clipboard_clear()              
        self.clipboard_append(text)

    
    def onCopy(self):
        self.clipboard_clear()
        text=self.text.get(SEL_FIRST,SEL_LAST)
        self.clipboard_append(text)
      
    def onPaste(self):                                    
        try:
            text = self.selection_get(selection='CLIPBOARD')
            self.text.insert(INSERT, text)
        except TclError:
            pass
    
    def onFind(self):
        target = askstring('SimpleEditor', 'Search String?')
        if target:
            where = self.text.search(target, INSERT, END)  
            if where:                                    
                print (where)
                pastit = where + ('+%dc' % len(target))   
               #self.text.tag_remove(SEL, '1.0', END)     
                self.text.tag_add(SEL, where, pastit)     
                self.text.mark_set(INSERT, pastit)         
                self.text.see(INSERT)                    
                self.text.focus()

if __name__ == '__main__':
    try:
        SimpleEditor(file=sys.argv[1]).mainloop()   
    except IndexError:
        SimpleEditor().mainloop()
