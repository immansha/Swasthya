import sys
try:
    import spacy
except Exception as e:
    print('spacy import error:', e)
    sys.exit(1)

try:
    n = spacy.load('en_core_web_sm')
    print('Loaded en_core_web_sm:', n.meta.get('name'))
except Exception as e:
    print('en_core_web_sm load error:', e)

try:
    models = spacy.util.get_installed_models()
    print('Installed spaCy models:', models)
except Exception as e:
    print('get_installed_models error:', e)
