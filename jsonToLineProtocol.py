import argparse
import json
import os
import sys
import datetime

RET_OK=0
RET_CONF_FAILURE=1
RET_EXEC_FAILURE=2

epoch = datetime.datetime(1970, 1, 1)

def buildTimestamp(baseDate, rawDate):
    d = baseDate.replace(hour=int(rawDate[:2]), minute=int(rawDate[3:]))
    return int((d - epoch).total_seconds()) * 1000000000

def buildLine(baseDate, rawDate, amount, location):
    return "linky,location={} conso={} {}".format(location, amount, buildTimestamp(baseDate, rawDate))    

def convert(sourcePath, location):
    try: 
        with open(sourcePath) as source:
            data = json.load(source)
            yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
            yesterday.replace(second=0, microsecond=0)
            for curHour in data['hourly']:
                print("{}".format(buildLine(yesterday, curHour['time'], curHour['conso'], location)))
    except IOError as e:
        print("Error when opening source file: {}", e)
        return RET_EXEC_FAILURE
    except json.JSONDecodeError as e:
        print("Error when decoding source file: {}", e)
        return RET_EXEC_FAILURE
    finally:
        source.close()
    return RET_OK

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source', required=True, help='Source file')
parser.add_argument('-l', '--location', required=True, help='Location identifier')
args = parser.parse_args()

if not os.path.exists(args.source):
    print("Source '{}' does not exist".format(args.source))
    sys.exit(RET_CONF_FAILURE)

ret=convert(args.source, args.location)
sys.exit(ret)