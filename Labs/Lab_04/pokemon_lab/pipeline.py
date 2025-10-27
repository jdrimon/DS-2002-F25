#!/usr/bin/env python3

import generate_summary
import sys
import update_portfolio

def run_production_pipeline():
    sys.stderr.write('--- Starting Production ---\n')

    print('--- Updating Portfolio ---')
    update_portfolio.main()

    print('--- Generating Report ---')
    generate_summary.main()

    sys.stderr.write('--- Production Complete ---\n')

if __name__ == '__main__':
    run_production_pipeline()