# Fraud Detection Service

Real-time fraud scoring engine with configurable rules,
velocity checks, and merchant whitelist/blacklist management.

## API Endpoints

- `POST /v1/fraud/score` - Get risk score for a transaction
- `GET /v1/fraud/rules` - List fraud rules
- `POST /v1/fraud/whitelist` - Add to whitelist
- `POST /v1/fraud/blacklist` - Add to blacklist

## Running

```bash
docker build -t fraud-detection-service .
docker run -p 8003:8000 fraud-detection-service
```
