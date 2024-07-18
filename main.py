import streamlit as st
import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import numpy as np

donnees = pd.read_csv("datas/teldakarvente.csv",dtype={'marque': str, 'prix': str})
donnees['prix'].fillna('N/A', inplace=True)

st.markdown("""
<style>
    .st-emotion-cache-10trblm e1nzilvr1{
        text-color:'red'
    }
</style>            
""",unsafe_allow_html=True)

def scrapMouton():
    # scraper sur plusieurs pages
    i=0
    indices = []
    lieux = []
    ind_lieux = []
    df = pd.DataFrame()
    df_vol = pd.DataFrame()
    df_lapin = pd.DataFrame()
    df_rongeur = pd.DataFrame()
    df_chat = pd.DataFrame()
    df_autre = pd.DataFrame()

    for p in range(1,5):
        url =f'https://sn.coinafrique.com/categorie/moutons?page={p}'
        resp = get(url)
        bsoup = bs(resp.text, 'html.parser')
        containers = bsoup.find_all('div', class_ ='col s6 m4 l3')
        data = []
        vol = []
        lapin = []
        rongeur = []
        chat = []
        autre =[]
        separ_Nom = []
        
        for container in containers:
            try:
                Nom = container.find('p', class_ = 'ad__card-description').text
                separ_Nom = Nom.split()

                Prix_CFA = int(container.find('p',class_='ad__card-price').find('a').text.replace('CFA','').replace(' ',''))
                Adresse = container.find_next('p',class_='ad__card-location').find('span').text.replace(',','').split()
                Image_lien = container.find('img',class_='ad__card-img')['src']
                # Nettoyage adresse
                Adresse.remove('Sénégal')
                if len(Adresse) in range(2,6):
                    Adresse.remove('Dakar')

                Adresse = ''.join(Adresse)
                Adresse = Adresse.replace('-','')
                ind = Adresse

                if Adresse not in lieux:
                    indice = len(lieux)
                    indices.append(indice)
                    lieu= ''.join(Adresse)
                    lieux.append(lieu)
                    ind_lieu = str(indice)+ '.'+ ''.join(Adresse)
                    ind_lieux.append(ind_lieu)
                    #ind =indice
                    i+=1
                else:
                    i+=0


                j=0
                for j in range(0,len(indices)):
                    if Adresse == lieux[j]:
                        ind=indices[j]
                        
                k=0
                for k in range(0,len(separ_Nom)):
                    types = separ_Nom[k]
                    if (types.lower() == 'dindons') or(types.lower() == 'canards') or(types.lower() == 'pintade') or(types.lower() == 'pintades') or (types.lower() == 'dindes') or (types.lower() == 'dinde')or(types.lower() == 'cailles')or(types.lower() == 'oies') or types.lower() == 'oie' or types.lower() == 'canard' or types.lower() == 'poussin' or types.lower() == 'poussins' or types.lower() == 'pigeon' or types.lower() == 'pigeons' or types.lower() == 'poulet' or types.lower() == 'poule' or types.lower() == 'coq' or types.lower() == 'poulets' or types.lower() == 'poules' or types.lower() == 'brahma' or types.lower() == 'brahman':
                        types = 'volaille'
                        break
                    elif (types.lower() == 'perroquets') or(types.lower() == 'perruche')or(types.lower() == 'perruches') or (types.lower() == 'perroquet') or (types.lower() == 'oiseaux') or (types.lower() == 'oiseau')or (types.lower() == 'paon') or (types.lower() == 'paons')or (types.lower() == 'paon'):
                        types = 'oiseau'
                        break

                    elif (types.lower() == 'lapin') or (types.lower() == 'lapins') or (types.lower() == 'lapereau') or (types.lower() == 'lapereaux'):
                        types = 'lapin'
                        break
                    elif (types.lower() == 'bœufs')or(types.lower() == 'vache') or (types.lower() == 'boeuf')or (types.lower() == 'boeufs')or (types.lower() == 'taureau') or (types.lower() == 'chèvre') or (types.lower() == 'chevre')or(types.lower() == 'veaux')or(types.lower() == 'vaches') or (types.lower() == 'bœuf') or (types.lower() == 'chèvres') or (types.lower() == 'chevres'):
                        types = 'bovin_caprin'
                        break
                    elif (types.lower() == 'hamster') or (types.lower() == 'hamsters') :
                        types = 'rongeur'
                        break
                    elif (types.lower() == 'chats') or types.lower() == 'chat' or types.lower() == 'chatons' or types.lower() == 'chaton' or types.lower() == 'chatte':
                        types = 'chat'
                        break
                    else: types = 'autre'
                k=0
                  #if len(separ_Nom) in range(2,5):
                    #separ_Nom.remove(separ_Nom[0])
                objet = {
                    'types': types,
                    'Nom': Nom,
                    'Prix_CFA': Prix_CFA,
                    'Adresse': Adresse,
                    'ind_adress': ind,
                    'Image_lien': Image_lien,
                }

                if 1000 < Prix_CFA < 300000:
                    data.append(objet)

                if types == 'volaille':
                    obj_vol = {
                        'types': types,
                        'Nom': Nom,
                        'Prix_CFA': Prix_CFA,
                        'Adresse': Adresse,
                        'ind_adress': ind,
                        'Image_lien': Image_lien,
                    }
                  
                if 1000 < Prix_CFA < 3000000:
                    vol.append(obj_vol)
        
                if types == 'lapin':
                    obj_lapin = {
                        'types': types,
                        'Nom': Nom,
                        'Prix_CFA': Prix_CFA,
                        'Adresse': Adresse,
                        'ind_adress': ind,
                        'Image_lien': Image_lien,
                    }
                  
                if 1000 < Prix_CFA < 2000000:
                  lapin.append(obj_lapin)
        
                if types == 'rongeur':
                    obj_rongeur = {
                        'types': types,
                        'Nom': Nom,
                        'Prix_CFA': Prix_CFA,
                        'Adresse': Adresse,
                        'ind_adress': ind,
                        'Image_lien': Image_lien,
                    }
                  
                if 1000 < Prix_CFA < 2000000:
                    rongeur.append(obj_rongeur)
                    
                if types == 'chat':
                    obj_chat = {
                        'types': types,
                        'Nom': Nom,
                        'Prix_CFA': Prix_CFA,
                        'Adresse': Adresse,
                        'ind_adress': ind,
                        'Image_lien': Image_lien,
                    }
                    
                if 1000 < Prix_CFA < 2000000:
                    chat.append(obj_chat)
                    
                if types == 'autre':
                    obj_autre = {
                        'types': types,
                        'Nom': Nom,
                        'Prix_CFA': Prix_CFA,
                        'Adresse': Adresse,
                        'ind_adress': ind,
                        'Image_lien': Image_lien,
                    }
                if 1000 < Prix_CFA < 2000000:
                    autre.append(obj_autre)
            except: pass

        DF_vol = pd.DataFrame(vol)
        DF_rongeur = pd.DataFrame(rongeur)
        DF_chat = pd.DataFrame(chat)
        DF_autre = pd.DataFrame(autre)
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF],axis = 0).reset_index(drop = True)
        df_vol = pd.concat([df_vol, DF_vol],axis = 0).reset_index(drop = True)
        df_rongeur = pd.concat([df_rongeur, DF_rongeur],axis = 0).reset_index(drop = True)
        df_chat = pd.concat([df_chat, DF_chat],axis = 0).reset_index(drop = True)
        df_autre = pd.concat([df_autre, DF_autre],axis = 0).reset_index(drop = True)
    return df

def scrapAutres():
    # scraper sur plusieurs pages
    i=0
    indices = []
    lieux = []
    ind_lieux = []
    df = pd.DataFrame()
    df_vol = pd.DataFrame()
    df_lapin = pd.DataFrame()
    df_rongeur = pd.DataFrame()
    df_chat = pd.DataFrame()
    df_autre = pd.DataFrame()

    for p in range(1,5):
        url =f'https://sn.coinafrique.com/categorie/autres-animaux?page={p}'
        resp = get(url)
        bsoup = bs(resp.text, 'html.parser')
        containers = bsoup.find_all('div', class_ ='col s6 m4 l3')
        data = []
        vol = []
        lapin = []
        rongeur = []
        chat = []
        autre =[]
        separ_Nom = []
        
        for container in containers:
            try:
                Nom = container.find('p', class_ = 'ad__card-description').text
                separ_Nom = Nom.split()

                Prix_CFA = int(container.find('p',class_='ad__card-price').find('a').text.replace('CFA','').replace(' ',''))
                Adresse = container.find_next('p',class_='ad__card-location').find('span').text.replace(',','').split()
                Image_lien = container.find('img',class_='ad__card-img')['src']
                # Nettoyage adresse
                Adresse.remove('Sénégal')
                if len(Adresse) in range(2,6):
                    Adresse.remove('Dakar')

                Adresse = ''.join(Adresse)
                Adresse = Adresse.replace('-','')
                ind = Adresse

                if Adresse not in lieux:
                    indice = len(lieux)
                    indices.append(indice)
                    lieu= ''.join(Adresse)
                    lieux.append(lieu)
                    ind_lieu = str(indice)+ '.'+ ''.join(Adresse)
                    ind_lieux.append(ind_lieu)
                    #ind =indice
                    i+=1
                else:
                    i+=0


                j=0
                for j in range(0,len(indices)):
                    if Adresse == lieux[j]:
                        ind=indices[j]
                        
                k=0
                for k in range(0,len(separ_Nom)):
                    types = separ_Nom[k]
                    if (types.lower() == 'dindons') or(types.lower() == 'canards') or(types.lower() == 'pintade') or(types.lower() == 'pintades') or (types.lower() == 'dindes') or (types.lower() == 'dinde')or(types.lower() == 'cailles')or(types.lower() == 'oies') or types.lower() == 'oie' or types.lower() == 'canard' or types.lower() == 'poussin' or types.lower() == 'poussins' or types.lower() == 'pigeon' or types.lower() == 'pigeons' or types.lower() == 'poulet' or types.lower() == 'poule' or types.lower() == 'coq' or types.lower() == 'poulets' or types.lower() == 'poules' or types.lower() == 'brahma' or types.lower() == 'brahman':
                        types = 'volaille'
                        break
                    elif (types.lower() == 'perroquets') or(types.lower() == 'perruche')or(types.lower() == 'perruches') or (types.lower() == 'perroquet') or (types.lower() == 'oiseaux') or (types.lower() == 'oiseau')or (types.lower() == 'paon') or (types.lower() == 'paons')or (types.lower() == 'paon'):
                        types = 'oiseau'
                        break

                    elif (types.lower() == 'lapin') or (types.lower() == 'lapins') or (types.lower() == 'lapereau') or (types.lower() == 'lapereaux'):
                        types = 'lapin'
                        break
                    elif (types.lower() == 'bœufs')or(types.lower() == 'vache') or (types.lower() == 'boeuf')or (types.lower() == 'boeufs')or (types.lower() == 'taureau') or (types.lower() == 'chèvre') or (types.lower() == 'chevre')or(types.lower() == 'veaux')or(types.lower() == 'vaches') or (types.lower() == 'bœuf') or (types.lower() == 'chèvres') or (types.lower() == 'chevres'):
                        types = 'bovin_caprin'
                        break
                    elif (types.lower() == 'hamster') or (types.lower() == 'hamsters') :
                        types = 'rongeur'
                        break
                    elif (types.lower() == 'chats') or types.lower() == 'chat' or types.lower() == 'chatons' or types.lower() == 'chaton' or types.lower() == 'chatte':
                        types = 'chat'
                        break
                    else: types = 'autre'
                k=0
                  #if len(separ_Nom) in range(2,5):
                    #separ_Nom.remove(separ_Nom[0])
                objet = {
                    'types': types,
                    'Nom': Nom,
                    'Prix_CFA': Prix_CFA,
                    'Adresse': Adresse,
                    'ind_adress': ind,
                    'Image_lien': Image_lien,
                }

                if 1000 < Prix_CFA < 300000:
                    data.append(objet)

                if types == 'volaille':
                    obj_vol = {
                        'types': types,
                        'Nom': Nom,
                        'Prix_CFA': Prix_CFA,
                        'Adresse': Adresse,
                        'ind_adress': ind,
                        'Image_lien': Image_lien,
                    }
                  
                if 1000 < Prix_CFA < 3000000:
                    vol.append(obj_vol)
        
                if types == 'lapin':
                    obj_lapin = {
                        'types': types,
                        'Nom': Nom,
                        'Prix_CFA': Prix_CFA,
                        'Adresse': Adresse,
                        'ind_adress': ind,
                        'Image_lien': Image_lien,
                    }
                  
                if 1000 < Prix_CFA < 2000000:
                  lapin.append(obj_lapin)
        
                if types == 'rongeur':
                    obj_rongeur = {
                        'types': types,
                        'Nom': Nom,
                        'Prix_CFA': Prix_CFA,
                        'Adresse': Adresse,
                        'ind_adress': ind,
                        'Image_lien': Image_lien,
                    }
                  
                if 1000 < Prix_CFA < 2000000:
                    rongeur.append(obj_rongeur)
                    
                if types == 'chat':
                    obj_chat = {
                        'types': types,
                        'Nom': Nom,
                        'Prix_CFA': Prix_CFA,
                        'Adresse': Adresse,
                        'ind_adress': ind,
                        'Image_lien': Image_lien,
                    }
                    
                if 1000 < Prix_CFA < 2000000:
                    chat.append(obj_chat)
                    
                if types == 'autre':
                    obj_autre = {
                        'types': types,
                        'Nom': Nom,
                        'Prix_CFA': Prix_CFA,
                        'Adresse': Adresse,
                        'ind_adress': ind,
                        'Image_lien': Image_lien,
                    }
                if 1000 < Prix_CFA < 2000000:
                    autre.append(obj_autre)
            except: pass

        DF_vol = pd.DataFrame(vol)
        DF_rongeur = pd.DataFrame(rongeur)
        DF_chat = pd.DataFrame(chat)
        DF_autre = pd.DataFrame(autre)
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF],axis = 0).reset_index(drop = True)
        df_vol = pd.concat([df_vol, DF_vol],axis = 0).reset_index(drop = True)
        df_rongeur = pd.concat([df_rongeur, DF_rongeur],axis = 0).reset_index(drop = True)
        df_chat = pd.concat([df_chat, DF_chat],axis = 0).reset_index(drop = True)
        df_autre = pd.concat([df_autre, DF_autre],axis = 0).reset_index(drop = True)
    return df

def scrapPLP():
    # scraper sur plusieurs pages
    i=0
    indices = []
    lieux = []
    ind_lieux = []
    df = pd.DataFrame()
    df_vol = pd.DataFrame()
    df_lapin = pd.DataFrame()
    df_rongeur = pd.DataFrame()
    df_chat = pd.DataFrame()
    df_autre = pd.DataFrame()

    for p in range(1,5):
        url =f'https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons?page={p}'
        #url =f'https://sn.coinafrique.com/categorie/autres-animaux?page={p}'
        resp = get(url)
        bsoup = bs(resp.text, 'html.parser')
        containers = bsoup.find_all('div', class_ ='col s6 m4 l3')
        data = []
        vol = []
        lapin = []
        rongeur = []
        chat = []
        autre =[]
        separ_Nom = []
        
        for container in containers:
            try:
                Nom = container.find('p', class_ = 'ad__card-description').text
                separ_Nom = Nom.split()

                Prix_CFA = int(container.find('p',class_='ad__card-price').find('a').text.replace('CFA','').replace(' ',''))
                Adresse = container.find_next('p',class_='ad__card-location').find('span').text.replace(',','').split()
                Image_lien = container.find('img',class_='ad__card-img')['src']
                # Nettoyage adresse
                Adresse.remove('Sénégal')
                if len(Adresse) in range(2,6):
                    Adresse.remove('Dakar')

                Adresse = ''.join(Adresse)
                Adresse = Adresse.replace('-','')
                ind = Adresse

                if Adresse not in lieux:
                    indice = len(lieux)
                    indices.append(indice)
                    lieu= ''.join(Adresse)
                    lieux.append(lieu)
                    ind_lieu = str(indice)+ '.'+ ''.join(Adresse)
                    ind_lieux.append(ind_lieu)
                    #ind =indice
                    i+=1
                else:
                    i+=0


                j=0
                for j in range(0,len(indices)):
                    if Adresse == lieux[j]:
                        ind=indices[j]
                        
                k=0
                for k in range(0,len(separ_Nom)):
                    types = separ_Nom[k]
                    if (types.lower() == 'dindons') or(types.lower() == 'canards') or(types.lower() == 'pintade') or(types.lower() == 'pintades') or (types.lower() == 'dindes') or (types.lower() == 'dinde')or(types.lower() == 'cailles')or(types.lower() == 'oies') or types.lower() == 'oie' or types.lower() == 'canard' or types.lower() == 'poussin' or types.lower() == 'poussins' or types.lower() == 'pigeon' or types.lower() == 'pigeons' or types.lower() == 'poulet' or types.lower() == 'poule' or types.lower() == 'coq' or types.lower() == 'poulets' or types.lower() == 'poules' or types.lower() == 'brahma' or types.lower() == 'brahman':
                        types = 'volaille'
                        break
                    elif (types.lower() == 'perroquets') or(types.lower() == 'perruche')or(types.lower() == 'perruches') or (types.lower() == 'perroquet') or (types.lower() == 'oiseaux') or (types.lower() == 'oiseau')or (types.lower() == 'paon') or (types.lower() == 'paons')or (types.lower() == 'paon'):
                        types = 'oiseau'
                        break

                    elif (types.lower() == 'lapin') or (types.lower() == 'lapins') or (types.lower() == 'lapereau') or (types.lower() == 'lapereaux'):
                        types = 'lapin'
                        break
                    elif (types.lower() == 'bœufs')or(types.lower() == 'vache') or (types.lower() == 'boeuf')or (types.lower() == 'boeufs')or (types.lower() == 'taureau') or (types.lower() == 'chèvre') or (types.lower() == 'chevre')or(types.lower() == 'veaux')or(types.lower() == 'vaches') or (types.lower() == 'bœuf') or (types.lower() == 'chèvres') or (types.lower() == 'chevres'):
                        types = 'bovin_caprin'
                        break
                    elif (types.lower() == 'hamster') or (types.lower() == 'hamsters') :
                        types = 'rongeur'
                        break
                    elif (types.lower() == 'chats') or types.lower() == 'chat' or types.lower() == 'chatons' or types.lower() == 'chaton' or types.lower() == 'chatte':
                        types = 'chat'
                        break
                    else: types = 'autre'
                k=0
                  #if len(separ_Nom) in range(2,5):
                    #separ_Nom.remove(separ_Nom[0])
                objet = {
                    'types': types,
                    'Nom': Nom,
                    'Prix_CFA': Prix_CFA,
                    'Adresse': Adresse,
                    'ind_adress': ind,
                    'Image_lien': Image_lien,
                }

                if 1000 < Prix_CFA < 300000:
                    data.append(objet)

                if types == 'volaille':
                    obj_vol = {
                        'types': types,
                        'Nom': Nom,
                        'Prix_CFA': Prix_CFA,
                        'Adresse': Adresse,
                        'ind_adress': ind,
                        'Image_lien': Image_lien,
                    }
                  
                if 1000 < Prix_CFA < 3000000:
                    vol.append(obj_vol)
        
                if types == 'lapin':
                    obj_lapin = {
                        'types': types,
                        'Nom': Nom,
                        'Prix_CFA': Prix_CFA,
                        'Adresse': Adresse,
                        'ind_adress': ind,
                        'Image_lien': Image_lien,
                    }
                  
                if 1000 < Prix_CFA < 2000000:
                  lapin.append(obj_lapin)
        
                if types == 'rongeur':
                    obj_rongeur = {
                        'types': types,
                        'Nom': Nom,
                        'Prix_CFA': Prix_CFA,
                        'Adresse': Adresse,
                        'ind_adress': ind,
                        'Image_lien': Image_lien,
                    }
                  
                if 1000 < Prix_CFA < 2000000:
                    rongeur.append(obj_rongeur)
                    
                if types == 'chat':
                    obj_chat = {
                        'types': types,
                        'Nom': Nom,
                        'Prix_CFA': Prix_CFA,
                        'Adresse': Adresse,
                        'ind_adress': ind,
                        'Image_lien': Image_lien,
                    }
                    
                if 1000 < Prix_CFA < 2000000:
                    chat.append(obj_chat)
                    
                if types == 'autre':
                    obj_autre = {
                        'types': types,
                        'Nom': Nom,
                        'Prix_CFA': Prix_CFA,
                        'Adresse': Adresse,
                        'ind_adress': ind,
                        'Image_lien': Image_lien,
                    }
                if 1000 < Prix_CFA < 2000000:
                    autre.append(obj_autre)
            except: pass

        DF_vol = pd.DataFrame(vol)
        DF_rongeur = pd.DataFrame(rongeur)
        DF_chat = pd.DataFrame(chat)
        DF_autre = pd.DataFrame(autre)
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF],axis = 0).reset_index(drop = True)
        df_vol = pd.concat([df_vol, DF_vol],axis = 0).reset_index(drop = True)
        df_rongeur = pd.concat([df_rongeur, DF_rongeur],axis = 0).reset_index(drop = True)
        df_chat = pd.concat([df_chat, DF_chat],axis = 0).reset_index(drop = True)
        df_autre = pd.concat([df_autre, DF_autre],axis = 0).reset_index(drop = True)
    return df

def scrapChien():
    # scraper sur plusieurs pages
    i=0
    indices = []
    lieux = []
    ind_lieux = []
    df = pd.DataFrame()
    df_vol = pd.DataFrame()
    df_lapin = pd.DataFrame()
    df_rongeur = pd.DataFrame()
    df_chat = pd.DataFrame()
    df_autre = pd.DataFrame()

    for p in range(1,5):
        url =f'https://sn.coinafrique.com/categorie/chiens?page={p}'
        resp = get(url)
        bsoup = bs(resp.text, 'html.parser')
        containers = bsoup.find_all('div', class_ ='col s6 m4 l3')
        data = []
        vol = []
        lapin = []
        rongeur = []
        chat = []
        autre =[]
        separ_Nom = []
        
        for container in containers:
            try:
                Nom = container.find('p', class_ = 'ad__card-description').text
                separ_Nom = Nom.split()

                Prix_CFA = int(container.find('p',class_='ad__card-price').find('a').text.replace('CFA','').replace(' ',''))
                Adresse = container.find_next('p',class_='ad__card-location').find('span').text.replace(',','').split()
                Image_lien = container.find('img',class_='ad__card-img')['src']
                # Nettoyage adresse
                Adresse.remove('Sénégal')
                if len(Adresse) in range(2,6):
                    Adresse.remove('Dakar')

                Adresse = ''.join(Adresse)
                Adresse = Adresse.replace('-','')
                ind = Adresse

                if Adresse not in lieux:
                    indice = len(lieux)
                    indices.append(indice)
                    lieu= ''.join(Adresse)
                    lieux.append(lieu)
                    ind_lieu = str(indice)+ '.'+ ''.join(Adresse)
                    ind_lieux.append(ind_lieu)
                    #ind =indice
                    i+=1
                else:
                    i+=0


                j=0
                for j in range(0,len(indices)):
                    if Adresse == lieux[j]:
                        ind=indices[j]
                        
                k=0
                for k in range(0,len(separ_Nom)):
                    types = separ_Nom[k]
                    if (types.lower() == 'dindons') or(types.lower() == 'canards') or(types.lower() == 'pintade') or(types.lower() == 'pintades') or (types.lower() == 'dindes') or (types.lower() == 'dinde')or(types.lower() == 'cailles')or(types.lower() == 'oies') or types.lower() == 'oie' or types.lower() == 'canard' or types.lower() == 'poussin' or types.lower() == 'poussins' or types.lower() == 'pigeon' or types.lower() == 'pigeons' or types.lower() == 'poulet' or types.lower() == 'poule' or types.lower() == 'coq' or types.lower() == 'poulets' or types.lower() == 'poules' or types.lower() == 'brahma' or types.lower() == 'brahman':
                        types = 'volaille'
                        break
                    elif (types.lower() == 'perroquets') or(types.lower() == 'perruche')or(types.lower() == 'perruches') or (types.lower() == 'perroquet') or (types.lower() == 'oiseaux') or (types.lower() == 'oiseau')or (types.lower() == 'paon') or (types.lower() == 'paons')or (types.lower() == 'paon'):
                        types = 'oiseau'
                        break

                    elif (types.lower() == 'lapin') or (types.lower() == 'lapins') or (types.lower() == 'lapereau') or (types.lower() == 'lapereaux'):
                        types = 'lapin'
                        break
                    elif (types.lower() == 'bœufs')or(types.lower() == 'vache') or (types.lower() == 'boeuf')or (types.lower() == 'boeufs')or (types.lower() == 'taureau') or (types.lower() == 'chèvre') or (types.lower() == 'chevre')or(types.lower() == 'veaux')or(types.lower() == 'vaches') or (types.lower() == 'bœuf') or (types.lower() == 'chèvres') or (types.lower() == 'chevres'):
                        types = 'bovin_caprin'
                        break
                    elif (types.lower() == 'hamster') or (types.lower() == 'hamsters') :
                        types = 'rongeur'
                        break
                    elif (types.lower() == 'chats') or types.lower() == 'chat' or types.lower() == 'chatons' or types.lower() == 'chaton' or types.lower() == 'chatte':
                        types = 'chat'
                        break
                    else: types = 'autre'
                k=0
                  #if len(separ_Nom) in range(2,5):
                    #separ_Nom.remove(separ_Nom[0])
                objet = {
                    'types': types,
                    'Nom': Nom,
                    'Prix_CFA': Prix_CFA,
                    'Adresse': Adresse,
                    'ind_adress': ind,
                    'Image_lien': Image_lien,
                }

                if 1000 < Prix_CFA < 300000:
                    data.append(objet)

                if types == 'volaille':
                    obj_vol = {
                        'types': types,
                        'Nom': Nom,
                        'Prix_CFA': Prix_CFA,
                        'Adresse': Adresse,
                        'ind_adress': ind,
                        'Image_lien': Image_lien,
                    }
                  
                if 1000 < Prix_CFA < 3000000:
                    vol.append(obj_vol)
        
                if types == 'lapin':
                    obj_lapin = {
                        'types': types,
                        'Nom': Nom,
                        'Prix_CFA': Prix_CFA,
                        'Adresse': Adresse,
                        'ind_adress': ind,
                        'Image_lien': Image_lien,
                    }
                  
                if 1000 < Prix_CFA < 2000000:
                  lapin.append(obj_lapin)
        
                if types == 'rongeur':
                    obj_rongeur = {
                        'types': types,
                        'Nom': Nom,
                        'Prix_CFA': Prix_CFA,
                        'Adresse': Adresse,
                        'ind_adress': ind,
                        'Image_lien': Image_lien,
                    }
                  
                if 1000 < Prix_CFA < 2000000:
                    rongeur.append(obj_rongeur)
                    
                if types == 'chat':
                    obj_chat = {
                        'types': types,
                        'Nom': Nom,
                        'Prix_CFA': Prix_CFA,
                        'Adresse': Adresse,
                        'ind_adress': ind,
                        'Image_lien': Image_lien,
                    }
                    
                if 1000 < Prix_CFA < 2000000:
                    chat.append(obj_chat)
                    
                if types == 'autre':
                    obj_autre = {
                        'types': types,
                        'Nom': Nom,
                        'Prix_CFA': Prix_CFA,
                        'Adresse': Adresse,
                        'ind_adress': ind,
                        'Image_lien': Image_lien,
                    }
                if 1000 < Prix_CFA < 2000000:
                    autre.append(obj_autre)
            except: pass

        DF_vol = pd.DataFrame(vol)
        DF_rongeur = pd.DataFrame(rongeur)
        DF_chat = pd.DataFrame(chat)
        DF_autre = pd.DataFrame(autre)
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF],axis = 0).reset_index(drop = True)
        df_vol = pd.concat([df_vol, DF_vol],axis = 0).reset_index(drop = True)
        df_rongeur = pd.concat([df_rongeur, DF_rongeur],axis = 0).reset_index(drop = True)
        df_chat = pd.concat([df_chat, DF_chat],axis = 0).reset_index(drop = True)
        df_autre = pd.concat([df_autre, DF_autre],axis = 0).reset_index(drop = True)
    return df


st.sidebar.subheader("Filtrer le scraping")
nb_page = st.sidebar.slider("Choisissez le nombre de page a scraper" , min_value=1,max_value=111)
print(nb_page)
st.sidebar.markdown("---")
res = st.sidebar.selectbox("Naviguez sur l'application",options=("Scrapper les données avec BS","Dashboard","Scrapper les données avec web Scraper","Formulaire de contact"))

if res == "Scrapper les données avec BS":
    st.title("Dashboard de scrapping")
    st.markdown("Ces données sont scrapées sur le site coin Afrique")
    st.text("Ci-dessous se trouve les données disponibles pour le scraping")
    st.markdown("---")
    # st.table(table)
    st.header("Moutons")
    
    st.image("images/mouton.jpg")
    click = st.button("Scrapper mouton")

    if click:
        sc = scrapMouton()
        st.dataframe(sc)

    st.header("Poule lapins pigeons")
    st.image("images/poule.jpg")
    click = st.button("Scrapper PLP")

    if click:
        sc = scrapPLP()
        st.dataframe(sc)

    st.header("Chien")
    st.image("images/chien.jpeg")
    click = st.button("Scrapper chien")

    if click:
        sc = scrapChien()
        st.dataframe(sc)
    
    st.header("Autres animaux")
    st.image("images/autres.jpg")
    click = st.button("Scrapper autres")

    if click:
        sc = scrapAutres()
        st.dataframe(sc)


elif res == "Formulaire de contact":
    st.markdown("""<iframe src="https://ee.kobotoolbox.org/i/cXvfevZE" width="800" height="600"></iframe>""",unsafe_allow_html=True)
elif res == "Dashboard":

    x = np.linspace(0, 2 * np.pi, 100)
    y = np.sin(x)

    st.title("Graphique Matplotlib avec Streamlit")

    graph_type = st.selectbox("Choisissez le type de graphique", ["ligne", "Nuage de points","barre","histogramme"])
        
    fig, ax = plt.subplots()

    if graph_type == "Nuage de points":
        plt.scatter(donnees['marque'], donnees['prix'])
        plt.xlabel("Nom de l'axe X")
        plt.ylabel("Nom de l'axe Y")
        plt.title('Nuage de points')
        plt.show()
    elif graph_type == "barre":
        plt.bar(donnees['marque'], donnees['prix'])
        plt.xlabel("Nom de l'axe X")
        plt.ylabel("Nom de l'axe Y")
        plt.title('Titre du graphique')
        plt.show()
    elif graph_type == "ligne":
        plt.plot(donnees['marque'], donnees['prix'], marker='o')
        plt.xlabel("Nom de l'axe X")
        plt.ylabel("Nom de l'axe Y")
        plt.title('Diagramme en lignes')
        plt.show()
    elif graph_type == "histogramme":
        plt.hist(donnees['prix'], bins=10, edgecolor='black')
        plt.xlabel("Nom de l'axe X")
        plt.ylabel("Nom de l'axe Y")
        plt.title('Histogramme')
        plt.show()

    st.pyplot(fig)
elif res == "Scrapper les données avec web Scraper":
    st.title("Scraping avec Web Scrapper")
    st.markdown("Ces données sont scrapées sur le site [dakarvente](https://www.dakarvente.com)")
    st.text("Ci-dessous se trouve les données disponible pour le scraping")
    st.markdown("---")
    # st.table(table)
    st.header("Moutons")
    
    st.image("images/mouton.jpg")
    click = st.button("Scrapper Moutons")

    if click:
        df = pd.read_csv("datas/moutons.csv")
        st.dataframe(df)

    st.header("Poules Lapin Pigeon")
    st.image("images/poule.jpg")
    click = st.button("Scrapper PLP")

    if click:
        df = pd.read_csv("datas/plp.csv")
        st.dataframe(df)

    st.header("Chien")
    st.image("images/chien.jpeg")
    click = st.button("Scrapper chien")

    if click:
        df = pd.read_csv("datas/chien.csv")
        st.dataframe(df)

    st.header("Autres")
    st.image("images/autres.jpg")
    click = st.button("Scrapper autres")

    if click:
        df = pd.read_csv("datas/autres.csv")
        st.dataframe(df)

