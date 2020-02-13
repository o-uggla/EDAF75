# EDAF75
Database Technology

## Run jupyter remote
### SSH to remote an run:
jupyter notebook --no-browser --port=8080
### Setup tunnel with:
ssh -N -L 8080:localhost:8080 login@remote
### See tokens on remote with:
jupyter notebook list
