import sys
import tweepy
from PyQt5 import QtCore, QtGui, QtWidgets
from firstgui2 import Ui_myfirstgui
from textblob import TextBlob
from matplotlib import pyplot as plt
import webbrowser

from numpy import array

#Authentication
consumer_key = 'AvcNG2dXEc97oBvOKdvBwo2QN'
consumer_secret = 'ClHRgg2GuHNysPqN5L67UaT0yOaQDn1POTbbeYYrSEKk5Oz6Sp'
access_token = '1090284795479949312-0MM9QBo5EpHFkX2NgvHEU9wtH9GG3O'
access_token_secret = '0N6vB0cPjtYfDTTACkcALhQNrRoQJhdZwD9IoOKfx8wrA'
global new_token
new_token = '1090284795479949312-0MM9QBo5EpHFkX2NgvHEU9wtH9GG3O'

keywordData1 = ""
numberOfTweetsData1 = ""
keywordData2 = ""
numberOfTweetsData2 = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
global api
api = tweepy.API(auth)

#userHandle and numberOfTweets declared
userHandle = ""
numberOfTweets = 0
filterWord = ""

tweetIDList = []
tweetDateList = []
tweetFavoriteList = []
tweetRetweetList = []
redirect_url = ""

dataTweetDateList = []
dataTweetFavoriteList = []
dataTweetRetweetList = []

#function to call on to get the tweets
#user = api.user_timeline(screen_name=userHandle, count=numberOfTweets, include_rts=False)

class MyFirstGuiProgram(Ui_myfirstgui):
	def __init__(self, dialog):
		Ui_myfirstgui.__init__(self)

		self.setupUi(dialog)

		# start of button functions
		self.pushButton.clicked.connect(self.addTwitterHandleTextToFunction)
		self.publishTweetBtn.clicked.connect(self.postTweetFunction)
		self.searchLiveFeedBtn.clicked.connect(self.searchStreamFunction)
		self.compareDataBtn.clicked.connect(self.graphData1Function)
		self.saveDataSet1Btn.clicked.connect(self.grabDataSet1Function)
		self.SaveDataSet2Btn.clicked.connect(self.grabDataSet2Function)
		self.compareTwoDataBtn.clicked.connect(self.compareDataSetsFunction)
		self.ClearDataSetsBtn.clicked.connect(self.clearDataSetsFunction)
		self.submitLogBtn.clicked.connect(self.linkToConnectTwitterFunction)
		self.submitPinBtn.clicked.connect(self.submitPinToConnectTwitterFunction)
		self.submitPinBtn.setDisabled(True)
		self.submitPinBtn.repaint()
		self.publishTweetBtn.setDisabled(True)
		self.publishTweetBtn.repaint()
		self.SaveDataSet2Btn.setDisabled(True)
		self.SaveDataSet2Btn.repaint()
		self.compareTwoDataBtn.setDisabled(True)
		self.compareTwoDataBtn.repaint()
		self.searchResultLabel.setText("")
		self.searchResultLabel.repaint()
		self.tweetPublishLabel.setText("")
		self.tweetPublishLabel.repaint()
		self.streamResultLabel.setText("")
		self.streamResultLabel.repaint()
		self.deleteTweetResultLabel.setText("")
		self.deleteTweetResultLabel.repaint()
		self.authenticationWorkedLabel.setText("")
		self.authenticationWorkedLabel.repaint()
		self.testRowBtn.clicked.connect(self.testingRowResponseFunction)
		self.tweetResultWidget.itemClicked.connect(self.printTweetInfoFunction)
		self.tweetStreamResultWidget.itemClicked.connect(self.printDataTweetInfoFunction)
		self.popularityStatusLabel.setText("")
		self.popularityStatusLabel.repaint()
		self.sentimentStatusLabel.setText("")
		self.sentimentStatusLabel.repaint()
		self.reportIssueBtn.clicked.connect(self.reportIssueFunction)
		self.unlinkAppBtn.clicked.connect(self.unlinkAppFunction)
		self.grabAccessTokenBtn.clicked.connect(self.grabAccessTokenFunction)
		self.checkAccountBtn.clicked.connect(self.checkAccountFunction)
		self.checkAuthStatusBtn.clicked.connect(self.checkAuthFunction)
		self.checkAuthResultLabel.setText("")
		self.checkAuthStatusBtn.repaint()
		self.accountResultLabel.setText("")
		self.accountResultLabel.repaint()
		self.followAppAccBtn.clicked.connect(self.followAppAccFunction)
		self.followDevAccBtn.clicked.connect(self.followDevAccFunction)
		self.appWebsiteBtn.clicked.connect(self.appWebsiteFunction)
		self.moreAppInfoBtn.clicked.connect(self.moreAppInfoFunction)
		self.contactDevBtn.clicked.connect(self.contactDevFunction)
		self.downloadSrcBtn.clicked.connect(self.downloadSrcFunction)
		self.downloadDocBtn.clicked.connect(self.downloadDocFunction)
		self.retweetGraphBtn.clicked.connect(self.checkRetweetGraphFunction)
		self.favoriteGraphBtn.clicked.connect(self.checkFavoriteGraphFunction)
		self.dataAnalysisResultLabel.setText("")
		self.dataAnalysisResultLabel.repaint()

	def checkRetweetGraphFunction(self):
		wordRetweets = []

		keywordGraph = self.filterStreamWordInput.text()
		numberOfTweetsGraph = self.numberDataTweetsBox.value()
		recentTypeGraph = "recent"

		if(keywordGraph != "" and numberOfTweetsGraph != 0):
			self.dataSetRetweetsLabel.setText(keywordGraph)
			self.dataSetRetweetsLabel.repaint()
			for tweet in tweepy.Cursor(api.search, q=keywordGraph, result_type=recentTypeGraph, lang="en").items(numberOfTweetsGraph):
				try:
					print(tweet.retweet_count)
					wordRetweets.append(tweet.retweet_count)

				except tweepy.TweepError as e:
					print(e.reason)

				except StopIteration:
					break

			tuple(wordRetweets)
			plt.plot(wordRetweets, 'go--')
			plt.legend([keywordGraph], handlelength = 3.0)
			plt.ylabel('# of Retweets')
			plt.xlabel('# of Tweets in Most Recent Order')
			plt.grid()
			plt.show()
			self.dataAnalysisResultLabel.setText("Successfully Graphed Retweets")
			self.dataAnalysisResultLabel.repaint()

	def checkFavoriteGraphFunction(self):
		wordFavorites = []

		keywordGraph = self.filterStreamWordInput.text()
		numberOfTweetsGraph = self.numberDataTweetsBox.value()
		recentTypeGraph = "recent"

		if(keywordGraph != "" and numberOfTweetsGraph != 0):
			self.dataSetFavoritesLabel.setText(keywordGraph)
			self.dataSetFavoritesLabel.repaint()
			for tweet in tweepy.Cursor(api.search, q=keywordGraph, result_type=recentTypeGraph, lang="en").items(numberOfTweetsGraph):
				try:
					wordFavorites.append(tweet.favorite_count)

				except tweepy.TweepError as e:
					print(e.reason)

				except StopIteration:
					break

			tuple(wordFavorites)
			plt.plot(wordFavorites, 'yo--')
			plt.legend([keywordGraph], handlelength = 3.0)
			plt.ylabel('# of Favorites')
			plt.xlabel('# of Tweets in Most Recent Order')
			plt.grid()
			plt.show()
			self.dataAnalysisResultLabel.setText("Successfully Graphed Favorites")
			self.dataAnalysisResultLabel.repaint()

	def followAppAccFunction(self):
		appAcc_url = "https://twitter.com/DataMineTweets"
		webbrowser.open(appAcc_url)

	def followDevAccFunction(self):
		devAcc_url = "https://twitter.com/DataMineDev"
		webbrowser.open(devAcc_url)

	def appWebsiteFunction(self):
		appWebsite_url = "https://tweetanalysis.weebly.com/"
		webbrowser.open(appWebsite_url)

	def moreAppInfoFunction(self):
		moreAppInfo_url = "https://tweetanalysis.weebly.com/about.html"
		webbrowser.open(moreAppInfo_url)

	def contactDevFunction(self):
		contactDev_url = "https://tweetanalysis.weebly.com/contact.html"
		webbrowser.open(contactDev_url)

	def downloadSrcFunction(self):
		downloadSrc_url = "https://github.com/"
		webbrowser.open(downloadSrc_url)

	def downloadDocFunction(self):
		downloadDoc_url = "https://github.com/"
		webbrowser.open(downloadDoc_url)

	def reportIssueFunction(self):
		reportIssue_url = "https://twitter.com/messages/compose?recipient_id=1090284795479949312"
		webbrowser.open(reportIssue_url)

	def checkAccountFunction(self):
		user = api.me()
		self.accountResultLabel.setText(user.name)
		self.accountResultLabel.repaint()

	def unlinkAppFunction(self):
		application_url = "https://twitter.com/settings/applications"
		webbrowser.open(application_url)

	def grabAccessTokenFunction(self):
		global new_token
		self.accesTokenResultBox.setText(new_token)

	def checkAuthFunction(self):
		self.checkAuthResultLabel.setText("Connected")
		self.checkAuthStatusBtn.repaint()

	def addInputTextToListbox(self):
		txt = self.myTextInput.text()
		self.listWidget.addItem(txt)

	def printTweetInfoFunction(self):
		print(self.tweetResultWidget.currentRow())
		dateResult = tweetDateList[self.tweetResultWidget.currentRow()]
		retweetResult = tweetRetweetList[self.tweetResultWidget.currentRow()]
		favoriteResult = tweetFavoriteList[self.tweetResultWidget.currentRow()]
		self.DateResultLabel.setText(dateResult)
		self.retweetResultLabel.setText(retweetResult)
		self.favoriteResultLabel.setText(favoriteResult)
		self.DateResultLabel.repaint()
		self.retweetResultLabel.repaint()
		self.favoriteResultLabel.repaint()

	def printDataTweetInfoFunction(self):
		dataDateResult = dataTweetDateList[self.tweetStreamResultWidget.currentRow()]
		dataRetweetResult = dataTweetRetweetList[self.tweetStreamResultWidget.currentRow()]
		dataFavoriteResult = dataTweetFavoriteList[self.tweetStreamResultWidget.currentRow()]
		self.dataDateResultLabel.setText(dataDateResult)
		self.dataDateResultLabel.repaint()
		self.dataRetweetResultLabel.setText(dataRetweetResult)
		self.dataRetweetResultLabel.repaint()
		self.dataFavoriteResultLabel.setText(dataFavoriteResult)
		self.dataFavoriteResultLabel.repaint()


	def testingRowResponseFunction(self):
		try:
			print(self.tweetResultWidget.currentItem())
			print(self.tweetResultWidget.currentRow())
			deleteTweet = tweetIDList[self.tweetResultWidget.currentRow()]
			api.destroy_status(deleteTweet)
			self.addTwitterHandleTextToFunction()
			self.deleteTweetResultLabel.setText("Successfully Deleted")
			self.deleteTweetResultLabel.repaint()
		except:
			print("You may not delete another user's status.")
			self.deleteTweetResultLabel.setText("Invalid Request")
			self.deleteTweetResultLabel.repaint()

	def linkToConnectTwitterFunction(self):
		global redirect_url
		try:
			redirect_url = auth.get_authorization_url()
		except tweepy.TweepError:
			print("Error! Failed to get request token.")

		#print(redirect_url)
		webbrowser.open(redirect_url)
		self.submitPinBtn.setEnabled(True)
		self.submitPinBtn.repaint()

	def submitPinToConnectTwitterFunction(self):
		verifier = self.authenticationPinInput.text()

		try:
			auth.get_access_token(verifier)
			self.authenticationWorkedLabel.setText("Successfully Linked Account")
			self.authenticationWorkedLabel.repaint()
			self.submitLogBtn.setDisabled(True)
			self.submitLogBtn.repaint()
			self.submitPinBtn.setDisabled(True)
			self.submitPinBtn.repaint()
			self.publishTweetBtn.setEnabled(True)
			self.publishTweetBtn.repaint()
			global new_token
			new_token = auth.access_token
			new_secret = auth.access_token_secret
			auth.set_access_token(new_token, new_secret)
			global api
			api = tweepy.API(auth)
		except tweepy.TweepError:
			self.authenticationWorkedLabel.setText("Error Linking Account")
			self.authenticationWorkedLabel.repaint()
			self.submitLogBtn.setEnabled(True)
			self.submitLogBtn.repaint()
			self.submitPinBtn.setDisabled(True)
			self.submitPinBtn.repaint()

	def grabDataSet1Function(self):
		if (self.filterStreamWordInput.text() != "" and self.numberDataTweetsBox.value() != 0):
			global keywordData1
			keywordData1 = self.filterStreamWordInput.text()
			print(keywordData1)
			self.dataSet1NameLabel.setText(keywordData1)
			self.dataSet1NameLabel.repaint()
			global numberOfTweetsData1
			numberOfTweetsData1 = self.numberDataTweetsBox.value()
			self.SaveDataSet2Btn.setEnabled(True)
			self.SaveDataSet2Btn.repaint()
			self.saveDataSet1Btn.setDisabled(True)
			self.saveDataSet1Btn.repaint()

	def grabDataSet2Function(self):
		global numberOfTweetsData1
		print(numberOfTweetsData1)
		global numberOfTweetsData2
		numberOfTweetsData2 = self.numberDataTweetsBox.value()
		if(numberOfTweetsData2 == numberOfTweetsData1):
			if (self.filterStreamWordInput.text() != "" and self.numberDataTweetsBox.value() != 0):
				global keywordData2
				keywordData2 = self.filterStreamWordInput.text()
				self.dataSet2NameLabel.setText(keywordData2)
				self.dataSet2NameLabel.repaint()
				self.SaveDataSet2Btn.setDisabled(True)
				self.SaveDataSet2Btn.repaint()
				self.compareTwoDataBtn.setEnabled(True)
				self.compareTwoDataBtn.repaint()
				self.compareDataSetNameLabel.setText("'" + keywordData1 + "'   versus   '" + keywordData2 + "'"
													 + "   for   '" + str(numberOfTweetsData1) + "'   tweets")
				self.compareDataSetNameLabel.repaint()

	def compareDataSetsFunction(self):
		#we need to do the graphing here
		global keywordData1
		global keywordData2
		global numberOfTweetsData1
		global numberOfTweetsData2
		#str(statusStream.retweet_count

		polarity_list = []
		numbers_list = []
		number = 1

		retweet_list1 = []
		sortCounter1 = 0
		retweet_list2 = []
		favorite_list1 = []
		favorite_list2 = []
		self.popularityStatusLabel.setText("Successfully Compared")
		self.popularityStatusLabel.repaint()

		for tweet in tweepy.Cursor(api.search, q=keywordData1, result_type="popular", lang="en").items(numberOfTweetsData1):
			try:
				retweet_list1.append(tweet.retweet_count)
				favorite_list1.append(tweet.favorite_count)

				numbers_list.append(number)
				number = number + 1
			except tweepy.TweepError as e:
				print(e.reason)
			except StopIteration:
				break

		for tweet in tweepy.Cursor(api.search, q=keywordData2, result_type="popular", lang="en").items(numberOfTweetsData2):
			try:
				retweet_list2.append(tweet.retweet_count)
				favorite_list2.append(tweet.favorite_count)

			except tweepy.TweepError as e:
				print(e.reason)

			except StopIteration:
				break

			# Plotting
		plt.figure(1)
		axes = plt.gca()
		axes.set_xlim([0, 100])
		plt.subplot(211)
		plt.plot(retweet_list1, 'ro--')
		plt.legend([keywordData1], handlelength=3.0)
		plt.title("Popularity Comparison of: " + keywordData1 + " versus " + keywordData2)
		plt.xlabel("Number of Tweets")
		plt.ylabel("Number of Retweets")
		plt.grid()

		plt.subplot(212)
		plt.plot(retweet_list2, 'bo--')
		plt.legend([keywordData2], handlelength=3.0)
		plt.grid()
		plt.xlabel("Number of Tweets")
		plt.ylabel("Number of Retweets")
		plt.show()

	def clearDataSetsFunction(self):
		global keywordData1
		keywordData1 = ""
		global keywordData2
		keywordData2 = ""
		global numberOfTweetsData1
		numberOfTweetsData1 = ""
		global numberOfTweetsData2
		numberOfTweetsData2 = ""
		self.compareTwoDataBtn.setDisabled(True)
		self.compareTwoDataBtn.repaint()
		self.saveDataSet1Btn.setEnabled(True)
		self.saveDataSet1Btn.repaint()
		self.SaveDataSet2Btn.setDisabled(True)
		self.SaveDataSet2Btn.repaint()
		self.dataSet1NameLabel.setText("None")
		self.dataSet1NameLabel.repaint()
		self.dataSet2NameLabel.setText("None")
		self.dataSet2NameLabel.repaint()
		self.compareDataSetNameLabel.setText("None")
		self.compareDataSetNameLabel.repaint()
		self.popularityStatusLabel.setText("")
		self.popularityStatusLabel.repaint()

	def graphData1Function(self):
		keywordGraph1 = self.filterStreamWordInput.text()
		numberOfTweetsGraph1 = self.numberDataTweetsBox.value()
		recentTypeGraph1 = "recent"

		polarity_list = []
		numbers_list = []
		number = 1

		if(keywordGraph1 != "" and numberOfTweetsGraph1 != 0):
			self.sentimentStatusLabel.setText("Success")
			self.sentimentStatusLabel.repaint()
			for tweet in tweepy.Cursor(api.search, q=keywordGraph1, result_type=recentTypeGraph1, lang="en").items(numberOfTweetsGraph1):
				try:
					analysis = TextBlob(tweet.text)
					analysis = analysis.sentiment
					polarity = analysis.polarity
					polarity_list.append(polarity)
					numbers_list.append(number)
					number = number + 1

				except tweepy.TweepError as e:
					print(e.reason)

				except StopIteration:
					break

			# Plotting
			axes = plt.gca()
			axes.set_ylim([-1, 2]) #axes numbers

			plt.scatter(numbers_list, polarity_list)

			averagePolarity = (sum(polarity_list)) / (len(polarity_list))
			averagePolarity = "{0:.0f}%".format(averagePolarity * 100)

			plt.text(1, 1.5, "Average Sentiment:  " + str(averagePolarity), fontsize=12,
				 	bbox=dict(facecolor='none', edgecolor='grey', boxstyle='round, pad = 1'))

			plt.title("Sentiment of " + keywordGraph1 + " on Twitter")
			plt.xlabel("Number of Tweets")
			plt.ylabel("Sentiment")
			plt.show()
		else:
			self.sentimentStatusLabel.setText("Invalid Request")
			self.sentimentStatusLabel.repaint()


	def postTweetFunction(self):
		tweetInputTxt = self.tweetInputBox.text()
		self.tweetPublishLabel.setText("")
		self.tweetPublishLabel.repaint()
		if tweetInputTxt != "":
			try:
				api.update_status(tweetInputTxt)
				self.tweetPublishLabel.setText("Tweet Posted")
				self.tweetPublishLabel.repaint()
			except:
				self.tweetPublishLabel.setText("Invalid Tweet")
				self.tweetPublishLabel.repaint()

	def searchStreamFunction(self):
		global dataTweetDateList
		global dataTweetFavoriteList
		global dataTweetRetweetList
		dataTweetDateList.clear()
		dataTweetFavoriteList.clear()
		dataTweetRetweetList.clear()
		self.tweetStreamResultWidget.clear()
		self.searchResultLabel.setText("")
		self.searchResultLabel.repaint()
		filterWordStreamTxt = self.filterStreamWordInput.text()
		numberOfStreamTweets = self.numberDataTweetsBox.value()
		resultTypeTxt = self.filterOptionBox.currentText()
		searchFoundNumber = 0
		self.dataHistoryWidget.addItem(filterWordStreamTxt)

		if filterWordStreamTxt != "":
			if numberOfStreamTweets != 0:
				stream = tweepy.Cursor(api.search, q=filterWordStreamTxt, result_type=resultTypeTxt, lang="en", include_rts = False).items(numberOfStreamTweets)
				for statusStream in stream:

					self.tweetStreamResultWidget.addItem(statusStream.text + "\n")

					searchFoundNumber = searchFoundNumber + 1
					notFoundNumber = (numberOfStreamTweets - searchFoundNumber)

					self.dataTweetsScannedResultLabel.setText(str(numberOfStreamTweets))
					self.dataTweetsScannedResultLabel.repaint()
					self.dataMatchedResultLabel.setText(str(searchFoundNumber))
					self.dataMatchedResultLabel.repaint()
					self.dataNotFoundResultLabel.setText(str(notFoundNumber))
					self.dataNotFoundResultLabel.repaint()


					dataTweetDateList.append(str(statusStream.created_at))
					dataTweetFavoriteList.append(str(statusStream.favorite_count))
					dataTweetRetweetList.append(str(statusStream.retweet_count))
				if searchFoundNumber != 0:
						self.dataSearchProgressBar.setValue(100)
						self.dataSearchProgressBar.repaint()

			else:
				if searchFoundNumber == 0:
					self.dataSearchProgressBar.setValue(0)
					self.dataSearchProgressBar.repaint()
					self.dataTweetsScannedResultLabel.setText(str(0))
					self.dataTweetsScannedResultLabel.repaint()
					self.dataMatchedResultLabel.setText(str(0))
					self.dataMatchedResultLabel.repaint()
					self.dataNotFoundResultLabel.setText(str(0))
					self.dataNotFoundResultLabel.repaint()

	# searching for keyword #can have 'recent' 'popular' 'mixed'
	# user = tweepy.Cursor(api.search, q='filterWord', result_type="recent", lang="en").items(numberOfTweets)

	def addTwitterHandleTextToFunction(self):
		#clear out result feed every time it is clicked submit
		global tweetIDList
		global tweetDateList
		global tweetFavoriteList
		global tweetRetweetList
		self.tweetResultWidget.clear()
		tweetIDList.clear()
		tweetDateList.clear()
		tweetRetweetList.clear()
		tweetFavoriteList.clear()
		searchesFound = 0
		self.searchProgressBar.setValue(0)
		searchProgressNumber = 0
		#starts to list
		twitterHandleTxt = self.twitterHandleInput.text()
		filterWordsTxt = self.filterWordsInput.text()
		boxNumberTweets = self.numberTweetsBox.value()
		includeRetweetsTxt = self.includeRetweetsComboBox.currentText()
		self.searchResultLabel.setText("")
		self.searchResultLabel.repaint()
		userHandle = twitterHandleTxt
		numberOfTweets = self.numberTweetsBox.value()
		self.userHistoryWidget.addItem(userHandle)

		if numberOfTweets != 0:
			try:
				if includeRetweetsTxt == 'False':
					user = tweepy.Cursor(api.user_timeline, id=userHandle, include_rts=False).items(numberOfTweets)
				else:
					user = tweepy.Cursor(api.user_timeline, id=userHandle, include_rts=True).items(numberOfTweets)
				for status in user:
					if filterWordsTxt in status.text:

						self.tweetResultWidget.addItem(status.text + "\n")
						# keeping track of tweet ids
						tweetIDList.append(str(status.id))
						tweetDateList.append(str(status.created_at))
						tweetFavoriteList.append(str(status.favorite_count))
						tweetRetweetList.append(str(status.retweet_count))
						print(tweetIDList[0])

						searchesFound = searchesFound + 1
						notFound = (numberOfTweets - searchesFound)
						self.searchResultLabel.setText("Success " + str(searchesFound) + "/" + str(numberOfTweets) + " Tweets Found")
						self.searchResultLabel.repaint()
						self.tweetsScannedResultLabel.setText(str(numberOfTweets))
						self.tweetsScannedResultLabel.repaint()
						self.matchedResultLabel.setText(str(searchesFound))
						self.matchedResultLabel.repaint()
						self.notFoundResultLabel.setText(str(notFound))
						self.notFoundResultLabel.repaint()

						if searchesFound != 0:
							self.searchProgressBar.setValue(100)
					else:
						if searchesFound == 0:
							self.searchResultLabel.setText("No Tweets Found")
							self.searchResultLabel.repaint()
			except:
				print("not authorized")
				self.searchResultLabel.setText("Not Authorized")
				self.searchResultLabel.repaint()
				self.searchProgressBar.setValue(0)


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	dialog = QtWidgets.QDialog()

	prog = MyFirstGuiProgram(dialog)

	dialog.show()
	sys.exit(app.exec_())