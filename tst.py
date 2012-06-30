from flask import Flask, request, session, g, redirect, url_for, \
abort, render_template, flash


app=Flask(__name__)

@app.route('/')    #raw url..
def index():
	return render_template('index.html')

@app.route('/home', methods=['POST'])	#logged in
def home():
	import tweepy
	print request.form['one_user']
	username=request.form['one_user']

	auth = tweepy.OAuthHandler("aU39ahEGFuTOWxYKsJ9gDw", "kfxj6ngmHcbwaWKeGfBdCGrbFZJAsUYd21EOl5mQ")
	api=tweepy.API(auth)

	user = tweepy.api.get_user(username)


	#1  Followers cnt----------------------------------------------------------------------
	print user.followers_count
	grade_1 = user.followers_count / 500.0000 * 45.0000
	print grade_1

	#2 Followers power---------------------------------------------------------------------
	power=0
	i=0
	c = tweepy.Cursor(api.followers,username)
	user_followers = c.items()

	for follower in user_followers:
    		power += follower.followers_count


	power = power / user.followers_count

	if power < 500:
		grade_2 = power / 500.0000 * 20.0000
	else:
		grade_2 = 20.0000
	print grade_2

	#3 Retweet Computation----------------------------------------------------------------
	retweet_cnt=0

	c = tweepy.Cursor(api.user_timeline,username)
	user_tweets = c.items()
	tweepy.api.user_timeline(screen_name=username)
	disp_tweet = []
	ii=0
	for tweet in user_tweets:
		retweet_cnt+=tweet.retweet_count
		if ii < 10:
			disp_tweet.append(tweet.text)
		ii=ii+1


	if retweet_cnt < 100:
		grade_3 = retweet_cnt / 100.00 * 25
	else:
		grade_3 = 25
	print grade_3


	#5 Following Count---------------------------------------------------------------------
	if user.friends_count < 300:
		grade_5 =  user.friends_count / 300.000 * 6
	else:
		grade_5 = 6

	print grade_5

	#6 Tweets Count---------------------------------------------------------------------

	if user.statuses_count < 3000:
		grade_6 =  user.statuses_count / 3000.000 * 4
	else:
		grade_6 = 4

	print grade_6

	grade = grade_1 + grade_2 + grade_3 + grade_5 + grade_6
	print grade
	tmp = user.followers_count

	data =[user.name,user.profile_image_url,tmp,user.friends_count,user.statuses_count,grade]
	return render_template('home.html',data = data,disp_tweet=disp_tweet)

if __name__ == '__main__':
	app.run(debug=True)
