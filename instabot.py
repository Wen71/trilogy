#from instabot import Bot
import random
import time
import glob
# bot = Bot()                                           #implement the bot object
# bot.login(username="UVC_BOT", password="217UVC2020")  #pass the login to online software

aegis = "C:/Users/wensu/Desktop/aegis/"
aegis_list = glob.glob(aegis+"*.jpg")                   #use glob to assemble a list
glob_list = [ele + "\n" for ele in aegis_list]
# print(glob_list)


posted_list = open("images.txt").readlines()            #read lines of images posted in posted_list to load all the posted files
print(posted_list)
nonposted_list = list(set(glob_list)-set(posted_list))  #images in glob_list that have not been posted yet

while len(nonposted_list) > 0:                          #while there are still images remain to be posted
    # print(len(nonposted_list))
    x = random.choice(nonposted_list)                       # Select a random image from nonposted_list
    # bot.upload_photo(x, caption="")                       # post with the Bot
    print(time.ctime(),x)                                   # print/check what image is posting and when
    nonposted_list.remove(x)                                # (after posting,)delete x from nonposted_list
    f = open("images_time.txt", "a")
    f.write(time.ctime() + x)                               # write which images have been posted and at what time to a text file
    f2 = open("images.txt", "a")
    f2.write(x)                                             # record which images have been posted to posted_list
    time.sleep(86400)                                           # post every day(86400 secs)
f.close()
f2.close()