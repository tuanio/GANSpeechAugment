import os
import glob
import argparse
import subprocess
from tqdm.auto import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--timit-path')
parser.add_argument('--target-path')
parser.add_argument('--sample-rate', default='16000', type=str)

args = parser.parse_args()

sample_rate = args.sample_rate

test_spklist = [
    "MDAB0",
    "MWBT0",
    "FELC0",
    "MTAS1",
    "MWEW0",
    "FPAS0",
    "MJMP0",
    "MLNT0",
    "FPKT0",
    "MLLL0",
    "MTLS0",
    "FJLM0",
    "MBPM0",
    "MKLT0",
    "FNLP0",
    "MCMJ0",
    "MJDH0",
    "FMGD0",
    "MGRT0",
    "MNJM0",
    "FDHC0",
    "MJLN0",
    "MPAM0",
    "FMLD0",
]

list_codec_bit_rates = [
    "3200", "2400", "1600", "1400", "1300", "1200", "700C", "450", "450PWB"
]

timit_train = os.path.join(args.timit_path, 'TRAIN')
timit_test = os.path.join(args.timit_path, 'TEST')

train_wav_files = glob.glob(timit_train + '/DR*/*/*.wav')
test_wav_files = glob.glob(timit_test + '/DR*/*/*.wav')

# for test_spk in test_spklist:
#     test_wav_files = [i for i in test_wav_files if test_spk in i]

print(f"Len Original | Train: {len(train_wav_files)}, Test: {len(test_wav_files)}")

def create_distortion(wav_files, subset):
    for wav_file in tqdm(wav_files, desc=f'Creating wavfiles of {subset} set'):
        for bit_rate in list_codec_bit_rates:
            _, spk, name = wav_file.rsplit(os.sep, 2)
            name = name.replace('.WAV', '')
            target_folder = os.path.join(args.target_path, subset, 'bitrate_' + bit_rate, spk)
            target_path = os.path.join(target_folder, name)
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            subprocess.run(['sh', 'compress.sh', wav_file, target_path, bit_rate, sample_rate])

create_distortion(train_wav_files, 'train')
create_distortion(test_wav_files, 'test')