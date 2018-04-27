from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


def get_friends(users):
    import itertools
    import tweepy

    def paginate(iterable, page_size):
        while True:
            i1, i2 = itertools.tee(iterable)
            iterable, page = (itertools.islice(i1, page_size, None),
                              list(itertools.islice(i2, page_size)))
            if len(page) == 0:
                break
            yield page

    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""

    '''
    from flaskapp.credentials import Credential
    c = Credential()
    auth = tweepy.OAuthHandler(c.consumer_key, c.consumer_secret)
    auth.set_access_token(c.access_token, c.access_token_secret)
    '''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    friends = []
    friends1 = []
    friends2 = []

    followers = api.followers_ids(screen_name=users[0])
    print(len(followers))

    for page in paginate(followers, int(len(followers)/20)+1):
        results = api.lookup_users(user_ids=page)
        for result in results:
            friends1.append(result.screen_name)

    followers = api.followers_ids(screen_name=users[1])
    for page in paginate(followers, int(len(followers)/20)+1):
        results = api.lookup_users(user_ids=page)
        for result in results:
            friends2.append(result.screen_name)

    for friend1 in friends1:
        for friend2 in friends2:
            if friend1 == friend2:
                friends.append(friend1)

    return friends

@app.route('/result', methods = ['POST'])
def result():
    if request.method == 'POST':
        user1 = request.form['user1']
        user2 = request.form['user2']
        users = [user1, user2]
        friends = get_friends(users)

    return render_template('result.html', friends = friends, users = users)


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
