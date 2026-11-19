from app.catalog.types import T, Tool, option

# To add a module to the Studio, add one Tool entry here. Placeholders in `instructions`:
# {level_rule}, {lang} (the language being learned), {help} (the learner's interface language)
# and one {id} per option. Describe the sections as '## Name': the page renders each one as a block,
# and a section named Answers is hidden behind a button.
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
            "Write an original {style} poem in {lang} about the user's theme, even if the theme is written in {help}. {level_rule} "
            "Sections: '## Poem' (a bold title, then the poem, one verse per line, a blank line between stanzas); "
            "'## Vocabulary' (4 to 6 bullets, each '**word or expression** — meaning in {help}'); "
            "'## Your turn' (one sentence in {help} inviting the learner to write their own verse)."
        ),
        temperature=0.9,
        max_words=250,
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
            "Write a short {genre} story in {lang} about the user's idea, even if the idea is written in {help}. {level_rule} "
            "Sections: '## Story' (a bold title, then 3 short paragraphs separated by blank lines, all in {lang}); "
            "'## Glossary' (5 bullets, each '**word taken from the story** — meaning in {help}'); "
            "'## Questions' (2 numbered comprehension questions in {lang}); "
            "'## Answers' (the 2 answers in {lang}, numbered)."
        ),
        temperature=0.9,
        max_words=350,
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
            "Rewrite the user's {lang} text in a {tone} tone, keeping its meaning. "
            "Sections: '## Rewritten text' (only the new text); "
            "'## Main changes' (3 bullets, each saying what changed and why, in {help})."
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
            "Teach the {lang} grammar point the user names, to a {help} speaker. The point may be written in {help} or {lang}. "
            "Sections: '## Explanation' (3 to 4 short sentences in {help}, with the {lang} forms in bold); "
            "'## Examples' (4 bullets, each '{lang} sentence — {help} translation'); "
            "'## Common mistakes' (2 bullets, each giving the wrong {lang} sentence, the correct one, and why in {help}); "
            "'## Exercises' (5 numbered {lang} sentences, each with one blank ______ and the base word in brackets); "
            "'## Answers' (the 5 completed sentences, numbered)."
        ),
        temperature=0.4,
        max_words=450,
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
            "Give 6 useful {kind} in {lang} about the user's theme. {level_rule} "
            "Sections: '## Expressions' (6 bullets, each '**expression** — meaning in {help}. Example sentence in {lang}'); "
            "'## Practice' (3 numbered {lang} sentences, each with one blank ______ to fill with one of the expressions); "
            "'## Answers' (the 3 completed sentences, numbered)."
        ),
        max_words=400,
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
            "Write a {kind} in {lang} from the user's notes, which may be in {help}. {level_rule} "
            "Sections: '## Message' (a 'Subject:' line when it is an email, then the full text, ready to send); "
            "'## Useful phrases' (3 bullets, each '**phrase from the message** — meaning in {help}')."
        ),
        temperature=0.5,
        max_words=350,
    ),
    Tool(
        id="simplify",
        icon="book",
        skill="reading",
        title=T("Simplifier un texte", "Simplify a text"),
        description=T("Colle un texte difficile : version à ton niveau, mots clés et questions.", "Paste a hard text: a version at your level, key words and questions."),
        placeholder=T("Colle un article ou un paragraphe", "Paste an article or a paragraph"),
        instructions=(
            "Rewrite the user's text in {lang} at the learner's level, keeping the key ideas. {level_rule} "
            "Sections: '## Simplified text'; "
            "'## Key words' (5 bullets, each '**word** — meaning in {help}'); "
            "'## Questions' (3 numbered comprehension questions in {lang}); "
            "'## Answers' (3 short answers in {lang}, numbered)."
        ),
        temperature=0.3,
        max_words=400,
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
            "Prepare the user for a {kind}, using their profile. {level_rule} "
            "Sections: '## Questions and model answers' (6 bullets, each '**likely question in {lang}** short model answer in {lang}'); "
            "'## Useful phrases' (5 bullets, each '**phrase to reuse** — meaning in {help}')."
        ),
        max_words=500,
    ),
    Tool(
        id="pitch",
        icon="mic",
        skill="speaking",
        title=T("Présenter mon travail", "Pitch my work"),
        description=T("Un discours de 60 secondes sur ton projet, à dire à voix haute.", "A 60-second talk about your project, to say out loud."),
        placeholder=T("Décris ton projet ou ta recherche en quelques phrases", "Describe your project or research"),
        instructions=(
            "Write a spoken 60-second pitch in {lang} from the user's description, which may be in {help}. {level_rule} "
            "Use short sentences that are easy to say out loud. "
            "Sections: '## Pitch' (about 140 words); "
            "'## Audience questions' (3 bullets in {lang}); "
            "'## Linking phrases' (4 bullets, each '**phrase** — meaning in {help}')."
        ),
        max_words=400,
    ),
)