from flask import Flask, request
from flask import render_template
from SPARQLWrapper import SPARQLWrapper, JSON
import calculator as calc

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
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?airport
        WHERE {
            ?airport nas:airportLocation ?loc .
            ?loc gen:latitude ?lat .
            ?loc gen:longitude ?long .
            ?airport fl:locatedIn fl:Europe .
        }
    """)
    results = sparql.query().convert()
    # hopefully this query retuns a list of the airports for the dropdown
    params = results["results"]["bindings"]
    #params = ['Red', 'Blue', 'Black', 'Orange']
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

        results = query(passengers, departure, arrival)
        total = 999  # dummy variable, not sure how to calculate this currently
        return render_template('generator.html', params=params, error="", results=results, total=total)

    else:
        return render_template('generator.html', params=params, error="")


def query(passengers, departure, arrival):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?aircraft ?burnrate ?unitcost ?lifetime ?mtw 
        WHERE {
          ?aircraft a fl:AircraftType .
          ?aircraft fl:burnRate ?burnrate .
          ?aircraft fl:unitCost ?unitcost .
          ?aircraft fl:maxDefaultFlightHours ?lifetime .
          ?aircraft eqp:hasAircraftWakeCategory ?wake .
          {?wake eqp:maxTakeoffWeightLowBound ?mtw .}
        UNION
        {?wake eqp:maxTaxeoffWeightHighBound ?mtw .}
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    aircraft_results = results["results"]["bindings"]

    sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?airport ?lat ?long
        WHERE {
            ?airport nas:airportLocation ?loc .
            ?loc gen:latitude ?lat .
            ?loc gen:longitude ?long .
            ?airport fl:locatedIn fl:Europe .
        }
    """)
    results = sparql.query().convert()
    airport_results = results["results"]["bindings"]


    #results = [[180, 'A320', 'Madrid', 100], [180, 'A320', 'Madrid', 100], [180, 'A320', 'Madrid', 100],
    #           [180, 'A320', 'Madrid', 100], [180, 'A320', 'Madrid', 100], [180, 'A320', 'Madrid', 100]]
    
    opt = calc.optimize('airport_results','aircraft_results', passengers)
    res = opt.main(opt.departure, opt.arrival, opt.passengers)
    return res
