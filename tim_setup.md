sudo apt-get install ca-certificates davfs2 
git clone https://github.com/cvat-ai/cvat
cd cvat

docker plugin install fentas/davfs
export SHARED_DRIVE_PASSWORD=
docker volume create \
  -d fentas/davfs \
  -o url=https://u399415:$SHARED_DRIVE_PASSWORD@u399415.your-storagebox.de/prepared_data/ROI_dataset/ \
  -o uid=1000 -o gid=1000 roi_dav_volume

sudo mount /mnt/shared

export CVAT_HOST=cvat.cancili.co

export CVAT_HOST=cvat.cancilico.site
<!-- export CVAT_UI_HOST=cvat.cancilico.site -->

export CVAT_HOST=localhost
<!-- export CVAT_UI_HOST=localhost -->

export CVAT_SERVERLESS=1

<!-- docker compose -f docker-compose.local.yml -f components/serverless/docker-compose.serverless.yml up -d --build
docker compose -f docker-compose.local.yml -f components/serverless/docker-compose.serverless.yml down -->
<!-- Drop above, the below official dev setup is recommended. -->

docker compose -f docker-compose.yml -f docker-compose.dev.yml -f components/serverless/docker-compose.serverless.yml up -d --build --remove-orphans

- for https
export ACME_EMAIL=schmittman@cancilico.com
docker compose -f docker-compose.yml -f docker-compose.dev.yml -f docker-compose.https.yml -f components/serverless/docker-compose.serverless.yml up --build --remove-orphans



docker exec -it cvat_server bash -ic 'python3 ~/manage.py createsuperuser'

docker compose -f docker-compose.yml -f docker-compose.dev.yml -f components/serverless/docker-compose.serverless.yml up

## Some troubleshooting for dev mode
- Make sure to run traffic via traefik. Otherwise you will get CORS errors when trying to access backend.
- Double check above environment variables are set correctly.
- Check you are running dev mode (server is using development django config, Dockerfile is building dev requirements, cvat_ui is using webpack serve --host 0.0.0.0 --config webpack.config.js --mode=development).


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
./serverless/deploy_cpu.sh serverless/pytorch/facebookresearch/sam/nuclio
./serverless/deploy_cpu.sh serverless/pytorch/facebookresearch/sam2/nuclio
- Port will change regularly, check nuclio dashboard matches docker ps. Otherwise delete function on dashboard and redeploy with above command.


- nuclio dashboard: localhost:8070
- cvat ui: localhost:8080 / cvat.cancili.co
