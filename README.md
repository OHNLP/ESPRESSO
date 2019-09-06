# ESPRESSO

  ESPRESSO NLP System for processing neuroimaging reports to classify a patient's SBI and WMD status

  CONFIGURATION:
  INPUT_DIR: full directory path of input folder 
  OUTPUT_DIR: full directory path of output folder
  OUTPUT_SUMMARY_DIR: full directory path of output summary folder
  RULES_DIR: full directory path of 'SBI' folder

  INPUT:
  Input file: patient level .txt file
  Input file preprocessing: replace all '/n' to '.'

  RUN:
  command line:
  ./runMedTagger-fit-sbi.sh

  OUTPUT:
  raw folder: concept level finding
  summary folder: patient level finding
