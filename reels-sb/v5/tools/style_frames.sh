#!/bin/bash
# Re-shoot the v5 style frames (lossless snapshots of the real compositions) into v5/style/
cd "$(dirname "$0")/.."
S=$(mktemp -d)
snap(){ (cd mg/entry/$1 && npx hyperframes snapshot --at $2 --no-end -o $S/$1_$2 >/dev/null 2>&1); cp $S/$1_$2/frame-00-*.png style/$3.png; }
snap test_ws 1.75 01_ws_hook; snap test_ws 14.7 02_ws_dashboard_boxes; snap test_ws 19.3 03_ws_count_chips; snap sf-ws-offer 5.3 04_ws_offer_1_per_ad_5x
snap test_ea 5.4 05_ea_ad_agent_angles; snap test_ea 7.3 06_ea_ad_agent_ad_lands; snap sf-ea-ret 8.45 07_ea_retention_flow; snap sf-ws-end 1.6 08_ws_end_card
rm -rf $S; ls style
