from flask import Flask, request
from flask import render_template
from SPARQLWrapper import SPARQLWrapper, JSON
import calculator as calc
import csv

app = Flask(__name__)


@app.route('/')
@app.route('/index/<name>')
def index(name=None):
    return render_template('index.html', name=name)


@app.route('/about')
def about(name=None):
    return render_template('about.html', name=name)


@app.route('/generator', methods=['GET', 'POST'])
def generator(name=None):
    sparql = SPARQLWrapper("http://localhost:5820/Aircraft/query")
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX nas: <https://data.nasa.gov/ontologies/atmonto/NAS#>
        PREFIX gen: <https://data.nasa.gov/ontologies/atmonto/general#>
        PREFIX fl: <http://www.exampleflight.org/>
        SELECT ?airport
        WHERE {
            ?airport a fl:Airport .
            ?airport fl:locatedIn fl:Europe .
        } LIMIT 10
    """)
    sparql.setReturnFormat(JSON)
    # sparql.addParameter("Accept", "Application/sparql-results+json")
    sparql.addParameter('reasoning', 'true')
    results = sparql.query().convert()
    # hopefully this query retuns a list of the airports for the dropdown
    dropdown = []
    params = results["results"]["bindings"]
    for val in params:
        dropdown.append(val['airport']['value'].split('resource/')[1].replace('_', ' ').strip())
    params = dropdown
    error1 = "The departure and arrival airports may not be the same."
    error2 = "Please enter a value for passengers."
    if request.method == 'POST':
        passengers = request.form['passengers']
        departure = request.form['dept']
        arrival = request.form['arr']
        if departure == arrival:
            return render_template('generator.html', params=params, error=error1)
        if passengers is '':
            return render_template('generator.html', params=params, error=error2)
        q = query(passengers, departure, arrival)
        results = q[0]
        total = q[1]  # dummy variable, not sure how to calculate this currently
        return render_template('generator.html', params=params, error="", results=results, total=total)

    else:
        return render_template('generator.html', params=params, error="")


def query(passengers, departure, arrival):
    sparql = SPARQLWrapper("http://localhost:5820/Aircraft/query")
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX fl: <http://www.exampleflight.org/>
        PREFIX eqp: <https://data.nasa.gov/ontologies/atmonto/equipment#>
        SELECT ?aircraftName ?burnrate ?unitcost ?lifetime ?mtw ?speed ?capacity ?cat
        WHERE {
            ?aircraft rdfs:label ?aircraftName .
            ?aircraft a fl:AircraftType .
            ?aircraft fl:burnRate ?burnrate .
            ?aircraft fl:unitCost ?unitcost .
            ?aircraft fl:maxDefaultFlightHours ?lifetime .
            ?aircraft eqp:hasAircraftWakeCategory ?wake .
            ?aircraft fl:hasSpeed ?speed .
            ?aircraft fl:numberOfSeats ?capacity .
            ?aircraft fl:hasNoiseCategory ?cat .
            {?wake eqp:maxTakeoffWeightLowBound ?mtw .}
            UNION
            {?wake eqp:maxTaxeoffWeightHighBound ?mtw .}
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    aircraft_results = results["results"]["bindings"]

    with open("aircraft.csv", "w") as aircrafts:
        writer = csv.writer(aircrafts)
        
        writer.writerow(["TYPE", "PRICE", "LIFETIME", "MTOW", "USAGE", "CAPACITY", "NOSIECAT", "SPEED"])
        for result in aircraft_results:
            writer.writerow([
                result["aircraftName"]["value"],
                result["unitcost"]["value"],
                result["lifetime"]["value"],
                result["mtw"]["value"],
                result["burnrate"]["value"],
                result["capacity"]["value"],
                result["cat"]["value"].split('flight.org/')[1].strip(),
                result["speed"]["value"]
            ])
        aircrafts.close()

    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX fl: <http://www.exampleflight.org/>
        PREFIX gen: <https://data.nasa.gov/ontologies/atmonto/general#>
        PREFIX nas: <https://data.nasa.gov/ontologies/atmonto/NAS#>
        SELECT ?airport ?lat ?long ?fuelprice ?country
        WHERE {
            ?airport nas:airportLocation ?loc .
            ?loc gen:latitude ?lat .
            ?loc gen:longitude ?long .
            ?airport fl:locatedIn fl:Europe .
            ?airport fl:locatedIn ?country .
            ?country fl:hasFuelPrice ?fuelprice .
        }
    """)
    
    sparql.setReturnFormat(JSON)
    sparql.addParameter('reasoning', 'true')

    # Aircraft country fuelprice header
    results = sparql.query().convert()
    airport_results = results["results"]["bindings"]

    with open("airports.csv", "w") as airports:
        writer = csv.writer(airports)
        
        writer.writerow(["AIRPORT", "COUNTRY", "FUELPRICE"])
        for result in airport_results:
            writer.writerow([
                result["airport"]["value"].split('resource/')[1].replace('_', ' ').strip(),
                result["country"]["value"].split('resource/')[1].replace('_', ' ').strip(),
                result["fuelprice"]["value"]
            ])
        airports.close()


    #results = [[180, 'A320', 'Madrid', 100], [180, 'A320', 'Madrid', 100], [180, 'A320', 'Madrid', 100],
    #           [180, 'A320', 'Madrid', 100], [180, 'A320', 'Madrid', 100], [180, 'A320', 'Madrid', 100]]
    
    opt = calc.optimize(departure, arrival, passengers)
    res = opt.main(opt.departure, opt.arrival, opt.passengers)
    return res
