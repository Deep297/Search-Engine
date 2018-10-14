from bottle import route, run, get, post, request, static_file, template
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import bottle

# Global dictionary used to store all searched keywords
keywords = {}

@route('<filename:re:.*\.css>', name="static")
def css(filename):
    print ("css:" + filename)
    return static_file(filename, root='./', mimetype='text/css')

# Display main search engine page without showing any tables by default
@route('/')
def hello():
  return template('Main-Page.html',ResultsTable="", HistoryTable="" ,root='./')

# Function that gets called when a user hits Submit button
@route('/', method="POST")
def count_words():
    # Get input string from input field and conver to lower case
    inputString = (request.forms.get('keywords')).lower()

    # Local dictionary used to store keywords from current search
    worddict = {}

    '''
        Go through every word in the input string and check if it exists
        in the global keywords dictionary and the local search keywords
        dictionary. If word exits, increment word count.
    '''
    for word in inputString.split():
        if word in worddict:
            worddict[word] += 1
        else:
            worddict[word] = 1
        if word in keywords:
            keywords[word] += 1
        else:
            keywords[word] = 1
    table = create_results_table(worddict)
    topWordsTable = create_history_table(keywords)
    # Reload main search page with results and search history tables
    return template('Main-Page.html', ResultsTable=table, HistoryTable=topWordsTable)

# Function used to generate HTML results table
def create_results_table(word_dict):
    table = '\t<table class="table table-bordered" id="results">\n'
    top_words_sorted = sorted(word_dict, key=word_dict.get, reverse=True)
    for word in top_words_sorted:
        table+="\t<tr>\n"
        table+="\t<td>" + word + "</td>\n"
        table+="\t<td>" + str(word_dict[word]) + "</td>\n"
        table+="\t</tr>\n"
    table += "\t</table>"
    return table

# Function usedd to generate HTML search history table
def create_history_table(top_words):
    table = '\t<table class="table table-bordered" id="history">\n'
    top_words_sorted = sorted(top_words, key=top_words.get, reverse=True)
    for word in top_words_sorted[:20]:
        table+="\t<tr>\n"
        table+="\t<td>" + word + "</td>\n"
        table+="\t<td>" + str(top_words[word]) + "</td>\n"
        table+="\t</tr>\n"
    table += "\t</table>"
    return table


@route('/sign-in')
def home():
    flow = flow_from_clientsecrets("client_secrets.json", scope="https://www.googleapis.com/auth/plus.me",
                                    redirect_uri="http://localhost:8080/redirect")
    uri = flow.step1_get_authorize_url()
    bottle.redirect(str(uri))

@route('/redirect')
def redirect_page():
    code = request.query.get('code', '')

run(host='localhost', port=8080, debug=True)
