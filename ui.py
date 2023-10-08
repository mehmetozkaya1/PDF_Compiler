from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PyPDF2 import PageObject, PdfReader, PdfWriter

master = Tk()

class App(Tk):
    def __init__(self):
        # Main adjustments
        master.title("Converter")
        master.resizable(False, False)
        bg_color = "grey"

        x = 500
        y = 250

        # Canvas
        self.canvas = Canvas(master, width=x, height=y)
        self.canvas.pack()

        # First Top Frame
        self.top_frame = Frame(master, bg=bg_color, width= x * 0.95, height= y * 0.15)
        self.top_frame.place(x= x * 0.025, y= y*0.025)

        # Second Top Frame
        self.top_frame2 = Frame(master, bg=bg_color, width= x * 0.95, height= y * 0.15)
        self.top_frame2.place(x= x * 0.025, y= y*0.2)

        # Left Frame
        self.left_frame = Frame(master, bg=bg_color, width= x * 0.69, height= y * 0.62)
        self.left_frame.place(x= x * 0.025, y= y*0.37)

        # Right Frame
        self.right_frame = Frame(master, bg=bg_color, width= x * 0.25, height= y * 0.62)
        self.right_frame.place(x= x * 0.73, y= y*0.37)

        # Input Label
        self.input_label = Label(self.top_frame, text="Please enter input files",fg="black", bg=bg_color)
        self.input_label.place(x=x*0.05, y=y*0.037)

        # Input Button
        self.btn_input = Button(self.top_frame, text="Input Files", width=15, height=1, command=self.select_files)
        self.btn_input.place(x=x*0.7, y=y*0.03)

        # Output Label
        self.output_label = Label(self.top_frame2, text="Please enter output files",fg="black", bg=bg_color)
        self.output_label.place(x=x*0.05, y=y*0.037)

        # Output Button
        self.btn_output = Button(self.top_frame2, text="Output Files", width=15, height=1, command=self.select_files2)
        self.btn_output.place(x=x*0.7, y=y*0.03)

        # Convert Button
        self.btn_convert = Button(self.right_frame, text="Convert", width=15, height=2, bg="green", fg="white", command=self.convert)
        self.btn_convert.place(x=x*0.01, y=y*0.13)

        # Cancel Button
        self.btn_cancel = Button(self.right_frame, text="Cancel", width=15, height=2, bg="red", fg="white")
        self.btn_cancel.place(x=x*0.01, y=y*0.3)

        # Checkboxes
        self.var1 = IntVar(master)
        self.option1 = Checkbutton(self.left_frame, text="Clear Empty Pages", onvalue=1, offvalue=0, variable=self.var1, font=("Verdana",15), bg=bg_color)
        self.option1.place(x = x* 0.005, y = y * 0.005)

        self.var2 = IntVar(master)
        self.option2 = Checkbutton(self.left_frame, text="Add Empty Pages", onvalue=1, offvalue=0,variable=self.var2, font=("Verdana",15), bg=bg_color)
        self.option2.place(x = x* 0.005, y = y * 0.23)
        
        self.var3 = IntVar(master)
        self.option3 = Checkbutton(self.left_frame, text="Option 3", onvalue=1, offvalue=0,variable=self.var3, font=("Verdana",15), bg=bg_color)
        self.option3.place(x = x* 0.005, y = y * 0.45)
    
    def page_scan(self, reader):

        pages = [] #sayfa listesi
        for pageNum in range(len(reader.pages)):
            pageObj = reader.pages[pageNum]
            pages.append(pageObj)
        
        return pages

    def select_files(self):
        try:
            self.source = filedialog.askopenfile().name
            self.input_label.config(text=self.source)
        except:
            error_msg = "Couldn't select the input file directory!"
            messagebox.showerror("Error", error_msg)

    def select_files2(self):
        try:
            self.path = filedialog.askdirectory()
            self.output_label.config(text=self.path)
        except:
            error_msg = "Couldn't select the output file directory!"
            messagebox.showerror("Error", error_msg)

    def file_reader(self, source):
        self.sourceFile = open(source,'rb')#dosyayi oku
        pdf_reader = PdfReader(self.sourceFile)

        listP = self.page_scan(reader = pdf_reader)
        return listP

    def close_reader(self, sourceFile):
        sourceFile.close()

    def pdf_writer(self, listP):
        pdf_writer = PdfWriter()

        for page in listP:
            pdf_writer.add_page(page)

        with open('out.pdf', 'wb') as f:
            pdf_writer.write(f)

    def convert(self):
        try:
            option1 = self.var1.get()
            option2 = self.var2.get()
            option3 = self.var3.get()

            listP = self.file_reader(self.source)

            if option1 :
                listP = self.clear_empties(listP)
            if option2 :
                listP = self.add_blanks(listP)
            if option3 :
                self.method3()

            self.pdf_writer(listP)

        except:
            error_msg = "Couldn't get the checkbox info. Please try again!"
            messagebox.showerror("Error", error_msg)

    def add_blanks(self, pages = list()):
        try:
            # Blanks adding codes
            newPages = list()
            h = 210
            w = 297

            empty = PageObject.create_blank_page(width=w, height=h)

            count = len(pages)# bu bir gun for dongusu olacak
            c = 0
            while c < count:
                for i in range(2):
                    if i%2 :
                        newPages.append(empty)
                        print('bos')
                    else :
                        newPages.append(pages[c])
                c += 1

            return newPages
        
        except:
            error_msg = "An error occured while adding blanks between the pages."
            messagebox.showerror("Error", error_msg)

    def clear_empties(self, pages=list()):
        try:
            # Empty page cleaning method
            oldStr = str()
            newPages = list()

            for page in range(len(pages)-1,-1,-1):
                tmpStr = pages[page].extract_text()[-7:]
                print(page,tmpStr)

                if oldStr != tmpStr:
                    newPages.append(pages[page])
                    oldStr  = tmpStr

            newPages.reverse()

            return newPages
        except:
            error_msg = "An error occured while clearing empty pages."
            messagebox.showerror("Error", error_msg)

    def method3(self):
        try:
            # Method 3 Codes
            print("Method")
        except:
            error_msg = "An error occured while <method3>"
            messagebox.showerror("Error", error_msg)

app = App()
master.mainloop()