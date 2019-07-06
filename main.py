#! /usr/bin/python3

import logging
import flask
import pandas as pd
import sqlalchemy
import json
import random
import copy

app = flask.Flask(__name__)


sqla_logger = logging.getLogger('sqlalchemy')
sqla_logger.propagate = False
# sqla_logger.addHandler(logging.FileHandler('/path/to/sqla.log'))

#------------------------------------------------------------------------------------------------#

# for mysql database. the user must have atleast "CREATE" and "SELECT" permissions.
user_name = 'yash'
user_pwd = '1234'
database_name = 'tag_cloud'
database_addr = 'localhost:3306'

#------------------------------------------------------------------------------------------------#




# connect to mysql database
engine = sqlalchemy.create_engine('mysql+mysqlconnector://' + user_name +
                                  ':' + user_pwd + '@' + database_addr + '/' + database_name, echo=True)

# load the csv files and add them to databse
quotes = pd.read_csv('data/quotes.csv')
quotes.to_sql(con=engine, name='quotes', if_exists='replace', index=False)
del quotes
words = pd.read_csv('data/words.csv')
words.to_sql(con=engine, name='words', if_exists='replace', index=False)
del words

# execute sql query
# select search_word, sum((length(quote) - length(replace(quote, search_word, '')))/length(search_word)) as count from words, quotes group by search_word
mysql_query = """SELECT search_word, SUM((LENGTH(quote) - LENGTH(REPLACE(quote, search_word, ''))) / LENGTH(search_word)) AS count
                    FROM words, quotes
                    GROUP BY search_word
                    ORDER BY count DESC"""

query_result = engine.execute(mysql_query)

word_count = pd.DataFrame(query_result)
word_count.columns = query_result.keys()
word_count['count'] = word_count['count'].astype(int)
count = word_count.to_dict(orient='records')

count_rand = copy.deepcopy(count)

# scale the count to use as font size
for i in range(len(count_rand)):
    temp = count_rand[i]['count']
    temp *= temp

    count_rand[i]['count'] += 50 - ((60/max(1, temp)) + 20)

print(count_rand)

@app.route('/')
def home():
    return flask.render_template('table.html', rows=count)


@app.route('/pretty')
def pretty():
    random.shuffle(count_rand)
    return flask.render_template('pretty.html', rows=count_rand)

if __name__ == '__main__':
    app.run('0.0.0.0', port='5000')
