#!/usr/bin/env python
# coding: utf-8
# https://nlp.seas.harvard.edu/annotated-transformer/

import os
import time
import gc
import torch
import torch.nn as nn
from torch.nn.functional import log_softmax, pad
import math
import copy
from torch.optim.lr_scheduler import LambdaLR
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler
import torch.distributed as dist
import torch.multiprocessing as mp
from torch.nn.parallel import DistributedDataParallel as DDP

from datasets import load_dataset
from tokenizers import Tokenizer, models, pre_tokenizers, processors
from tokenizers.trainers import BpeTrainer


from tqdm.auto import tqdm
import matplotlib.pyplot as plt

from torch.nn.functional import pad
from torch.utils.data import DataLoader

from detect_torch_device import detect_torch_device

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HOME"] = "/inspire/hdd/project/fdu-aidake-cfff/public/hf-home"


class DummyOptimizer(torch.optim.Optimizer):
    def __init__(self):
        self.param_groups = [{"lr": 0}]
        None

    def step(self):
        None

    def zero_grad(self, set_to_none=False):
        None

class DummyScheduler:
    def step(self):
        None


class EncoderDecoder(nn.Module):
    """
    A standard Encoder-Decoder architecture. Base for this and many
    other models.
    """

    def __init__(self, encoder, decoder, src_embed, tgt_embed, generator):
        super(EncoderDecoder, self).__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.src_embed = src_embed
        self.tgt_embed = tgt_embed
        self.generator = generator

    def forward(self, src, tgt, src_mask, tgt_mask):
        "Take in and process masked src and target sequences."
        return self.decode(self.encode(src, src_mask), src_mask, tgt, tgt_mask)

    def encode(self, src, src_mask):
        return self.encoder(self.src_embed(src), src_mask)

    def decode(self, memory, src_mask, tgt, tgt_mask):
        return self.decoder(self.tgt_embed(tgt), memory, src_mask, tgt_mask)


class Generator(nn.Module):
    "Define standard linear + softmax generation step."

    def __init__(self, d_model, vocab):
        super(Generator, self).__init__()
        self.proj = nn.Linear(d_model, vocab)

    def forward(self, x):
        return log_softmax(self.proj(x), dim=-1)


def clones(module, N):
    "Produce N identical layers."
    return nn.ModuleList([copy.deepcopy(module) for _ in range(N)])


class Encoder(nn.Module):
    "Core encoder is a stack of N layers"

    def __init__(self, layer, N):
        super(Encoder, self).__init__()
        self.layers = clones(layer, N)
        self.norm = LayerNorm(layer.size)

    def forward(self, x, mask):
        "Pass the input (and mask) through each layer in turn."
        for layer in self.layers:
            x = layer(x, mask)
        return self.norm(x)


class LayerNorm(nn.Module):
    "Construct a layernorm module (See citation for details)."

    def __init__(self, features, eps=1e-6):
        super(LayerNorm, self).__init__()
        self.a_2 = nn.Parameter(torch.ones(features))
        self.b_2 = nn.Parameter(torch.zeros(features))
        self.eps = eps

    def forward(self, x):
        mean = x.mean(-1, keepdim=True)
        std = x.std(-1, keepdim=True)
        return self.a_2 * (x - mean) / (std + self.eps) + self.b_2


class SublayerConnection(nn.Module):
    """
    A residual connection followed by a layer norm.
    Note for code simplicity the norm is first as opposed to last.
    """

    def __init__(self, size, dropout):
        super(SublayerConnection, self).__init__()
        self.norm = LayerNorm(size)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, sublayer):
        "Apply residual connection to any sublayer with the same size."
        return x + self.dropout(sublayer(self.norm(x)))


class EncoderLayer(nn.Module):
    "Encoder is made up of self-attn and feed forward (defined below)"

    def __init__(self, size, self_attn, feed_forward, dropout):
        super(EncoderLayer, self).__init__()
        self.self_attn = self_attn
        self.feed_forward = feed_forward
        self.sublayer = clones(SublayerConnection(size, dropout), 2)
        self.size = size

    def forward(self, x, mask):
        "Follow Figure 1 (left) for connections."
        x = self.sublayer[0](x, lambda x: self.self_attn(x, x, x, mask))
        return self.sublayer[1](x, self.feed_forward)


class Decoder(nn.Module):
    "Generic N layer decoder with masking."

    def __init__(self, layer, N):
        super(Decoder, self).__init__()
        self.layers = clones(layer, N)
        self.norm = LayerNorm(layer.size)

    def forward(self, x, memory, src_mask, tgt_mask):
        for layer in self.layers:
            x = layer(x, memory, src_mask, tgt_mask)
        return self.norm(x)


class DecoderLayer(nn.Module):
    "Decoder is made of self-attn, src-attn, and feed forward (defined below)"

    def __init__(self, size, self_attn, src_attn, feed_forward, dropout):
        super(DecoderLayer, self).__init__()
        self.size = size
        self.self_attn = self_attn
        self.src_attn = src_attn
        self.feed_forward = feed_forward
        self.sublayer = clones(SublayerConnection(size, dropout), 3)

    def forward(self, x, memory, src_mask, tgt_mask):
        "Follow Figure 1 (right) for connections."
        m = memory
        x = self.sublayer[0](x, lambda x: self.self_attn(x, x, x, tgt_mask))
        x = self.sublayer[1](x, lambda x: self.src_attn(x, m, m, src_mask))
        return self.sublayer[2](x, self.feed_forward)


def subsequent_mask(size):
    "Mask out subsequent positions."
    attn_shape = (1, size, size)
    subsequent_mask = torch.triu(torch.ones(attn_shape), diagonal=1).type(
        torch.uint8
    )
    return subsequent_mask == 0


def attention(query, key, value, mask=None, dropout=None):
    "Compute 'Scaled Dot Product Attention'"
    d_k = query.size(-1)
    scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d_k)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    p_attn = scores.softmax(dim=-1)
    if dropout is not None:
        p_attn = dropout(p_attn)
    return torch.matmul(p_attn, value), p_attn


class MultiHeadedAttention(nn.Module):
    def __init__(self, h, d_model, dropout=0.1):
        "Take in model size and number of heads."
        super(MultiHeadedAttention, self).__init__()
        assert d_model % h == 0
        # We assume d_v always equals d_k
        self.d_k = d_model // h
        self.h = h
        self.linears = clones(nn.Linear(d_model, d_model), 4)
        self.attn = None
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, query, key, value, mask=None):
        "Implements Figure 2"
        if mask is not None:
            # Same mask applied to all h heads.
            mask = mask.unsqueeze(1)
        nbatches = query.size(0)

        # 1) Do all the linear projections in batch from d_model => h x d_k
        query, key, value = [
            lin(x).view(nbatches, -1, self.h, self.d_k).transpose(1, 2)
            for lin, x in zip(self.linears, (query, key, value))
        ]

        # 2) Apply attention on all the projected vectors in batch.
        x, self.attn = attention(
            query, key, value, mask=mask, dropout=self.dropout
        )

        # 3) "Concat" using a view and apply a final linear.
        x = (
            x.transpose(1, 2)
            .contiguous()
            .view(nbatches, -1, self.h * self.d_k)
        )
        del query
        del key
        del value
        return self.linears[-1](x)


class PositionwiseFeedForward(nn.Module):
    "Implements FFN equation."

    def __init__(self, d_model, d_ff, dropout=0.1):
        super(PositionwiseFeedForward, self).__init__()
        self.w_1 = nn.Linear(d_model, d_ff)
        self.w_2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        return self.w_2(self.dropout(self.w_1(x).relu()))


class Embeddings(nn.Module):
    def __init__(self, d_model, vocab):
        super(Embeddings, self).__init__()
        self.lut = nn.Embedding(vocab, d_model)
        self.d_model = d_model

    def forward(self, x):
        return self.lut(x) * math.sqrt(self.d_model)


class PositionalEncoding(nn.Module):
    "Implement the PE function."

    def __init__(self, d_model, dropout, max_len=5000):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)

        # Compute the positional encodings once in log space.
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2) * -(math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer("pe", pe)

    def forward(self, x):
        x = x + self.pe[:, : x.size(1)].requires_grad_(False)
        return self.dropout(x)

def make_model(
    src_vocab, tgt_vocab, N=2, d_model=128, d_ff=256, h=4, dropout=0.1
):
    "Helper: Construct a model from hyperparameters."
    c = copy.deepcopy
    attn = MultiHeadedAttention(h, d_model)
    ff = PositionwiseFeedForward(d_model, d_ff, dropout)
    position = PositionalEncoding(d_model, dropout)
    model = EncoderDecoder(
        Encoder(EncoderLayer(d_model, c(attn), c(ff), dropout), N),
        Decoder(DecoderLayer(d_model, c(attn), c(attn), c(ff), dropout), N),
        nn.Sequential(Embeddings(d_model, src_vocab), c(position)),
        nn.Sequential(Embeddings(d_model, tgt_vocab), c(position)),
        Generator(d_model, tgt_vocab),
    )

    # This was important from their code.
    # Initialize parameters with Glorot / fan_avg.
    for p in model.parameters():
        if p.dim() > 1:
            nn.init.xavier_uniform_(p)
    return model


class Batch:
    """Object for holding a batch of data with mask during training."""

    def __init__(self, src, tgt=None, pad=2):  # 2 = <blank>
        self.src = src
        self.src_mask = (src != pad).unsqueeze(-2)
        if tgt is not None:
            self.tgt = tgt[:, :-1]
            self.tgt_y = tgt[:, 1:]
            self.tgt_mask = self.make_std_mask(self.tgt, pad)
            self.ntokens = (self.tgt_y != pad).data.sum()

    @staticmethod
    def make_std_mask(tgt, pad):
        "Create a mask to hide padding and future words."
        tgt_mask = (tgt != pad).unsqueeze(-2)
        tgt_mask = tgt_mask & subsequent_mask(tgt.size(-1)).type_as(
            tgt_mask.data
        )
        return tgt_mask


class TrainState:
    """Track number of steps, examples, and tokens processed"""

    step: int = 0  # Steps in the current epoch
    accum_step: int = 0  # Number of gradient accumulation steps
    samples: int = 0  # total # of examples used
    tokens: int = 0  # total # of tokens processed


def run_epoch(
    data_iter,
    model,
    loss_compute,
    optimizer,
    scheduler,
    mode="train",
    accum_iter=1,
    train_state=TrainState(),
    epoch=None,
    total=None,
):
    """Train a single epoch"""
    start = time.time()
    total_tokens = 0
    total_loss = 0
    tokens = 0
    n_accum = 0
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    desc = f"Epoch {epoch} [{mode}]" if epoch is not None else mode
    pbar = tqdm(data_iter, desc=desc, total=total, leave=False)
    for i, batch in enumerate(pbar):
        batch.src = batch.src.to(device)
        batch.tgt = batch.tgt.to(device)
        batch.src_mask = batch.src_mask.to(device)
        batch.tgt_mask = batch.tgt_mask.to(device)
        batch.tgt_y = batch.tgt_y.to(device)
        batch.ntokens = batch.ntokens.to(device)
        out = model.forward(
            batch.src, batch.tgt, batch.src_mask, batch.tgt_mask
        )
        loss, loss_node = loss_compute(out, batch.tgt_y, batch.ntokens)
        # loss_node = loss_node / accum_iter
        if mode == "train" or mode == "train+log":
            loss_node.backward()
            train_state.step += 1
            train_state.samples += batch.src.shape[0]
            train_state.tokens += batch.ntokens
            if i % accum_iter == 0:
                optimizer.step()
                optimizer.zero_grad(set_to_none=True)
                n_accum += 1
                train_state.accum_step += 1
            scheduler.step()

        total_loss += loss
        total_tokens += batch.ntokens
        tokens += batch.ntokens
        if mode == "train" or mode == "train+log":
            lr = optimizer.param_groups[0]["lr"]
            elapsed = time.time() - start
            pbar.set_postfix(
                step=i,
                accum=n_accum,
                loss=f"{(loss / batch.ntokens).item():.2f}",
                tok_s=f"{(tokens / elapsed):.1f}",
                lr=f"{lr:.1e}",
            )
        del loss
        del loss_node
    return total_loss / total_tokens, train_state



def rate(step, model_size, factor, warmup):
    """
    we have to default the step to 1 for LambdaLR function
    to avoid zero raising to negative power.
    """
    if step == 0:
        step = 1
    return factor * (
        model_size ** (-0.5) * min(step ** (-0.5), step * warmup ** (-1.5))
    )


class LabelSmoothing(nn.Module):
    "Implement label smoothing."

    def __init__(self, size, padding_idx, smoothing=0.0):
        super(LabelSmoothing, self).__init__()
        self.criterion = nn.KLDivLoss(reduction="sum")
        self.padding_idx = padding_idx
        self.confidence = 1.0 - smoothing
        self.smoothing = smoothing
        self.size = size
        self.true_dist = None

    def forward(self, x, target):
        assert x.size(1) == self.size
        true_dist = x.data.clone()
        true_dist.fill_(self.smoothing / (self.size - 2))
        true_dist.scatter_(1, target.data.unsqueeze(1), self.confidence)
        true_dist[:, self.padding_idx] = 0
        mask = torch.nonzero(target.data == self.padding_idx)
        if mask.dim() > 0:
            true_dist.index_fill_(0, mask.squeeze(), 0.0)
        self.true_dist = true_dist
        return self.criterion(x, true_dist.clone().detach())

def loss(x, crit):
    d = x + 3
    eps = 1e-9
    predict = torch.tensor([[eps, x / d, 1 / d, 1 / d, 1 / d]], dtype=torch.float32)
    predict = predict / predict.sum(dim=1, keepdim=True)
    return crit(predict.log(), torch.tensor([1], dtype=torch.long)).item()


def data_gen(V, batch_size, nbatches):
    "Generate random data for a src-tgt copy task."
    for i in range(nbatches):
        data = torch.randint(1, V, size=(batch_size, 10))
        data[:, 0] = 1
        src = data.requires_grad_(False).clone().detach()
        tgt = data.requires_grad_(False).clone().detach()
        yield Batch(src, tgt, 0)


class SimpleLossCompute:
    "A simple loss compute and train function."

    def __init__(self, generator, criterion):
        self.generator = generator
        self.criterion = criterion

    def __call__(self, x, y, norm):
        x = self.generator(x)
        sloss = (
            self.criterion(
                x.contiguous().view(-1, x.size(-1)), y.contiguous().view(-1)
            )
            / norm
        )
        return sloss.data * norm, sloss


def greedy_decode(model, src, src_mask, max_len, start_symbol):
    memory = model.encode(src, src_mask)
    ys = torch.zeros(1, 1).fill_(start_symbol).type_as(src.data)
    for i in range(max_len - 1):
        out = model.decode(
            memory, src_mask, ys, subsequent_mask(ys.size(1)).type_as(src.data)
        )
        prob = model.generator(out[:, -1])
        _, next_word = torch.max(prob, dim=1)
        next_word = next_word.data[0]
        ys = torch.cat(
            [ys, torch.zeros(1, 1).type_as(src.data).fill_(next_word)], dim=1
        )
    return ys


def build_paper_tokenizer(ds):
    tokenizer = Tokenizer(models.BPE(unk_token="<unk>"))
    tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()

    trainer = BpeTrainer(
        vocab_size=37000,
        special_tokens=["<blank>", "<s>", "</s>", "<unk>"]
    )

    total_examples = sum(len(ds[split]) for split in ["train", "validation", "test"])

    def batch_iterator():
        pbar = tqdm(total=2 * total_examples, desc="Training tokenizer")
        for split in ["train", "validation", "test"]:
            for example in ds[split]:
                yield example["translation"]["de"]
                pbar.update(1)
                yield example["translation"]["en"]
                pbar.update(1)
        pbar.close()

    tokenizer.train_from_iterator(batch_iterator(), trainer=trainer)

    tokenizer.post_processor = processors.TemplateProcessing(
        single="<s> $A </s>",
        pair="<s> $A </s> $B:1 </s>:1",
        special_tokens=[
            ("<s>", tokenizer.token_to_id("<s>")),
            ("</s>", tokenizer.token_to_id("</s>")),
        ],
    )
    return tokenizer


def load_or_build_tokenizer(ds, tokenizer_path="wmt14_bpe_tokenizer.json"):
    if os.path.exists(tokenizer_path):
        print(f"Loading tokenizer from {tokenizer_path}")
        tokenizer = Tokenizer.from_file(tokenizer_path)
    else:
        print("Building tokenizer...")
        tokenizer = build_paper_tokenizer(ds)
        tokenizer.save(tokenizer_path)
        print(f"Tokenizer saved to {tokenizer_path}")
    return tokenizer


def collate_batch(
    batch,
    tokenizer,
    device,
    max_padding=128,
    pad_id=None,
):
    if pad_id is None:
        pad_id = tokenizer.token_to_id("<blank>")

    src_list, tgt_list = [], []

    for _src, _tgt in batch:
        processed_src = torch.tensor(
            tokenizer.encode(_src).ids,
            dtype=torch.int64,
            device=device,
        )
        processed_tgt = torch.tensor(
            tokenizer.encode(_tgt).ids,
            dtype=torch.int64,
            device=device,
        )

        processed_src = processed_src[:max_padding]
        processed_tgt = processed_tgt[:max_padding]

        src_list.append(
            pad(processed_src, (0, max_padding - len(processed_src)), value=pad_id)
        )
        tgt_list.append(
            pad(processed_tgt, (0, max_padding - len(processed_tgt)), value=pad_id)
        )

    src = torch.stack(src_list)
    tgt = torch.stack(tgt_list)
    return src, tgt

def create_dataloaders(
    device,
    ds,
    tokenizer,
    batch_size=32,
    max_padding=128,
    is_distributed=False,
):
    def collate_fn(batch):
        text_batch = [
            (example["translation"]["de"], example["translation"]["en"])
            for example in batch
        ]
        return collate_batch(
            text_batch,
            tokenizer,
            device,
            max_padding=max_padding,
            pad_id=tokenizer.token_to_id("<blank>"),
        )

    train_dataloader = DataLoader(
        ds["train"],
        batch_size=batch_size,
        shuffle=True,
        collate_fn=collate_fn,
    )

    valid_dataloader = DataLoader(
        ds["validation"],
        batch_size=batch_size,
        shuffle=False,
        collate_fn=collate_fn,
    )

    return train_dataloader, valid_dataloader

def train_worker(
    tokenizer,
    ds,
    config,
):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}", flush=True)

    pad_idx = tokenizer.token_to_id("<blank>")
    vocab_size = tokenizer.get_vocab_size()
    d_model = 512
    d_model = config["d_model"]
    model = make_model(
        vocab_size,
        vocab_size,
        N=config["N"],
        d_model=config["d_model"],
        d_ff=config["d_ff"],
        h=config["h"],
        dropout=config["dropout"],
    ).to(device)
    criterion = LabelSmoothing(
        size=vocab_size, padding_idx=pad_idx, smoothing=0.1
    ).to(device)

    train_dataloader, valid_dataloader = create_dataloaders(
        device=device,
        ds=ds,
        tokenizer=tokenizer,
        batch_size=config["batch_size"],
        max_padding=config["max_padding"],
        is_distributed=False,
    )

    optimizer = torch.optim.Adam(
        model.parameters(), lr=config["base_lr"], betas=(0.9, 0.98), eps=1e-9
    )
    lr_scheduler = LambdaLR(
        optimizer=optimizer,
        lr_lambda=lambda step: rate(
            step, d_model, factor=1, warmup=config["warmup"]
        ),
    )
    train_state = TrainState()

    for epoch in range(config["num_epochs"]):
        model.train()
        print(f"Epoch {epoch} Training ====", flush=True)
        _, train_state = run_epoch(
            (Batch(b[0], b[1], pad_idx) for b in train_dataloader),
            model,
            SimpleLossCompute(model.generator, criterion),
            optimizer,
            lr_scheduler,
            mode="train+log",
            accum_iter=config["accum_iter"],
            train_state=train_state,
            epoch=epoch,
            total=len(train_dataloader),
        )

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        file_path = "%s%.2d.pt" % (config["file_prefix"], epoch)
        torch.save(model.state_dict(), file_path)

        print(f"Epoch {epoch} Validation ====", flush=True)
        model.eval()
        sloss = run_epoch(
            (Batch(b[0], b[1], pad_idx) for b in valid_dataloader),
            model,
            SimpleLossCompute(model.generator, criterion),
            DummyOptimizer(),
            DummyScheduler(),
            mode="eval",
            epoch=epoch,
            total=len(valid_dataloader),
        )
        print(sloss)

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    file_path = "%sfinal.pt" % config["file_prefix"]
    torch.save(model.state_dict(), file_path)


def check_outputs(
    valid_dataloader,
    model,
    tokenizer,
    n_examples=15,
    pad_idx=None,
    eos_string="</s>",
    max_len=72,
    start_symbol=0,
    device=None,
):
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if pad_idx is None:
        pad_idx = tokenizer.token_to_id("<blank>")

    model.eval()
    results = []

    valid_iter = iter(valid_dataloader)

    for idx in range(n_examples):
        print(f"\nExample {idx} ========\n")

        b = next(valid_iter)
        rb = Batch(b[0].to(device), b[1].to(device), pad_idx)

        model_out = greedy_decode(model, rb.src, rb.src_mask, max_len, start_symbol)[0]

        src_ids = [x.item() for x in rb.src[0] if x.item() != pad_idx]
        tgt_ids = [x.item() for x in rb.tgt[0] if x.item() != pad_idx]
        out_ids = [x.item() for x in model_out if x.item() != pad_idx]

        src_text = tokenizer.decode(src_ids)
        tgt_text = tokenizer.decode(tgt_ids)
        model_txt = tokenizer.decode(out_ids)

        if eos_string in model_txt:
            model_txt = model_txt.split(eos_string, 1)[0] + eos_string

        print("Source Text (Input)        : " + src_text.replace("\n", ""))
        print("Target Text (Ground Truth) : " + tgt_text.replace("\n", ""))
        print("Model Output               : " + model_txt.replace("\n", ""))

        results.append((rb, src_ids, tgt_ids, out_ids, model_txt))

    return results


def train_model(tokenizer, wmt_ds, config):
    train_worker(tokenizer, wmt_ds, config)


def load_trained_model(shared_tokenizer, wmt_ds, sampling=True):
    config = {
        "batch_size": 512,
        "num_epochs": 5,
        "accum_iter": 5,
        "base_lr": 1.0,
        "max_padding": 72,
        "warmup": 3000,
        "N": 6,
        "d_model": 512,
        "d_ff": 2048,
        "h": 8,
        "dropout": 0.1,
    }

    if sampling:
        n_train = int(0.1 * len(wmt_ds["train"]))
        small_wmt_ds = DatasetDict({
            "train": wmt_ds["train"].select(range(n_train)),
            "validation": wmt_ds["validation"],
            "test": wmt_ds["test"],
        })
        config["file_prefix"] = "wmt14_small_"
        model_path = "wmt14_small_final.pt"
        train_ds = small_wmt_ds
    else:
        config["file_prefix"] = "wmt14_full_"
        model_path = "wmt14_full_final.pt"
        train_ds = wmt_ds

    if not os.path.exists(model_path):
        train_model(shared_tokenizer, train_ds, config)

    vocab_size = shared_tokenizer.get_vocab_size()
    model = make_model(
        vocab_size,
        vocab_size,
        N=config["N"],
        d_model=config["d_model"],
        d_ff=config["d_ff"],
        h=config["h"],
        dropout=config["dropout"],
    )
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    return model


def main():
    device = detect_torch_device()
    print("Device:", device)
    print("HF_ENDPOINT:", os.environ.get("HF_ENDPOINT"))

    jnk_start_time = time.time()

    wmt_ds = load_dataset("wmt14", "de-en")
    print(wmt_ds)

    start = time.time()
    shared_tokenizer = load_or_build_tokenizer(wmt_ds)
    print("Vocab size:", shared_tokenizer.get_vocab_size())
    elapsed = time.time() - start

    print("Vocab size:", shared_tokenizer.get_vocab_size())
    print(f"Tokenizer build time: {elapsed/60:.2f} minutes")

    if torch.cuda.is_available():
        print(torch.cuda.memory_allocated() / 1024**2, "MB allocated")
        print(torch.cuda.memory_reserved() / 1024**2, "MB reserved")

    for name in ["model", "optimizer", "batch", "loss", "outputs"]:
        if name in globals():
            del globals()[name]
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    if torch.cuda.is_available():
        print(torch.cuda.memory_allocated() / 1024**2, "MB allocated")
        print(torch.cuda.memory_reserved() / 1024**2, "MB reserved")

    model = load_trained_model(
        shared_tokenizer=shared_tokenizer,
        wmt_ds=wmt_ds,
        sampling=False,   # change to True for 10% training
    )

    total_elapsed = time.time() - jnk_start_time
    print(f"Total run time: {total_elapsed/60:.2f} minutes")

    return model


if __name__ == "__main__":
    model = main()