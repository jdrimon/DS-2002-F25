#!/usr/bin/env python3

import json
import math
import numpy as np
import pandas as pd
import subprocess
import sys

def _load_lookup_data(lookup_dir):
    all_lookup_df = []

    for file_name in subprocess.run(['ls', lookup_dir], capture_output=True, text=True).stdout.split():
        if not file_name.endswith('.json'):
            continue

        filepath = lookup_dir + file_name

        with open(filepath, 'r') as f:
            data = json.load(f)

        df = pd.json_normalize(data['data'])
        
        if not 'tcgplayer.prices.holofoil.market' in df.keys() and not 'tcgplayer.prices.normal.market' in df.keys():
            card_market_value_list = []
            for i in range(len(df)):
                card_market_value_list.append(0.0)
            df['card_market_value'] = card_market_value_list
        elif not 'tcgplayer.prices.holofoil.market' in df.keys() and 'tcgplayer.prices.normal.market' in df.keys():
            df['card_market_value'] = df['tcgplayer.prices.normal.market']
            for i in range(len(df)):
                if np.isnan(df.loc[i, 'card_market_value']):
                    df.loc[i, 'card_market_value'] = 0.0
        elif 'tcgplayer.prices.holofoil.market' in df.keys() and not 'tcgplayer.prices.normal.market' in df.keys():
            df['card_market_value'] = df['tcgplayer.prices.holofoil.market']
            for i in range(len(df)):
                if np.isnan(df.loc[i, 'card_market_value']):
                    df.loc[i, 'card_market_value'] = 0.0
        elif 'tcgplayer.prices.holofoil.market' in df.keys() and 'tcgplayer.prices.normal.market' in df.keys():
            df['card_market_value'] = df['tcgplayer.prices.holofoil.market']
            for i in range(len(df)):
                if np.isnan(df.loc[i, 'card_market_value']):
                    if not np.isnan(df.loc[i, 'tcgplayer.prices.normal.market']):
                        df.loc[i, 'card_market_value'] = df.loc[i, 'tcgplayer.prices.normal.market']
                    else:
                        df.loc[i, 'card_market_value'] = 0.0

        df = df.rename(columns={'id': 'card_id', 'name': 'card_name', 'number': 'card_number', 'set.id': 'set_id', 'set.name': 'set_name'})
        required_cols = ['card_id', 'card_name', 'card_number', 'set_id', 'set_name', 'card_market_value']
        
        all_lookup_df.append(df[required_cols])
    
    lookup_df = pd.concat(all_lookup_df)
    return lookup_df.sort_values(by='card_market_value', ascending=False).drop_duplicates(subset=['card_id'], keep='first')

def _load_inventory_data(inventory_dir):
    inventory_data = []

    for file_name in subprocess.run(['ls', inventory_dir], capture_output=True, text=True).stdout.split():
        if not file_name.endswith('.csv'):
            continue

        filepath = inventory_dir + file_name
        inventory_data.append(pd.read_csv(filepath))
    
    if len(inventory_data) == 0:
        return pd.DataFrame()

    inventory_df = pd.concat(inventory_data).reset_index(drop=True)

    card_id_list = []
    for i in range(len(inventory_df)):
        card_id_list.append(str(inventory_df.loc[i, 'set_id']) + '-' + str(inventory_df.loc[i, 'card_number']))
    inventory_df['card_id'] = card_id_list
        
    return inventory_df

def update_portfolio(inventory_dir, lookup_dir, output_file):
    lookup_df = _load_lookup_data(lookup_dir)
    inventory_df = _load_inventory_data(inventory_dir)

    if inventory_df.empty:
        sys.stderr.write('--- Error: Card inventory is empty ---\n')
        with open(output_file, 'w') as f:
            f.write('index,card_id,card_name,set_name,card_market_value\n')
        return
    
    inventory_df = pd.merge(inventory_df, lookup_df, 'left', 'card_id').reset_index(drop=True)
    
    for i in range(len(inventory_df)):
        if np.isnan(inventory_df.loc[i, 'card_market_value']):
            inventory_df.loc[i, 'card_market_value'] = 0.0
        
        if type(inventory_df.loc[i, 'set_name']) == float:
            if math.isnan(inventory_df.loc[i, 'set_name']):
                inventory_df.loc[i, 'set_name'] = 'NOT_FOUND'
    
    index_list = []
    for i in range(len(inventory_df)):
        index_list.append(str(inventory_df.loc[i, 'binder_name']) + '-' + str(inventory_df.loc[i, 'page_number']) + '-' + str(inventory_df.loc[i, 'slot_number']))
    inventory_df['index'] = index_list

    inventory_df = inventory_df.rename(columns={'card_name_x': 'card_name', 'set_id_x': 'set_id', 'card_number_x': 'card_number'})
    final_cols = ['index', 'card_id', 'card_name', 'set_name', 'card_market_value']

    inventory_df = inventory_df[final_cols]
    inventory_df.to_csv(output_file, index=False)

    print('--- Successfully updated portfolio into ' + output_file + ' ---')

    return

def main():
    update_portfolio('./card_inventory/', './card_set_lookup/', 'card_portfolio.csv')

def test():
    update_portfolio('./card_inventory_test/', './card_set_lookup_test/', 'test_card_portfolio.csv')

if __name__ == '__main__':
    sys.stderr.write('--- Starting script in Test Mode ---\n')
    test()
