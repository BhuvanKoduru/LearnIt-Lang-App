import requests

url = "https://thefluentme.p.rapidapi.com/post"

words = {
    'Olá ':'Hello',
    'Amor': 'Love',
    'Felicidade':'Happiness',
    'Gato':'cat',
    'Cão' : 'Dog',
    'Sim':'Yes',
    'Obrigado':'Thank You',
    'amanhã':'Tomorrow',
    'Ontem':'Yesterday',
    'Seguendo':'Second',
    'Ponte':'Bridge',
    'Rua':'Street',
    'Suco':'Juice',
    'Bolo':'cake',
    'bom':'Good',
    'frio':'cold',
}
i = 0
for word in words:
	payload = {
		"post_language_id": "57",
		"post_title": "test"+str(i),
		"post_content": word
	}
	headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "a975cce100msh85e7f0a286a7052p170016jsn7d628e53b9fa",
	"X-RapidAPI-Host": "thefluentme.p.rapidapi.com"
	}

	response = requests.post(url, json=payload, headers=headers)
	i+=1
	print(response.json())
