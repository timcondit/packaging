# for each package:
#   - create a subdirectory to store it
#   - download it to the subdirectory
#   - extract it into the subdirectory
#   - copy the MSI to a convenient central location

import os
import os.path
import shutil
import subprocess

DEBUG = False

# remote paths
BASE = r"\\Bigfoot\Releases\9\9.12\9.12.0000.60"
CD1 = os.path.join(BASE, "CD1")
CD2 = os.path.join(BASE, "CD2")
#CD3 = os.path.join(BASE, "CD3")
UTILS = os.path.join(BASE, CD2, "utils")

# local paths
CWD = os.getcwd()
GENERATED = os.path.join(CWD, "generated")
COMMON_STORE = os.path.join(CWD, "common_store")


packages = {
        # CD1
        "AgentSupport" : os.path.join(CD1, "AgentSupport_Setup.exe"),
        "PerformanceSuite" : os.path.join(CD1, "PerformanceSuite_Setup.exe"),
        # CD2
        "Analytics" : os.path.join(CD2, "Analytics_Setup.exe"),
        "CentricityWebApplications" : os.path.join(CD2, "CentricityWebApplications_Setup.exe"),
        "Centricity" : os.path.join(CD2, "Centricity_Setup.exe"),
        "Server" : os.path.join(CD2, "Server_Setup.exe"),
        "SpeechProcessingClient" : os.path.join(CD2, "SpeechProcessingClient_Setup.exe"),
        "SpeechServerService" : os.path.join(CD2, "SpeechServerService_Setup.exe"),
        "WMWrapperService" : os.path.join(CD2, "WMWrapperService_Setup.exe"),
        # CD2/utils
        "ADIT" : os.path.join(UTILS, "ADIT_Setup.exe"),
        "AGMS" : os.path.join(UTILS, "AGMS_Setup.exe"),
        "DADI" : os.path.join(UTILS, "DADI_Setup.exe"),
        "DBMigration" : os.path.join(UTILS, "DBMigration_Setup.exe"),
        "EvaluationConsistencyCheck" : os.path.join(UTILS, "EvaluationConsistencyCheck_Setup.exe"),
       }


for dir in GENERATED, COMMON_STORE:
    if os.path.exists(dir):
        print("warning: found directory %s" % dir)
    else:
        os.mkdir(dir)

for pkg in packages:
    setup_file = os.path.basename(packages[pkg])
    remote_file = packages[pkg]
    local_path = os.path.join(GENERATED, pkg)
    local_setup = os.path.join(local_path, setup_file)
    local_msi = local_setup.replace("_Setup.exe", ".msi", 1)
    print("## processing %s" % setup_file)
    if DEBUG:
        print("remote_file: %s" % remote_file)
        print("local_path: %s" % local_path)
        print("local_setup: %s" % local_setup)
        print("local_msi: %s" % local_msi)
    if not os.path.exists(local_path):
        os.makedirs(local_path)
        shutil.copy(remote_file, local_setup)
    else:
        print("warning: file already exists: %s" % local_setup)
    cmd = local_setup + " /extract"
    returncode = subprocess.check_call(cmd)
    if returncode != 0:
        # TODO return the returncode?
        print("possible error: %s" % cmd)
    else:
        try:
            shutil.copy(local_msi, COMMON_STORE)
#            shutil.move(local_msi, COMMON_STORE)
#            shutil.rmtree(local_path)
        except:
            print("something broke doing the [re]move!")

# TODO make this a command-line option.  I may want to keep the files around.
#
# Not a great idea to delete COMMON_STORE until after I've done the installer
# work.  But os.rmdir() won't delete a directory with contents anyway.
#for dir in GENERATED, COMMON_STORE:
#for dir in GENERATED,: #COMMON_STORE:
#    try:
#        os.rmdir(dir)
#    except OSError:
#        print("warning: '%s' not empty, cannot be removed" % dir)

