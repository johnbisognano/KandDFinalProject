import pandas as pd
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

def schipholTaxes(numberOfPassengers, noiseCategory, MTOW):
    serviceChargePerPassenger = 11.77
    securityChargePerPassenger = 10.88
    passengerCharges = (serviceChargePerPassenger + securityChargePerPassenger) * numberOfPassengers

    if MTOW < 20000:
        MTOW = 20000
    #we assume only connected stands
    #we only count prices for daytime arrivals/departures

    if noiseCategory = 'Category MCC3':
        landingTakeOfCharge = (MTOW/1000) * 6.21
    elif noiseCategory = 'Category A':
        landingTakeOfCharge = (MTOW/1000) * 5.43
    elif noiseCategory = 'Category B':
        landingTakeOfCharge = (MTOW/1000) * 3.88
    elif noiseCategory = 'Category C':
        landingTakeOfCharge = (MTOW/1000) * 3.10

    if status = 'departing':
        result = passengerCharges + landingTakeOfCharge
    else:
        result = landingTakeOfCharge
    return result

def charlesDesGaullesTaxes(numberOfPassengers, noiseCategory, MTOW):
    landingFee = 286.03 + 3.993 * MTOW
    #assuming only daytime arrivals/departures
    if wingArea <= 90:
        landingFee = landingFee * 1.3
    elif wingArea >90 & <=200:
        landingFee = landingFee * 1.2
    elif wingArea >200 & <=300:
        landingFee = landingFee*1.150
    elif wingArea >300 & <=800:
        landingFee = landingFee*1.00
    else:
        landingFee = landingFee*0.850

    parkingFee = 3.704 * MTOW
    passengerFee = 9.05 * numberOfPassengers

    if status = 'departing':
        result = (landingFee/2)+(parkingFee/2)+passengerFee
    else:
        result = (landingFee/2)+(parkingFee/2)
    return result

def munichTaxes(numberOfPassengers, noiseCategory, MTOW):
    #average between bonus and non-bonus planes
    #assuming only daytime takeoffs and landings
    landingFeeMunich = (2.72+4.36)/2 * MTOW

    #noise categories
    passengerFeeMunich = (19.95 + 0.70 + 0.37)*numberOfPassengers

    if status = 'departing':
        result = (landingFeeMunich / 2) +  passengerFeeMunich
    else:
        result = (landingFeeMunich / 2)
    return result

def frankfurtTaxes(numberOfPassengers, noiseCategory, MTOW):
    landingFeeFrankfurt = 0
    if MTOW<=15:
        landingFeeFrankfurt = 226.36 +1.36*numberOfPassengers
    if MTOW>15 & MTOW<=35:
        landingFeeFrankfurt = 136.85 +1.36*numberOfPassengers
    if MTOW>35 & MTOW<=66:
        landingFeeFrankfurt = 33.95 +1.36*numberOfPassengers
    passengerChargeFrankfurt = numberOfPassengers * (18.16 + 1.24)

    #parking charges are skipped due to manual categorization reasons

    if status = 'departing':
        result = (landingFeeFrankfurt / 2) + passengerChargeFrankfurt
    else:
        result = (landingFeeFrankfurt / 2)
    return result

def barcelonaTaxes(numberOfPassengers, noiseCategory, MTOW):
    landingFeeBarcelona = (7,112002+3,313090) * MTOW
    passengerFeeBarcelona = 13.7*numberOfPassengers
    parkingFeeBarcelona = 4*MTOW*(0,124357+26,853551)

    if status = 'departing':
        result = (landingFeeBarcelona/2) + (parkingFeeBarcelona/2) + passengerFeeBarcelona
    else:
        result = (landingFeeBarcelona/2) + (parkingFeeBarcelona/2)
    return result

def madridTaxes(numberOfPassengers, noiseCategory, MTOW):
    landingFeeMarid = (8,072800+3,333669) * MTOW
    passengerFeeMadrid = 14.73 * numberOfPassengers
    parkingFeeMadrid = 4*MTOW*(0,130366+29,618851)

    if status = 'departing':
        result = (landingFeeMarid/2)+(parkingFeeMadrid/2)+passengerFeeMadrid
    else:
        result = (landingFeeMarid/2)+(parkingFeeMadrid/2)
    return result

def romeTaxes(numberOfPassengers, noiseCategory, MTOW):
    #assuming peak hour prices
    if MTOW<=25:
        landingTakeOffRome = 54.15 + MTOW*4.67
    elif MTOW>25 & MTOW<=75 :
        landingTakeOffRome = 54.15 + MTOW*4.99
    elif MTOW>75 & MTOW<=150 :
        landingTakeOffRome = 54.15 + MTOW*2.32
    elif MTOW>150 & MTOW<=250:
        landingTakeOffRome = 54.15 + MTOW*2.53
    elif MTOW >250:
        landingTakeOffRome = 54.15 + MTOW*1.58

    #assuming only adults
    passengerChargeRome = numberOfPassengers * (17.77 + 3.34 + 2.27)

    if status = 'departing':
        result = (landingTakeOffRome/2) + passengerChargeRome
    else:
        result = (landingTakeOffRome/2)
    return result

def heathrowTaxes(numberOfPassengers, noiseCategory, MTOW):
    euroMultiplier = 1.13932259
    passengerFeeHeathrow = numberOfPassengers * 24.13
    if passengerFeeHeathrow<1378.08:
        passengerFeeHeathrow = 1378.08

def pricePerFlight(aircraftPrice, lifetime):
    pricePerHour = aircraftPrice/lifetime
    return pricePerHour

def airportTaxes(numberOfPassengers, noiseCategory, MTOW):
    if airportName = 'Schiphol':
        schipholTaxes(numberOfPassengers, noiseCategory, MTOW)
    elif airportName = 'Charles de Gaulle':
        charlesDesGaullesTaxes(numberOfPassengers, noiseCategory, MTOW)
    elif airportName = 'Munich':
        munichTaxes(numberOfPassengers, noiseCategory, MTOW)
    elif airportName = 'Frankfurt':
        frankfurtTaxes(numberOfPassengers, noiseCategory, MTOW)
    elif airportName = 'Barcelona':
        barcelonaTaxes(numberOfPassengers, noiseCategory, MTOW)
    elif airportName = 'Madrid':
        madridTaxes(numberOfPassengers, noiseCategory, MTOW)
    elif airportName = 'Rome':
        romeTaxes(numberOfPassengers, noiseCategory, MTOW)
    elif airportName = 'Heathrow':
        heathrowTaxes(numberOfPassengers, noiseCategory, MTOW)

def distance(input1, input2, airport):

    geolocator = Nominatim(user_agent="calculator")
    location1 = geolocator.geocode(input1)
    location2 = geolocator.geocode(input2)
    distanceTotal = geodesic((location1.latitude, location1.longitude), (location2.latitude, location2.longitude)).kilometers
    return distanceTotal





def fuelCosts(usage, distance, pricePerLiter):
    fuelCost = usage * distance * pricePerLiter #in case of KG's include fuel density too
    return fuelCost

def refuelLocation(airport1, airport2, df):
    priceCountryA = df.loc[df['AIRPORT'] == airport1]['PRICE INCL VAT']
    priceCountryB = df.loc[df['AIRPORT'] == airport2]['PRICE INCL VAT']

    if (priceCountryA.iloc[0] < priceCountryB.iloc[0]):
        return priceCountryA.iloc[0]
    else:
        return priceCountryB.iloc[0]

def main():
    aircraft = pd.read_csv('test.csv', delimiter=',', skipinitialspace=True)
    airport = pd.read_csv('airporttest.csv', delimiter=',', skipinitialspace=True)
    fuelCSV = pd.read_csv('19-10-2018_prix_europe.csv', delimiter=',', skipinitialspace=True)

    input1 = 'Schiphol'
    input2 = 'Frankfurt Airport'

    mergedDF = pd.merge(fuelCSV, airport, how='left', on=['COUNTRY'])

    aircraft['PRICEPERFLIGHT']=pricePerFlight(aircraft['PRICE'], aircraft['LIFETIME'])
    aircraft['FUELCOSTS'] = fuelCosts(aircraft['USAGE'], distance(input1, input2, airport), refuelLocation(input1, input2, mergedDF))

    print(aircraft)

    # airportTaxes()

    # refuelLocation(priceCountryA, princeCountryB)



if __name__ == '__main__':
    main()