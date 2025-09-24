# Indicates that "all", "fetch", "analyze", and "clean" are not associated with files of the same name, and that if such files do exist, it will still execute the commands for the targets listed
.PHONY: all fetch analyze clean

# Default target
all: analyze

# A rule to fetch the data
fetch:
	./fetch_metars.sh

# A rule to analyze the data, which depends on 'fetch'
analyze: fetch
	./analyze_data.sh
	@echo "--- Pipeline successfully complete ---""

# A rule to clean up the generated files
clean:
	@echo "--- Cleaning up ---"
	rm -rf raw_metars weather_report.csv
	@echo "--- Done cleaning up ---"