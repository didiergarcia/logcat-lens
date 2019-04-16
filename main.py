import subprocess
import os

# hug = os.system("adb logcat -v time")


proc = subprocess.Popen(["adb", "logcat", "-v", "threadtime"], stdout=subprocess.PIPE)


# subprocess.run(["adb", "logcat", "-v", "time"], stdout=subprocess.PIPE)

# Set to keep track of all seen tags.
tag_set = set()
tag_color = dict()
color_index = 0

def getnextcolor():

    # Colors (Need to double check these with different OS terms)
    colors = {
        0: '\033[0;30m',
        1: '\033[0;31m',
        2: '\033[0;32m',
        3: '\033[0;33m',
        4: '\033[0;34m',
        5: '\033[0;35m',
        6: '\033[0;36m',
        7: '\033[0;37m',
        8: '\033[0;38m',
        9: '\033[0;39m',

        10: '\033[1;30m',
        11: '\033[1;31m',
        12: '\033[1;32m',
        13: '\033[1;33m',
        14: '\033[1;34m',
        15: '\033[1;35m',
        16: '\033[1;36m',
        17: '\033[1;37m',
        18: '\033[1;38m',
        19: '\033[1;39m',

        20: '\033[0;60m',
        21: '\033[0;61m',
        22: '\033[0;62m',
        23: '\033[0;63m',
        24: '\033[0;64m',
        25: '\033[0;65m',
        26: '\033[0;66m',
        27: '\033[0;67m',
        28: '\033[0;68m',
        29: '\033[0;69m',

        30: '\033[1;60m',
        31: '\033[1;61m',
        32: '\033[1;62m',
        33: '\033[1;63m',
        34: '\033[1;64m',
        35: '\033[1;65m',
        36: '\033[1;66m',
        37: '\033[1;67m',
        38: '\033[1;68m',
        39: '\033[1;69m',
    }

    global color_index
    color = colors.get(color_index % len(colors))
    color_index += 1

    return color

def gettagcolor( tag ):

    assigned_color = tag_color.get(tag)

    if not assigned_color:
        color_start = getnextcolor()
        tag_color[tag] = color_start
        assigned_color = color_start

    return assigned_color

def getendcolor():

    return '\033[0m'


def main():
    while True:
        out = proc.stdout.readline()
        if out == '' and proc.poll() != None:
            break;

        str_line = out.decode('UTF-8')

        if not str_line.startswith('----'):
            split_str = str_line.split()

            date = split_str[0]
            time = split_str[1]
            pid = split_str[2]
            tid = split_str[3]
            level = split_str[4]

            # Join the rest of the message
            split_msg = (' '.join(split_str[5:])).split(':')
            tag = split_msg[0]
            msg = ':'.join(split_msg[1:])



            tag_set.add(tag)

            start_color  = gettagcolor(tag)

            # print('TAGS: {}'.format(len(tag_set)))

            if start_color:
                print(start_color, date, time, pid, tid, level, tag + ':', sep='\t', end='')
                print(msg, getendcolor())
            else:
                print(date, time, pid, tid, level, tag + ':', sep='\t', end='')
                print(msg,)

        else:
            print(str_line, end='')



        #print(str_line, end='')


# Main start
if __name__ == '__main__':
    main()