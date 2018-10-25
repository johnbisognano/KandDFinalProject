import numpy as npy
import scipy as sp
from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd
from pandas import Series,DataFrame

def main():
    df = pd.read_csv('19-10-2018_prix_europe.csv', delimiter=',',skipinitialspace=True)

    newCountryName = 'ex:' + df['COUNTRY']
    property = 'dbo:price'
    newValue = df['PRICE INCL VAT']
    #print(newCountryName, newValue)
    #print(newValue)
    print('@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>. \n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.\n@prefix ex: <http://example.com/FinalProject/>. \n@prefix dbo: http://dbpedia.org/ontology>. \n')

    for i in range(0, len(df.index)):
        print(newCountryName.ix[i], property,'"'+str(newValue.ix[i])+'"^^xsd:decimal ;')
if __name__ == '__main__':
    main()
