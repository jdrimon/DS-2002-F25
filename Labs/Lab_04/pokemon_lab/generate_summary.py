#!/usr/bin/env python3

import os
import pandas as pd
import sys

def generate_summary(portfolio_file):
    if not os.path.exists(portfolio_file):
        sys.stderr.write('--- Error: Portfolio file does not exist ---\n')
        sys.exit(1)
    
    df = pd.read_csv(portfolio_file)

    if df.empty:
        print('--- Portfolio file is empty ---')
        return
    
    total_portfolio_value = sum(df['card_market_value'])

    most_valuable_card = df.loc[df.idxmax()['card_market_value']]

    print('Total Portfolio Value: ' + str(total_portfolio_value) + '\n' +
          'Most Valuable Card Details:\n' +
          '\tName: ' + most_valuable_card['card_name'] + '\n' +
          '\tID: ' + most_valuable_card['card_id'] + '\n' +
          '\tValue: ' + f'{most_valuable_card['card_market_value']:,.2f}'
          )

def main():
    generate_summary('card_portfolio.csv')

def test():
    generate_summary('test_card_portfolio.csv')

if __name__ == '__main__':
    test()