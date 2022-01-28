import csv
import json
import os
from functools import partial
from multiprocessing.pool import Pool
import cv2
import youtube_dl

# check if videos are downloaded successfully, report indices of which fileNames were not downloaded
# input:
# fileNameList: a list of fileName that will be check whether they exist among files
# files: source of files that fileName will be checked on
def downloadValidationCheck(fileNameList, files):
    # fileNameList.sort()
    failureIndices = []
    for i, fileName in enumerate(fileNameList):
        Exist = False
        for file in files:
            if fileName in file:
                Exist = True
                break
        if not Exist:
            failureIndices.append(i)
            print(i, fileName)
    print(failureIndices)
    print(f'{len(failureIndices)} / {len(fileNameList)}')

def extractVideosFromDataset(dataset, split):
    if not os.path.exists(f'../../dataset/{dataset}/{split}_videos'):
        os.mkdir(f'../../dataset/{dataset}/{split}_videos')
    classList = []
    fileNameList = []
    with open(f'../../dataset/{dataset}/{split}.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            print(f'{i}')
            if row['label'] not in classList:
                classList.append(row['label'])

            if i < 170:
                fileName = f"{i}_{row['label']}_{row['youtube_id']}"
                print(fileName)
                fileNameList.append(fileName)
                cmd = f"youtube-dl -4 -o '../../dataset/{dataset}/{split}_videos/{fileName}.%(ext)s' http://www.youtube.com/watch?v={row['youtube_id']}"
                # print(cmd)
                # os.system(cmd)
                # break
            elif i >= 170:
                break
        classList.sort()
        files = os.listdir(f'../../dataset/{dataset}/{split}_videos/')
        downloadValidationCheck(fileNameList, files)

        return classList
def main():
    dataset = 'kinetics700_2020'
    # dataset = 'kinetics700'
    split = 'train'
    classList700 = extractVideosFromDataset(dataset, split)


if __name__ == "__main__":
    main()
