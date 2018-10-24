import pandas as pd
import numpy as np
from geopy.distance import geodesic
from geopy.geocoders import Nominatim


def schipholTaxes(numberOfPassengers, noiseCategory, MTOW):
    schipholMTOW = MTOW.copy()

    serviceChargePerPassenger = 11.77
    securityChargePerPassenger = 10.88
    passengerCharges = (serviceChargePerPassenger + securityChargePerPassenger) * numberOfPassengers

    for i in range(0, len(schipholMTOW.index)):
        if schipholMTOW.iloc[i] < 20:
            schipholMTOW.iloc[i] = 20

        # we assume only connected stands
        # we only count prices for daytime arrivals/departures

    if noiseCategory == 'Category MCC3':
        landingTakeOfCharge = (schipholMTOW) * 6.21
    elif noiseCategory == 'Category A':
        landingTakeOfCharge = (schipholMTOW) * 5.43
    elif noiseCategory == 'Category B':
        landingTakeOfCharge = (schipholMTOW) * 3.88
    elif noiseCategory == 'Category C':
        landingTakeOfCharge = (schipholMTOW) * 3.10

    result = (passengerCharges / 2) + (landingTakeOfCharge / 2)

    return result


# def charlesDesGaullesTaxes(numberOfPassengers, noiseCategory, MTOW):
#     landingFee = 286.03 + 3.993 * MTOW
#     #assuming only daytime arrivals/departures
#     if wingArea <= 90:
#         landingFee = landingFee * 1.3
#     elif wingArea >90 & wingArea<=200:
#         landingFee = landingFee * 1.2
#     elif wingArea >200 & wingArea<=300:
#         landingFee = landingFee*1.150
#     elif wingArea >300 & wingArea<=800:
#         landingFee = landingFee*1.00
#     else:
#         landingFee = landingFee*0.850
#
#     parkingFee = 3.704 * MTOW
#     passengerFee = 9.05 * numberOfPassengers
#
#     result = (landingFee / 2) + (parkingFee / 2) + (passengerFee / 2)
#     return result


def munichTaxes(numberOfPassengers, noiseCategory, MTOW):
    # average between bonus and non-bonus planes
    # assuming only daytime takeoffs and landings
    landingFeeMunich = (2.72 + 4.36) / (2 * MTOW)

    # noise categories
    passengerFeeMunich = (19.95 + 0.70 + 0.37) * numberOfPassengers

    result = (landingFeeMunich / 2) + (passengerFeeMunich / 2)

    return result


def frankfurtTaxes(numberOfPassengers, noiseCategory, MTOW):

    landingFeeFrankfurt=[]
    for i in range(0, len(MTOW.index)):
        if MTOW.iloc[i] <= 15:
            landingFeeFrankfurt.append(226.36 + 1.36 * numberOfPassengers)
        elif MTOW.iloc[i] > 15:
            if MTOW.iloc[i] <= 35:
                landingFeeFrankfurt.append(136.85 + 1.36 * numberOfPassengers)
            elif MTOW.iloc[i] > 35:
                landingFeeFrankfurt.append(33.95 + 1.36 * numberOfPassengers)

    vLandingFeeFrankfurt = np.array(landingFeeFrankfurt)
    passengerChargeFrankfurt = numberOfPassengers * (18.16 + 1.24)

    # parking charges are skipped due to manual categorization reasons

    result = (vLandingFeeFrankfurt / 2) + (passengerChargeFrankfurt / 2)
    df = pd.Series(result, name='something')


    return df


def barcelonaTaxes(numberOfPassengers, noiseCategory, MTOW):
    landingFeeBarcelona = (7.112002 + 3.313090) * MTOW
    passengerFeeBarcelona = 13.7 * numberOfPassengers
    parkingFeeBarcelona = 4 * MTOW * (0.124357 + 26.853551)

    result = (landingFeeBarcelona / 2) + (parkingFeeBarcelona / 2) + (passengerFeeBarcelona / 2)

    return result


def madridTaxes(numberOfPassengers, noiseCategory, MTOW):
    landingFeeMarid = (8.072800 + 3.333669) * MTOW
    passengerFeeMadrid = 14.73 * numberOfPassengers
    parkingFeeMadrid = 4 * MTOW * (0.130366 + 29.618851)

    result = (landingFeeMarid / 2) + (parkingFeeMadrid / 2) + (passengerFeeMadrid / 2)

    return result


def romeTaxes(numberOfPassengers, noiseCategory, MTOW):
    # assuming peak hour prices
    landingTakeOffRome = []
    for i in range (0,len(MTOW.index)):
        if MTOW.iloc[i] <= 25:
            landingTakeOffRome.append(54.15 + MTOW.iloc[i] * 4.67)
        elif MTOW.iloc[i] > 25:
            if MTOW.iloc[i] <= 75:
                landingTakeOffRome.append(54.15 + MTOW.iloc[i] * 4.99)
            elif MTOW.iloc[i] > 75:
                if MTOW.iloc[i] <= 150:
                    landingTakeOffRome.append(54.15 + MTOW.iloc[i] * 2.32)
                elif MTOW.iloc[i] > 150:
                    if MTOW.iloc[i] <= 250:
                        landingTakeOffRome.append(54.15 + MTOW.iloc[i] * 2.53)
                    elif MTOW.iloc[i] > 250:
                        landingTakeOffRome.append(54.15 + MTOW.iloc[i] * 1.58)

    #assuming only adults
    vLandingTakeOffRome = np.array(landingTakeOffRome)
    passengerChargeRome = numberOfPassengers * (17.77 + 3.34 + 2.27)

    result = (vLandingTakeOffRome / 2) + (passengerChargeRome / 2)
    df = pd.Series(result, name='something')

    return df



def pricePerFlight(aircraftPrice, lifetime):
    pricePerHour = aircraftPrice / lifetime
    return pricePerHour


def airportTaxes(numberOfPassengers, noiseCategory, MTOW, airportName):
    if airportName == 'Schiphol':
        return (schipholTaxes(numberOfPassengers, 'Category B', MTOW))
    elif airportName == 'Charles de Gaulle':
        charlesDesGaullesTaxes(numberOfPassengers, noiseCategory, MTOW)
    elif airportName == 'Munich Airport':
        return munichTaxes(numberOfPassengers, noiseCategory, MTOW)
    elif airportName == 'Frankfurt Airport':
        return frankfurtTaxes(numberOfPassengers, noiseCategory, MTOW)
    elif airportName == 'Barcelona Airport':
        return barcelonaTaxes(numberOfPassengers, noiseCategory, MTOW)
    elif airportName == 'Madrid Airport':
        return madridTaxes(numberOfPassengers, noiseCategory, MTOW)
    elif airportName == 'Rome Airport':
        return romeTaxes(numberOfPassengers, noiseCategory, MTOW)


def distance(input1, input2, airport):
    geolocator = Nominatim(user_agent="calculator")
    location1 = geolocator.geocode(input1)
    location2 = geolocator.geocode(input2)
    distanceTotal = geodesic((location1.latitude, location1.longitude),
                             (location2.latitude, location2.longitude)).kilometers
    return distanceTotal


def fuelCosts(usage, distance, pricePerLiter):
    fuelCost = usage * distance * pricePerLiter  # in case of KG's include fuel density too
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

    airportList = []
    input1 = 'Madrid Airport'
    airportList.append(input1)
    input2 = 'Rome Airport'
    airportList.append(input2)
    input3 = 2000
    noiseCategory = 'A'

    mergedDF = pd.merge(fuelCSV, airport, how='left', on=['COUNTRY'])

    aircraft['PRICEPERFLIGHT'] = pricePerFlight(aircraft['PRICE'], aircraft['LIFETIME'])
    aircraft['FUELCOSTS'] = fuelCosts(aircraft['USAGE'], distance(input1, input2, airport),
                                      refuelLocation(input1, input2, mergedDF))

    aircraft['Airport 1 charge'] = np.nan
    aircraft['Airport 2 charge'] = np.nan

    aircraft['Airport 1 charge'] = airportTaxes(input3, aircraft['NOISECAT'], aircraft['MTOW'], input1)
    aircraft['Airport 2 charge'] = airportTaxes(input3, aircraft['NOISECAT'], aircraft['MTOW'], input2)

    print(aircraft)

    #check for capacity



if __name__ == '__main__':
    main()
