# Budget der Toronto Police

## Kibana-Zuordnungen

```bash
PUT /tps_budget

PUT /tps_budget/_mapping
{
	"properties": {
		"opendata_id": {
			"type": "integer"
		},
		"fiscal_year": 
		{
			"type": "date",
			"format": "yyyy"
		},
		"budget_type": {
			"type": "keyword"
		},
		"organization_entity": {
			"type": "keyword"
		},
		"command_name": {
			"type": "keyword"
		},
		"pillar_name": {
			"type": "keyword"
		},
		"district_name": {
			"type": "keyword"
		},
		"unit_name": {
			"type": "keyword"
		},
		"feature_category": {
			"type": "keyword"
		},
		"cost_element": {
			"type": "integer"
		},
		"cost_element_long_name": {
			"type": "keyword"
		},
		"amount": {
			"type": "double"
		}
	}
}
```

## Download-Linken: 

2024
https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/668434ee-9541-40a8-adb6-0ad805fcc9b6/resource/725e6d57-a83c-4b73-80f2-784b8014eb29/download/TPS%20Budget%202024.json

2023
https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/668434ee-9541-40a8-adb6-0ad805fcc9b6/resource/725e6d57-a83c-4b73-80f2-784b8014eb29/download/TPS%20Budget%202023.json

2022
https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/668434ee-9541-40a8-adb6-0ad805fcc9b6/resource/725e6d57-a83c-4b73-80f2-784b8014eb29/download/TPS%20Budget%202022.json

2021
https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/668434ee-9541-40a8-adb6-0ad805fcc9b6/resource/725e6d57-a83c-4b73-80f2-784b8014eb29/download/TPS%20Budget%202021.json

2020
https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/668434ee-9541-40a8-adb6-0ad805fcc9b6/resource/725e6d57-a83c-4b73-80f2-784b8014eb29/download/TPS%20Budget%202020.json