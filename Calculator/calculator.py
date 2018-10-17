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
    if noiseCategory = 'Category A':
        landingTakeOfCharge = (MTOW/1000) * 5.43
    if noiseCategory = 'Category B':
        landingTakeOfCharge = (MTOW/1000) * 3.88
    if noiseCategory = 'Category C':
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
    if wingArea >90 & <=200:
        landingFee = landingFee * 1.2
    if wingArea >200 & <=300:
        landingFee = landingFee*1.150
    if wingArea >300 & <=800:
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
    if MTOW <= 15:
        landingFeeFrankfurt = 226.36 +1.36*numberOfPassengers
    if MTOW >15 & <= 35:
        landingFeeFrankfurt = 136.85 +1.36*numberOfPassengers
    if MTOW >35 & <=66:
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

def  romeTaxes(numberOfPassengers, noiseCategory, MTOW):
    

def pricePerFlight():
    pricePerHour = aircraftPrice/lifetime
    return pricePerHour

def airportTaxes(numberOfPassengers, noiseCategory, MTOW):
    if airportName = 'Schiphol':
        schipholTaxes(numberOfPassengers, noiseCategory, MTOW)
    if airportName = 'Charles de Gaulle':
        charlesDesGaullesTaxes(numberOfPassengers, noiseCategory, MTOW)
    if airportName = 'Munich':
        munichTaxes(numberOfPassengers, noiseCategory, MTOW)
    if airportName = 'Frankfurt':
        frankfurtTaxes(numberOfPassengers, noiseCategory, MTOW)
    if airportName = 'Barcelona':
        barcelonaTaxes(numberOfPassengers, noiseCategory, MTOW)
    if airportName = 'Madrid':
        madridTaxes(numberOfPassengers, noiseCategory, MTOW)
    if airportName = 'Rome':
        romeTaxes(numberOfPassengers, noiseCategory, MTOW)


def fuelCosts():
    fuelCost = usage * distance * price per Liter #in case of KG's include fuel density too
    return fuelCost

def refuelLocation():
    if (priceCountryA < priceCountryB):
        return priceCountryA
    else:
        return priceCountryB

def main():
    pricePerFlight()
    airportTaxes()
    fuelCosts()
    refuelLocation()



if __name__ == '__main__':
    main()