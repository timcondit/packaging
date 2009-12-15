# for each package:
#   - create a subdirectory to store it
#   - download it to the subdirectory
#   - extract it into the subdirectory
#   - copy the MSI to a convenient central location

import os
import os.path
import shutil
import subprocess

# remote paths
R_BASE = r"\\Bigfoot\Releases\9\9.12\9.12.0000.60"
R_CD1 = os.path.join(R_BASE, "CD1")
R_CD2 = os.path.join(R_BASE, "CD2")
#R_CD3 = os.path.join(R_BASE, "CD3")
R_UTILS = os.path.join(R_BASE, R_CD2, "utils")

# local paths
CWD = os.getcwd()
GENERATED = os.path.join(CWD, "generated")
COMMON_STORE = os.path.join(CWD, "common_store")


packages = {
        # CD1
        "AgentSupport" : [
            os.path.join(R_CD1, "AgentSupport_Setup.exe"),
            os.path.join(GENERATED, "AgentSupport", "AgentSupport_Setup.exe"),
            ],

        "PerformanceSuite" : [
            os.path.join(R_CD1, "PerformanceSuite_Setup.exe"),
            os.path.join(GENERATED, "PerformanceSuite", "PerformanceSuite_Setup.exe"),
            ],

        # CD2
        "Analytics" : [
            os.path.join(R_CD2, "Analytics_Setup.exe"),
            os.path.join(GENERATED, "Analytics", "Analytics_Setup.exe"),
            ],

        "CentricityWebApplications" : [
            os.path.join(R_CD2, "CentricityWebApplications_Setup.exe"),
            os.path.join(GENERATED, "CentricityWebApplications", "CentricityWebApplications_Setup.exe"),
            ],

        "Centricity" : [
            os.path.join(R_CD2, "Centricity_Setup.exe"),
            os.path.join(GENERATED, "Centricity", "Centricity_Setup.exe"),
            ],

        "Server" : [
            os.path.join(R_CD2, "Server_Setup.exe"),
            os.path.join(GENERATED, "Server", "Server_Setup.exe"),
            ],

        "SpeechProcessingClient" : [
            os.path.join(R_CD2, "SpeechProcessingClient_Setup.exe"),
            os.path.join(GENERATED, "SpeechProcessingClient", "SpeechProcessingClient_Setup.exe"),
            ],

        "SpeechServerService" : [
            os.path.join(R_CD2, "SpeechServerService_Setup.exe"),
            os.path.join(GENERATED, "SpeechServerService", "SpeechServerService_Setup.exe"),
            ],

        "WMWrapperService" : [
            os.path.join(R_CD2, "WMWrapperService_Setup.exe"),
            os.path.join(GENERATED, "WMWrapperService", "WMWrapperService_Setup.exe"),
            ],

        # CD2/utils
        "ADIT" : [
            os.path.join(R_UTILS, "ADIT_Setup.exe"),
            os.path.join(GENERATED, "ADIT", "ADIT_Setup.exe"),
            ],

        "AGMS" : [
            os.path.join(R_UTILS, "AGMS_Setup.exe"),
            os.path.join(GENERATED, "AGMS", "AGMS_Setup.exe"),
            ],

        "DADI" : [
            os.path.join(R_UTILS, "DADI_Setup.exe"),
            os.path.join(GENERATED, "DADI", "DADI_Setup.exe"),
            ],

        "DBMigration" : [
            os.path.join(R_UTILS, "DBMigration_Setup.exe"),
            os.path.join(GENERATED, "DBMigration", "DBMigration_Setup.exe"),
            ],

        "EvaluationConsistencyCheck" : [
            os.path.join(R_UTILS, "EvaluationConsistencyCheck_Setup.exe"),
            os.path.join(GENERATED, "EvaluationConsistencyCheck", "EvaluationConsistencyCheck_Setup.exe"),
            ],
        }

if not os.path.exists(GENERATED):
    os.mkdir(GENERATED)

for paths in packages.values():
    if not os.path.exists(paths[1]):
        os.makedirs(os.path.dirname(paths[1]))
        shutil.copy(paths[0], paths[1])
    else:
        print("error?  File already exists: %s" % paths[1])

    cmd = paths[1] + " /extract"
    returncode = subprocess.check_call(cmd)
    if returncode != 0:
        print("possible error: %s" % cmd)


#if not os.path.exists(COMMON_STORE):
#    os.mkdir(COMMON_STORE)
#
#for pkg in 
#
#    self.






#setup_files = [
#    r"\\Bigfoot\Releases\9\9.12\9.12.0000.60\CD1\AgentSupport_Setup.exe",
#    r"\\Bigfoot\Releases\9\9.12\9.12.0000.60\CD1\PerformanceSuite_Setup.exe",
#    r"\\Bigfoot\Releases\9\9.12\9.12.0000.60\CD2\Analytics_Setup.exe",
#    r"\\Bigfoot\Releases\9\9.12\9.12.0000.60\CD2\CentricityWebApplications_Setup.exe",
#    r"\\Bigfoot\Releases\9\9.12\9.12.0000.60\CD2\Centricity_Setup.exe",
#    r"\\Bigfoot\Releases\9\9.12\9.12.0000.60\CD2\Server_Setup.exe",
#    r"\\Bigfoot\Releases\9\9.12\9.12.0000.60\CD2\SpeechProcessingClient_Setup.exe",
#    r"\\Bigfoot\Releases\9\9.12\9.12.0000.60\CD2\SpeechServerService_Setup.exe",
#    r"\\Bigfoot\Releases\9\9.12\9.12.0000.60\CD2\WMWrapperService_Setup.exe",
#    r"\\Bigfoot\Releases\9\9.12\9.12.0000.60\CD2\utils\ADIT_Setup.exe",
#    r"\\Bigfoot\Releases\9\9.12\9.12.0000.60\CD2\utils\AGMS_Setup.exe",
#    r"\\Bigfoot\Releases\9\9.12\9.12.0000.60\CD2\utils\DADI_Setup.exe",
#    r"\\Bigfoot\Releases\9\9.12\9.12.0000.60\CD2\utils\DBMigration_Setup.exe",
#    r"\\Bigfoot\Releases\9\9.12\9.12.0000.60\CD2\utils\EvaluationConsistencyCheck_Setup.exe",
#    ]

