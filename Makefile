pythonExec = "/usr/local/bin/python"

outputDir = "output"

# Set up variables for all the file names
contactsVcf = Contacts.vcf
contactsCsv = Contacts.csv
txtsSqlite = txts.sqlite
txtsCsv = txts.csv
facebookHtml = facebook-andrewbr/html/messages.htm
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
	$(pythonExec) extract_facebook.py $(facebookHtml) $(outputDir)/$(facebookCsv)

clean :
	-rm -r $(outputDir) *.pyc