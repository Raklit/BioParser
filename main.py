import sys
import re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import sklearn.decomposition

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import pandas as pd

import numpy as np

import ParserRecord as pr

def color_func_txt(bioms, index):
    if bioms[index].startswith("water"):
        return 'b'
    else:
        return 'g'


def color_func_csv(bioms, index):
    temp = bioms[index].lower()
    if "aquatic" in temp or "Marine" in temp or "water" in temp:
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
        if f["PULDB URL"][i] is np.nan or f["Habitat"][i] is np.nan: continue
        urls.append(f["PULDB URL"][i])
        bioms.append(f["Habitat"][i])
    return urls, bioms
    

def main():
    args = sys.argv
    browser = webdriver.Firefox()
    # urls, bioms = get_data_from_txt()
    # color_func = color_func_txt
    urls, bioms = get_data_from_csv()
    color_func = color_func_csv
    if len(urls) == 0:
        print("Empty url list")
        return
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
        temp = record.generate_features(share_vector)
        features.append(temp)
        f.write(str(temp)+"\n")
    f.close()

    pca = sklearn.decomposition.PCA(n_components=3)
    pca.fit(features)
    X = pca.transform(features)

    for i in range(len(records)):
        print(records[i].name, X[i], color_func(bioms, i))
    
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
    
    pca = sklearn.decomposition.PCA(n_components=2)
    pca.fit(features)
    X = pca.transform(features)
    
    fig2 = plt.figure(2, figsize=(4,3))
    plt.clf()
    ax2 = fig2.add_subplot(111)
    plt.cla()
    ax2.scatter(X[:, 0], X[:, 1], color=list(map(lambda item: color_func(bioms, item), range(len(X)))), cmap=plt.cm.nipy_spectral,
           edgecolor='k')
    
    ax2.set_yticklabels([])
    ax2.set_xticklabels([])
    
    plt.show()

if __name__ == "__main__":
    main()