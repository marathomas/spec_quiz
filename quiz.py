#!/usr/bin/env python
# coding: utf-8

# In[1]:


print("Wait for build...")

from tkinter import Tk, Frame, Label, Button, Entry
from time import sleep
from pygame import mixer
from os.path import basename
from time import sleep
from PIL import ImageTk, Image
from glob import glob
from pandas.core.common import flatten
from pandas import read_csv


# In[2]:


audios = sorted(glob('data/wavs/'+'*.wav'))


# In[3]:


# Find corresponding images
ids = [basename(x).split('.')[0] for x in audios]
img_paths = [glob('data/imgs/'+fileID+'.*') for fileID in ids]
img_paths = [["NA"] if not x else x for x in img_paths] # Replace empty lists with "NA"
img_paths = list(flatten(img_paths)) # Flatten list


# In[4]:


# Find corresponding nb images
nb_img_paths = [glob('data/nb_imgs/'+fileID+'.*') for fileID in ids]
nb_img_paths = [["NA"] if not x else x for x in nb_img_paths] # Replace empty lists with "NA"
nb_img_paths = list(flatten(nb_img_paths)) # Flatten list


# In[5]:


info_tab=read_csv('data/info.csv')
info_tab.index = info_tab['index']
ori_label = [info_tab.loc[int(x),'call_lable'] for x in ids]
sc_label = [info_tab.loc[int(x),'neighbor_1'] for x in ids]


# In[6]:


DEFAULT_IMG = 'data/default_img.png'
SR = 8000


# In[7]:


answers = []
ori_correct = 0
sc_correct = 0
neither_correct = 0

class Question:
    def __init__(self, question, answers):
        self.question = question
        self.answers = answers

    def check(self, letter, view):
        answers.append(letter)
        with open('answers.txt', 'w') as f:
            for sound_id,a in zip(ids[0:len(answers)],answers):
                item = sound_id+';'+a
                f.write("%s\n" % item)
        self.unpackView(view)
        
    
    def getView_answer(self, window):
        global index, ori_correct, sc_correct, neither_correct
        view = Frame(window)  
        
        if answers[index]==ori_label[index]:
            answertype='Manual assignment wins!'
            ori_correct += 1
        elif answers[index]==sc_label[index]:
            answertype='Nearest neighbor assignment wins!'
            sc_correct += 1
        else:
            answertype = 'Neither assignment wins.'
            neither_correct += 1
            
        progress_text = str(index+1)+"/"+str(len(audios))
        progress_label = Label(view, text=progress_text)
        progress_label.pack(side="top")
        
        status_text = "Manual: "+str(ori_correct)+" | Nearest Neighbor: "+str(sc_correct)+" | Neither: "+str(neither_correct)
        status_label = Label(view, text=status_text)
        status_label.pack(side="top")
        
        info_text = "Your choice: "+str(answers[index])
        info_label = Label(view, text=info_text)
        info_label.pack(side="top")    
        
        spacer = Label(view, text=' ')
        spacer.pack(side="top")
        
        label = Label(view, text="Five nearest neighbors:", bd=4)
        label.pack(side="top")
        
        #info = Label(view, text=audios[index])
        #info.pack(side="top")
        
        button_m = Button(view, text="Play sound again",command=play_music)
        button_m.pack(side="top")
        
        # Show spec
        img = show_nb_img()
        spec_img = Label(view, image=img)
        spec_img.pack(side = "top", fill = "both", expand = "yes")
        
        button_continue = Button(view, text="Continue", command=lambda *args: self.unpackViewCont(view))
        button_continue.pack(side="bottom")
        
        
        return view
        


    def getView(self, window):
        global ori_correct, sc_correct, neither_correct
        view = Frame(window)
        
        progress_text = str(index+1)+"/"+str(len(audios))
        progress_label = Label(view, text=progress_text)
        progress_label.pack(side="top")
        
        status_text = "Manual: "+str(ori_correct)+" | Nearest Neighbor: "+str(sc_correct)+" | Neither: "+str(neither_correct)
        status_label = Label(view, text=status_text)
        status_label.pack(side="top")
        
        spacer = Label(view, text=' ')
        spacer.pack(side="top")
        
        label = Label(view, text=self.question)
        button_a = Button(view, text="agg", command=lambda *args: self.check("agg", view))
        button_b = Button(view, text="al", command=lambda *args: self.check("al", view))
        button_c = Button(view, text="cc", command=lambda *args: self.check("cc", view))
        button_d = Button(view, text="ld", command=lambda *args: self.check("ld", view))
        button_e = Button(view, text="mo", command=lambda *args: self.check("mo", view))
        button_f = Button(view, text="sn", command=lambda *args: self.check("sn", view))
        button_g = Button(view, text="soc", command=lambda *args: self.check("soc", view))
        button_h = Button(view, text="Not a real call", command=lambda *args: self.check("Not a real call", view))
        
        spacer = Label(view, text=' ')
        info = Label(view, text=audios[index])
        
        button_m = Button(view, text="Play sound",command=play_music)

        label.pack(side="top")
        button_a.pack(side="top")
        button_b.pack(side="top")
        button_c.pack(side="top")
        button_d.pack(side="top")
        button_e.pack(side="top")
        button_f.pack(side="top")
        button_g.pack(side="top")
        button_h.pack(side="top")
        
        spacer.pack(side="top")
        
        button_m.pack(side="top")
        info.pack(side="top")
        
        # Show spec
        img = show_img()
        spec_img = Label(view, image=img)
        spec_img.pack(side = "bottom", fill = "both", expand = "yes")

        return view
    
    def unpackView(self, view):
        view.pack_forget()
        show_answer()
    
    def unpackViewCont(self, view):
        view.pack_forget()
        askQuestion()
        
def show_answer():
    global questions, window, index
    questions[index].getView_answer(window).pack()

def askQuestion():
    global questions, window, index, button 
    if(len(questions) == index + 1):
        Label(window, text="Thank you for answering the questions.").pack()
        with open('answers.txt', 'w') as f:
            for sound_id,a in zip(ids,answers):
                item = sound_id+';'+a
                f.write("%s\n" % item)
        return
    button.pack_forget()
    index += 1
    questions[index].getView(window).pack()


questions = [Question('Please assign to call type group: ', ['random', 'random', 'random'])]*len(audios)

index = -1
right = 0
number_of_questions = len(questions)

#pygame.mixer.pre_init(SR, -16, 1, 262144)
#pygame.mixer.init()
mixer.pre_init(SR, -16, 1, 262144)
mixer.init()


def play_music():
    global questions, window, index, button, right, number_of_questions
    #pygame.mixer.music.load(audios[index])
    #pygame.mixer.music.play()
    mixer.music.load(audios[index])
    mixer.music.play()

def show_img():
    global img, index
    if img_paths[index] != 'NA':
        image1 = Image.open(img_paths[index])
    else:
        image1 = Image.open(DEFAULT_IMG)
    img = ImageTk.PhotoImage(image1)
    return img

def show_nb_img():
    global img, index
    if nb_img_paths[index] != 'NA':
        image1 = Image.open(nb_img_paths[index])
    else:
        image1 = Image.open(DEFAULT_IMG)
    img = ImageTk.PhotoImage(image1)
    return img
    
    
window = Tk()
window.title('Meerkat Sound Classification')
window.geometry("800x650")
button = Button(window, text="Start", command=askQuestion)
button.pack()

window.mainloop()


# In[ ]:




