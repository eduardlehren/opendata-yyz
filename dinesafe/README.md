# Zusammenfassung

Lorem Ipsum

# Download-Speicherort

https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/b6b4f3fb-2e2c-47e7-931d-b87d22806948/resource/e9df9d33-727e-4758-9a84-67ebefec1453/download/Dinesafe.json

# ElasticSearch Index Aufbau

Melden Sie sich bei den Kibana-Entwicklertools an und führen Sie die folgenden Befehle aus

```bash
PUT /dinesafe

PUT /dinesafe/_mapping
{
  "properties": {
    "odt_id": {
      "type": "keyword"
    },
    "establishment_id": {
      "type": "keyword"
    },
    "inspection_id": {
      "type": "keyword"
    },
    "establishment_name": {
      "type": "keyword"
    },
    "establishment_type": {
      "type": "keyword"
    },
    "establishment_address": {
      "type": "keyword"
    },
    "establishment_status": {
      "type": "keyword"
    },
    "min_inspections_per_year": {
      "type": "keyword"
    },
    "infrasction_details": {
      "type": "keyword"
    },
    "inspection_date": {
      "type": "date"
    },
    "severity": {
      "type": "keyword"
    },
    "action": {
      "type": "keyword"
    },
    "outcome": {
      "type": "keyword"
    },
    "amount_fined": {
      "type": "keyword"
    },
    "location_point": {
      "type": "geo_point"
    },
    "unique_id": {
      "type": "keyword"
    }
  }
}
```