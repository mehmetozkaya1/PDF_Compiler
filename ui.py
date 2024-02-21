from tkinter import *
from tkinter import filedialog , font
from tkinter import messagebox
from PyPDF2 import PageObject, PdfReader, PdfWriter

master = Tk()

class App(Tk):
    def __init__(self):
        # Main adjustments
        master.title("Converter")
        master.resizable(False, False)
        bg_color = "#bec4c4"

        x , y = 400 , 50*4

        v = x*0.975

        button_font = font.Font(family = "Arial", size = 8, weight = "bold")

        # Canvas
        self.canvas = Canvas(master, width=x, height=y)
        self.canvas.pack()

        # First Top Frame
        self.top_frame = Frame(master, bg=bg_color, width=v, height= y/4-5)
        self.top_frame.place(anchor='n',x=x/2,y=y/4*0+5)

        # Second Top Frame
        self.top_frame2 = Frame(master, bg=bg_color, width=v, height= y/4-5)
        self.top_frame2.place(anchor='n',x=x/2,y=y/4*1+5)

        # Left Frame
        self.left_frame = Frame(master, bg=bg_color, width= v/3*2-5, height= y/4*2-5)
        self.left_frame.place(anchor='nw',x= x/80,y=y/4*2+5)

        # Right Frame
        self.right_frame = Frame(master, bg=bg_color, width= v/3, height= y/4*2-5)
        self.right_frame.place(anchor='ne',x= x-(x/80),y=y/4*2+5)




        # Input Label
        self.input_label = Label(self.top_frame, text="Please enter input files",fg="black", font=('Arial',10), bg=bg_color)
        self.input_label.place(anchor='w',x= x/20, y= (y/4*1-5)/2)

        # Input Button
        self.btn_input = Button(self.top_frame, text="Input Files", width= 14 , height=1, command=self.select_files, font=button_font)
        self.btn_input.place(anchor='w',x= (x/80)+x/3*2,y= (y/4*1-5)/2)


        # Output Label
        self.output_label = Label(self.top_frame2, text="Please enter output files",fg="black",font=('Arial',10), bg=bg_color)
        self.output_label.place(anchor='w',x= x/20, y= (y/4*1-5)/2)

        # Output Button
        self.btn_output = Button(self.top_frame2, text="Output Files", width=14, height=1, command=self.select_files2, font=button_font)
        self.btn_output.place(anchor='w',x= (x/80)+x/3*2,y= (y/4*1-5)/2)


        # Convert Button
        self.btn_convert = Button(self.right_frame, text="Convert", width=14, height=1, bg="#96ff9f", fg="black", command=self.convert, font=button_font)
        self.btn_convert.place(anchor='center',x= x/6, y= (y/4*1)/2)

        # Cancel Button
        self.btn_cancel = Button(self.right_frame, text="Cancel", width=14, height=1, bg="#fff196", fg="black", command=self.convert, font=button_font)
        self.btn_cancel.place(anchor='n',x= x/6, y= (y/4*2)/2)

        # Checkboxes
        self.var1 = IntVar(master)
        self.option1 = Checkbutton(self.left_frame, text="Clear Duplicates", onvalue=1, offvalue=0, variable=self.var1, bg=bg_color) #, font=("Arial",15)
        self.option1.place(anchor='nw',x= x/80, y = (y/2)/3*0+2)

        self.var2 = IntVar(master)
        self.option2 = Checkbutton(self.left_frame, text="Add Empty Pages", onvalue=1, offvalue=0,variable=self.var2, bg=bg_color)#, font=("Arial",15)
        self.option2.place(anchor='nw',x= x/80, y = (y/2)/3*1+2)
        
        self.var3 = IntVar(master)
        self.option3 = Checkbutton(self.left_frame, text="Useless Button", onvalue=1, offvalue=0,variable=self.var3, bg=bg_color)#, font=("Arial",15)
        self.option3.place(anchor='nw',x= x/80, y = (y/2)/3*2+2)
    
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

        with open(self.path+'/'+self.source.split('/')[-1], 'wb') as f:
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