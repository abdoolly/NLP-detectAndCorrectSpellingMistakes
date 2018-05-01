import tkinter as Tkinter
from tkinter.filedialog import askopenfilename

from funcy import compose
from app.core.spellcheckers.fullTextSearchSpellChecker import fullTextSearchSpellChecker


class DesktopInitializer:
    title = 'Awesome Spell checker'
    textBox: Tkinter.Text = None

    def __init__(self):
        self.root = Tkinter.Tk()
        self.initializeDesktop(self.root)
        self.makeMenuBar(self.root)
        self.root.mainloop()

    # This is where we launch the file manager
    def OpenFile(self):
        name = askopenfilename(
            filetypes=(("Text File", "*.txt"), ("All Files", "*.*")),
            title="Choose a file."
        )

        # Using try in case user types in unknown file or closes without choosing a file.
        try:
            with open(name, 'r') as UseFile:
                self.setTextData('Processing text...')
                self.sendToSpellCheck(UseFile.read())
        except ValueError as err:
            print(err)

    # initialize main desktop items
    def initializeDesktop(self, tk: Tkinter):
        compose(
            self.setTextArea,
            self.setButtons,
            self.setAppWindowSize,
            self.setAppTitle,
        )(tk)

    # set title
    def setAppTitle(self, tk: Tkinter):
        tk.title(self.title)
        return tk

    # setting app window size
    def setAppWindowSize(self, tk: Tkinter):
        tk.geometry('500x500')
        return tk

    # setting app buttons
    def setButtons(self, tk: Tkinter):
        # browse button
        browseBtn = Tkinter.Button(master=tk, text='Browse', command=self.OpenFile, bg='white')
        browseBtn.pack()

        # spell check button
        spellCheckBtn = Tkinter.Button(master=tk, text='Spell check', command=self.processTextAreaInput, bg='white')
        spellCheckBtn.pack()

        clearTextAreaBtn = Tkinter.Button(master=tk, text='Clear', command=self.setTextData, bg='white')
        clearTextAreaBtn.pack()

        return tk

    # set text area
    def setTextArea(self, tk: Tkinter):
        text = Tkinter.Text(master=tk, bg='white')

        text.tag_configure('bold_italics',
                           font=('Verdana', 12, 'bold', 'italic'))

        text.tag_configure('big',
                           font=('Verdana', 24, 'bold'))
        text.tag_configure('color',
                           foreground='blue',
                           font=('Tempus Sans ITC', 14))

        text.tag_configure('groove',
                           relief=Tkinter.GROOVE,
                           borderwidth=2)

        text.tag_bind('bite',
                      '<1>',
                      lambda e, t=text: t.insert(Tkinter.END, "Text"))

        text.pack(side=Tkinter.LEFT)
        self.textBox = text
        return tk

    # make a menu bar
    def makeMenuBar(self, tk: Tkinter):
        menu = Tkinter.Menu(master=tk, bg='white')
        tk.config(menu=menu)
        file = Tkinter.Menu(menu)
        # add the exit option
        file.add_command(label='Exit', command=lambda: exit())

        # put a file menu
        menu.add_cascade(label='File', menu=file)

    # set data in text area
    def setTextData(self, text=''):
        self.textBox.delete('1.0', Tkinter.END)
        self.textBox.insert('1.0', text)

    # spell check data in text area
    def processTextAreaInput(self):
        text = self.textBox.get('1.0', Tkinter.END)
        self.sendToSpellCheck(text)

    # send the text to get spell checked and viewed in the text area after it was processed
    def sendToSpellCheck(self, text):
        # making something like a loader which will man the text is being processed
        self.setTextData('Processing text...')

        correctedText = fullTextSearchSpellChecker.spellCheckDocument(text)

        # setting the newly corrected text
        self.setTextData(correctedText)
