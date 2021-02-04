#!/usr/bin/env python
# coding: utf-8

# In[2]:


from tkinter import Tk, Frame, Label, Button, Entry
from pygame import mixer
from os.path import basename
from PIL import ImageTk, Image
from glob import glob
from pandas.core.common import flatten
from pandas import read_csv


# In[3]:


audios = sorted(glob('data/wavs/'+'*.wav'))
ids = [basename(x).split('.')[0] for x in audios]
nb_audios = ['data/nb_wavs/'+basename(x) for x in audios]


# In[4]:


# Find corresponding images and nb_images
def find_corresponding(in_folder, ids):
    corr_paths = [glob(in_folder+fileID+'.*') for fileID in ids]
    corr_paths = [["NA"] if not x else x for x in corr_paths]
    return list(flatten(corr_paths))

img_paths = find_corresponding('data/imgs/', ids)
nb_img_paths = find_corresponding('data/nb_imgs/', ids)  


# In[5]:


info_tab=read_csv('data/info.csv')
info_tab.index = info_tab['index']

ori_label = [info_tab.loc[int(x),'call_lable'] for x in ids]
sc_label = [info_tab.loc[int(x),'neighbor_1'] for x in ids]

DEFAULT_IMG = 'data/default_img.png'
SR = 8000


# In[8]:


answers = []

def check(letter, view):
    answers.append(letter)
    with open('answers.txt', 'w') as f:
        for sound_id,a in zip(ids[0:len(answers)],answers):
            item = sound_id+';'+a
            f.write("%s\n" % item)
    f.close()
    unpackView(view)
           
def getView_answer(window):
    global index
    view = Frame(window) # frame with parent: window 
      
    progress_label = Label(view, text=str(index+1)+"/"+str(len(audios)))
    progress_label.pack(side="top")       
        
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
        
    button_continue = Button(view, text="Continue", command=lambda *args: unpackViewCont(view))
    button_continue.pack(side="bottom")    
        
    return view
        

def getView(window):
    view = Frame(window)
        
    progress_text = str(index+1)+"/"+str(len(audios))
    progress_label = Label(view, text=progress_text)
    progress_label.pack(side="top")
        
    spacer = Label(view, text=' ')
    spacer.pack(side="top")
        
    label = Label(view, text="Please assign to calltype")
    label.pack(side="top")        
        
    for calltype in ['agg', 'al', 'cc', 'ld', 'mo', 'sn', 'soc', 'Not a real call']:
        button_x = Button(view, text=calltype, command=lambda calltype=calltype: check(calltype, view))
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
    
def unpackView(view):
    global window
    view.pack_forget()
    getView_answer(window).pack()
    
def unpackViewCont(view):
    view.pack_forget()
    askQuestion()

def askQuestion():
    global window, index, button 
    if(number_of_questions == index + 1):
        Label(window, text="Thank you. You can close the window.").pack()
        return
    button.pack_forget()
    index += 1
    getView(window).pack()


index = -1
right = 0
number_of_questions = len(audios)

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




