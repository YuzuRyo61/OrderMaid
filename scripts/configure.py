from PyInquirer import prompt

questions = [
    {
        "type": "input",
        "name": "client_id",
        "message": "Please input Discord application client ID"
    },
    {
        "type": "password",
        "name": "token",
        "message": "Please input Discord token"
    }
]

answers = prompt(questions)
