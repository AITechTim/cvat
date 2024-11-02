
# Enable GPU for docker
- https://collabnix.com/introducing-new-docker-cli-api-support-for-nvidia-gpus-under-docker-engine-19-03-0-beta-release/


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
## Running dev mode
### HTTP
docker compose -f docker-compose.yml -f docker-compose.dev.yml -f components/serverless/docker-compose.serverless.yml up -d --build --remove-orphans

### HTTPS
export ACME_EMAIL=schmittman@cancilico.com
docker compose -f docker-compose.yml -f docker-compose.dev.yml -f docker-compose.https.yml -f components/serverless/docker-compose.serverless.yml up --build --remove-orphans

## Production mode
- Build docker UI image. Don't get confused by the dev tag, any self built image should have dev tag all others should get pulled from docker hub.
```
docker build -t cvat/ui:dev -f Dockerfile.ui .
```
- Run production docker compose
```
export ACME_EMAIL=schmittman@cancilico.com
export CVAT_VERSION=prod
docker compose -f docker-compose.yml -f docker-compose.https.yml -f components/serverless/docker-compose.serverless.yml up -d --build --remove-orphans
```
## Initial Setup
docker exec -it cvat_server bash -ic 'python3 ~/manage.py createsuperuser'


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

## Testing fininshed image as standalone container
docker run --volume /var/lib/docker/volumes/nuclio-nuclio-pth-facebookresearch-sam2-vit-h-allmodels/_data:/etc/nuclio/config/processor cvat.pth.facebookresearch.sam2.vit_h_allmodels:latest processor

## deploy finished image as nuclio function (Still has some issues. Get's registered in nuclio, but https://cvat.cancilico.site/api/lambda/functions gives 500 server error. Probably due to wrong config, should pass function.yaml as well.)
nuctl deploy pth-facebookresearch-sam2-vit-h-allmodels --run-image cvat.pth.facebookresearch.sam2.vit_h_allmodels:latest  --handler main:handler --project-name cvat --platform local --runtime python:3.9

## Some leftover code snippets
```
docker run --volume nuclio-cvat-pth-facebookresearch-sam2-vit-h-allmodels:/etc/nuclio/config/processor cvat.pth.facebookresearch.sam2.vit_h_allmodels:latest processor

nuctl deploy cvat.pth.facebookresearch.sam2.vit_h_allmodels:latest processor --handler main:handler --namespace cvat 

nuctl deploy pth-facebookresearch-sam2-vit-h-allmodels --run-image nuclio/processor-pth-facebookresearch-sam2-vit-h-allmodels:latest --runtime python:3.10 --handler main:handler --namespace cvat 
```

## Developing images on nuclio
### CPU
- Build basic docker image. For speeding up development, I recommend putting most logic in the Dockerfile.dev and use that as base_image in function.yaml. Also function.yaml is very badly documented.
```
cd cvat/serverless/pytorch/facebookresearch/sam2/nuclio
docker build -f Dockerfile.dev -t sam2-samexport-allmodels:latest-cpu .
```
- Deploy function (get name from function.yaml)
```
nuctl delete function -f pth-facebookresearch-sam2-large-cpu && ./serverless/deploy_cpu.sh serverless/pytorch/facebookresearch/sam2/nuclio && docker logs -f nuclio-nuclio-pth-facebookresearch-sam2-large-cpu
```
### GPU
- Build gpu docker image
```
cd cvat/serverless/pytorch/facebookresearch/sam2/nuclio
docker build -f Dockerfile.gpu -t sam2-samexport-allmodels:latest-gpu .
```
- Deploy gpu function (large)
```
nuctl delete function -f pth-facebookresearch-sam2-large-gpu && ./serverless/deploy_gpu.sh serverless/pytorch/facebookresearch/sam2/nuclio && docker logs -f nuclio-nuclio-pth-facebookresearch-sam2-large-gpu
```
- Deploy gpu function (tiny)
```
nuctl delete function -f pth-facebookresearch-sam2-tiny-gpu && ./serverless/deploy_func_config.sh serverless/pytorch/facebookresearch/sam2/nuclio/function-tiny-gpu.yaml && docker logs -f nuclio-nuclio-pth-facebookresearch-sam2-tiny-gpu
```



- nuclio dashboard: localhost:8070
- cvat ui: localhost:8080 / cvat.cancili.co
