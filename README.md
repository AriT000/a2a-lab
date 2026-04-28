# A2A-lab Setup:

## 1.
- open powershell or wsl
- run `git clone https://github.com/AriT000/a2a-lab.git`
- run `python -m venv .venv`
- run `.\.venv\Scripts\activate.bat` for powershell or `.venv/scripts/activate` for wsl

## 2.
- pip install -r server/requirements.txt
- pip install httpx
- pip install "google-cloud-aiplatform[agent_engines]"

## 3.
- install gcloud CLI in wsl or powershell
- Run `gcloud auth application-default login`
- run `gcloud config set project pe4680`

## 4.
- start docker
- uvicorn server.main:app --host 0.0.0.0 --port 8000

## 5.
- set URL in client/demo.py: `agent_url = "http://localhost:8000"`
- run `python -m client.demo`

## 6.
- run `./cloud/deploy_cloud_run.sh`
- service url: https://echo-a2a-agent-741297514794.us-central1.run.app
- run `python -m client.demo`
- 

# 7.
- run `gsutil mb -l us-central1 gs://pe4680-a2a-staging`
- run `python cloud/deploy_agent_engine.py`
- In cloud/test_agent_engine.py, set engine resource
- run `python cloud/test_agent_engine.py`

This is the cloud run url: https://echo-a2a-agent-ht4cbsfpxq-uc.a.run.app
