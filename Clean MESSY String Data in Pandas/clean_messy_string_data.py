import pandas as pd

# Address Data
data = {
    "Address" : [
        "123 MAIN ST.",
        "456 Elm Avenue",
        "789 Oak St",
        "1011 Pine Road",
        "12 Maple Ln",
        "13 Aspen Rd",
        "1415 Birch St",
        "16 CEDAR Blvd.",
        "17 Dogwood Dr",
        "1819 Elderberry Ave",
        "2021 FIR WAY",
        "22 Grove Rd",
        "2324 Hawthorne Ln",
        "2526 Tris Ct",
        "2728 Jasnine Dr",
        "2930 KELP St",
        "3132 Lavender Ave",
        "3334 Magnolia Rd",
        "3536 Nectarine Way",
        "3738 Olive Rd"
    ]
}

# Criando o DataFrame
df = pd.DataFrame(data)
df["Address"] = df["Address"].str.title()
df["Address"] = df["Address"].str.replace(".", "", regex=False)
df[["Number", "Street"]] = df["Address"].str.split(" ", n=1, expand=True)

# Remove suffixes
df["Street"] = df["Street"].str.replace(" St", " Street", regex=False)
df["Street"] = df["Street"].str.replace(" Ave", " Avenue", regex=False)
df["Street"] = df["Street"].str.replace(" Rd", " Road", regex=False)
df["Street"] = df["Street"].str.replace(" Ln", " Lane", regex=False)
df["Street"] = df["Street"].str.replace(" Blvd", " Boulevard", regex=False)
df["Street"] = df["Street"].str.replace(" Dr", " Drive", regex=False)
df["Street"] = df["Street"].str.replace(" Way", " Way", regex=False)
df["Street"] = df["Street"].str.replace(" Ct", " Court", regex=False)

print(df)
