git clone https://github.com/cvat-ai/cvat
cd cvat
docker exec -it cvat_server bash -ic 'python3 ~/manage.py createsuperuser'
export CVAT_HOST=cvat.cancili.co 
export CVAT_SERVERLESS=1
docker compose up -d

