import os
from bs4 import BeautifulSoup, Comment

def html2txt(file):
    path = os.path.join('final_html', file)
    filename = file.split('.')[0]
    txt_path = os.path.join('final_txt',filename + '.txt')
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text()
        url = soup.find(string=lambda text: isinstance(text, Comment))
    
    with open(txt_path, 'w', encoding='utf-8') as file:
        file.write(url)
        file.write(text)
    
def h2t_batch(batch: list):
    for file in batch:
        html2txt(file)


batch_size = 250
count = 0
batch = []
batch_num = 33
for file in os.listdir('final_html'):
    batch.append(file)
    if len(batch) == batch_size:
        count += 1
        h2t_batch(batch)
        batch = []
        print(f'Batch ({count}/33) has been transformed.')



