#############################################
 #											#
 # META DATA HERE							#
 #											#
#############################################
 #Descripttion:								#
 #											#
 # This program opens streams from			#

 # http://docs.livestreamer.io/plugin_matrix.html#plugin-matrix
 
 # and plays them in vlc media player		#
 #											#
 ############################################

import time
import os
import platform
from urllib.request import urlopen
from urllib.error import URLError
import json
#import livestreamer

#Sets up the input variables that is used later in the script

restart = 'yes'
statAdd = 'no'

#Opens the json file for the list of tracked streamers
with open('list.json') as data_file:    
	data = json.load(data_file)
	#data_file.close()

streamDataTemp = data['data']['streamData']['streamTemplate']
startCount = data['data']['logs']['timesStarted']
startCount = startCount + 1
data['data']['logs']['timesStarted'] = startCount

#Menu Prompts
global options
options = ""																		+"\n"+\
			"Avalible options:"														+"\n"+\
			""																		+"\n"+\
			"----------"															+"\n"+\
			""																		+"\n"+\
			"Check (checks status of a specific user"								+"\n"+\
			"List (Checks the status of a list of predefined users"					+"\n"+\
			"Open (opens a stream)"													+"\n"+\
			"Add (Adds a user to to the tracked user list)"							+"\n"+\
			"Stats (Views the list of tracked stats)"								+"\n"+\
			""																		+"\n"+\
			"----------"															+"\n"+\
			""

global optionsstreaming
optionsstreaming = ""																+"\n"+\
			"Avalible options:"														+"\n"+\
			""																		+"\n"+\
			"----------"															+"\n"+\
			""																		+"\n"+\
			"The stream you chose is opening"										+"\n"+\
			"So sit back and watch/listen to you stream"							+"\n"+\
			"Enjoy!"																+"\n"+\
			""																		+"\n"+\
			"----------"															+"\n"+\
			""

global optionsopen
optionsopen = ""																	+"\n"+\
			"Avalible options:"														+"\n"+\
			""																		+"\n"+\
			"----------"															+"\n"+\
			""																		+"\n"+\
			"This is to open stream service The only two options avaliable are:"	+"\n"+\
			"Youtube -- Allows you to open a stream with a youtube url ir video id"	+"\n"+\
			"Twitch -- Opens a twitch stream when you input user"					+"\n"+\
			""																		+"\n"+\
			"----------"															+"\n"+\
			""	

global optionsstream
optionsstream = ""																	+"\n"+\
			"Avalible options:"														+"\n"+\
			""																		+"\n"+\
			"----------"															+"\n"+\
			""																		+"\n"+\
			"This is to specify a stream"											+"\n"+\
			"Input a username if for Twitch"										+"\n"+\
			"Input a video id if for Youtube"										+"\n"+\
			""																		+"\n"+\
			"----------"															+"\n"+\
			""

global optionsopenaudio
optionsopenaudio = ""																+"\n"+\
			"Avalible options:"														+"\n"+\
			""																		+"\n"+\
			"----------"															+"\n"+\
			""																		+"\n"+\
			"This is if you want to listen to the audio only for the stream"		+"\n"+\
			"Input yes to only get the audio and no video"							+"\n"+\
			"Input no to have video as well as audio"								+"\n"+\
			""																		+"\n"+\
			"----------"															+"\n"+\
			""

global optionslist
optionslist = ""																	+"\n"+\
			"Avalible options:"														+"\n"+\
			""																		+"\n"+\
			"----------"															+"\n"+\
			""																		+"\n"+\
			"This is used to list users present in the list.json"					+"\n"+\
			"This only works for twitch streamers at the moment"					+"\n"+\
			"Will maybe extend to youtube in the future"							+"\n"+\
			""																		+"\n"+\
			"----------"															+"\n"+\
			""

global optionscheck
optionscheck = ""																	+"\n"+\
			"Avalible options:"														+"\n"+\
			""																		+"\n"+\
			"----------"															+"\n"+\
			""																		+"\n"+\
			"This is used to check the status of a individual twitch streamer"		+"\n"+\
			"This is unavaliable for youtube unless it is otherwisse possible"		+"\n"+\
			"Might have youtube support in the future"								+"\n"+\
			""																		+"\n"+\
			"----------"															+"\n"+\
			""

global optionsstatscheck
optionsstatscheck = ""																+"\n"+\
			"Avalible options:"														+"\n"+\
			""																		+"\n"+\
			"----------"															+"\n"+\
			""																		+"\n"+\
			"This is used to view the stats being tracked"							+"\n"+\
			"You can view the stats of a individual user"							+"\n"+\
			"You can also view the total global stats"								+"\n"+\
			"You can also Clear the stats"											+"\n"+\
			"You can also check the errorLogs"										+"\n"+\
			""																		+"\n"+\
			"---------"																+"\n"+\
			""

global optionsstatsclear
optionsstatsclear = ""																+"\n"+\
			"Avalible options:"														+"\n"+\
			""																		+"\n"+\
			"----------"															+"\n"+\
			""																		+"\n"+\
			"This is the danger zone!"												+"\n"+\
			"This is where you can clear a users stats or the global stats"			+"\n"+\
			"Continue if you sure of what you are doing!"							+"\n"+\
			""																		+"\n"+\
			"----------"															+"\n"+\
			""	

global optionsadd
optionsadd = ""																		+"\n"+\
			"Avalible options:"														+"\n"+\
			""																		+"\n"+\
			"----------"															+"\n"+\
			""																		+"\n"+\
			"This is used to add a user to the tracked list"						+"\n"+\
			"This make ther status to be checked with the list command"				+"\n"+\
			"It also allows statistic tracking for the user"						+"\n"+\
			""																		+"\n"+\
			"----------"															+"\n"+\
			""	

global listing
listing = ""																		+"\n"+\
			"-------------"															+"\n"+\
			""



########################
#  Inverted Funcitons  #
########################

global status_list
status_list={
	  "Dailymotion"	:{},
	  "Livestream"	:{},
	  "Twitch"		:{},
	  "UStream"		:{},
	  "YouTube Live":{},
}

####################
# stream functions #
####################

#def openstream(service,user):
	#if service.lower() == 'youtube' or service.lower() == 'twitch':
		#if service.lower() == 'twitch':
			#try:
				#audioOnly = data['data']['streamData'][user.lower()]['musicStream']
				#if audioOnly == 'true':
					#clearscreen()
					#print(optionsopenaudio)
					#audio = input('Do you want to do audio only?: ')
					#
					#if audio.lower() == 'yes':
						#lvsting = lsTwitch + user + ' audio'
					#else:
						#lvsting = lsTwitch + user + ' source'
						#pass
					#pass
				#else:
					#lvsting = lsTwitch + user + ' source'
					#pass
				#pass
			#except:
				#lvsting = lsTwitch + user + ' source'
				#return
			#
			##Process for youtube streams
		#if service.lower() == 'youtube':
			#clearscreen()
			#print(optionsopenaudio)
			#if user[1:32] == 'https://www.youtube.com/watch?v=':
				#user=user[32:]
			#audio = input('Do you want to do audio only?: ')
			#if audio.lower() == 'yes':
				#lvsting = lsYoutube + user + ' audio_mp4'
			#else:
				#lvsting = lsYoutube + user + ' best'
				#pass
			#pass
	#else:
		#print('\nStream service not supported!\n')
		#streamError = 'true'
		#serviceErrorCnt = data['data']['errorLogs']['unsupportedServices']
		#serviceErrorCnt = serviceErrorCnt + 1
		#data['data']['errorLogs']['unsupportedServices'] = serviceErrorCnt
		#pass
	#pass
	#	
 ##Starts timer and opens stream

###########################
# subscriptions managment #
###########################

def update_user_status(server,user):
	global status_list
	if server=="Dailymotion":
		pass
	if server=="Livestream":
		pass
	if server=="Twitch":
		url = 'https://api.twitch.tv/kraken/streams/' + user
		try:
			info = json.loads(urlopen(url, timeout = 15).read().decode('utf-8'))
			if info['stream'] == None:
				status_list["Twitch"][user] = "Offline"
			else:
				status_list["Twitch"][user] = "Online"
		except URLError as e:
			if e.reason == 'Not Found' or e.reason == 'Unprocessable Entity':
				status_list["Twitch"][user] = "Not Found"
			else:
				status_list["Twitch"][user] = "ERROR"
		return status
	if server=="UStream":
		pass
	if server=="YouTube Live":
		pass
def update_known_users_stati():
	for s in status_list:
		for u in s:
			update_user_status(s,u)

#todo
#replace lvsting with call to livestreamer

#populate status_list from json
def readJSON():
	for u in data["streams"]:
		update_user_status(data["streamData"][u]["type"],u)

#add new user to json and status_list
def addUser(service,user):
	#query user for informaiton
		#"type": service,
		#"days": 0,
		#"hours": 0,
		#"mins": 0,
		#"musicStream": ask user,
		#"playCount": 0,
		#"secs": 0,
		#"totalTime": "0 Days 0:0:0"
	#add to json
	readJSON()
	update_known_users_stati()

#open a user's stream


#get stats for display in popup window

######################
# graphics managment #
######################

def grfthing():
	from tkinter import *
	from tkinter import ttk


	root = Tk()
	root.title("Stream to VLC")
	def calculate():
		pass
	mainframe = ttk.Frame(root, padding="12 12 12 12")
	mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
	mainframe.columnconfigure(0, weight=1)
	mainframe.rowconfigure(0, weight=1)

	feet = StringVar()
	meters = StringVar()



	ttk.Button(mainframe, text="Open", command=open).grid(column=2, row=3, sticky=W)
	ttk.Button(mainframe, text="List", command=lvstList).grid(column=3, row=3, sticky=W)
	ttk.Button(mainframe, text="Check", command=check).grid(column=4, row=3, sticky=W)
	ttk.Button(mainframe, text="Add", command=userAdd).grid(column=5, row=3, sticky=W)

	ttk.Label(mainframe, text=options).grid(column=1, row=1, sticky=W)
	#ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
	ttk.Label(mainframe, text="Things!").grid(column=1, row=1, sticky=E)
	ttk.Label(mainframe, text="Yey Tests!").grid(column=1, row=2, sticky=W)

	for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

	#feet_entry.focus()
	root.bind('<Return>', calculate)

	root.mainloop()

###################
#  Old Functions  #
###################

#Function to add new tracked users
def userAdd():
	global streamDataTemp
	global data
	global statAdd
	global statwho

	goodRecord = 0
	emptyRecord = 0
	allRecords = 0

	if statAdd.lower() == 'yes':

		array = data['streams']
		array.append(statwho.lower())
		data['data']['streamData'][statwho.lower()] = streamDataTemp
		pass

	if statAdd.lower() != 'yes':
		for i in range(len(data["streams"])):
			if data['streams'][i] != "null":
				goodRecord = goodRecord + 1
			elif data['streams'][i] == "null":
				emptyRecord = emptyRecord + 1
				pass
			allRecords = allRecords + 1
			pass
	
		goodRecord = str(goodRecord)
		emptyRecord = str(emptyRecord)
		allRecords = str(allRecords)
	
		clearscreen()
		print(optionsadd)
		print('\nThere are ' + goodRecord + ' used records and  ' + emptyRecord + ' empty records out of ' + allRecords + '\n')
		userAdd = input('Name of the user to add?: ')
		data['streams'].append(userAdd.lower())
		data['data']['streamData'][userAdd.lower()] = streamDataTemp

		isMusicStream = input('Is this stream a music stream? (Yes or No): ')

		if isMusicStream.lower() == 'yes':
			data['data']['streamData'][userAdd]['musicStream'] = 'true'
			pass
	
		for i in range(len(data["streams"])):
			if data['streams'][i] != "null":
				datanum = i
			pass
	
		datanum = datanum + 1
		data['data']['logs']['streamNum'] = datanum
		pass
	pass

def statCheck():
	global data
	global statAdd
	global statwho

	statAdd = 'no'
	clearscreen()
	print(optionsstatscheck)
	statWhat = input('Which stat do you want to see? (User, Global, Error or Clear): ')
	if statWhat.lower() == 'user':
		clearscreen()
		print(optionsstatscheck)
		statwho = input('Who do you want to check the stats of?: ')
		try:
			print("\nThis stream has been played: " + str(data['data']['streamData'][statwho.lower()]['playCount']))
			print("\nThis stream has been played for a total of: " + data['data']['streamData'][statwho.lower()]['totalTime'])
			if data['data']['streamData'][statwho.lower()]['musicStream'] == 'true':
				print('\nThis stream is also marked as a music stream')
				pass
			pass

		except:
			clearscreen()
			print(optionsstatscheck)
			print('\nThere are no stats for this user!\n')
			statAdd = input('Whould you like to add this user to the tracked list?: ')
			if statAdd.lower() == 'yes':
				userAdd()
				pass
			pass

	if statWhat.lower() == 'global':
		clearscreen()
		print(optionsstatscheck)
		print('\nThe total ammount of streams played is: ' + str(data['data']['logs']['totalPlay']))
		print('\nTheres a total of: ' + str(data['data']['logs']['streamNum']) + ' streams being tracked.')
		print('\nThe total ammount of time the streams have been played for is: ' + data['data']['timeCounters']['totalTime'])
		print('\nThe script has been started: ' + str(data['data']['logs']['timesStarted']) + ' times.')
		print('\nThe script has been restarted: ' + str(data['data']['logs']['timesRestarted']) + ' times.')
		pass

	if statWhat.lower() == 'error':
		clearscreen()
		print(optionsstatscheck)
		print('\nThe total ammount of times the script has been interuppted is: ' + str(data['data']['errorLogs']['timesInterrupted']))
		print('\nThe total of unsupported services entered is:  ' + str(data['data']['errorLogs']['unsupportedServices']))
		print('\nThe total ammount of unrecgonized commands entered is: ' + str(data['data']['errorLogs']['unRecgonizedCmds']))
		print('\nThe total number of Unknown Errors encountered: ' + str(data['data']['errorLogs']['unknownError']))
		pass

	if statWhat.lower() == 'clear':
		clearscreen()
		print(optionsstatsclear)
		statClear = input('Do you want to clear global stats or the stats of a specific user? (Global, User): ')
		if statClear.lower() == 'global':
			clearscreen()
			print(optionsstatsclear)
			data['data']['logs']['totalPlay'] = 0
			data['data']['timeCounters']['totalTime'] = "0 Days 0:0:0"
			data['data']['timeCounters']['secs'] = 0
			data['data']['timeCounters']['mins'] = 0
			data['data']['timeCounters']['hours'] = 0
			data['data']['timeCounters']['days'] = 0
			print('\nStat Clear Done!\n')
		elif statClear.lower() == 'user':
			clearscreen()
			print(optionsstatsclear)
			statClearUser = input('Whos stats do you want to clear?: ')
			data['data']['streamData'][statClearUser] = streamDataTemp
			print('\nStat clear done!')
		else:
			print('\nStat clear aborted!')
		pass
	pass

#Individual user status check
def check():
	clearscreen()
	print(optionscheck)
	user = input('User to check status of: ')	
	print('')
	update_user_status("Twitch",user)
	print('')
	pass

#User status list from the list.json file
def lvstList():
	global data
	global datanum
	global data_file

	clearscreen()
	print(optionslist)
	for i in range(len(data["streams"])):
		if data['streams'][i] != "null":
			datanum = i
		pass

	datanum = datanum + 1
	datanum = str(datanum)
	data['data']['logs']['streamNum'] = int(datanum)
	print('There are ' + datanum + ' streams on being tracked.\n\nDisplaying Online Users')

	for i in range(len(data["streams"])):
		if data["streams"][i] != "null":
			if update_user_status("Twitch",data["streams"][i]) != 1:
				update_user_status("Twitch",data["streams"][i])
				pass
			pass
		pass
	pass

def cmdwin():
	global times
	global lvsting
	global options
	global streamError

	if streamError != 'true':
		clearscreen()
		print(optionsstreaming)
		print('Opening ' + lvst + "'s stream on " + service + ".\n")
		try:
			print('Total times ' + lvst + " has been played: " + str(data['data']['streamData'][lvst]['playCount']) + ".\n")
			print('Total ammount of time ' + lvst + " Has been played for: " + data['data']['streamData'][lvst]['totalTime'] + " \n")
			pass
		except:
			pass
		start = time.time()
		os.system(lvsting)
		end = time.time()
		times = end - start
		times = int(times)
	else:
		print('There was a error opening the stream!')
		pass
	pass
 
 #Timer calculation
def timeCalc():
	global times
	global timem
	global timeh

	while times > 59:
		times = times - 60
		timem = timem + 1
		pass

	while timem > 59:
		timem = timem - 60
		timeh = timeh + 1
		pass
	
	#converts timer values to strings to display with print
	times = str(times)
	timem = str(timem)
	timeh = str(timeh)
	#Prints the elapsed time
	elapsedTime = timeh + ':' + timem + ':' + times
	print('')
	print ('Time elapsed: ' + elapsedTime)
	print('')
	pass

#Updates Stats
def stattracker():
	global times
	global timem
	global timeh
	global lvst
	global elapsedTime
	global totalsec
	global totalmin
	global totalhrs
	global totaldays
	global totalusersec
	global totalusermin
	global totaluserhrs
	global totaluserdays

	#Updates the play count on the active streamer
	try:
		playnum = data['data']['streamData'][lvst]['playCount']
		playnum = playnum + 1
		data['data']['streamData'][lvst]['playCount'] = playnum
		pass
	except:
		pass

	#Updates the total play count for all streams
	totalplay = data['data']['logs']['totalPlay']
	totalplay = totalplay + 1
	data['data']['logs']['totalPlay'] = totalplay

	#Updates overall time totals
	totalsec = data['data']['timeCounters']['secs']
	totalmin = data['data']['timeCounters']['mins']
	totalhrs = data['data']['timeCounters']['hours']
	totaldays = data['data']['timeCounters']['days']

	times = int(times)
	timem = int(timem)
	timeh = int(timeh)

	totalsec = totalsec + times
	totalmin = totalmin + timem
	totalhrs = totalhrs + timeh

	while totalsec > 59:
		totalsec = totalsec - 60
		totalmin = totalmin + 1
		pass
	while totalmin > 59:
		totalmin = totalmin - 60
		totalhrs = totalhrs + 1
		pass
	while totalhrs > 23:
		totalhrs - 24
		totaldays + 1
		pass

	data['data']['timeCounters']['secs'] = totalsec
	data['data']['timeCounters']['mins'] = totalmin
	data['data']['timeCounters']['hours'] = totalhrs
	data['data']['timeCounters']['days'] = totaldays
	totalsec = str(totalsec)
	totalmin = str(totalmin)
	totalhrs = str(totalhrs)
	totaldays = str(totaldays)
	totalelapsed = totaldays + " Days " + totalhrs + ":" + totalmin + ":" + totalsec
	data['data']['timeCounters']['totalTime'] = totalelapsed

	#Updates user time totals
	if service.lower() == 'twitch':
		try:
			totalusersec = data['data']['streamData'][lvst]['secs']
			totalusermin = data['data']['streamData'][lvst]['mins']
			totaluserhrs = data['data']['streamData'][lvst]['hours']
			totaluserdays = data['data']['streamData'][lvst]['days']
		
			totalusersec = totalusersec + times
			totalusermin = totalusermin + timem
			totaluserhrs = totaluserhrs + timeh

			while totalusersec > 59:
				totalusersec = totalusersec - 60
				totalusermin = totalusermin + 1
				pass
	
			while totalusermin > 59:
				totalusermin = totalusermin - 60
				totaluserhrs = totaluserhrs + 1
				pass

			while totaluserhrs > 23:
				totaluserhrs - 24
				totaluserdays + 1
				pass
		
			data['data']['streamData'][lvst]['secs'] = totalusersec
			data['data']['streamData'][lvst]['mins'] = totalusermin
			data['data']['streamData'][lvst]['hours'] = totaluserhrs
			data['data']['streamData'][lvst]['days'] = totaluserdays
			totalusersec = str(totalusersec)
			totalusermin = str(totalusermin)
			totaluserhrs = str(totaluserhrs)
			totaluserdays = str(totaluserdays)
			totaluserelapsed = totaluserdays + " Days " + totaluserhrs + ":" + totalusermin + ":" + totalusersec
			data['data']['streamData'][lvst]['totalTime'] = totaluserelapsed
		except:
			pass
	pass


#Main Starter
def start():
	global option
	global times
	global timem
	global restart
	global options
	global lvst
	global streamError

	#Option input
	print(options)
	option = input('What do you want to do?: ')
	clearscreen()
	print(options)

	#checks what option was chosen
	if option.lower() == "check":
		check()
	elif option.lower() == "list":
		lvstList()
	elif option.lower() == "open":
		openstream()
		cmdwin()
		if streamError != 'true':
			timeCalc()
			stattracker()
			pass
	elif option.lower() == "add":
		userAdd()
	elif option.lower() == "stats":
		statCheck()
	else:
		unrecgonizedCmd = data['data']['errorLogs']['unRecgonizedCmds']
		unrecgonizedCmd = unrecgonizedCmd + 1
		data['data']['errorLogs']['unRecgonizedCmds'] = unrecgonizedCmd
		print("\n\n-----------\n\nOption Not Recgonized\n\n-----------\n")
		pass
	print('')
	restart = input('Restart the Script?: ')
	pass

#Restarts the script
#while restart.lower() == "yes":
	#try:
		#start()
		#if restart == "yes":
			#clearscreen()
			#pass
		#pass
	#except KeyboardInterrupt:
		#print('\n\nEnding Script')
		#timesInterrupted = data['data']['errorLogs']['timesInterrupted']
		#timesInterrupted = timesInterrupted + 1
		#data['data']['errorLogs']['timesInterrupted'] = timesInterrupted
		#restart = 'no'
		#pass
	#except:
		#print('\n\nUnknown Error!')
		#unknownError = data['data']['errorLogs']['unknownError']
		#unknownError = unknownError + 1
		#data['data']['errorLogs']['unknownError'] = unknownError
		#restart = 'no'
		#pass
	#if restart.lower() == "yes":
		#timesRestarted = data['data']['logs']['timesRestarted']
		#timesRestarted = timesRestarted + 1
		#data['data']['logs']['timesRestarted'] = timesRestarted
		#pass
	#pass

#Script end confirmation
print('')
#input("Press Enter to continue...")

with open('list.json', "w") as write_file:  
	json.dump(data, write_file)

##End##