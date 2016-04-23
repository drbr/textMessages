pythonExec = "/usr/local/bin/python"


# The input files - must be supplied by the user
contactsVcf = Contacts.vcf
txtsSqlite = txts.sqlite
facebookHtml = facebook-andrewbr/html/messages.htm
facebookAccessToken = facebookAccessToken.txt

# Output files - these land in the outputDir directory
outputDir = "output"
txtsCsv = txts.csv
contactsCsv = Contacts.csv
facebookCsv = facebookMessages.csv
allMessagesFile = allMessages.csv

all : text facebook
	/bin/cat $(outputDir)/$(txtsCsv) $(outputDir)/$(facebookCsv) > $(outputDir)/$(allMessagesFile)

makeOutputDirectory :
	-mkdir -p $(outputDir)

vcfToCsv : makeOutputDirectory $(contactsVcf)
	$(pythonExec) extract_vcf.py $(contactsVcf) $(outputDir)/$(contactsCsv)

text : makeOutputDirectory vcfToCsv $(txtsSqlite)
	$(pythonExec) extract_txts.py $(txtsSqlite) $(outputDir)/$(contactsCsv) $(outputDir)/$(txtsCsv)

facebook : makeOutputDirectory $(facebookHtml)
	$(pythonExec) extract_facebook.py $(facebookHtml) $(facebookAccessToken) $(outputDir)/$(facebookCsv)

clean :
	-rm -r $(outputDir) *.pyc