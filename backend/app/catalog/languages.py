from app.catalog.types import T, Language

# To open a new language, add one entry with available=True and add its first lines in
# scenarios.py and topics.py (the app falls back to English when a line is missing).
LANGUAGES: tuple[Language, ...] = (
    Language("en", "English", "English", "en-US", T("Anglais", "English")),
    Language("fr", "French", "Français", "fr-FR", T("Français", "French")),
    Language("es", "Spanish", "Español", "es-ES", T("Espagnol", "Spanish")),
    Language("de", "German", "Deutsch", "de-DE", T("Allemand", "German"), available=False),
    Language("pt", "Portuguese", "Português", "pt-PT", T("Portugais", "Portuguese"), available=False),
    Language("it", "Italian", "Italiano", "it-IT", T("Italien", "Italian"), available=False),
    Language("zh", "Chinese", "中文", "zh-CN", T("Chinois", "Chinese"), available=False),
    Language("ar", "Arabic", "العربية", "ar-SA", T("Arabe", "Arabic"), available=False),
)
