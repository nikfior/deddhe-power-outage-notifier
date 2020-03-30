import requests
from bs4 import BeautifulSoup
import re
from tkinter import *

#import time
#start_time = time.time()



#Enter the keywords and don't forget to add the words with and without the acute accent over the stressed vowel(τους τόνους)
#It doesn't matter if it's capital or lower case
keywords=["μονα","μονά","ΥΨΗΛΑΝΤΟΥ","ΥΨΗΛΆΝΤΟΥ"]


keywords=[keyword.lower() for keyword in keywords]

##-----------------------------


#Enter the correct PrefectureID of the place of your interest.This will be improved in a future update.
response=requests.get('https://siteapps.deddie.gr/Outages2Public/?PrefectureID=10&MunicipalityID=&X-Requested-With=XMLHttpRequest')
soup = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
tables=soup.select('#tblOutages tbody tr')

cells=[tables[i].find_all('td') for i in range(len(tables)) ]

for i in range(len(cells)):
    for j in range(len(cells[0])):
        cells[i][j]=(re.sub(' +|\r\n',' ',cells[i][j].text)).strip()



cell_index=0
found_flag=False
cells_len=len(cells)
for i in range(cells_len):
    for j in range(len(keywords)):
        if (cells[cell_index][3].lower().find(keywords[j])!=-1):
            cell_index=cell_index+1
            found_flag=True
            break
    if not found_flag:
        del cells[cell_index]
    else:
        found_flag=False

        


####------------------for testing purposes-----test for the gui using already saved lists using pickle
##import pickle
##cells=pickle.load(open('pickles.p','rb'))
####-------------------------

#print("--- %s seconds ---" % (time.time() - start_time))
        
if len(cells)==0:
    exit()     

    
window=Tk()
window.title("Προγραμματισμένες διακοπές ρεύματος")
canvas=Canvas(window)
scroll_x = Scrollbar(window, orient="horizontal", command=canvas.xview)
scroll_y = Scrollbar(window, orient="vertical", command=canvas.yview)
frame=Frame(canvas)
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
#label_width=int((screen_width-20)/6)
label_width=int((screen_width-30)/2)

titleLbl=[]
titleLbl.append(Label(frame,text="Από",borderwidth=3,relief="solid"))
titleLbl.append(Label(frame,text="Έως",borderwidth=3,relief="solid"))
titleLbl.append(Label(frame,text="Δήμος/Κοινότητα",borderwidth=3,relief="solid"))
titleLbl.append(Label(frame,text="Περιγραφή",borderwidth=3,relief="solid"))
titleLbl.append(Label(frame,text="Αριθμός Σημειώματος",borderwidth=3,relief="solid"))
titleLbl.append(Label(frame,text="Σκοπός Διακοπής",borderwidth=3,relief="solid"))

for i in range(len(cells[0])):
    titleLbl[i].grid(column=i,row=0,sticky="nsew")

cellsLbl=[[Label(frame,text=cells[i][j],borderwidth=1,relief="solid",wraplength=label_width) for j in range(len(cells[0]))] for i in range(len(cells))]

    
for i in range(len(cells)):
    for j in range(len(cells[0])):
        cellsLbl[i][j].grid(column=j,row=1+i,sticky="nsew") 


#make vertical scroll
        
canvas.create_window(0, 0, anchor='nw', window=frame)
canvas.update_idletasks()

canvas.configure(scrollregion=canvas.bbox('all'),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
scroll_x.pack(fill='x', side='bottom')
scroll_y.pack(fill='y', side='right')
canvas.pack(fill='both', expand=True, side='left')



canvas.update_idletasks()
framewidth=frame.winfo_reqwidth()+25
frameheight=frame.winfo_reqheight()+25
positionRight = int(screen_width/2 - framewidth/2)
positionDown = int(screen_height/2 - frameheight/2)
window.geometry("{}x{}+{}+{}".format(framewidth,frameheight,positionRight, positionDown))


window.mainloop()
