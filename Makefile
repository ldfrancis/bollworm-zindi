conda-update:
	conda env update --prune -f environment.yaml

pip-update:
	pip install -U pip --quiet
	pip install -r requirements/dev.txt

yolov7-clone:
	git clone https://github.com/WongKinYiu/yolov7.git

yolov7-clean:
	rm -rf yolov7

bollworm-dummy:


