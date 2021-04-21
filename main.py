import sys
import re

from selenium import webdriver

import sklearn.decomposition
import sklearn.cluster

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import pandas as pd
import numpy as np

import ParserRecord as pr

def color_func(bioms, index):
    if bioms[index] is np.nan:
        return 'r'
    temp = bioms[index].lower()
    if "aquatic" in temp or "marine" in temp or "water" in temp:
        return 'b'
    else:
        return 'g'

def get_data_from_txt():
    f = open("links.txt", 'r', encoding="utf8")
    urls, bioms = [], []
    re_sep = re.compile(r'[\s\t]+')
    for line in f:
        temp = re_sep.split(line)
        urls.append(temp[0])
        bioms.append(temp[1])
    f.close()
    return urls, bioms

def get_data_from_csv():
    f = pd.read_csv("table.csv")
    nrows = len(f)
    urls, bioms = [], []
    for i in range(nrows):
        if f["PULDB URL"][i] is np.nan or f["Habitat"][i] is np.nan:
            continue
        urls.append(f["PULDB URL"][i])
        bioms.append(f["Habitat"][i])
    return urls, bioms

def generate_csv(path, records, bioms, share_vector):
    types = [("name", str), ("habitat", str)]
    types.extend([(value, int) for value in share_vector])
    data = np.empty(0, dtype=types)
    df = pd.DataFrame(data)
    n = len(records)
    for i in range(n):
        temp = [records[i].name, bioms[i]]
        temp.extend(records[i].generate_features_by_existence(share_vector))
        df = df.append(pd.Series(temp,index=df.columns),ignore_index=True)
    df.to_csv(path, encoding="utf8")
    return df


def main():
    args = sys.argv
    # urls, bioms = get_data_from_txt()
    urls, bioms = get_data_from_csv()
    
    print("URLs number:", len(urls))
    if len(urls) == 0:
        print("Empty url list")
        return
    
    browser = webdriver.Firefox()
    records, share_vector, features = [], [], []
    for url in urls:
        temp = pr.ParserRecord()
        temp.load_from_url(browser, url)
        records.append(temp)
        share_vector.extend(temp.unique_genes())
    browser.quit()
    share_vector = list(sorted(set(share_vector)))

    f = open("vecs.txt", "w+", encoding="utf8")
    f.write(str(share_vector)+"\n")
    for record in records:
        # temp = record.generate_features_by_count(share_vector)
        temp = record.generate_features_by_count(share_vector)
        features.append(temp)
        f.write(str(temp)+"\n")
    f.close()

    pca = sklearn.decomposition.PCA(n_components=3)
    pca.fit(features)
    X = pca.transform(features)
    
    fig = plt.figure(1, figsize=(4, 3))
    plt.clf()
    ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
    plt.cla()
    
    for name, label in [(records[i].name, i) for i in range(len(X))]:
        pass
        # ax.text3D(X[label][0], X[label][1], X[label][2] + 0.5, name, horizontalalignment='center', size='x-small',bbox=dict(alpha=.5, edgecolor='w', facecolor='w'))

    ax.scatter(X[:, 0], X[:, 1], X[:, 2], color=list(map(lambda item: color_func(bioms, item), range(len(X)))), cmap=plt.cm.nipy_spectral,
           edgecolor='k')

    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])


    plt.show()
    
    # pca
    
    pca = sklearn.decomposition.PCA(n_components=2)
    pca.fit(features)
    X = pca.transform(features)
    
    fig2 = plt.figure(2, figsize=(16,9))
    plt.clf()
    ax2 = fig2.add_subplot(111)
    plt.cla()
    ax2.scatter(X[:, 0], X[:, 1], color=list(map(lambda item: color_func(bioms, item), range(len(X)))), cmap=plt.cm.nipy_spectral,
           edgecolor='k')
    for i in range(len(X)):
        ax2.annotate(i, (X[:, 0][i],X[:, 1][i]))
    
    ax2.set_yticklabels([])
    ax2.set_xticklabels([])
    
    plt.show()
    
    for i in range(len(records)):
        print(i, records[i].name, X[i], color_func(bioms, i))

    # KMean
    
    kmean = sklearn.cluster.KMeans(n_clusters=3, random_state=0)
    kmean.fit(features)
    X = kmean.transform(features)
    pred = kmean.predict(features)
    
    fig3 = plt.figure(3, figsize=(16,9))
    plt.clf()
    ax3 = fig3.add_subplot(111)
    plt.cla()
    ax3.scatter(X[:, 0], X[:, 1], color=list(map(lambda item: color_func(bioms, item), range(len(X)))), cmap=plt.cm.nipy_spectral,
           edgecolor='k')
    for i in range(len(X)):
        ax3.annotate(i, (X[:, 0][i],X[:, 1][i]))
    
    ax3.set_yticklabels([])
    ax3.set_xticklabels([])
    
    plt.show()
    
    print("Theories output:")
    for i in range(len(records)):
        if pred[i] == pred[17] and i != 17:
            print(i, records[i].name, bioms[i])
    print()
    
if __name__ == "__main__":
    main()