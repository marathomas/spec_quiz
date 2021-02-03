#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import Tk, Frame, Label, Button, Entry
from pygame import mixer
from os.path import basename
from PIL import ImageTk, Image
from glob import glob
from pandas.core.common import flatten
from pandas import read_csv


# In[2]:


audios = sorted(glob('data/wavs/'+'*.wav'))
ids = [basename(x).split('.')[0] for x in audios]
nb_audios = ['data/nb_wavs/'+basename(x) for x in audios]


# In[3]:


# Find corresponding images and nb_images
def find_corresponding(in_folder, ids):
    corr_paths = [glob(in_folder+fileID+'.*') for fileID in ids]
    corr_paths = [["NA"] if not x else x for x in corr_paths]
    return list(flatten(corr_paths))

img_paths = find_corresponding('data/imgs/', ids)
nb_img_paths = find_corresponding('data/nb_imgs/', ids)  


# In[4]:


info_tab=read_csv('data/info.csv')
info_tab.index = info_tab['index']

ori_label = [info_tab.loc[int(x),'call_lable'] for x in ids]
sc_label = [info_tab.loc[int(x),'neighbor_1'] for x in ids]

DEFAULT_IMG = 'data/default_img.png'
SR = 8000


# In[26]:


answers = []
ori_correct, sc_correct, neither_correct = 0,0,0

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

        button_m = Button(view, text="Play sound",command=play_music)
        button_m.pack(side="top")
        
        button_m = Button(view, text="Play nearest neighbor sound",command=play_nb_music)
        button_m.pack(side="top")
        
        
        # Show spec
        img = show_image(nb_img_paths, False)
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
        label.pack(side="top")        
        
        for calltype in ['agg', 'al', 'cc', 'ld', 'mo', 'sn', 'soc', 'Not a real call']:
            button_x = Button(view, text=calltype, command=lambda calltype=calltype: self.check(calltype, view))
            button_x.pack(side="top")
        
        spacer = Label(view, text=' ')
        spacer.pack(side="top")
        
        button_m = Button(view, text="Play sound",command=play_music)
        button_m.pack(side="top")
        
        info = Label(view, text=audios[index])
        info.pack(side="top")
        
        # Show spec
        img = show_image(img_paths, True)
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
        Label(window, text="Thank you. You can close the window.").pack()
        return
    button.pack_forget()
    index += 1
    questions[index].getView(window).pack()


questions = [Question('Please assign to call type group: ', ['random', 'random', 'random'])]*len(audios)

index = -1
right = 0
number_of_questions = len(questions)

mixer.pre_init(SR, -16, 1, 262144)
mixer.init()


def play_music():
    global questions, window, index, button, right, number_of_questions
    mixer.music.load(audios[index])
    mixer.music.play()

def play_nb_music():
    global questions, window, index, button, right, number_of_questions
    mixer.music.load(nb_audios[index])
    mixer.music.play()

def show_image(image_path, do_resize):
    global img, index
    if image_path[index] != 'NA':
        image1 = Image.open(image_path[index])
    else:
        image1 = Image.open(DEFAULT_IMG)
    if do_resize:
        image1 = image1.resize((360 , 240), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(image1)
    return img
    
    
window = Tk()
window.title('Meerkat Sound Classification')
window.geometry("800x650")
button = Button(window, text="Start", command=askQuestion)
button.pack()

window.mainloop()


# In[ ]:




