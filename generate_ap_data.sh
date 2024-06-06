#!/bin/sh
cd "$(dirname "$0")"
cd ..
python -m cavern_of_dreams_ap_logic.generate_ap_data
