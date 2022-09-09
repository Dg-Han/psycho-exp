
from tkinter import *
from tkinter.messagebox import *
import random
'''
BART:仿真气球冒险试验。已知每个气球的操作（充气）上限，且每个气球在达到充气上限前的每次充气的爆炸概率一致。气球在爆炸前充气次数越多，收益越高；但一旦气球爆炸，将不会得到任何收益。
count为试次计数，trial为试次内收益，total为总收益，BART_result记录每次试次结果（未爆炸前终止为充气次数，爆炸为-1）

SBPS为状态测量量表
每进行一个BART试次后施测SBPS中一个条目
'''

SBPS_Q=['时间过得比平时慢。','我容易分心。','现在，似乎所有的事情都能激怒我。','我希望时间能过得更快。',
        '对我来说，所有的事情都是重复的和乏味的。','我感到沮丧。','我不得不做一些对我毫无价值的事情。','我觉得无聊。',
        '对我来说，时间是漫长的。','我比平时更喜怒无常。','我感到焦虑不安。','我觉得空虚。',
        '我很难集中我的注意力。','我想做一些有趣的事情，但是什么都吸引不了我。','时间流逝的非常缓慢。','我希望我做的是令我更兴奋的事情。',
        '我集中注意的时间比平时更短。','现在我没有耐心。','我正在浪费时间，如果把这些时间花在别的事情上会更好。','我在走神。',
        '我希望某件事情发生，但我不确定那是什么事。','此刻，时间好像过得很慢。','我对我周围的人都感到恼火。','我觉得我正在坐等某些事情的发生。']
SBPS_S=[0 for i in range(24)]
BART_result=[]

def st():
    global pd
    if not pd:
        pd=True

class BART_Ui(Frame):
    def __init__(self,master=None):
        global strt
        Frame.__init__(self,master)
        self.master.title('Balloon Analogue Risk Task')
        self.master.geometry('1080x720')
        if strt:
            self.createWidgets1()
        else:
            self.createWidgets()
        
    def createWidgets(self):
        global strt
        strt=True
        self.top=self.winfo_toplevel()
        self.lb=Label(self.top,text='指导语：接下来你要完成一项给气球充气的任务。\n\
每个气球充气次数的上限是128，且每次充气都有相等的概率会爆炸。\n\
你可以在气球爆炸前停止充气，这将得到与充气次数成正比的收益；\n\
但一旦气球爆炸，该气球的收益将会清零。\n\
可以通过鼠标左键单击pump按钮进行充气，\n\
也可以通过键盘回车键进行充气。\n\
停止充气请鼠标左键单击end按钮。\n\
在充气任务之间还会呈现一些描述性的句子，\n\
请你根据当前的状态进行评分。1为极不符合，7为极为符合。\n\
建议不要调整窗口大小以确保显示的准确性。',font='宋体 -24')
        self.lb.place(relx=0.1,rely=0.2,relwidth=0.8,relheight=0.5)

        self.btn=Button(self.top,text='Start',command=lambda:self.createWidgets1())
        self.btn.place(relx=0.4,rely=0.7,relwidth=0.2,relheight=0.1)
        
    """创建图标"""
    def createWidgets1(self):
        
        self.top=self.winfo_toplevel()
        self.lb.destroy()
        self.btn.destroy()
        self.btn1=Button(self.top,text='pump',command=self.run1,font='Times\sNew\sRoman -16')
        self.btn1.focus_set()
        self.btn1.place(relx=0.1,rely=0.75,relwidth=0.3,relheight=0.1)
        self.btn1.bind('<Return>',self.run1)

        self.btn2=Button(self.top,text='end',command=self.run2,font='Times\sNew\sRoman -16')
        self.btn2.place(relx=0.6,rely=0.75,relwidth=0.3,relheight=0.1)

        self.lb1=Label(self.top,text="Trial earn:\n%.2f"%(trial.get()/100),font='Times\sNew\sRoman -20')
        self.lb1.place(relx=0.75,rely=0.3,relwidth=0.2,relheight=0.1)

        self.lb2=Label(self.top,text="Total earn:\n%.2f"%(total.get()/100),font='Times\sNew\sRoman -20')
        self.lb2.place(relx=0.75,rely=0.5,relwidth=0.2,relheight=0.1)

        self.lb3=Label(self.top,text="Now pumping\nthe %d/%d\nballoon"%(count,tr_num),font='Times\sNew\sRoman -20')
        self.lb3.place(relx=0.75,rely=0.1,relwidth=0.2,relheight=0.1)

        self.balloon=Canvas(self.top,width=480,height=480)
        self.balloon.place(relx=0.05,rely=0.05)
        self.balloon.create_oval(232-1.8*trial.get(),232-1.8*trial.get(),248+1.8*trial.get(),248+1.8*trial.get(),fill='red')
        
    """更新气球图片"""    
    def upgrade_pic(self,pump):
        self.balloon.delete(ALL)
        self.balloon.create_oval(232-1.8*trial.get(),232-1.8*trial.get(),248+1.8*trial.get(),248+1.8*trial.get(),fill='red')

    """切换Ui"""
    def change(self):
        self.btn1.destroy()
        self.btn2.destroy()
        self.lb1.destroy()
        self.lb2.destroy()
        self.lb3.destroy()
        self.balloon.destroy()
        MSBS_Ui.__init__(self)

class MSBS_Ui(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master.title('MSBS')
        self.master.geometry('1080x720')
        self.createWidgets2()
    """创建图标"""
    def createWidgets2(self):
        global pd
        
        self.top=self.winfo_toplevel()
        self.lb=Label(self.top,text=SBPS_Q[rd_lst[c]],font='宋体 -24')
        self.lb.place(relx=0.2,rely=0.3,relwidth=0.6,relheight=0.1)
        
        var=IntVar()
        self.rd1=Radiobutton(self.top,text='1',variable=var,value=1,command=lambda: st(),font='Times\sNew\sRoman -16')
        self.rd1.place(relx=0.1,rely=0.5,relwidth=0.05,relheight=0.1)
        self.rd2=Radiobutton(self.top,text='2',variable=var,value=2,command=lambda: st(),font='Times\sNew\sRoman -16')
        self.rd2.place(relx=0.2,rely=0.5,relwidth=0.05,relheight=0.1)
        self.rd3=Radiobutton(self.top,text='3',variable=var,value=3,command=lambda: st(),font='Times\sNew\sRoman -16')
        self.rd3.place(relx=0.3,rely=0.5,relwidth=0.05,relheight=0.1)
        self.rd4=Radiobutton(self.top,text='4',variable=var,value=4,command=lambda: st(),font='Times\sNew\sRoman -16')
        self.rd4.place(relx=0.4,rely=0.5,relwidth=0.05,relheight=0.1)
        self.rd5=Radiobutton(self.top,text='5',variable=var,value=5,command=lambda: st(),font='Times\sNew\sRoman -16')
        self.rd5.place(relx=0.5,rely=0.5,relwidth=0.05,relheight=0.1)
        self.rd6=Radiobutton(self.top,text='6',variable=var,value=6,command=lambda: st(),font='Times\sNew\sRoman -16')
        self.rd6.place(relx=0.6,rely=0.5,relwidth=0.05,relheight=0.1)
        self.rd7=Radiobutton(self.top,text='7',variable=var,value=7,command=lambda: st(),font='Times\sNew\sRoman -16')
        self.rd7.place(relx=0.7,rely=0.5,relwidth=0.05,relheight=0.1)
        self.lb1=Label(self.top,text='极不符合',font='宋体 -16')
        self.lb1.place(relx=0.1,rely=0.6,relwidth=0.1,relheight=0.05)
        self.lb2=Label(self.top,text='极为符合',font='宋体 -16')
        self.lb2.place(relx=0.7,rely=0.6,relwidth=0.1,relheight=0.05)
        '''
        for t,num in [(str(i),i) for i in range(1,8)]:
            self.rd=Radiobutton(self.top,text=t,variable=var,value=num)
            self.rd.place(relx=num/10,rely=0.45,relwidth=0.05,relheight=0.1)
        '''
        self.btn1=Button(self.top,text="确认",command=lambda:self.next_item(var),font='宋体 -16')
        self.btn1.place(relx=0.4,rely=0.75,relwidth=0.2,relheight=0.1)
        '''
        self.btn2=Button(self.top,text='返回上一题',command=self.rt)
        self.btn2.place(relx=0.6,rely=0.7,relwidth=0.2,relheight=0.1)
        '''
        
    """切换Ui"""
    def back(self):
        self.lb.destroy()
        self.lb1.destroy()
        self.lb2.destroy()
        self.btn1.destroy()
        #self.btn2.destroy()
        self.rd1.destroy()
        self.rd2.destroy()
        self.rd3.destroy()
        self.rd4.destroy()
        self.rd5.destroy()
        self.rd6.destroy()
        self.rd7.destroy()
        if c<24:
            BART_Ui.__init__(self)
        else:
            self.top.destroy()
    
    """返回上一题"""
    def rt(self):
        global c
        if c:
            c-=1
        print(c)
        pass

class BART(BART_Ui,MSBS_Ui):
    global trial
    global total
    global count

    def __init__(self,master=None):
        self.initiate()
        if b:
            BART_Ui.__init__(self,master)

    """充气按钮"""
    def run1(self,event=None):
        global sets
        global count
        global pd
        
        trial.set(trial.get()+1)                                                        #计数器加1
        if trial.get()>sets[count-1]:                                                   #判断是否到达设定界限
            showwarning('Warning','由于充气过多，气球爆炸了！本轮收益清零。')
            trial.set(0)                                                                #超过界限返回异常值-1
            self.lb1.configure(text="Trial earn:\n%.2f"%(0))                            #显示清零
            BART_result.append(-1)                                                      #记录结果
            count+=1                                                                    #试次计数器加1
            self.lb3.configure(text="Now pumping\nthe %d/%d\nballoon"%(count,tr_num))
            self.change()
        else:
            self.lb1.configure(text="Trial earn:\n%.2f"%(trial.get()/100))              #更新显示
            #print(count,trial.get())
        self.upgrade_pic(trial.get())

    """试次终止按钮"""
    def run2(self):
        global count
        global pd
        
        total.set(total.get()+trial.get())                                  #将成功结果加入总收益
        self.lb2.configure(text="Total earn:\n%.2f"%(total.get()/100))      #更新显示
        BART_result.append(trial.get())                                     #记录结果
        #print(BART_result)                                                  #test输出
        trial.set(0)                                                        #计数器清零
        self.lb1.configure(text="Trial earn:\n%.2f"%(trial.get()/100))
        count+=1                                                            #试次计数器加1
        self.lb3.configure(text="Now pumping\nthe %d/%d\nballoon"%(count,tr_num))
        self.change()

    """选中单选项后跳转下一题""" 
    def next_item(self,var):
        global c
        global pd
        
        if pd:
            SBPS_S[rd_lst[c]]=var.get()
            #print(SBPS_S)
            c+=1
            if c<24:
                self.lb.config(text=SBPS_Q[rd_lst[c]])
            #print(c)
            self.back()
            pd=False
        else:
            showwarning('Warning','未选择选项！')

    """初始化环境判断是否已存在记录文件"""
    def initiate(self):
        global b
        try:
            file=open('result.csv','r')
            b = askquestion(title='Warning',message="检测到目录下已存在实验记录文件，再次运行会覆盖之前的记录，是否继续？")
            if b=='no':
                b=False
        except:
            pass

def output_result():
    with open('result.csv','w') as f:
        f.write('BART,')
        for i in range(len(BART_result)):
            f.write(str(BART_result[i]))
            if i+1 != len(BART_result):
                f.write(',')
        f.write('\n')
        f.write('SBPS,')
        for i in range(len(SBPS_S)):
            f.write(str(SBPS_S[i]))
            if i+1 != len(SBPS_S):
                f.write(',')

if __name__=='__main__':
    tr_num=24                                                   #试次设定
    #sets=[random.randint(1,128) for i in range(tr_num)]        #随机化试次爆炸时间
    sets=[87, 106, 127, 31, 84, 26, 75, 94, 127, 52, 112, 64, 50, 15, 7, 76, 49, 37, 10, 92, 34, 6, 23, 101]
    #print(sets)
    """随机量表项目顺序"""
    cache=[random.random() for i in range(24)]                  
    rd_lst=[]
    c=0                                                         #量表计数器
    for i in range(24):
        rd_lst.append(sorted(cache).index(cache[i]))
    #print(rd_lst)
    
    top=Tk()
    #top.attributes("-fullscreen",True)
    trial=IntVar()                                              #试次内收益计数器
    trial.set(0)
    total=IntVar()                                              #总收益计数器
    total.set(0)
    count=1                                                     #试次计数器
    pd=False                                                    #单选题判断是否已选
    strt=False
    b=True
    BART(top).mainloop()
    output_result()
