from app.catalog.types import T, Tool, option

# To add a module to the Studio, add one Tool entry here. Placeholders in `instructions`:
# {level_rule}, {help} (the learner's interface language) and one {id} per option.
TOOLS: tuple[Tool, ...] = (
    Tool(
        id="poem",
        icon="feather",
        skill="creative",
        title=T("Poème", "Poem"),
        description=T("Un poème à ton niveau, avec le vocabulaire expliqué.", "A poem at your level, with the vocabulary explained."),
        placeholder=T("Un thème : la mer, la nostalgie, mon pays…", "A theme: the sea, nostalgia, my country..."),
        options=(
            option("style", T("Style", "Style"),
                   ("free verse", T("Vers libres", "Free verse")), ("rhyming", T("Rimé", "Rhyming")),
                   ("haiku", T("Haïku", "Haiku")), ("limerick", T("Limerick", "Limerick")), ("song lyrics", T("Chanson", "Song"))),
        ),
        instructions=(
            "Write an original {style} poem in {lang} about the user's theme. {level_rule} "
            "Then add a short 'Vocabulary' list of 4 to 6 useful words or expressions from the poem with a "
            "translation or explanation in {help}. Finish with one line inviting the learner to write their own verse."
        ),
        temperature=0.9,
        max_words=220,
    ),
    Tool(
        id="story",
        icon="feather",
        skill="creative",
        title=T("Histoire", "Short story"),
        description=T("Une courte histoire à lire, avec glossaire.", "A short story to read, with a glossary."),
        placeholder=T("Un sujet, un personnage, un lieu…", "A subject, a character, a place..."),
        options=(
            option("genre", T("Genre", "Genre"),
                   ("everyday life", T("Quotidien", "Everyday")), ("adventure", T("Aventure", "Adventure")),
                   ("mystery", T("Mystère", "Mystery")), ("funny", T("Humour", "Funny")), ("science fiction", T("Science-fiction", "Sci-fi"))),
        ),
        instructions=(
            "Write a short {genre} story in {lang} about the user's idea. {level_rule} Use short paragraphs. "
            "After the story add a 'Glossary' with 5 useful words and their meaning in {help}, then two questions "
            "in {lang} to check understanding."
        ),
        temperature=0.9,
        max_words=300,
    ),
    Tool(
        id="rewrite",
        icon="pencil",
        skill="writing",
        title=T("Reformuler", "Rewrite"),
        description=T("Change le ton d'un texte : formel, naturel, simple, académique.", "Change the tone of a text: formal, natural, simple, academic."),
        placeholder=T("Colle ton texte", "Paste your text"),
        options=(
            option("tone", T("Ton", "Tone"),
                   ("formal", T("Formel", "Formal")), ("natural and friendly", T("Naturel", "Natural")),
                   ("simpler", T("Plus simple", "Simpler")), ("academic", T("Académique", "Academic")),
                   ("professional", T("Professionnel", "Professional"))),
        ),
        instructions=(
            "Rewrite the user's {lang} text in a {tone} tone, keeping its meaning. Give the rewritten text first. "
            "Then list the 3 most important changes with a one-sentence explanation each, written in {help}."
        ),
        temperature=0.4,
        max_words=300,
    ),
    Tool(
        id="grammar",
        icon="book",
        skill="grammar",
        title=T("Grammaire", "Grammar"),
        description=T("Une règle expliquée simplement, avec exemples et exercices.", "A rule explained simply, with examples and practice."),
        placeholder=T("Un point : present perfect, articles, conditionnel…", "A point: present perfect, articles, conditionals..."),
        instructions=(
            "Explain the grammar point the user names. Write the explanation in {help}, short and clear, for a {help} "
            "speaker learning {lang}. Give 4 example sentences in {lang}, the 2 most common mistakes {help} speakers make, and then "
            "5 fill-in-the-blank practice sentences in {lang}. Put the answers at the very end under 'Answers'."
        ),
        temperature=0.4,
        max_words=350,
    ),
    Tool(
        id="idioms",
        icon="chat",
        skill="vocabulary",
        title=T("Expressions", "Expressions"),
        description=T("Expressions idiomatiques et phrasal verbs sur un thème.", "Idioms and phrasal verbs around a theme."),
        placeholder=T("Un thème : le travail, l'argent, les émotions…", "A theme: work, money, feelings..."),
        options=(
            option("kind", T("Type", "Type"),
                   ("idioms", T("Idiomes", "Idioms")), ("phrasal verbs", T("Phrasal verbs", "Phrasal verbs")),
                   ("everyday expressions", T("Expressions courantes", "Everyday"))),
        ),
        instructions=(
            "Give 6 useful {kind} about the user's theme. {level_rule} For each: the expression in bold, its meaning "
            "in {help}, and one natural example sentence in {lang}."
        ),
        max_words=300,
    ),
    Tool(
        id="email",
        icon="send",
        skill="writing",
        title=T("Emails et lettres", "Emails and letters"),
        description=T("Un email ou une lettre prêts à envoyer, à partir de tes notes.", "A ready-to-send email or letter from your notes."),
        placeholder=T("Explique en quelques mots ce que tu veux dire (même en français)", "Say in a few words what you want to write"),
        options=(
            option("kind", T("Type", "Type"),
                   ("professional email", T("Email pro", "Work email")), ("motivation letter", T("Lettre de motivation", "Motivation letter")),
                   ("scholarship application email", T("Candidature bourse", "Scholarship email")),
                   ("polite follow-up", T("Relance", "Follow-up")), ("message to a friend", T("Message à un ami", "Friend"))),
        ),
        instructions=(
            "Write a {kind} in {lang} from the user's notes. The notes may be in French. {level_rule} Add a subject "
            "line when it is an email. After the text, give 3 useful phrases from it with their meaning in {help}."
        ),
        temperature=0.5,
        max_words=300,
    ),
    Tool(
        id="simplify",
        icon="book",
        skill="reading",
        title=T("Simplifier un texte", "Simplify a text"),
        description=T("Colle un texte difficile : version à ton niveau, mots clés et questions.", "Paste a hard text: a version at your level, key words and questions."),
        placeholder=T("Colle un article ou un paragraphe", "Paste an article or a paragraph"),
        instructions=(
            "Rewrite the user's text at the learner's level, keeping the key ideas. {level_rule} Then add 'Key words' "
            "(5 words with their meaning in {help}) and 3 comprehension questions in {lang}."
        ),
        temperature=0.3,
        max_words=350,
    ),
    Tool(
        id="interview_prep",
        icon="mic",
        skill="speaking",
        title=T("Préparer un entretien", "Interview preparation"),
        description=T("Questions probables, réponses modèles et phrases utiles.", "Likely questions, model answers and useful phrases."),
        placeholder=T("Ton profil, le poste ou la bourse visée…", "Your profile, the job or scholarship..."),
        options=(
            option("kind", T("Type", "Type"),
                   ("PhD scholarship interview", T("Bourse de doctorat", "PhD scholarship")), ("job interview", T("Emploi", "Job")),
                   ("visa interview", T("Visa", "Visa"))),
        ),
        instructions=(
            "Prepare the user for a {kind}. Give 6 likely questions. For each, write a short model answer in {lang} "
            "based on the user's profile, then list 5 useful phrases to reuse with their meaning in {help}. {level_rule}"
        ),
        max_words=450,
    ),
    Tool(
        id="pitch",
        icon="mic",
        skill="speaking",
        title=T("Présenter mon travail", "Pitch my work"),
        description=T("Un discours de 60 secondes sur ton projet, à dire à voix haute.", "A 60-second talk about your project, to say out loud."),
        placeholder=T("Décris ton projet ou ta recherche en quelques phrases", "Describe your project or research"),
        instructions=(
            "Write a spoken 60-second pitch in {lang} from the user's description. {level_rule} Use short sentences "
            "that are easy to say out loud. Then give 3 questions the audience may ask, and 4 linking phrases to sound "
            "natural, with their meaning in {help}."
        ),
        max_words=350,
    ),
)
