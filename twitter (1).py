from flask import Flask, request, redirect, render_template, session, make_response

import json
import datetime

import boto3
import uuid
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr #to help with scanning the table as we are searching by email instead of UserID

#code for the S3 bucket and Dynamo
#AWSKEY = 'AKIAQUFLQBDS3N7KO6FB'
#AWSSECRET = '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'
#PUBLIC_BUCKET = 'twitter-public-bucket'
#STORAGE_URL = 'https://s3.amazonaws.com/' + PUBLIC_BUCKET + '/'

AWSKEY = 'AKIAZPPF776CNURBMRH3'
AWSSECRET = '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'
PUBLIC_BUCKET = 'nstewart-web-public'
STORAGE_URL = 'https://s3.amazonaws.com/' + PUBLIC_BUCKET + '/'

def get_public_bucket():
    s3client = boto3.resource(service_name = 's3',
                            region_name = 'us-east-1',
                            aws_access_key_id = AWSKEY,
                             aws_secret_access_key = AWSSECRET
    )
    bucket = s3client.Bucket(PUBLIC_BUCKET)
    return bucket

def get_table(name):
    dbclient = boto3.resource(service_name = 'dynamodb',
                          region_name = 'us-east-1',
                          aws_access_key_id = AWSKEY,
                          aws_secret_access_key = AWSSECRET)

    table = dbclient.Table(name)
    return table

#####################################################################login codes#################################################3

def auto_login():
    cookie = request.cookies.get('remember')
    if cookie is None:
        return False
    table = get_table('Remember')
    result = table.get_item(Key={'key': cookie})
    if 'Item' not in result:
        return False

    remember = result['Item']
    email = remember['email']
    table = get_table('TUsers')
    getResult = table.get_item(Key={'email':email})
    user = getResult['Item']

    session['email'] = user['email']
    session['username'] = user['username']
    session['TUserID'] = user['TUserID'] #K put this here
    return True

def get_remember_key(email):
    table = get_table('Remember')
    key = str(uuid.uuid4()) + str(uuid.uuid4())
    item = {'key' : key, 'email' : email}
    table.put_item(Item=item)
    return key

def login():
    email = request.args.get('email', '')
    password = request.args.get('password', '')


    if not email or not password:
        return{'result': 'Bad Login'}

    table = get_table('TUsers')
    #scans table till matching email is found, needed since second sort key is not established in table build
    response = table.scan(FilterExpression=Attr('email').eq(email))


    if 'Items' not in response or not response['Items']:
        return {'result': 'Email not found'}

    user = response['Items'][0] #get first match

    if password != user['password']:
        return {'result': 'Password not valid'}

    #at this point, the email and password are correct
    session['email'] = user['email']
    session['username'] = user['username']
    session['TUserID'] = user['TUserID'] #K added this here

    result =  {'result': 'OK', 'username': session['username']}
    response = make_response(result)


    remember = request.args.get('remember', 'no')
    if remember == 'no':
        response.delete_cookie('remember')
    else:
        key = get_remember_key(user['email'])
        response.set_cookie('remember', key, max_age=60*60*24*14) #remember for 14 days

    return response


####################################################Sign up Code##################################################################

def is_email_taken(email):
    table = get_table('TUsers')
    response = table.scan(FilterExpression=Attr('email').eq(email))
    return len(response['Items'])>0

def is_valid_email(email):
    return '@' in email and '.' in email

def signup():
    #bucket = get_public_bucket()
    #file = request.files["file"]
    #filename = file.filename
    #ct = 'image/jpeg'
    #if filename.endswith('.png'):
        #ct = 'image/png'
    #bucket.upload_fileobj(file, filename, ExtraArgs = {'ContentType': ct})

    imageTable = get_table('Image')
    table = get_table('TUsers')

    txtNewEmail = request.args.get('email')
    txtNewUsername = request.args.get('username')
    txtNewPassword = request.args.get('password')

    if not txtNewUsername or not  txtNewEmail:
        return {'result' : 'Username/Email can not be blank'}

    #basic email format validation
    if not is_valid_email(txtNewEmail):
        return {'result':'Invalid email format'}

    if is_email_taken(txtNewEmail):
        return {'return': 'Email is already in use'}

    TUserID = str(uuid.uuid4()) #need to generate unique ID in order for item to be put into table

    account = {'username' : txtNewUsername,
                'email' : txtNewEmail,
                'password' : txtNewPassword,
                'TUserID': TUserID,     # we can figure out how to add a user's default pfp
                'profilePic': {'ImageID' : str(uuid.uuid4()),
                                'Filename' : 'https://i.pinimg.com/736x/2f/15/f2/2f15f2e8c688b3120d3d26467b06330c.jpg',
                                'user_id' : TUserID
                }
    }

    session['email'] = txtNewEmail
    session['username'] = txtNewUsername
    session['TUserID'] = account['TUserID'] # K added this in

    image = account['profilePic']
    imageTable.put_item(Item=image)

    table.put_item(Item=account)
    #return{'result' : 'OK', 'TUserID': TUserID}
    return{'result': 'OK', 'username' : txtNewUsername} #Carmines request

#############################################Profile code############################################################################
def userProfile(username): #might use these later
    #hope this works
    userTable = get_table('TUsers')
    results = []
    for item in userTable.scan()['Items']:
        if (username == item['username']):
            #posts = listProfilePosts(item["user_id"])
            u = {'username': item['username'],'email': item['email'], 'password': item['password'], 'TUserID': item['TUserID'], 'profilePic': item['profilePic']} #add back in "profilePic": item["profilePic"] later
            results.append(u)
    return {'profileResults': results}
def someoneProfile(username): #might use these later
    #also hope this works
    userTable = get_table('TUsers')
    results = []
    for item in userTable.scan()['Items']:
        if (username == item['username']):
            #posts = listProfilePosts(item["TUserID"])
            u = {'username': item['username'],'email': item['email'], 'password': item['password'], 'TUserID': item['TUserID'], 'profilePic': item['profilePic']}#all items needed for displaying profile is in this json, and add back in "profilePic": item["profilePic"] later
            results.append(u)
    return {'profileResults': results}
def send_Username():
    username = request.args.get("username")
    userTable = get_table("TUsers")
    for item in userTable.scan()['Items']:
        if (username == item['username']):
            profile_username = item['username']
    return render_template('profile.html', profile_username=profile_username)
def send_SessionUsername():
    session_username = session['username']
    return render_template('profile.html', session_username=session_username)
def send_SessionUserID():
    TUserID = session['TUserID']
    return render_template('profile.html', TUserID=TUserID)
def send_imageID():
    user_id = request.args.get("user_id")
    userTable = get_table("TUsers")
    for item in userTable.scan()['Items']:
        if (user_id == item['user_id']):
            profile_pfpID = item['user_id']
    return render_template('profile.html', profile_pfpID)
def addPost(user_id): #coming back to test once I get the profile fixed
    table = get_table('TPosts')

    postID = str(uuid.uuid4())
    text = request.form.get("text")
    date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
    #userID = request.form.get("userID")
    #parent_id = str(uuid.uuid4()) removing as this is causing replies to show up on feed

    post = {'TPostID': postID, #might need to change to TPostID
            'text': text,
            'date': date,
            'user_id': user_id,
            #'parent_id': parent_id only include parent id if it is a reply
    }
    table.put_item(Item=post)
    return {'results':'OK'}

def uploadImage(user_id): #maybe delete current image and replace it here (thank you)
    bucket = get_public_bucket()
    file = request.files["file"]
    filename = file.filename
    ct = 'image/jpeg'
    if filename.endswith('.png'):
        ct = 'image/png'
    bucket.upload_fileobj(file, filename, ExtraArgs = {'ContentType': ct})

    table = get_table('Image') #hope this is the right table
    for item in table.scan()['Items']:
        if (item['user_id'] == user_id):
            ImageID = item['ImageID']
            table.delete_item(Key={'ImageID':ImageID})

    ImageID = str(uuid.uuid4())

    image = {'ImageID': ImageID,  #new image added
            'Filename': filename,
            'user_id': user_id
    }
    table.put_item(Item=image)
    return {'results':'OK'}

def showPfp(user_id):
    table = get_table('Image')
    results = []
    imageID = ''
    for item in table.scan()['Items']:
        if (item.get('user_id') == user_id):
            d = {"ImageID":item["ImageID"],"Filename": item["Filename"], "user_id": item.get('user_id')}
            imageID = item["ImageID"]
            results.append(d)

    bucket = get_public_bucket() #s3 part
    items = []
    for item in bucket.objects.all():
        if (imageID == item.key):
            items.append(item.key)

    return {'results':results, 'url':STORAGE_URL, 'items':items}

def listProfilePosts(user_id):
    table = get_table('TPosts')
    results = []
    for item in table.scan()['Items']:
        #if (user_id == item['user_id']):
        if item.get('user_id') == user_id and item.get('parent_id') in [None, '', 'null']: #added the and
            d = {"TPostID": item["TPostID"], "text": item["text"], "date": item["date"], "user_id": item.get('user_id'), "parent_id": item.get('parent_id')} #might need to change postID -> TPostID

            #only add parent_id if it exists (test)
            if "parent_id" in item:
                d["parent_id"] = item["parent_id"]

            results.append(d)

    results = sorted(results, key=lambda x: x['date'], reverse=True)
    return {'results': results}
    #return results

############################################ Feed Codes ###########################################################################
def list_posts():
    table = get_table('TPosts')
    post_list = []
    for item in table.scan()['Items']:

        #added to only include posts that are NOT replies to the feed
        #if 'parent_id' not in item:
        if item.get('parent_id') in [None, '', 'null']:
	        s = {'TPostID' : item['TPostID'], 'text' : item['text'], 'date' : item['date'], 'user_id': item.get('user_id')}
	        post_list.append(s)

    post_list = sorted(post_list, key=lambda x:x['date'], reverse=True)
    recent_posts = post_list[:10] #get the first 10

    for post in recent_posts:
        user_id = post.get('user_id')
        #if user_id:
	        #username = get_username_byId(user_id)
            #posts['username'] = username
	    #else:
	        #posts['username'] = 'Unknown User"
        post['username'] = get_username_byId(user_id) if user_id else 'Uknown User'
    session_username = session.get('username')
    return {'result': 'OK', 'posts': recent_posts, 'session_username' : session_username}

def get_username_byId(user_id):
    if not user_id:
        return "Unknown User"

    user_table = get_table('TUsers')

    response = user_table.get_item(
        Key={
            'TUserID' : user_id
        }
    )
    if 'Item' in response:
        return response['Item'].get('username', 'Unknown User')
    return 'Unknown User'

###################################### Post View Codes ########################################3
def get_post_view(post_id):
    table = get_table('TPosts')
    posts = table.scan()['Items']

    post = next((p for p in posts if p['TPostID'] == post_id), None)
    if not post:
        return {'result': 'Error', 'message': 'Post not found'}

    post['username'] = get_username_byId(post.get('user_id'))

    # Find replies where parent_id == post_id
    replies = [p for p in posts if p.get('parent_id') == post_id]

    for reply in replies:
        reply['username'] = get_username_byId(reply.get('user_id'))

    replies = sorted(replies, key=lambda r: r['date'])

    return {'result': 'OK', 'post': post, 'replies': replies}

def addReply(user_id, parent_id, text):
    if not user_id or not parent_id or not text:
        return {'result':'Error', 'message': 'Missing requried fields'}

    table = get_table('TPosts')
    reply_id = str(uuid.uuid4())
    #parent_id = request.form.get('parent_id')
    #text = request.form.get('text')
    date = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")

    reply = {
        'TPostID': reply_id,
        'text': text,
        'date': date,
        'user_id': user_id,
        'parent_id': parent_id
    }
    table.put_item(Item=reply)
    return {'result': 'OK'}
