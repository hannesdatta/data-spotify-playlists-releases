# Makefile for \raw-parse of the platform power project
# by Hannes Datta
# requires GNU Make

TEMP_DIR = ../../temp
OUTPUT_DIR = ../../release
EXT_DIR = ../../rawdata-confidential

# run get-raw...bat first to pull in the most recent raw data.

all: $(OUTPUT_DIR)/everynoise-playlist-promotions.csv $(OUTPUT_DIR)/everynoise-new-releases.csv

# parse everynoise
$(OUTPUT_DIR)/everynoise-playlist-promotions.csv: parse_promotions.py
	python.exe parse_promotions.py

$(OUTPUT_DIR)/everynoise-new-releases.csv: parse_releases.py
	python.exe parse_releases.py
