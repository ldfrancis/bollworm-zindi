#!/usr/bin/env python
from helpers import download
import argparse

if __name__ == "__main__":
    arg = argparse.ArgumentParser()
    arg.add_argument(
        "--download",
        type=str,
        help="name of checkpoint to download from yolov7"
    )
    arg.add_argument(
        "--clean", 
        type=str, 
        default="", 
        help=(
            "path of yolov7 checkpoint to clean. Cleaning involves removing values for"
            " certain keys (like wandb_id) in the checkpoint"
        )
    )
    args = arg.parse_args()
    
    # download checkpoint
    if args.download:
        chkpt = arg.download
        url = (
            "https://github.com/WongKinYiu/yolov7"
            f"/releases/download/v0.1/{chkpt}"
        )
        if not (yolov7_path/chkpt).exists():
            download(url, chkpt)
        else:
            print(f"File {yolov7_path/chkpt} already exists!")

    # clean checkpoint
    elif args.clean:
        chkpt = command[2]
        state_dict = torch.load(chkpt)
        state_dict["wandb_id"] = None
        state_dict["optimizer"] = None
        state_dict["updates"] = None
        state_dict["ema"] = None
        state_dict["training_results"] = None
        torch.save(state_dict, chkpt)
        print(f"Updated checkpoint {chkpt}")
        