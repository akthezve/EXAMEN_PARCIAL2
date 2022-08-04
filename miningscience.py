from Bio import Entrez 
import re
import csv

def download_pubmed(keyword): 
    """Docstring descarga la base de datos de pubmed a un archivo.
    """
    # Always tell NCBI who you are (edit the e-mail below!)
    Entrez.email = "gualapuro.moises@gmail.com"
    handle = Entrez.esearch(db="pubmed", 
                            term=keyword,
                            usehistory="y")
    record = Entrez.read(handle)
    # generate a Python list with all Pubmed IDs of articles about Dengue Network
    id_list = record["IdList"]
    record["Count"]
    webenv = record["WebEnv"]
    query_key = record["QueryKey"]
    handle = Entrez.efetch(db="pubmed",
                            rettype="medline", 
                            retmode="text", 
                            retstart=0,
    retmax=543, webenv=webenv, query_key=query_key)
    out_handle = open("pubmed_results.txt", "w")
    data = handle.read()
    handle.close()
    out_handle.write(data)
    out_handle.close()
    return(id_list)

def map_science(tipo):
    """Docstring crea un gráfico de acuerdo a las cinco ciudades elegida de la base de datos anteriormente creada
    """
    #if tipo == "AD":
    with open(tipo) as f:
        my_text = f.read()
    my_text = re.sub(r'\n\s{6}', ' ', my_text)  
    zipcodes = re.findall(r'[A-Z]{2}\s(\d{5}), USA', my_text)
    unique_zipcodes = list(set(zipcodes))
    unique_zipcodes.sort()
    unique_zipcodes[:10]
    zip_coordinates = {}
    with open('data/zipcodes_coordinates.txt') as f:
        csvr = csv.DictReader(f)
        for row in csvr:
            zip_coordinates[row['ZIP']] = [float(row['LAT']), 
                                        float(row['LNG'])]
    zip_code = []
    zip_long = []
    zip_lat = []
    zip_count = []
    for z in unique_zipcodes:
    # if we can find the coordinates
        if z in zip_coordinates.keys():
            zip_code.append(z)
            zip_lat.append(zip_coordinates[z][0])
            zip_long.append(zip_coordinates[z][1])
            zip_count.append(zipcodes.count(z))
    import matplotlib.pyplot as plt
    #%matplotlib inline
    fig = plt.figure()
    plt.scatter(zip_long, zip_lat, s = zip_count, c= zip_count)
    plt.colorbar()
    # only continental us without Alaska
    plt.xlim(-125,-65)
    plt.ylim(23, 50)
    # add a few cities for reference (optional)
    ard = dict(arrowstyle="->")
    plt.annotate('Francia', xy = (-118.25, 34.05), 
                   xytext = (-108.25, 34.05), arrowprops = ard)
    plt.annotate('Argentina', xy = (-122.1381, 37.4292), 
                   xytext = (-112.1381, 37.4292), arrowprops= ard)
    plt.annotate('España', xy = (-71.1106, 42.3736), 
                   xytext = (-73.1106, 48.3736), arrowprops= ard)
    plt.annotate('Colombia', xy = (-87.6847, 41.8369), 
                   xytext = (-87.6847, 46.8369), arrowprops= ard)
    plt.annotate('Noruega', xy = (-122.33, 47.61), 
                   xytext = (-116.33, 47.61), arrowprops= ard)
    plt.annotate('Japon', xy = (-80.21, 25.7753), 
                   xytext = (-80.21, 30.7753), arrowprops= ard)
    params = plt.gcf()
    plSize = params.get_size_inches()
    params.set_size_inches( (plSize[0] * 3, plSize[1] * 3) )
    plt.show()
    fig.savefig("img/mapas.jpg")
    return