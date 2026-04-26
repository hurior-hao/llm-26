"""
FineWeb-Edu dataset (for srs pretraining)
https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu
Downloads and tokenizes the data and saves data shards to disk.
Run simply as:
$ python fineweb.py
Will save shards to the local directory "edu_fineweb10B".
"""

import os
import multiprocessing as mp
import numpy as np
from transformers import GPT2Tokenizer


os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
# change it to your local folder if you are not using qz.cfff platform.
os.environ["HF_HOME"] = "/inspire/hdd/project/fdu-aidake-cfff/public/hf-home"
print(os.environ.get("HF_ENDPOINT"))

from datasets import load_dataset # pip install datasets
from tqdm import tqdm # pip install tqdm

print(f"HF_DATASETS_CACHE: {os.environ.get('HF_DATASETS_CACHE')}")
print(f"HF_HOME: {os.environ.get('HF_HOME')}")
print(f"HF_ENDPOINT: {os.environ.get('HF_ENDPOINT')}")
print("Starting download of fineweb-edu sample-10BT (~27GB)... this may take a while")
# download the dataset
fw = load_dataset("HuggingFaceFW/fineweb-edu", name="sample-10BT", split="train")
print("Download complete!")

# init the tokenizer

tokenizer = GPT2Tokenizer.from_pretrained("./gpt2_weights")
eot = tokenizer.eos_token_id # end of text token

def tokenize(doc):
    # tokenizes a single document and returns a numpy array of uint16 tokens
    tokens = [eot] # the special  token delimits all documents
    tokens.extend(tokenizer.encode(doc["text"]))
    tokens_np = np.array(tokens)
    assert (0 <= tokens_np).all() and (tokens_np < 2**16).all(), "token dictionary too large for uint16"
    tokens_np_uint16 = tokens_np.astype(np.uint16)
    return tokens_np_uint16

def write_datafile(filename, tokens_np):
    np.save(filename, tokens_np)


if __name__ == '__main__':
    local_dir = "/inspire/hdd/project/fdu-aidake-cfff/public/baojian/global_public/datasets-models/lecture-06-gpts-edu_fineweb10B"
    shard_size = int(1e8)
    DATA_CACHE_DIR = local_dir
    os.makedirs(DATA_CACHE_DIR, exist_ok=True)

    fw = load_dataset("HuggingFaceFW/fineweb-edu", name="sample-10BT", split="train")

    nprocs = 15
    print(f"Using {nprocs} / {os.cpu_count()} CPUs")

    with mp.Pool(nprocs) as pool:
        shard_index = 0
        all_tokens_np = np.empty((shard_size,), dtype=np.uint16)
        token_count = 0
        progress_bar = None
        for tokens in pool.imap(tokenize, fw, chunksize=16):
            if token_count + len(tokens) <= shard_size:
                all_tokens_np[token_count:token_count+len(tokens)] = tokens
                token_count += len(tokens)
                if progress_bar is None:
                    progress_bar = tqdm(total=shard_size, unit="tokens", desc=f"Shard {shard_index}")
                progress_bar.update(len(tokens))
            else:
                split = "val" if shard_index == 0 else "train"
                filename = os.path.join(DATA_CACHE_DIR, f"edufineweb_{split}_{shard_index:06d}")
                remainder = shard_size - token_count
                progress_bar.update(remainder)
                all_tokens_np[token_count:token_count+remainder] = tokens[:remainder]
                write_datafile(filename, all_tokens_np)
                progress_bar.close()
                shard_index += 1
                progress_bar = None
                all_tokens_np[0:len(tokens)-remainder] = tokens[remainder:]
                token_count = len(tokens)-remainder

        if token_count != 0:
            split = "val" if shard_index == 0 else "train"
            filename = os.path.join(DATA_CACHE_DIR, f"edufineweb_{split}_{shard_index:06d}")
            write_datafile(filename, all_tokens_np[:token_count])