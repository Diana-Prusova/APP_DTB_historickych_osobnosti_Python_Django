import json

def load_data_without_key(model, file):
    """
    Funce pro načtení dat do tabulky století. 
    :model: třída modelu (stoleti)
    :file: soubor s daty
    """
    with open(file, mode='r', encoding='utf-8') as f:
        data = json.load(f)

    for each in data:
        model.objects.create(**each)