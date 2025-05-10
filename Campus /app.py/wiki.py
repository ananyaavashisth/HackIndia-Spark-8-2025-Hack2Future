import wikipedia

def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=3)
        return summary
    except Exception:
        return None