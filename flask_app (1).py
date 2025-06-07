
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, redirect, request, render_template, session, make_response

from flask_session import Session

from twitter import get_table #testing

import twitter

app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

def is_logged_in():
    if not session.get('email'):
        return twitter.auto_login()
    return True

@app.route('/project5') #change the route to be /final --> its on the pdf instructions
def project5(): #change this as well (only once everything is done and working change the /project5's btw)
    return render_template('home.html')

@app.route('/signup.html')
def signup_html():
    return render_template('signup.html')

@app.route('/twitter/signup', methods=['GET'])
def signup_endpoint():
    #txtNewEmail = request.args.get('email')
    #txtNewUsername = request.args.get('username')
    #txtNewPassword = request.args.get('password')


    #result = twitter.signup(txtNewEmail, txtNewUsername, txtNewPassword)

    #if result.get('result') == 'OK':
      #  session['email'] = txtNewEmail
      #  session['username'] = txtNewUsername

   # if result.get('result') == 'OK':
     #   return '{"result": "OK"}'
   # else:
      #  error_message = result.get('result', 'Unknown error')
      #  return '{"result": "' + error_message + '"}'
      return twitter.signup()

@app.route('/login.html')
def login_html():
    return render_template('login.html')

@app.route('/twitter/login')
def twitter_login():
    return twitter.login()

@app.route('/logout.html')
def logout():
    session.pop('email', None)
    session.pop('username', None)
    response = make_response( redirect('/project5')) #change to /final
    response.delete_cookie('remember')
    return response

@app.route('/profile.html')
def base_profile():
    return render_template('profile.html')

@app.route('/profile/<username>') #extra help for handling
@app.route('/twitter/profile/<username>')
#def profile():
def profile(username): #changed to handle the new updates made
    #profile_username = request.args.get('username')
   # session_username = session.get('username')
    #TUserID = session.get('TUserID')

    #fetch user profile data
    #profile_data = twitter.userProfile(username) #testing

    #return render_template('profile.html', session_username = session_username, profile_username = profile_username)
    #return render_template('profile.html', session_username = session_username, profile_username = username, TUserID=TUserID) test

    #return render_template('profile.html', session_username = session_username, profile_username = username, TUserID=TUserID, profile_data = profile_data) test

    return render_template('profile.html', session_username = session.get('username'), profile_username = username, TUserID = session.get('TUserID'))


    #if (currentUser == username):
        #looking at self
        #return render_template('profile.html', username = currentUser)
        #tried: profile_data = twitter.userProfile(username)

    #else:
        #looking at someone else
        #return render_template('profile.html', username = username)
        #tried: profile_data = twitter.someoneProfile(username)

    # tried: user_data = profile_data.get('profileResults', [])[0] if profile_data.get('profileResults') else None
    # tried: user_id = user_data.get('TUserID') if user_data else ''

    #tried: return render_template('profile.html',username=username, profile_username = username, session_username=currentUser,TUserID=session.get('TUserID', ''))


@app.route('/twitter/profile/uploadImage', methods = ['POST'] )
def profile_uploadImage():
    TUserID = session.get('TUserID') #remember to put TUserID in session
    return twitter.uploadImage(TUserID)

@app.route('/twitter/profile/addPost', methods = ['POST'])
def profile_addPost():
    TUserID = session.get('TUserID') #remember to put TUserID in session
    return twitter.addPost(TUserID)

@app.route('/twitter/profile/showPfp')
def profile_showPfp():
    user_id = request.args.get('user_id')
    return twitter.showPfp(user_id)

@app.route('/twitter/userProfile/<username>') #just to check that all the info is inside
def profile_stuff(username):
    return twitter.userProfile(username)

@app.route('/twitter/profile/listProfilePosts')
def profile_listProfilePosts():
    #TUserID = session.get('TUserID')

    #testing
    username = request.args.get('username')
    userTable = get_table('TUsers')
    TUserID = ''
    for item in userTable.scan()['Items']:
        if item['username'] == username:
            TUserID = item['TUserID']
            break
    if (TUserID != ''):
        return twitter.listProfilePosts(TUserID)
    else:
        return {'results':[]}
    #return twitter.listProfilePosts(TUserID)

@app.route('/feed')
def feed():
    if not is_logged_in():
        return redirect('/login.html')

    return render_template('feed.html')

@app.route('/feed.html')
def twitter_feed():
    return render_template('feed.html')

@app.route('/twitter/list_posts')
def twitter_list_posts():
    return twitter.list_posts()

@app.route('/post.html')
def post():
    return render_template('post.html')

@app.route('/twitter/post', methods=['GET'])
def get_post():
    post_id = request.args.get("id")
    if not post_id:
        return {'result': 'Error', 'message': 'Missing post ID'}

    return twitter.get_post_view(post_id)

@app.route('/twitter/post/view')
def view_post():
    post_id = request.args.get("id")
    if not post_id:
        return redirect ('/feed') #redirects to feed if no post ID

    return render_template('post.html')

@app.route('/twitter/post/reply', methods=['POST'])
def reply_post():
    if not is_logged_in():
        return {'result': 'Error', 'message': 'User not logged in'}

    user_id = session.get("TUserID")
    parent_id = request.form.get('parent_id')
    text = request.form.get('text')

    if not parent_id or not text:
        return {'result': 'Error', 'message': 'Missing required fields'}

    return twitter.addReply(user_id, parent_id, text)