from app.catalog.types import T, Topic

# Conversation starters shown as chips. Add one entry to add a topic.
TOPICS: tuple[Topic, ...] = (
    Topic("day", T("Ma journée", "My day"), "Let's talk about my day."),
    Topic("news", T("L'actualité", "The news"), "I'd like to talk about the news today."),
    Topic("sport", T("Le sport et le foot", "Sport and football"), "Let's talk about sport, especially football."),
    Topic("politics", T("Un débat politique", "A political debate"), "I'd like to discuss a political topic. Ask me what I think."),
    Topic("work", T("Mon travail", "My work"), "Let's talk about my work."),
    Topic("family", T("Famille et amis", "Family and friends"), "Let's talk about my family and friends."),
    Topic("movies", T("Films et séries", "Movies and series"), "Let's talk about movies and series."),
    Topic("music", T("Musique", "Music"), "Let's talk about music."),
    Topic("food", T("Cuisine et repas", "Food and cooking"), "Let's talk about food and cooking."),
    Topic("travel", T("Voyages", "Travel"), "Let's talk about travel and places I know."),
    Topic("tech", T("Technologie et IA", "Technology and AI"), "Let's talk about technology and artificial intelligence."),
)
