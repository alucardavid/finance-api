# Finance API

This api can show and execute some operations about finance information

## Instalação

How to install and run

```bash
# Clone the repo
git clone https://github.com/alucardavid/finance-api

# Access the dir in the terminal/cmd
cd finance-api

# Create a environvment python
python -m venv finance-api

# Active the environvment
Windows -- .\finance-api\Scripts\activate 
Linux -- source finance-api/bin/activate

# Install the dependencies
pip install -r .\requirements.txt

# Execute o projeto
fastapi dev app/main.py --port 7000

# To create a docker container with de production image
docker run -d --name finance-api -p 8001:80 dpereira99/finance-api:latest
