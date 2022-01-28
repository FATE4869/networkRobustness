import os

def main():
    cmd = '~/Yang/projects/openpose/build/examples/openpose/openpose.bin --video  ~/Yang/projects/openpose/examples/media/video.avi --write_json ~/Yang/projects/networksRobustness/output_json/'
    os.system(cmd)
if __name__ == '__main__':
    main()