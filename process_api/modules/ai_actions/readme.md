# Notes

These notes pertains to running a llm on your local machine.

## Run in an environment

To run the llm, you need to install the requirements in the requirements.txt file.
To do so, you can create a virtual environment and install the requirements in it.
https://docs.python.org/3/library/venv.html

### Create a virtual environment

```bash
python -m venv myenv
```

### Activate the virtual environment

```bash
myenv\Scripts\activate.bat
```

## Installing the right torch.

To go the URL, look at the chart and select the exact command required to install your torch version.
https://pytorch.org/get-started/locally/

For example:
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117

You can check if you have GPU access by running

```python
import torch
print(torch.cuda.is_available())
```

The result should be True

## Cuda

You will need cuda installed on your machine.
You can download the toolkit from here: https://developer.nvidia.com/cuda-downloads
Make sure it is installed and the path is in your environment variables.

## Usage of LLM 
https://huggingface.co/upstage/Llama-2-70b-instruct-v2

## Cache
Downloaded models are cached on windows at
C:\Users\<yourname>\.cache\huggingface\hub