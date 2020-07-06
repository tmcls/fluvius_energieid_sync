##### HOWTO #####
## 1. Download your history csv file from https://mijnverbruik.fluvius.be/verbruikshistoriek
## 2. Rename the file to <import.csv>
## 3. Run the following command: python run.py

import sys

##### CONFIG #####
# This are the names of your meter at EnergieId.be
energieId_usage_day       = "Elek.Afname.Dag"
energieId_usage_night     = "Elek.Afname.Nacht"
energieId_prod_day        = "Elek.Injectie.Dag"
energieId_prod_night      = "Elek.Injectie.Nacht"
energieId_export_filename = "energieid.csv"

try:
    # Check for filename argument (first is run.py, second is the import file)
    if len(sys.argv) <= 1:
        raise IndexError('No importfile as argument.')

    # Read importfilename from arguments
    import_filename = sys.argv[1]

    # Read Fluvius Import file
    with open(import_filename) as fluvius:

        # skip first row with headers
        next(fluvius)
        data = [line.split(";") for line in fluvius]

        # Writer for EnergieID file
        with open(energieId_export_filename, 'w') as export:
            export.write("Timestamp;{0};{1};{2};{3}\n".format(energieId_usage_day, energieId_usage_night, energieId_prod_day, energieId_prod_night))

            date_from = "00/00/0000"
            date_to   = "00/00/0000"
            for row in data:

                # If date is different, put data in export file
                if date_from != row[0] and date_to != row[2] and date_from != "00/00/0000":
                    print "{0} - {1}: {2} - {3} - {4} - {5}".format(date_from, date_to, usage_day, usage_night, prod_day, prod_night)
                    export.write("{0} 23:59;{2};{3};{4};{5}\n".format(date_from, date_to, usage_day, usage_night, prod_day, prod_night))

                print " *** 0:{0} - 1:{1} - 2:{2} - 3:{3} - 4:{4} - 5:{5} - 6:{6} - 7:{7} - 8:{8} - 9:{9}".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])

                # If date is different, reset all parameters
                if date_from != row[0] and date_to != row[2]:
                    date_from  = row[0]
                    date_to    = row[2]
                    usage_day = "0,000"    
                    usage_night = "0,000"    
                    prod_day = "0,000"    
                    prod_night = "0,000"    

                # Process correct register to variable
                if row[7] == "Afname Dag" and row[8] != "":
                    usage_day = row[8]
                if row[7] == "Afname Nacht" and row[8] != "":
                    usage_night = row[8]
                if row[7] == "Injectie Dag" and row[8] != "":
                    prod_day = row[8]
                if row[7] == "Injectie Dag" and row[8] != "":
                    prod_night = row[8]

except IndexError as e:
    print "Error: {0}".format(e)
    sys.exit(2)
except IOError:
    print "Error: Cannot open {0}".format(import_filename)
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise