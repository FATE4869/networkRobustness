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

def extractVideosFromDataset(dataset, split, download=False):
    if not os.path.exists(f'../../dataset/{dataset}/{split}_videos'):
        os.mkdir(f'../../dataset/{dataset}/{split}_videos')
    classList = []
    fileNameList = []
    with open(f'../../dataset/{dataset}/{split}.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            # print(f'{i}')
            if row['label'] not in classList:
                classList.append(row['label'])

            if i < 5:
                fileName = f"{i}_{row['label']}_{row['youtube_id']}"
                print(fileName)
                fileNameList.append(fileName)
                cmd = f"youtube-dl -4 -o '../../dataset/{dataset}/{split}_videos/{fileName}.%(ext)s' http://www.youtube.com/watch?v={row['youtube_id']}"
                # print(cmd)
                if download:
                    os.system(cmd)
                # break
            # elif i >= 170:
            else:
                break
        # classList.sort()
        # files = os.listdir(f'../../dataset/{dataset}/{split}_videos/')
        # downloadValidationCheck(fileNameList, files)

        return classList

# Extracts the meta-information from given dataset, such as class_list and url_list
def extractMetaInfo(dataset, split='train'):
    classes = []
    metaInfo = {}
    with open(f'../../dataset/{dataset}/{split}.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            # print(f'{i}')
            if row['label'] not in classes:
                classes.append(row['label'])
            metaInfo[row['youtube_id']] = {'label': row['label'], 'time_start': row['time_start'],
                                           'end_time': row['time_end'],
                                           'duration': int(row['time_end']) - int(row['time_start'])}
    return metaInfo

# check common classes in classList1 and classList2
def getCommonClasses(dataset1, dataset2, split="train", exist=True):
    commonClasses = []
    if exist:
        with open("commonClasses.txt", "r") as f:
            for line in f:
                commonClasses.append(line.strip())
    else:
        class_list_1, label_url_List_1 = extractMetaInfo(dataset1, split)
        print(len(class_list_1))

        class_list_2, label_url_List_2 = extractMetaInfo(dataset2, split)
        print(len(class_list_2))

        for class1 in class_list_1:
            if class1 in class_list_2:
                commonClasses.append(class1)
    return commonClasses

def extractUrls(dataset, split='train', classes=None):
    urls = {}
    with open(f'../../dataset/{dataset}/{split}.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            if row['label'] in classes:
                urls[row['youtube_id']] = row['label']
                # label_url = row['label'] + '_' +
                # label_url_List.append(label_url)
    return urls

# iterate through urls1 and check if it is in urls2, if so put this url1 and corresponding label1
# to common_urls and common_labels list, otherwise put them into different_urls and different_labels list
def get_common_and_different_urls_and_labels(metaInfo1, metaInfo2):
    common = {}
    different = {}
    for i, key1 in enumerate(metaInfo1.keys()):
        if key1 in metaInfo2.keys():
            common[key1] = metaInfo1[key1]
        else:
            different[key1] = metaInfo1[key1]
    return common, different

def main():


    dataset1 = 'kinetics400'
    dataset2 = 'kinetics600'

    metaInfo1 = extractMetaInfo(dataset1)
    # print(len(classes1))
    # print(len(labels1), len(urls1), len(start_times1), len(end_times1), durations1)

    metaInfo2 = extractMetaInfo(dataset2)
    # print(len(classes2))
    # print(len(labels2), len(urls2), len(start_times2), len(end_times2), len(durations2))

    # exist = True
    # commonClasses = getCommonClasses(dataset1, dataset2, exist)
    # # print(commonClasses)

    common, different = get_common_and_different_urls_and_labels(metaInfo1, metaInfo2)
    # print(common, different)
    with open("dataset/common.json", "w") as outfile:
        json.dump(common, outfile, indent=4)
    with open("dataset/different.json", "w") as outfile:
        json.dump(different, outfile, indent=4)

if __name__ == "__main__":
    main()
