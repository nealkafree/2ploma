import os


def get_texts(path):
    files = os.listdir(path)
    texts = {}
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            t = get_texts(file_path)
            texts.update(t)
        else:
            with open(file_path, encoding='UTF-8') as text_file:
                texts[file] = text_file.read()
    return texts


print(get_texts('Corpus').values())
