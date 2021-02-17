import sys
import re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

import sklearn.decomposition

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

import ParserRecord as pr

def main():
    args = sys.argv
    browser = webdriver.Firefox()
    f = open("links.txt", 'r', encoding="utf8")
    urls = []
    for line in f:
        urls.append(line)
    f.close()
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
    
    fig = plt.figure(1, figsize=(4, 3))
    plt.clf()
    ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
    plt.cla()
    
    for name, label in [(records[i].name, i) for i in range(len(X))]:
        pass
        # ax.text3D(X[label][0], X[label][1], X[label][2],
        #     name,
        #       horizontalalignment='center',
        #       bbox=dict(alpha=.5, edgecolor='w', facecolor='w'))

    ax.scatter(X[:, 0], X[:, 1], X[:, 2], cmap=plt.cm.nipy_spectral,
           edgecolor='k')

    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])


    plt.show()

if __name__ == "__main__":
    main()