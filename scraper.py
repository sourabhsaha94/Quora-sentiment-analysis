from bs4 import BeautifulSoup
from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from cassandra.cqlengine.query import DoesNotExist
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model
import requests
import sys

base_url = 'https://www.quora.com/'
secret_sauce = '?share=1'
scrape_ques = []
class QuestionModel(Model):
    question_url = columns.Text(primary_key=True)
    question_que = columns.Text(required=True)
    question_body = columns.Text(required=True)

def scrape_que_and_ans(qs):
    scrape_ques = [] 
    if len(qs) == 0:
        return
    while len(qs) > 0:
        q = qs.pop(0)
        url = base_url + q.get('href') + secret_sauce
        try:
            QuestionModel.get(question_url=url)
            continue
        except DoesNotExist:
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            try:
                question = soup.select('div.question_text_edit span.rendered_qtext')[0].text
                bodyp  = soup.select('div.Answer span.rendered_qtext p')
                bodyli = soup.select('div.Answer span.rendered_qtext li')
                bodys  = soup.select('div.Answer span.rendered_qtext')
                body = bodyp + bodyli + bodys
                bodyt = ' '
                for b in body:
                    bodyt = bodyt + '. ' + b.text
                if bodyt != ' ':
                    print('Inserting: {}'.format(question.encode('utf-8')))
                    QuestionModel.create(
                            question_url=url,
                            question_que=question,
                            question_body=bodyt
                            )
                scrape_ques += soup.select('li.related_question a')
                if len(scrape_ques) > 10000:
                    break 
            except IndexError:
                continue
    scrape_que_and_ans(scrape_ques)

if __name__ == '__main__':
    connection.setup(['127.0.0.1'], 'cqlengine')
    sync_table(QuestionModel)
    scrape_que_and_ans([{ 'href': sys.argv[1] }])
