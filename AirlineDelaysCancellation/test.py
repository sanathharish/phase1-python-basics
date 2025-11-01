
import pandas as pd
# airline = pd.read_csv(".//RawData//airlines.csv")
# print(airline.shape)
# print(airline.head())
# print(airline.isnull().sum())
# print(airline.dtypes)



airports = pd.read_csv(".//RawData//airports.csv")
# print(airport.shape)
# print(airport.head())
# print(airport.isnull().sum())
# print(airport.dtypes)

#Track airports with missing latitudes and longitudes
missing_airports = airports[airports[['LATITUDE','LONGITUDE']].isnull().any(axis=1)]
print(airports[['LATITUDE','LONGITUDE']].isnull().any(axis=1))

print("Airports with missing coordinates :")
print(missing_airports[['IATA_CODE','AIRPORT']])
missing_codes = missing_airports['IATA_CODE'].tolist()



# flights = pd.read_csv(".//RawData//flights.csv") 
# print(flights.shape)
# print(flights.head())
# print(flights.isnull().sum())
# print(flights.dtypes)
