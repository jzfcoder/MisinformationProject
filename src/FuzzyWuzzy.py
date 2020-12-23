from fuzzywuzzy import process
str2Match = "Stimulus Bill"
strOptions = ["Michael expected to sign covid stimulus bill","Congress passes long awaited covid relief stimulus bill to Michael","Congress races to finalize covid stimulus bill","Cat races dog for food","Michael alleged to have stolen fast food in hopes to run faster"]
Ratios = process.extract(str2Match,strOptions)
print(Ratios)
# You can also select the string with the highest matching percentage
highest = process.extractOne(str2Match,strOptions)
print(highest)