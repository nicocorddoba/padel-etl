FROM python:3.9.5
WORKDIR /app
COPY requirements.txt ./
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && apt-get autoremove -yqq --purge \
    && apt-get install libnss3 \
    libnspr4 \           
    libdbus-1-3 \        
    libatk1.0-0 \        
    libatk-bridge2.0-0 \ 
    libatspi2.0-0 \      
    libxcomposite1 \     
    libxdamage1 \        
    libxfixes3 \         
    libxrandr2 \         
    libgbm1 \            
    libxkbcommon0 \      
    libasound2  -y \
    && apt-get clean
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install
# RUN playwright install-deps
COPY ./ ./
CMD ["python","-u","main.py"]