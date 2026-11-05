from app.catalog.types import S, T, Scenario

# To add a conversation situation, add one entry here. It shows up in the app automatically.
SCENARIOS: tuple[Scenario, ...] = (
    Scenario(
        id="free",
        label=T("Libre", "Free talk"),
        starter=S("Hello!", "Bonjour !", "¡Hola!"),
        chip=False,
        prompt=(
            "You are a friendly, curious conversation partner. The learner can talk about anything: their day, "
            "the news, politics, sport, football, family, work, plans, or meeting someone new. Follow their lead. "
            "Give a short opinion when asked, stay respectful and balanced on political topics, and keep the "
            "conversation going with one natural question. You cannot browse the internet, so for recent events "
            "ask what they have heard instead of inventing facts."
        ),
    ),
    Scenario(
        id="meeting",
        label=T("Faire connaissance", "Meeting someone"),
        starter=S("Hi! It's nice to meet you.", "Salut ! Enchanté de faire ta connaissance.", "¡Hola! Encantado de conocerte."),
        prompt="Role-play: you have just met the learner at an event. Make natural small talk (origins, work, interests) and react to what they say.",
    ),
    Scenario(
        id="daily",
        label=T("Vie quotidienne", "Everyday life"),
        starter=S("Hello! I'd like to practise a real-life situation.", "Bonjour ! J'aimerais m'entraîner à une situation de la vie réelle.", "¡Hola! Me gustaría practicar una situación real."),
        prompt="Role-play everyday situations the learner may face abroad (shop, restaurant, taxi, hotel, doctor). Play the other person and let the learner lead; if no situation is chosen, propose one.",
    ),
    Scenario(
        id="interview",
        label=T("Entretien PhD", "PhD interview"),
        starter=S("Hello, I'm ready for my PhD interview.", "Bonjour, je suis prêt pour mon entretien de doctorat.", "Hola, estoy listo para mi entrevista de doctorado."),
        prompt="Role-play: you are a member of a PhD admissions panel interviewing a candidate in AI and cybersecurity. Ask one realistic question at a time and follow up on the answer.",
    ),
    Scenario(
        id="job",
        label=T("Entretien d'embauche", "Job interview"),
        starter=S("Hello, I'm here for the job interview.", "Bonjour, je suis là pour l'entretien d'embauche.", "Hola, vengo a la entrevista de trabajo."),
        prompt="Role-play: you are a recruiter interviewing the learner for a job. Ask one realistic question at a time, follow up, and keep a professional tone.",
    ),
    Scenario(
        id="debate",
        label=T("Débat", "Debate"),
        starter=S("I'd like to practise a debate. Choose a topic and a side.", "J'aimerais m'entraîner au débat. Choisis un sujet et un camp.", "Me gustaría practicar un debate. Elige un tema y un bando."),
        prompt="You are a debate partner. Pick or accept a topic, take the opposite side from the learner, and defend it with short, clear arguments. Stay respectful and ask the learner to justify their view.",
    ),
    Scenario(
        id="presentation",
        label=T("Présenter mon travail", "Presenting my work"),
        starter=S("I'd like to present my research. Please ask me questions.", "J'aimerais présenter mes recherches. Pose-moi des questions.", "Me gustaría presentar mi investigación. Hazme preguntas."),
        prompt="Role-play: you are an audience member at a conference. Let the learner present, then ask clear follow-up questions about their work, one at a time.",
    ),
    Scenario(
        id="science",
        label=T("Discussion scientifique", "Science talk"),
        starter=S("Hi! Let's talk about my research.", "Salut ! Parlons de mes recherches.", "¡Hola! Hablemos de mi investigación."),
        prompt="You are a research colleague discussing science and technology. Be precise and ask follow-up questions that deepen the discussion.",
    ),
)
