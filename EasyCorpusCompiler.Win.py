import wx
import sys
import praw
import csv
import os
import time
import json

class MyFrame(wx.Frame):
    """A class with two boxes, a button and a statictext"""
    def __init__(self, parent):
        """constructor"""
        wx.Frame.__init__(self, parent, -1, 'Easy Corpus Compiler 0.01', size=(350, 200))
        self.panel = wx.Panel(self)
#        self.box1 = wx.TextCtrl(self.panel, -1, "type number")
#        self.box2 = wx.TextCtrl(self.panel, -1, "type number")
#        self.box1.SetBackgroundColour("gray")
#        self.box2.SetBackgroundColour("gray")
        self.gtext = wx.TextCtrl(self.panel, -1, size =(200,-1), value="subreddit goes here")
        button = wx.Button(self.panel,wx.ID_ANY, label="enter", size=(100, 50))
        self.Bind(wx.EVT_BUTTON, self.yesitstrue, button)
        self.stext = wx.StaticText(self.panel,wx.ID_ANY, label='Ready')

        siz = wx.BoxSizer(wx.VERTICAL)
#        siz.Add(self.box1, 1)
#        siz.Add(self.box2, 1)
        siz.Add(self.gtext,1)
        siz.Add(button,1)
        siz.Add(self.stext,1)
        self.panel.SetSizer(siz)

    def yesitstrue(self, event):
        try:
            config = json.loads(open('config.json').read())
            pass
        except:
            dlg2 = wx.MessageDialog(self,'Please make sure that you have the config.json file present in the same folder',wx.OK)
            result2 = dlg2.ShowModal()
            dlg2.Destroy()
            if result2 == wx.ID_OK:
                self.Destroy()
        username = config['username']
        password = config['password']   
        useragent = config['userAgent']
        #login to reddit
        r = praw.Reddit(useragent)
        r.login(username, password)
        self.stext.SetLabel('Logging into Reddit.....')
        #Change to selected location
        #os.chdir(sav)
        #Folder to contain the files
        if not os.path.exists('corpus'):
            os.makedirs('corpus')
        
        
        #Get subreddit
        subrdt = self.gtext.GetValue()
        #raw_input('Please enter a subreddit to collect comments from: ')
        #set up lists
        sublist = []
        comlist = []
        #get hot submissions
        subreddit = r.get_subreddit(subrdt)
        posts = subreddit.get_hot()
        for submission in posts:
            sublist.append(submission.id)
        #set number of loops
        missionlist = len(sublist)
        mlst = str(missionlist)
        self.stext.SetLabel('There are '+mlst+' hot submissions in that subreddit.')
        #define starting point for using the list
        i = 0
        if missionlist > 100:
            missionlist = 100
        self.stext.SetLabel('That\'s too many, I am going to parse 100 instead.')
        def cleanUp(text):
            alpha = text.encode('utf-8')
            return alpha
            
        while i < missionlist:
            submission = r.get_submission(submission_id=sublist[i])
            submission.replace_more_comments(limit=16, threshold=10)
            flat_comments = praw.helpers.flatten_tree(submission.comments)
            pstitle = submission.title.encode('ascii',errors='ignore')
            self.stext.SetLabel('Now processing: '+pstitle)
            stitle = ((submission.title.encode('ascii',errors='ignore')).replace(' ','_')).replace('"','')
            ftitle = 'corpus\\'+stitle[:40]
            file = open('corpus\\+stitle[:40]+'.csv','a')
            writer = csv.writer(file)
            writer.writerow(['Karma','Comment Body','Comment ID'])
            for comment in flat_comments: 
                comtitle = comment.id
                if comment.id not in comlist:
                    cleancomment = cleanUp(comment.body)
                    comlist.append(comment.id)
                    cleanscore = str(comment.score)
                    writer.writerow([cleanscore,cleancomment,comtitle])
            file.close()
            i+=1
            time.sleep(10)
            
        self.stext.SetLabel('Done')


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None)
    frame.Show()
    app.MainLoop()