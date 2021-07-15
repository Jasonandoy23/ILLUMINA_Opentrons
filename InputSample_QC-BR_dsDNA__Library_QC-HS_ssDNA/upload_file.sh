HOST="root@169.254.72.169"
LOCAL_DIRECTORY="/home/ontlab/illumina/Opentrons/Protocols/InputSample_QC-BR_dsDNA__Library_QC-HS_ssDNA/24input.csv"
REMOTE_DIRECTORY="/data/user_files/*.csv"

ssh -i ot2_ssh_key_OT2CEP20210330B18 $HOST $REMOTE_DIRECTORY
scp -i ot2_ssh_key_OT2CEP20210330B18 $LOCAL_DIRECTORY $HOST:/data/user_files/input.csv
read -n 1 -r -s -p $'Press enter to continue...\n'