# pylint: disable=line-too-long, too-many-arguments, too-many-instance-attributes

"""
Methods for sending exercise answers to the testing server and checking grades and available tasks.
"""

import os
import requests
import inspect
from IPython.display import display, clear_output, Markdown
import ipywidgets as widgets
from . import config
from IPython.core.interactiveshell import InteractiveShell


class GradesBy:
    EXERCICE = "EXERCICE"
    TASK = "TASK"


class ActivitySender:
    """
    Class for sending exercise answers to the testing server
    """

    def __repr__(self):
        return f"ActivitySender(answer={self.answer}, task={self.task}, question={self.question}, answer_type={self.answer_type}, subject={self.subject}, offering={self.offering}, url={self.url})"

    def __str__(self):
        return f"ActivitySender(answer={self.answer}, task={self.task}, question={self.question}, answer_type={self.answer_type}, subject={self.subject}, offering={self.offering}, url={self.url})"

    def __init__(
        self,
        answer,
        task,
        question,
        answer_type="pyvar",
        subject=None,
        offering=None,
        token=None,
        url=None,
    ):
        self.answer = answer
        self.task = task
        self.question = question
        self.answer_type = answer_type
        if subject is None:
            subject = os.getenv("IAG_SUBJECT")
        self.subject = subject

        if offering is None:
            offering = os.getenv("IAG_OFFERING")
        self.offering = offering

        if token is None:
            token = os.getenv("IAG_TOKEN")
        self.token = str(token)

        if url is None:
            base_url = os.getenv("IAG_SERVER_URL")
            url = f"{base_url}/test"
        self.url = url

    def _display_header(self):
        display(
            Markdown(
                f"### Enviando exercício `{self.question}` da `{self.task}` para o servidor..."
            )
        )

    def _display_answer(self):
        display(
            Markdown(
                f"""
**Resposta enviada**:
```
{self._full_answer}
```
Aguarde... <img src="{config.URL_IMG_WAITING}" width="200" heigth="200">
"""
            )
        )

    @property
    def _full_answer(self):
        if self.answer_type not in ("pyvar", "pycode", "plain"):
            raise AttributeError(
                'Argumento `answer_type` inválido. Valores aceitos: `"plain"`, `"pyvar"` ou `"pycode"`.'
            )

        if self.answer_type == "plain":
            return self.answer

        glob = __import__("__main__").__dict__

        if not self.answer in glob:
            raise AttributeError(
                f"`{self.answer}` não encontrada. Confira o identificador ou execute a célula com a declaração da variável ou função!"
            )

        if self.answer_type == "pyvar":
            return glob[self.answer]

        # pycode case
        return inspect.getsource(glob[self.answer])

    def _send(self):
        self._display_header()

        self._display_answer()

        headers = {"Authorization": "Bearer " + self.token}

        data = {
            "task_name": self.task,
            "question_name": self.question,
            "subject_name": self.subject,
            "offering_name": self.offering,
            "answer": self._full_answer,
        }

        req = requests.post(
            self.url, json=data, headers=headers, timeout=config.POST_TASKS_TIMEOUT
        )
        clear_output()
        display(Markdown(req.text[1:-1].replace("\\n", "\n")))


def sender(
    answer,
    task,
    question,
    answer_type="pyvar",
    subject=None,
    offering=None,
    token=None,
    url=None,
):
    act_sender = ActivitySender(
        answer=answer,
        task=task,
        question=question,
        answer_type=answer_type,
        subject=subject,
        offering=offering,
        token=token,
        url=url,
    )
    button = widgets.interactive(
        act_sender._send, {"manual": True, "manual_name": f"Enviar {question}"}
    )
    return button


def tasks(subject=None, offering=None, url=None):
    if subject is None:
        subject = os.getenv("IAG_SUBJECT")

    if offering is None:
        offering = os.getenv("IAG_OFFERING")

    if subject is None or offering is None:
        clear_output()
        display(Markdown("Defina os argumentos `subject` e `offering`!"))
        return

    if url is None:
        url = os.getenv("IAG_SERVER_URL")

    url = f"{url}/tasks/{subject}/{offering}"
    req = requests.get(url=url, timeout=config.GET_TASKS_TIMEOUT)

    clear_output()
    display(Markdown(req.text[1:-1].replace("\\n", "\n")))


def grades(by=GradesBy.EXERCICE, subject=None, offering=None, task=None, url=None):
    if subject is None:
        subject = os.getenv("IAG_SUBJECT")

    if offering is None:
        offering = os.getenv("IAG_OFFERING")

    if subject is None or offering is None:
        clear_output()
        display(Markdown("Defina os argumentos `subject` e `offering`!"))
        return

    if url is None:
        url = os.getenv("IAG_SERVER_URL")

    if by == GradesBy.EXERCICE:
        route = "grade_by_exercice"
    else:
        route = "grade_by_task"

    if task is None:
        url = f"{url}/{route}/{subject}/{offering}"
    else:
        url = f"{url}/{route}/{subject}/{offering}/{task}"

    token = os.getenv("IAG_TOKEN")
    headers = {"Authorization": "Bearer " + token}
    req = requests.get(url=url, headers=headers, timeout=config.GET_GRADES_TIMEOUT)

    clear_output()
    display(Markdown(req.text[1:-1].replace("\\n", "\n")))
