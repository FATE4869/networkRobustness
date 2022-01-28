import csv
import json
import os
from functools import partial
from multiprocessing.pool import Pool
import cv2
import youtube_dl
import pickle
# check if videos are downloaded successfully, report indices of which fileNames were not downloaded
# input:
# fileNameList: a list of fileName that will be check whether they exist among files
# files: source of files that fileName will be checked on
def downloadValidationCheck(fileNameList, files):
    # fileNameList.sort()
    failureIndices = []
    for i, fileName in enumerate(fileNameList):
        a = fileName.split('_')
        index, label, url = a[0], a[1], a[2]
        # print(index, label, url)
        Exist = False
        for file in files:
            if url in file:
                Exist = True
                b = file.split('_')
                ext = b[-1]
                print(ext)
                os.rename(f'../../dataset/kinetics700_2020/train_videos/{file}', f'../../dataset/kinetics700_2020/train_videos/{index}_{label}')
                break
        if not Exist:
            failureIndices.append(i)
            # print(i, fileName)

    print(failureIndices)
    print(f'{len(failureIndices)} / {len(fileNameList)}')

def extractVideosFromDataset(dataset, download=False):
    for i, key in enumerate(dataset.keys()):
        print("current index: ", i)
        # if i < -1:
        if i > 47539:
        # print(key)
        # save the output of this command to output.txt
            cmd = f"youtube-dl -4 -g http://www.youtube.com/watch?v={key} 1> output.txt"
            os.system(cmd)
        #
        #     # read output.txt
            file = open("output.txt")
            line = file.read().split('\n')

            line = line[0]
            file.close()

            print(line)
            # start_time = dataset[key]['time_start']
            # duration = dataset[key]['duration']
            # start_time = int(start_time)
            # hours = start_time // 3600
            # minutes = (start_time - 3600 * hours) // 60
            # seconds = (start_time - 3600 * hours - 60 * minutes)
            # cmd = f'ffmpeg -ss {hours}:{minutes}:{seconds}.00 -i \"{line}\" -t 00:00:{duration}.0 -c:v copy -c:a copy ../../dataset/kinetics600/dataset/different_videos_ctn/___{i}___{key}.mp4'
            # print(cmd)
            # os.system(cmd)
            break

def main():
    # with open('../../dataset/kinetics600/dataset/different.json', 'r') as f:
    #     dataset = json.load(f)
    # # print(dataset)
    # download = False
    # extractVideosFromDataset(dataset, download)
    with open('../../dataset/kinetics600/validate.json', 'r') as f:
        validate = json.load(f)
    print(validate)

if __name__ == "__main__":
    main()
