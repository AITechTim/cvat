git clone https://github.com/cvat-ai/cvat
cd cvat

docker plugin install fentas/davfs
export SHARED_DRIVE_PASSWORD=
docker volume create \
  -d fentas/davfs \
  -o url=https://u399415:$SHARED_DRIVE_PASSWORD@u399415.your-storagebox.de/prepared_data/ROI_dataset/ \
  -o uid=1000 -o gid=1000 roi_dav_volume

docker exec -it cvat_server bash -ic 'python3 ~/manage.py createsuperuser'
export CVAT_HOST=cvat.cancili.co
export CVAT_SERVERLESS=1

docker compose -f docker-compose.local.yml -f components/serverless/docker-compose.serverless.yml up -d --build

docker compose -f docker-compose.local.yml -f components/serverless/docker-compose.serverless.yml down

## [Setup nuclio](https://docs.cvat.ai/docs/administration/advanced/installation_automatic_annotation/)
- check nuclio version in components/serverless/docker-compose.serverless.yml
- download nuclio
wget https://github.com/nuclio/nuclio/releases/download/1.13.0/nuctl-1.13.0-linux-amd64
- make it executable
chmod +x nuctl-1.13.0-linux-amd64
sudo mv nuctl-1.13.0-linux-amd64 /usr/local/bin/nuctl
- deploy example functions
./serverless/deploy_cpu.sh serverless/openvino/dextr
./serverless/deploy_cpu.sh serverless/openvino/omz/public/yolo-v3-tf

docker compose up -d

- nuclio dashboard: localhost:8070
- cvat ui: localhost:8080 / cvat.cancili.co
