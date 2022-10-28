# BollWorm-Zindi
Solution to the zindi challenge involving detecting bollworms in images

## setup
- Install anaconda or miniconda
- activate the bollworm-zindi environment by running `source activate-env`

## usage
- The script `main` is the entry point from which all other scripts are executed. To know the possible scripts to execute simply run `./main`
### training
- To train, execute the script `train.py` from yolov7. This can be achieved by running `./main train.py`. To know the possible options and flags used in the `train.py` script, run `./main train.py -h`. A sample command for training is 

```
./main.py train --workers 2 --device 0 --batch-size 4 --data ../data/config.yaml --img 640 640 --weights yolov7_training.pt --cfg cfg/training/yolov7.yaml --name yolov7-custom --hyp data/hyp.scratch.custom.yaml
```

### detecting
- To detect objects in a source image, execute the script `detect.py` from yolov7. To know the possible options and flags used, run `./main detect.py`. A sample detection command:
```
./main.py detect --weights runs/train/yolov7-custom/weights/best.pt  --conf 0.25 --img-size 640 --source data/images/bollworm.jpg
```

### data
- To prepare the bollworm data for training and inference, first download all the data files from zindi and move them to the data folder. Run `./main data-prep`

### submission
- To prepare the submission on the test data, run `./main submission.py`. To check the performance on the train or val data in terms of MAE run `./main submission.py --train-mae` or `./main submission.py --val-mae`