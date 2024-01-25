import json
import os
import io
from src.globals import globals
import pandas as pd
import matplotlib.pyplot as plt
from fastapi.responses import StreamingResponse

def get_dates():
    result = []

    folder = globals["log_folder"]
    for folder_name in os.listdir(folder):
        result.append(folder_name)

    return result


def get_summary(date):
    result = []
    folder =  os.path.normpath(globals["log_folder"] + "/" + date)
    sub_folders = os.listdir(folder)
    save_folders_to_result(folder, sub_folders, result)
    return result


def get_summary_memory_graph(date):
    # Your existing code to get data and create DataFrame
    data = get_summary(date)
    memory = []
    for item in data:
        value = item["memory_diff"]
        memory.append({"memory": value})
    df = pd.DataFrame(memory)

    # Create the plot
    fig, ax = plt.subplots()
    df.plot(kind='line', ax=ax, title="Memory", ylabel="Memory", xlabel="Test")

    # Save the plot to a BytesIO object
    image_io = io.BytesIO()
    plt.savefig(image_io, format='png', bbox_inches='tight')
    image_io.seek(0)
    plt.close(fig)

    # Generator function to yield image data
    def iterfile():
        image_io.seek(0)  # Ensure you're at the start of the BytesIO object
        while True:
            chunk = image_io.read(4096)  # Read in 4KB chunks
            if not chunk:
                break
            yield chunk
        image_io.close()

    # Return the response
    return StreamingResponse(iterfile(), media_type="image/png")


def save_folders_to_result(folder, folders, result):
    for sub_folder in folders:
        file = os.path.normpath(folder + "/" + sub_folder + "/test.summary.json")

        # check if the file exists
        if os.path.isfile(file):
            with open(file, "r") as json_file:
                data = json.load(json_file)
                file_path = data["log"]
                parts = file_path.split('\\logs\\')
                data["log"] = parts[1].replace("test.log", "").replace("#", "_35_")
                result.append(data)

            json_file.close()

        else:
            new_folder = os.path.normpath(folder + "/" + sub_folder)
            sub_folders = os.listdir(new_folder)
            save_folders_to_result(new_folder, sub_folders, result)

