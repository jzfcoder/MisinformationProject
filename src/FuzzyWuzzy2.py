from fuzzywuzzy import process

str2Match = "hack democrat haul russia"
#strOptions = ["Michael expected to sign covid stimulus bill","Congress passes long awaited covid relief stimulus bill to Michael","Congress races to finalize covid stimulus bill","Cat races dog for food","Michael alleged to have stolen fast food in hopes to run faster"]
strOptions = [
    "Top Intelligence Democrat accuses Russia of cyber hack that resulted in 'big haul'",
    "'Pretty clear' Russia behind SolarWinds hack, Pompeo says, becoming 1st US official to blame Moscow",
    "FBI scrambles to assess damage from Russia-linked US government hack",
    "Senator: Treasury Dept. email accounts compromised in hack"
    ]
Ratios = process.extract(str2Match,strOptions)

matches = []

for i in Ratios:
    if (i[1] >= 50):
        matches.append(i)

print("MATCHES: " , matches)
# print(Ratios)
# You can also select the string with the highest matching percentage
highest = process.extractOne(str2Match,strOptions)
print("HIGHEST: " , highest)