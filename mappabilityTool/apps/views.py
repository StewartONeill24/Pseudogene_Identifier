from django.shortcuts import render,redirect
from script.pyscript import get_Accessions,get_NM_Accessions_Only,create_BEDs,bedGraphFile,intersect,create_PNG
import os, glob
from mysite.settings import BASE_DIR
import urllib.request
import bs4
import shutil

def index(request):
    template = 'index.html'
    context = {}
    return render(request,template,context)

def result(request):
    template = 'result.html'
    context = {}
    try:
        gene = request.GET['gene']
        context['gene'] = gene
    except:
        return redirect('index')
    prevfolders = []
    for i,j,k in os.walk(BASE_DIR):
        for l in j:
            prevfolders.append(l)
        break
    deffolders = ['apps','mysite','script','static','templates']
    for i in prevfolders:
        if i not in deffolders:
            shutil.rmtree(BASE_DIR+'/'+i)
    list_of_papers = {}
    r = urllib.request.urlopen('https://www.ncbi.nlm.nih.gov/pubmed/?term='+gene)
    sp = bs4.BeautifulSoup(r,'lxml')
    count = 0
    for i in sp.find_all('p'):
        if i.get('class') == ['title']:
            href = 'https://www.ncbi.nlm.nih.gov'
            a = str(i).split('href="')[1]
            for j in a:
                if j == '"':
                    break
                else:
                    href = href + str(j)
            list_of_papers[i.text] = href
            href = 'https://www.ncbi.nlm.nih.gov'
            count = count + 1
            if count >= 10:
                break
    context['list_of_papers'] = list_of_papers
    acc_dict = get_Accessions(gene)
    acc_trimmed = get_NM_Accessions_Only(acc_dict)
    create_BEDs(acc_trimmed)
    for file in glob.glob("*.bed"):
        if os.stat(os.path.abspath(file)).st_size == 0:
            os.remove(os.path.abspath(file))
        else:
            intersect(file,bedGraphFile)
    for file in glob.glob("*.bed.intersect"):
        create_PNG(file, acc_trimmed)
    datas = []
    count = 1
    latest_folders = []
    for i,j,k in os.walk(BASE_DIR):
        for l in j:
            latest_folders.append(l)
        break
    for i in latest_folders:
        if i not in deffolders:
            for j,k,l in os.walk(BASE_DIR+'/'+i):
                for m in l:
                    a = {'image_url':'/static/'+i+'/'+m,
                        'image_name':m.split('.')[0],
                        'image_num':count}
                    count = count + 1
                    if count > 2:
                        a['image_show'] = 'none;'
                    else:
                        a['image_show'] = 'block;'
                    datas.append(a)
    context['images'] = datas
    return render(request,template,context)
