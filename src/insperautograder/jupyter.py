import requests
import os
from dotenv import load_dotenv
from IPython.display import display, clear_output, Markdown
import ipywidgets as widgets

load_dotenv(override=True)

class GradesBy:
    EXERCICE='EXERCICE'
    TASK='TASK'

class ActivitySender():

    def __init__(self, answer, task, question, answer_type='pyvar', subject=None, offering=None, token=None, url=None):
        self.answer = answer
        self.task = task
        self.question = question
        self.answer_type = answer_type
        if subject is None:
            subject = os.getenv('IAG_SUBJECT')
        self.subject = subject

        if offering is None:
            offering = os.getenv('IAG_OFFERING')
        self.offering = offering

        if token is None:
            token = os.getenv('IAG_TOKEN')
        self.token = str(token)

        if url is None:
            base_url = os.getenv('IAG_SERVER_URL')
            url = f'{base_url}/test'
        self.url = url

    def display_header(self):
        display(Markdown(f'### Enviando exercício `{self.question}` da `{self.task}` para o servidor...'))

    def display_answer(self):
        display(Markdown(f'''
**Resposta enviada**:
```
{self.full_answer}
```
Aguarde... <img src="https://github.com/Codelessly/FlutterLoadingGIFs/blob/master/assets/images/cupertino_activity_indicator_small.gif?raw=true" width="200" heigth="200">
'''))

    @property
    def full_answer(self):
        glob = __import__('__main__').__dict__
        if self.answer_type == 'pyvar':
            if self.answer in glob:
                return glob[self.answer]
            else:
                raise AttributeError(f'Variável `{self.answer}` não encontrada. Confira o identificador ou execute a célula com a declaração da variável!')
        elif self.answer=='plain':
            return self.answer
        else:
            raise AttributeError(f'Argumento `answer_type` inválido. Valores aceitos: `"pyvar"` ou `"plain".`')


    def send(self):

        self.display_header()

        self.display_answer()

        headers = {'Authorization': 'Bearer ' + self.token}

        data = {

            'task_name': self.task,
            'question_name': self.question,
            'subject_name': self.subject,
            'offering_name': self.offering,
            'answer': self.full_answer
        }

        req = requests.post(self.url, json=data, headers=headers)
        clear_output()
        display(Markdown(req.text[1:-1].replace('\\n', '\n')))

def sender(answer, task, question, answer_type='pyvar', subject=None, offering=None, token=None, url=None):
    act_sender = ActivitySender(
                                    answer= answer,
                                    task=task,
                                    question=question,
                                    answer_type=answer_type,
                                    subject=subject,
                                    offering=offering,
                                    token=token,
                                    url=url
                                )
    button = widgets.interactive(
                                    act_sender.send,
                                    {
                                        'manual': True,
                                        'manual_name': f'Enviar {question}'
                                    }
                                )
    return button


def tasks(subject=None, offering=None, url=None):

    if subject is None:
        subject = os.getenv('IAG_SUBJECT')

    if offering is None:
        offering = os.getenv('IAG_OFFERING')

    if subject is None or offering is None:
        clear_output()
        display(Markdown('Defina os argumentos `subject` e `offering`!'))
        return

    if url is None:
        url = os.getenv('IAG_SERVER_URL')

    url = f'{url}/tasks/{subject}/{offering}'
    req = requests.get(url=url)

    clear_output()
    display(Markdown(req.text[1:-1].replace('\\n', '\n')))


def grades(by=GradesBy.EXERCICE, subject=None, offering=None, task=None, url=None):

    if subject is None:
        subject = os.getenv('IAG_SUBJECT')

    if offering is None:
        offering = os.getenv('IAG_OFFERING')

    if subject is None or offering is None:
        clear_output()
        display(Markdown('Defina os argumentos `subject` e `offering`!'))
        return

    if url is None:
        url = os.getenv('IAG_SERVER_URL')

    if by == GradesBy.EXERCICE:
        route = 'grade_by_exercice'
    else:
        route = 'grade_by_task'

    if task is None:
        url = f'{url}/{route}/{subject}/{offering}'
    else:
        url = f'{url}/{route}/{subject}/{offering}/{task}'
    
    token = os.getenv('IAG_TOKEN')
    headers = {'Authorization': 'Bearer ' + token}
    req = requests.get(url=url, headers=headers)

    clear_output()
    display(Markdown(req.text[1:-1].replace('\\n', '\n')))