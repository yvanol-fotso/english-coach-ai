from app.catalog.types import T, Unit

# The beginner course (A0 to A1). Each unit is taught in any available language: add a unit here
# and it exists everywhere. Lessons are written by the model, then cached.
UNITS: tuple[Unit, ...] = (
    Unit("hello", T("Dire bonjour", "Saying hello"), T("Saluer, remercier, prendre congé", "Greet, thank, say goodbye"),
         "greetings and politeness: hello, goodbye, please, thank you, excuse me, how are you"),
    Unit("me", T("Se présenter", "Introducing yourself"), T("Dire son nom, son pays, son âge", "Say your name, country, age"),
         "introducing yourself: my name is, I am from, I am ... years old, nice to meet you, do you speak"),
    Unit("numbers", T("Les nombres", "Numbers"), T("Compter de 0 à 20 et dire un prix", "Count from 0 to 20 and say a price"),
         "numbers from 0 to 20, simple prices, how many, phone numbers"),
    Unit("family", T("La famille", "Family"), T("Présenter sa famille et ses amis", "Talk about family and friends"),
         "family members, this is my..., he/she is, I have a brother/sister"),
    Unit("food", T("Manger et boire", "Food and drink"), T("Commander au restaurant", "Order in a restaurant"),
         "food and drinks, I would like, the menu, the bill, I like / I don't like"),
    Unit("day", T("Ma journée", "My day"), T("Parler de ses habitudes et de l'heure", "Talk about routines and the time"),
         "daily routine, the time, morning/afternoon/evening, I wake up, I work, I eat", "A1"),
    Unit("places", T("Se repérer", "Finding your way"), T("Demander et comprendre un chemin", "Ask for and understand directions"),
         "where is, left, right, straight on, near, far, the station, the bank", "A1"),
    Unit("shopping", T("Faire des achats", "Shopping"), T("Demander un prix, acheter", "Ask a price, buy things"),
         "how much is it, too expensive, I'll take it, sizes, colors, paying", "A1"),
    Unit("feelings", T("Santé et émotions", "Health and feelings"), T("Dire comment on va", "Say how you feel"),
         "I am tired/happy/sad, I have a headache, I need a doctor, are you ok", "A1"),
    Unit("plans", T("Projets et invitations", "Plans and invitations"), T("Proposer, accepter, refuser", "Suggest, accept, refuse"),
         "what are you doing tomorrow, would you like to, let's meet at, I can't, see you soon", "A1"),
)
