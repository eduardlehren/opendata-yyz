# opendata-yyz
Herumspielen mit Daten aus dem OpenData-Toronto-Katalog

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