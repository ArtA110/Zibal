# Zibal

Django Task for zibal.
## Prerequisites

- Docker
- Make

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ArtA110/Zibal.git
   cd zibal
2. Create venv (Optional):  
```python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. install requirements (Optional)
```
pip install -r requirements.txt
```
4. Start project:  
```bash
make build
make up
make calculate_transaction_summaries # for adding collection for cache
```

