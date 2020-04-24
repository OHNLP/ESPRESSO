#/bin/bash

INPUT_DIR="/Users/m176320/Documents/a_projects/LongTerm/SBI/data/raw_report/"
# INPUT_DIR="/Users/m176320/Documents/workspace3/ESPRESSO_NLP/input/"

OUTPUT_DIR="/Users/m176320/Documents/workspace3/ESPRESSO_NLP/output/raw"
OUTPUT_SUMMARY_DIR="/Users/m176320/Documents/workspace3/ESPRESSO_NLP/output/summary"
RULES_DIR="/Users/m176320/Documents/workspace3/ESPRESSO_NLP/SBI"

java -Xms512M -Xmx2000M -jar MedTagger-fit.jar $INPUT_DIR $OUTPUT_DIR $RULES_DIR

python SBI/model/run_output_sbi.py $OUTPUT_DIR $OUTPUT_SUMMARY_DIR "0"
