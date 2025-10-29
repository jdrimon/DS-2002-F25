#!/bin/bash

echo "--- Refreshing all card sets in card_set_lookup directory ---"

for FILE in "card_set_lookup"/*
do
    SET_ID=$(basename "$FILE" .json)
    echo "--- Updating set with ID $SET_ID ---"
    curl -s "https://api.pokemontcg.io/v2/cards?q=set.id:$SET_ID" > card_set_lookup/$SET_ID.json
    echo "--- Data written to card_set_lookup/$SET_ID.json ---"
done

echo "--- All card sets are refreshed ---"