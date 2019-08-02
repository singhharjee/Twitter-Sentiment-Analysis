import re
import matplotlib.pyplot as plt
import numpy as np
import tweepy
from textblob import TextBlob  
from tweepy import OAuthHandler
from tkinter import Tk,Label,Entry,Text,END,Button,PhotoImage





api_key=""
api_secret_key=""

access_token =""
access_token_secret=""




auth = OAuthHandler(api_key, api_secret_key)                # set access token and secret

auth.set_access_token(access_token, access_token_secret)    # create tweepy API object to fetch tweets

api = tweepy.API(auth)


root = Tk()     #main GUI window
root.title("Twitter Sentiment Analysis") 
root.geometry('1000x800')
root.configure(bg="#E1E8ED")
root.iconbitmap(r"E:\Twitter_Logo_Blue.ico")

icon =PhotoImage(file = r"E:\oauth_application.png")    # taking image from the directory and storing the source in a variable

icon1=PhotoImage(file=r"E:\sentimentanalysis.png")

background =Label(root, image = icon,bg="#E1E8ED")   # displaying the picture using a 'Label' by passing the 'picture' variriable to 'image' parameter
background.pack()
background1=Label(root,image=icon1)
background1.pack(side="bottom",expand=True)

label1 = Label(root, text="Search",font="Helvetica 20 bold",bg="#E1E8ED")   #get data from the user

E1 = Entry(root, bd =5,font="Helvetica 15",bg="#F5F8FA")



def tweet():        #master code,here lies the main code for analysis

    topics=E1.get()
    try:
        tweets=api.search(q=topics,count=1000)
        #print(tweets)   
        positive=0
        negative=0
        neutral=0
        for t in tweets:
            text = clean_data(t.text)     #clean_data()is defined after this function
            #print(text)
            analysis=TextBlob(text)
                    
            if analysis.sentiment.polarity>0:
                positive+=1
            elif analysis.sentiment.polarity<0:
                negative+=1
            elif analysis.sentiment.polarity==0:
                neutral+=1
  
        total=positive+negative+neutral
        posperc=round((positive*100)/total,2)
        negperc=round((negative*100)/total,2)
        neuperc=round((neutral*100)/total,2)

        
        T = Text(root,height=9, width=50,bd=5,font="Helvetica 15",bg="#F5F8FA")
        T.pack()
        T.insert(END,"********************************************************************"+"\n")
        T.insert(END,"No. of positive tweets: "+str(positive)+"\n")
        T.insert(END,"No. of negative tweets: "+str(negative)+"\n")
        T.insert(END,"No. of neutral tweets: "+str(neutral)+"\n"+"\n")
        T.insert(END,"Percentage of positive tweets: "+str(posperc)+"%"+"\n")
        T.insert(END,"Percentage of negative tweets: "+str(negperc)+"%"+"\n")
        T.insert(END,"percentage of neutral tweets: "+str(neuperc)+"%"+"\n")
        T.insert(END,"********************************************************************")
        graph(positive,negative,neutral,topics)       #graph() is defined after clean_data()
    except ZeroDivisionError:
        t1=Text(root,height=1, width=60,font="Helvetica 15",bd=5,bg="#F5F8FA")
        t1.pack()
        t1.insert(END,"OOPS!!!Twitter doesn't have any tweets regarding the entered topic")
    except tweepy.error.TweepError:
        t2=Text(root,height=1, width=45,font="Helvetica 15",bd=5,bg="#F5F8FA")
        t2.pack()
        t2.insert(END,"NO INTERNET!!! Check your internet connection")



def clean_data(tweets):                 #cleaning up the data which is not required
    return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweets).split()) 

 






def graph(positive,negative,neutral,topics):                 #plotting Graph
    #fig, ax = plt.subplots()
    index = np.arange(1)
    bar_width = 0.1
    opacity = 1

    plt.bar(index, positive, bar_width, alpha=opacity, color='g', edgecolor='w', label='positive')


    plt.bar(index + bar_width, negative, bar_width, alpha=opacity, color='r', edgecolor='w', label='negative')


    plt.bar(index + bar_width+ bar_width, neutral, bar_width, alpha=opacity, color='b', edgecolor='w', label='neutral')


    plt.xticks(index+bar_width, [topics],family='fantasy')
    plt.xlabel('Topics',fontweight='bold',fontsize='10')
    plt.ylabel('Sentiments',fontweight='bold',fontsize='10')
    plt.title('Twitter Sentiment Analysis',fontweight='bold', color = 'white', fontsize='17', horizontalalignment='center',backgroundcolor='black')
    plt.legend()
        
    plt.tight_layout()
    plt.show()
       

    
     

submit = Button(root, text ="Submit", command = tweet,font="Helvetica 16",bg="#E1E8ED",bd=5,relief="raised")
label1.pack()
E1.pack()

submit.pack()


root.mainloop()

