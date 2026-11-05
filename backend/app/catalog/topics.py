from app.catalog.types import S, T, Topic

# Conversation starters shown as chips. Add one entry to add a topic.
TOPICS: tuple[Topic, ...] = (
    Topic("day", T("Ma journée", "My day"), S("Let's talk about my day.", "Parlons de ma journée.", "Hablemos de mi día.")),
    Topic("news", T("L'actualité", "The news"), S("I'd like to talk about the news today.", "J'aimerais parler de l'actualité.", "Me gustaría hablar de las noticias.")),
    Topic("sport", T("Le sport et le foot", "Sport and football"), S("Let's talk about sport, especially football.", "Parlons de sport, surtout de football.", "Hablemos de deporte, sobre todo de fútbol.")),
    Topic("politics", T("Un débat politique", "A political debate"), S("I'd like to discuss a political topic. Ask me what I think.", "J'aimerais discuter d'un sujet politique. Demande-moi ce que j'en pense.", "Me gustaría hablar de un tema político. Pregúntame qué pienso.")),
    Topic("work", T("Mon travail", "My work"), S("Let's talk about my work.", "Parlons de mon travail.", "Hablemos de mi trabajo.")),
    Topic("family", T("Famille et amis", "Family and friends"), S("Let's talk about my family and friends.", "Parlons de ma famille et de mes amis.", "Hablemos de mi familia y mis amigos.")),
    Topic("movies", T("Films et séries", "Movies and series"), S("Let's talk about movies and series.", "Parlons de films et de séries.", "Hablemos de películas y series.")),
    Topic("music", T("Musique", "Music"), S("Let's talk about music.", "Parlons de musique.", "Hablemos de música.")),
    Topic("food", T("Cuisine et repas", "Food and cooking"), S("Let's talk about food and cooking.", "Parlons de cuisine et de repas.", "Hablemos de comida y cocina.")),
    Topic("travel", T("Voyages", "Travel"), S("Let's talk about travel and places I know.", "Parlons de voyages et de lieux que je connais.", "Hablemos de viajes y lugares que conozco.")),
    Topic("tech", T("Technologie et IA", "Technology and AI"), S("Let's talk about technology and artificial intelligence.", "Parlons de technologie et d'intelligence artificielle.", "Hablemos de tecnología e inteligencia artificial.")),
)
