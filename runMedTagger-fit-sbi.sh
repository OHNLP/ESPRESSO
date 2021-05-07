#/bin/bash

INPUT_DIR="/SBI/data/raw_report/"

OUTPUT_DIR="/ESPRESSO_NLP/output/raw"
OUTPUT_SUMMARY_DIR="/ESPRESSO_NLP/output/summary"
RULES_DIR="/ESPRESSO_NLP/SBI"


java -Xms512M -Xmx2000M -jar MedTagger-fit.jar $INPUT_DIR $OUTPUT_DIR $RULES_DIR
python SBI/model/run_output_sbi.py $OUTPUT_DIR $OUTPUT_SUMMARY_DIR "0"
