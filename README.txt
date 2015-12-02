Kaustas original on lihtsalt mäng. Kõik on single player jne.

Kaustas Additional files on mapi generaatori moodul, mis genereerib mängule kaardi, mille peal mängija liigub.

Kaustas multiprocessing_implementation on sama mäng, mida proovisin ehitada ümber multiprocessingu peale kasutades
pythonisse sisseehitatud multiprocessing moodulit. Eesmärk oli teha mängu sujuvamaks jaotades selle erinevate
pythoni protsesside peale. Kahjuks see tulemust ei andud. Mäng jäi jooksma sama kiiresti ning midagi ei muutunud.
Ma kardan, et mul polnud selleks lihtsalt piisavalt oskusi.

Kaustas socket_implementation on minu proov teha see mängi mitme mängijaga mänguks. Hetkel seisab asi selle taga, et
ma ei oska efektiivselt teha kaardi uuendamist erinevates mängijate client programmides. Ehk mis ma selle all mõtlen on
see, et kui üks mängija lõhub kaardil ära mingi blocki, siis see peaks ju uuenduma kõikide teiste mängijate client
programmi aknas. Samuti ei tea ma ka, et milliseid socketi protokolle kasutada, et mäng võimalikult kiiresti ja sujuvalt
toimiks. Samuti peaks kõik olema ka arusaadav ja mitte väga keeruline...

Hetkel tegelen kaustas original oleva mänguga. See on hetkel kõige uuem ja kõige rohkemate funktsioonidega. Tahaksin
edasi arendada ka socket_implementation kaustas olevat mängu, aga selleks on vaja häid mõtteid oma ideede teostamiseks...
Kui selle saaks valmis, siis saaks original kaustas oleva mängu funtsionaalsuse sinna ümber tõsta.