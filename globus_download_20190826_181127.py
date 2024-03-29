import sys
import argparse
import os

from random import SystemRandom
from uuid import uuid4

# Revised version by Matt Pritchard, CEDA/STFC to work with globus-cli

def listEndpoints(gendpointDict):

    endNames = gendpointDict.keys()
    print ("Endpoints involved:")
    for thisEndName in endNames:
        print (thisEndName)

def arguments(argv):

    parser = argparse.ArgumentParser(description = \
        '''To use this script, you must have the Globus Command Line Interface
        tools installed locally (see https://docs.globus.org/cli/)
        The host where you install these tools does
        NOT need to be one of the endpoints in the transfer.
        This script makes use of the Globus CLI 'transfer' command.
        You need to ensure the endpoints involved are activated, see "Endpoints
        to be activated" in output (use "globus endpoint activate")
        By default, the transfer command will:
        - verify the checksum of the transfer
        - encrypt the transfer
        - and delete any fies at the user endpoint with the same name.'''
            )
    parser.add_argument('-e', '--user-endpoint', type=str, help='endpoint you wish to download files to', required=True)
    parser.add_argument('-u', '--username', type=str, help='your Globus username', required=True)
    parser.add_argument('-p', '--path', type=str, help='the path on your endpoint where you want files to be downloaded to', default='/~/')
    parser.add_argument('-l', '--list-endpoints', help='List the endpoints to be activated and exit (no transfer attempted)', action='store_true')
    parser._optionals.title = 'required and optional arguments'
    args = parser.parse_args()

    username = args.username
    uendpoint = args.user_endpoint
    upath = args.path
    listonly = args.list_endpoints

    if '/' in uendpoint:
        print ("Do not include the download path in the endpoint name, please use the -p option")
        sys.exit()
    if '#' in upath:
        print ("The '#' character is invalid in your path, please re-enter")
        sys.exit()
    if upath[0] != '/' and upath != '/~/':
        upath = '/' + upath

    return (uendpoint, username, upath, listonly)

def getFiles(gendpointDict, uendpoint, username, upath):

    label = str(uuid4())

    endNames = gendpointDict.keys()

    for thisEndName in endNames:

        fileList = gendpointDict[thisEndName]

        cryptogen = SystemRandom()
        transferFile = '/tmp/transferList_' + thisEndName + '_' + str(cryptogen.randint(1,9999)) + '.txt'
        file = open(transferFile, 'w')

        for thisFile in fileList:

            basename = os.path.basename(thisFile)

            if upath[-1] != '/':
                basename = '/' + basename

            remote = thisFile
            local = upath + basename

            file.write(remote + ' ' + local + '\n')

        file.close()

        os.system("globus transfer "+thisEndName+" "+uendpoint+" --batch --label \"CLI Batch\" < "+transferFile)

        os.remove(transferFile)

    return

if __name__ == '__main__':

    gendpointDict = {u'ee3aa1a0-7e4c-11e6-afc4-22000b92c261': [u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/huss/huss_day_HadGEM2-ES_rcp45_r4i1p1_20051201-20151130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/huss/huss_day_HadGEM2-ES_rcp45_r4i1p1_20151201-20251130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/huss/huss_day_HadGEM2-ES_rcp45_r4i1p1_20251201-20351130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/huss/huss_day_HadGEM2-ES_rcp45_r4i1p1_20351201-20451130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/huss/huss_day_HadGEM2-ES_rcp45_r4i1p1_20451201-20551130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/huss/huss_day_HadGEM2-ES_rcp45_r4i1p1_20551201-20651130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/huss/huss_day_HadGEM2-ES_rcp45_r4i1p1_20651201-20751130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/huss/huss_day_HadGEM2-ES_rcp45_r4i1p1_20751201-20851130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/huss/huss_day_HadGEM2-ES_rcp45_r4i1p1_20851201-20951130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/huss/huss_day_HadGEM2-ES_rcp45_r4i1p1_20951201-21001130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/huss/huss_day_HadGEM2-ES_rcp45_r4i1p1_21001201-21001230.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/pr/pr_day_HadGEM2-ES_rcp45_r4i1p1_20051201-20151130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/pr/pr_day_HadGEM2-ES_rcp45_r4i1p1_20151201-20251130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/pr/pr_day_HadGEM2-ES_rcp45_r4i1p1_20251201-20351130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/pr/pr_day_HadGEM2-ES_rcp45_r4i1p1_20351201-20451130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/pr/pr_day_HadGEM2-ES_rcp45_r4i1p1_20451201-20551130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/pr/pr_day_HadGEM2-ES_rcp45_r4i1p1_20551201-20651130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/pr/pr_day_HadGEM2-ES_rcp45_r4i1p1_20651201-20751130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/pr/pr_day_HadGEM2-ES_rcp45_r4i1p1_20751201-20851130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/pr/pr_day_HadGEM2-ES_rcp45_r4i1p1_20851201-20951130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/pr/pr_day_HadGEM2-ES_rcp45_r4i1p1_20951201-21001130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/pr/pr_day_HadGEM2-ES_rcp45_r4i1p1_21001201-21001230.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/psl/psl_day_HadGEM2-ES_rcp45_r4i1p1_20051201-20151130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/psl/psl_day_HadGEM2-ES_rcp45_r4i1p1_20151201-20251130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/psl/psl_day_HadGEM2-ES_rcp45_r4i1p1_20251201-20351130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/psl/psl_day_HadGEM2-ES_rcp45_r4i1p1_20351201-20451130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/psl/psl_day_HadGEM2-ES_rcp45_r4i1p1_20451201-20551130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/psl/psl_day_HadGEM2-ES_rcp45_r4i1p1_20551201-20651130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/psl/psl_day_HadGEM2-ES_rcp45_r4i1p1_20651201-20751130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/psl/psl_day_HadGEM2-ES_rcp45_r4i1p1_20751201-20851130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/psl/psl_day_HadGEM2-ES_rcp45_r4i1p1_20851201-20951130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/psl/psl_day_HadGEM2-ES_rcp45_r4i1p1_20951201-21001130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/psl/psl_day_HadGEM2-ES_rcp45_r4i1p1_21001201-21001230.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/sfcWind/sfcWind_day_HadGEM2-ES_rcp45_r4i1p1_20051201-20151130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/sfcWind/sfcWind_day_HadGEM2-ES_rcp45_r4i1p1_20151201-20251130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/sfcWind/sfcWind_day_HadGEM2-ES_rcp45_r4i1p1_20251201-20351130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/sfcWind/sfcWind_day_HadGEM2-ES_rcp45_r4i1p1_20351201-20451130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/sfcWind/sfcWind_day_HadGEM2-ES_rcp45_r4i1p1_20451201-20551130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/sfcWind/sfcWind_day_HadGEM2-ES_rcp45_r4i1p1_20551201-20651130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/sfcWind/sfcWind_day_HadGEM2-ES_rcp45_r4i1p1_20651201-20751130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/sfcWind/sfcWind_day_HadGEM2-ES_rcp45_r4i1p1_20751201-20851130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/sfcWind/sfcWind_day_HadGEM2-ES_rcp45_r4i1p1_20851201-20951130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/sfcWind/sfcWind_day_HadGEM2-ES_rcp45_r4i1p1_20951201-21001130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/sfcWind/sfcWind_day_HadGEM2-ES_rcp45_r4i1p1_21001201-21001230.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tas/tas_day_HadGEM2-ES_rcp45_r4i1p1_20051201-20151130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tas/tas_day_HadGEM2-ES_rcp45_r4i1p1_20151201-20251130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tas/tas_day_HadGEM2-ES_rcp45_r4i1p1_20251201-20351130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tas/tas_day_HadGEM2-ES_rcp45_r4i1p1_20351201-20451130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tas/tas_day_HadGEM2-ES_rcp45_r4i1p1_20451201-20551130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tas/tas_day_HadGEM2-ES_rcp45_r4i1p1_20551201-20651130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tas/tas_day_HadGEM2-ES_rcp45_r4i1p1_20651201-20751130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tas/tas_day_HadGEM2-ES_rcp45_r4i1p1_20751201-20851130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tas/tas_day_HadGEM2-ES_rcp45_r4i1p1_20851201-20951130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tas/tas_day_HadGEM2-ES_rcp45_r4i1p1_20951201-21001130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tas/tas_day_HadGEM2-ES_rcp45_r4i1p1_21001201-21001230.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tasmax/tasmax_day_HadGEM2-ES_rcp45_r4i1p1_20051201-20151130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tasmax/tasmax_day_HadGEM2-ES_rcp45_r4i1p1_20151201-20251130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tasmax/tasmax_day_HadGEM2-ES_rcp45_r4i1p1_20251201-20351130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tasmax/tasmax_day_HadGEM2-ES_rcp45_r4i1p1_20351201-20451130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tasmax/tasmax_day_HadGEM2-ES_rcp45_r4i1p1_20451201-20551130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tasmax/tasmax_day_HadGEM2-ES_rcp45_r4i1p1_20551201-20651130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tasmax/tasmax_day_HadGEM2-ES_rcp45_r4i1p1_20651201-20751130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tasmax/tasmax_day_HadGEM2-ES_rcp45_r4i1p1_20751201-20851130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tasmax/tasmax_day_HadGEM2-ES_rcp45_r4i1p1_20851201-20951130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tasmax/tasmax_day_HadGEM2-ES_rcp45_r4i1p1_20951201-21001130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tasmax/tasmax_day_HadGEM2-ES_rcp45_r4i1p1_21001201-21001230.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tasmin/tasmin_day_HadGEM2-ES_rcp45_r4i1p1_20051201-20151130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tasmin/tasmin_day_HadGEM2-ES_rcp45_r4i1p1_20151201-20251130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tasmin/tasmin_day_HadGEM2-ES_rcp45_r4i1p1_20251201-20351130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tasmin/tasmin_day_HadGEM2-ES_rcp45_r4i1p1_20351201-20451130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tasmin/tasmin_day_HadGEM2-ES_rcp45_r4i1p1_20451201-20551130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tasmin/tasmin_day_HadGEM2-ES_rcp45_r4i1p1_20551201-20651130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tasmin/tasmin_day_HadGEM2-ES_rcp45_r4i1p1_20651201-20751130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tasmin/tasmin_day_HadGEM2-ES_rcp45_r4i1p1_20751201-20851130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tasmin/tasmin_day_HadGEM2-ES_rcp45_r4i1p1_20851201-20951130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tasmin/tasmin_day_HadGEM2-ES_rcp45_r4i1p1_20951201-21001130.nc', u'/esg_dataroot/cmip5/output1/MOHC/HadGEM2-ES/rcp45/day/atmos/day/r4i1p1/v20111205/tasmin/tasmin_day_HadGEM2-ES_rcp45_r4i1p1_21001201-21001230.nc']}
    jiayusun, sjy, C:\Users\sjy\Downloads\globus_download_20190826_181127.py, listonly = arguments(sys.argv)
    if (listonly):
        listEndpoints(gendpointDict)
    else:
        getFiles(gendpointDict, jiayusun, sjy, C:\Users\sjy\Downloads\globus_download_20190826_181127.py)
