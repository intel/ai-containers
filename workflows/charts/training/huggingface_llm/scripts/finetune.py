#!/usr/bin/env python
#
# Copyright (c) 2022 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0


import datasets
import importlib
import logging
import math
import os
import sys
import torch
import transformers
import copy

from dataclasses import dataclass, field
from datasets import load_dataset
from datetime import datetime
from peft import (
    LoraConfig,
    PeftModel,
    TaskType,
    get_peft_model
)
from transformers import (
    AutoConfig,
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    HfArgumentParser,
    TrainingArguments,
    TrainerCallback,
    Trainer,
    set_seed,
)
from transformers.trainer_utils import is_main_process
from typing import Optional, List

from inc_utils import INCDataloader, calculate_latency_and_throughput

# COMMENT OUT FOR SINGLE NODE
import torch.distributed as dist  # noqa # pylint: disable=unused-import

os.environ["WANDB_DISABLED"] = "true"

logger = logging.getLogger(__name__)

CNVRG_LINE_FORMAT = '\"cnvrg_linechart_{} value: {}\"\n'


class CustomPrinterCallback(TrainerCallback):
    def on_log(self, args, state, control, logs=None, **kwargs):
        _ = logs.pop("total_flos", None)
        if state.is_local_process_zero:
            print(logs)
            if 'loss' in logs:
                print(CNVRG_LINE_FORMAT.format('loss', str(logs['loss'])))
            if 'learning_rate' in logs:
                print(CNVRG_LINE_FORMAT.format('learningrate', str(logs['learning_rate'])))
            if 'epoch' in logs:
                print(CNVRG_LINE_FORMAT.format('epoch', str(logs['epoch'])))


@dataclass
class ModelArguments:
    """
    Arguments pertaining to which model/config/tokenizer we are going to fine-tune, or train from scratch.
    """

    model_name_or_path: Optional[str] = field(
        default=None,
        metadata={
            "help": "The model checkpoint for weights initialization."
                    "Don't set if you want to train a model from scratch."
        },
    )
    config_name: Optional[str] = field(
        default=None, metadata={"help": "Pretrained config name or path if not the same as model_name"}
    )
    tokenizer_name: Optional[str] = field(
        default=None, metadata={"help": "Pretrained tokenizer name or path if not the same as model_name"}
    )
    cache_dir: Optional[str] = field(
        default=None,
        metadata={"help": "Where do you want to store the pretrained models downloaded from huggingface.co"},
    )
    token: Optional[str] = field(
        default=None,
        metadata={"help": "auth token for private models"},
    )
    use_fast_tokenizer: bool = field(
        default=True,
        metadata={"help": "Whether to use one of the fast tokenizer (backed by the tokenizers library) or not."},
    )
    model_revision: str = field(
        default="main",
        metadata={"help": "The specific model version to use (can be a branch name, tag name or commit id)."},
    )
    use_auth_token: bool = field(
        default=False,
        metadata={
            "help": "Will use the token generated when running `transformers-cli login` (necessary to use this script "
                    "with private models)."
        },
    )
    use_auth_token: bool = field(
        default=False,
        metadata={
            "help": "The `use_auth_token` argument is deprecated and will be removed in v4.34. Please use `token` "
                    "instead."
        },
    )
    trust_remote_code: bool = field(
        default=False,
        metadata={
            "help": "should enable when using custom model architecture that is not yet part of the Hugging Face "
                    "transformers package like MPT)."
        },
    )
    use_cache: bool = field(
        default=True,
        metadata={
            "help": (
                "Whether or not the model should return the last key/values attentions (not used by all models)."
                "Only relevant if `config.is_decoder=True`."
            )
        },
    )
    low_cpu_mem_usage: bool = field(
        default=False,
        metadata={
            "help": (
                "It is an option to create the model as an empty shell, then only materialize its parameters when the "
                "pretrained weights are loaded. When set to True, it will benefit LLM loading time and RAM consumption."
            )
        },
    )
    attn_softmax_bf16: bool = field(
        default=False,
        metadata={
            "help": (
                "Whether to run attention softmax layer in bf16 precision for fine-tuning. The current support is "
                "limited to Llama only."
            )
        },
    )
    use_flash_attention: bool = field(
        default=False,
        metadata={
            "help": (
                "Whether to use Habana flash attention for fine-tuning. The current support is limited to Llama only."
            )
        },
    )
    flash_attention_recompute: bool = field(
        default=False,
        metadata={
            "help": (
                "Whether to enable recompute in Habana flash attention for fine-tuning."
                " It is applicable only when use_flash_attention is True."
            )
        },
    )
    flash_attention_causal_mask: bool = field(
        default=False,
        metadata={
            "help": (
                "Whether to enable causal mask in Habana flash attention for fine-tuning."
                " It is applicable only when use_flash_attention is True."
            )
        },
    )
    use_fused_rope: bool = field(
        default=True,
        metadata={
            "help": (
                "Whether to use Habana fused-rope for fine-tuning. The current support is limited to Llama only."
            )
        },
    )
    load_meta_device: bool = field(
        default=False,
        metadata={
            "help": (
                "It is an option to load the model to the device instead of the host, so it can reduce the host RAM "
                "usage. https://huggingface.co/blog/accelerate-large-models"
            )
        },
    )


@dataclass
class DataArguments:
    """
    Arguments pertaining to what data we are going to input our model for training and eval.
    """

    dataset_name: Optional[str] = field(
        default=None, metadata={"help": "The name of the dataset to use (via the datasets library)."}
    )
    dataset_config_name: Optional[str] = field(
        default=None, metadata={"help": "The configuration name of the dataset to use (via the datasets library)."}
    )
    train_file: Optional[str] = field(default=None, metadata={"help": "The input training data file (a text file)."})
    validation_file: Optional[str] = field(
        default=None,
        metadata={"help": "An optional input evaluation data file to evaluate the perplexity on (a text file)."},
    )
    max_seq_length: Optional[int] = field(
        default=512,
        metadata={
            "help": "The maximum total input sequence length after tokenization. Sequences longer "
                    "than this will be truncated."
        },
    )
    validation_split_percentage: Optional[float] = field(
        default=0,
        metadata={
            "help": "The percentage of the train set used as validation set in case there's no validation split"
        },
    )
    overwrite_cache: bool = field(
        default=False, metadata={"help": "Overwrite the cached preprocessed datasets or not."}
    )
    pad_to_max_length: bool = field(
        default=False,
        metadata={
            "help": "Whether to pad all samples to `max_seq_length`. "
                    "If False, will pad the samples dynamically when batching to the maximum length in the batch."
        },
    )
    max_train_samples: Optional[int] = field(
        default=None,
        metadata={
            "help": "For debugging purposes or quicker training, truncate the number of training examples to this "
                    "value if set."
        },
    )
    max_eval_samples: Optional[int] = field(
        default=None,
        metadata={
            "help": "For debugging purposes or quicker training, truncate the number of evaluation examples to this "
                    "value if set."
        },
    )
    keep_in_memory: bool = field(
        default=False,
        metadata={
            "help": "Whether to keep in memory the loaded dataset. Defaults to False."
        },
    )
    dataset_seed: int = field(
        default=42,
        metadata={
            "help": "Seed to use in dataset processing, different seeds might yield different datasets. This seed and "
                    "the seed in training arguments are not related"
        },
    )
    dataset_cache_directory: Optional[str] = field(
        default=None,
        metadata={
            "help": "Path to directory where the processed dataset will be saved. If path exists, try to load "
                    "processed dataset from this path."
        }
    )
    dataset_concatenation: Optional[bool] = field(
        default=False,
        metadata={
            "help": "Whether to concatenate the sentence for more efficient training."
        }
    )
    streaming: Optional[bool] = field(
        default=False,
        metadata={
            "help": "If set to True, don’t download the data files. Instead, it streams the data progressively while "
                    "iterating on the dataset."
        }
    )
    prompt_with_input: str = field(
        default="Below is an instruction that describes a task, paired with an input that provides further context. "
                "Write a response that appropriately completes the request.",
        metadata={"help": "The prompt string to use with an instruction that has an input/context string"}
    )
    prompt_without_input: str = field(
        default="Below is an instruction that describes a task. Write a response that appropriately completes the "
                "request.",
        metadata={"help": "The prompt string to use with an instruction that does not include an input/context string."}
    )
    instruction_column_name: Optional[str] = field(
        default=None,
        metadata={
            "help": "Name of the column in the dataset that describes the task that the model should perform. By "
                    "default, the 'instruction' column is used for non-SQL prompts and the 'question' column is used for SQL prompts."
        },
    )
    input_column_name: Optional[str] = field(
        default=None,
        metadata={
            "help": "Name of the column in the dataset that optionally provides context or input for the task. By "
                    "default, the 'input' column is used for non-SQL prompts and the 'context' column is used for SQL prompts."
        },
    )
    output_column_name: Optional[str] = field(
        default=None,
        metadata={
            "help": "Name of the column in the dataset with the answer to the instruction. By default, the "
                    "'output' column is used for non-SQL prompts and the 'answer' column is used for SQL prompts."
        },
    )


@dataclass
class FinetuneArguments:
    """
    Arguments of finetune we are going to apply on the model.
    """
    use_lora: bool = field(
        default=True,
        metadata={
            "help": "Whether or not to use LoRA."
        },
    )

    lora_rank: int = field(
        default=8,
        metadata={
            "help": "Rank parameter in the LoRA method."
        },
    )
    lora_alpha: int = field(
        default=32,
        metadata={
            "help": "Alpha parameter in the LoRA method."
        },
    )
    lora_dropout: float = field(
        default=0.1,
        metadata={
            "help": "Dropout parameter in the LoRA method."
        },
    )
    lora_target_modules: List[str] = field(
        default_factory=lambda: ["q_proj", "v_proj"],
        metadata={
            "help": "Target modules for the LoRA method."
        },
    )


@dataclass
class QuantizationArguments:
    """
    Arguments used to do weights only post training quantization using the Intel Neural Compressor.
    """
    peft_model_dir: str = field(
        default=None,
        metadata={
            "help": "If not training the model, load a model that was previously trained using peft."
        },
    )
    do_quantize: bool = field(
        default=False,
        metadata={
            "help": "Perform weight only post training quantization."
        },
    )
    quantize_output_dir: str = field(
        default=None,
        metadata={
            "help": "If quantization is successful, the quantized model will be saved to this directory."
        },
    )
    woq_bits: int = field(
        default=8,
        metadata={
            "help": "Bits for weight only quantization, 1-8 bits."
        },
    )
    woq_group_size: int = field(
        default=-1,
        metadata={
            "help": "Group size for weight only quantization. Group_size=[1-N] indicates "
                    "splitting the input channel elements per group_size. -1 indicates "
                    "the per-channel quantization per output channel."
        },
    )
    woq_scheme: str = field(
        default="sym",
        metadata={
            "help": "Scheme for weight only quantization. Choose from 'sym' and 'asym'."
        },
    )
    woq_algo: str = field(
        default="RTN",
        metadata={
            "help": "Algorithm for weight only quantization. Choose from: RTN, AWQ, GPTQ, or TEQ"
        },
    )


@dataclass
class BenchmarkArguments:
    """
    Arguments used to benchmark the model using the Intel Neural Compressor.
    """
    do_benchmark: bool = field(
        default=False,
        metadata={
            "help": "Benchmark the trained and/or quantized model."
        },
    )
    benchmark_warmup: int = field(
        default=10,
        metadata={
            "help": "The number of iterations to warmup before running performance tests."
        },
    )
    benchmark_iterations: int = field(
        default=100,
        metadata={
            "help": "The number of iterations to run performance tests."
        },
    )
    benchmark_cores_per_instance: int = field(
        default=None,
        metadata={
            "help": "The of CPU cores to use per instance"
        },
    )
    benchmark_num_instances: int = field(
        default=1,
        metadata={
            "help": "The number of instances to use for performance testing"
        },
    )


# Prompt dictionary with output used for chat models
CHAT_PROMPT_DICT = {
    "prompt_with_input": (
        "<s>[INST] <<SYS>>\n{prompt_with_input}<</SYS>>\n\n{instruction} {input} [/INST] "
        "{output} </s>"
    ),
    "prompt_without_input": (
        "<s>[INST] <<SYS>>\n{prompt_without_input}<</SYS>>\n\n{instruction} [/INST] {output} </s>"
    ),
}

# Prompt dictionary without output used for chat models
CHAT_PROMPT_DICT2 = {
    "prompt_with_input": (
        "<s>[INST] <<SYS>>\n{prompt_with_input}\n\n{instruction} {input} [/INST]"
    ),
    "prompt_without_input": (
        "<s>[INST] <<SYS>>\n{prompt_without_input}<</SYS>>\n\n{instruction} [/INST]"
    ),
}

# Prompt dictionary without output used for instruction tuning
STANDARD_PROMPT_DICT = {
    "prompt_with_input": (
        "{prompt_with_input}\n\n### Instruction:\n{instruction}\n\n### Input:\n{input}\n\n### Response:\n{output}"
    ),
    "prompt_without_input": (
        "{prompt_without_input}\n\n### Instruction:\n{instruction}\n\n### Response:\n{output}"
    ),
}

# Prompt dictionary without output used for instruction tuning
STANDARD_PROMPT_DICT2 = {
    "prompt_with_input": (
        "{prompt_with_input}\n\n### Instruction:\n{instruction}\n\n### Input:\n{input}\n\n### Response:"
    ),
    "prompt_without_input": (
        "{prompt_without_input}\n\n### Instruction:\n{instruction}\n\n### Response:"
    ),
}


def create_prompts(examples, prompt_dict):
    prompts = []

    for example in examples:
        prompt_template = prompt_dict["prompt_with_input"] \
            if example["input"] != "" else prompt_dict["prompt_without_input"]
        prompt = prompt_template.format_map(example)
        prompts.append(prompt)
    return prompts


def create_system_turn(examples, prompt_dict):
    prompts = []

    for example in examples:
        prompt_template = prompt_dict["prompt_with_input"] \
            if example["input"] != "" else prompt_dict["prompt_without_input"]
        prompt = prompt_template.format_map(example)
        prompts.append(prompt)
    return prompts


def is_optimum_habana_available():
    """
    Check for optimum-habana and return False if the library is not found.
    """
    if importlib.util.find_spec('optimum'):
        return importlib.util.find_spec('optimum.habana') is not None
    return False


def main():
    start_time = datetime.now()

    script_args = (ModelArguments, DataArguments, FinetuneArguments, QuantizationArguments, BenchmarkArguments)

    # If optimum-habana is available, use GaudiTrainingArguments. Otherwise, use Transformers TrainingArguments
    if is_optimum_habana_available():
        from optimum.habana import GaudiTrainingArguments
        script_args += (GaudiTrainingArguments,)
    else:
        script_args += (TrainingArguments,)

    # See all possible arguments in src/transformers/training_args.py
    # or by passing the --help flag to this script.
    # We now keep distinct sets of args, for a cleaner separation of concerns.
    parser = HfArgumentParser(script_args)

    if len(sys.argv) == 2 and sys.argv[1].endswith(".json"):
        # If we pass only one argument to the script and it's the path to a json file,
        # let's parse it to get our arguments.
        model_args, data_args, finetune_args, quant_args, benchmark_args, training_args = parser.parse_json_file(
            json_file=os.path.abspath(sys.argv[1]))
    else:
        # model_args, data_args, training_args, finetune_args = parser.parse_args_into_dataclasses()
        model_args, data_args, finetune_args, quant_args, benchmark_args, training_args, optim_args = \
            parser.parse_args_into_dataclasses(return_remaining_strings=True)

    # Setup logging
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    logger.setLevel(logging.INFO if is_main_process(training_args.local_rank) else logging.WARN)

    # Log on each process the small summary
    b16 = training_args.fp16 or training_args.bf16
    logger.warning(
        f"Process rank: {training_args.local_rank}, device: {training_args.device}\ndistributed training: "
        f"{bool(training_args.local_rank != -1)}, 16-bits training: {b16}"
    )
    # Set the verbosity to info of the Transformers logger (on main process only):
    if is_main_process(training_args.local_rank):
        transformers.utils.logging.set_verbosity_info()
        transformers.utils.logging.enable_default_handler()
        transformers.utils.logging.enable_explicit_format()
    logger.info(f"Training/evaluation parameters {training_args}")

    # Set seed before initializing model.
    set_seed(training_args.seed)

    # Load pretrained model and tokenizer
    #
    # Distributed training:
    # The .from_pretrained methods guarantee that only one local process can concurrently
    # download model & vocab.
    config_kwargs = {
        "cache_dir": model_args.cache_dir,
        "revision": model_args.model_revision,
        "use_auth_token": True if model_args.use_auth_token else None,
        "trust_remote_code": True if model_args.trust_remote_code else None,
        "use_cache": False if training_args.gradient_checkpointing else model_args.use_cache,
        "token": model_args.token,
    }
    if model_args.config_name:
        config = AutoConfig.from_pretrained(model_args.config_name, **config_kwargs)
    elif model_args.model_name_or_path:
        config = AutoConfig.from_pretrained(model_args.model_name_or_path, **config_kwargs)
    else:
        raise ValueError("Please provide value for model_name_or_path or config_name.")

    tokenizer_kwargs = {
        "cache_dir": model_args.cache_dir,
        "use_fast": model_args.use_fast_tokenizer,
        "revision": model_args.model_revision,
        "use_auth_token": True if model_args.use_auth_token else None,
        "add_bos_token": False,
        "add_eos_token": False,
        "token": model_args.token,
    }
    if model_args.tokenizer_name:
        tokenizer = AutoTokenizer.from_pretrained(model_args.tokenizer_name, **tokenizer_kwargs)
    elif model_args.model_name_or_path:
        tokenizer = AutoTokenizer.from_pretrained(model_args.model_name_or_path, **tokenizer_kwargs)
    else:
        raise ValueError(
            "You are instantiating a new tokenizer from scratch. This is not supported by this script."
            "You can do it from another script, save it, and load it from here, using --tokenizer_name."
        )

    # Create the dataset cache directory, if one is specified
    if data_args.dataset_cache_directory:
        os.makedirs(data_args.dataset_cache_directory, exist_ok=True)

    # Get the datasets: you can either provide your own CSV/JSON/TXT training and evaluation files (see below)
    # or just provide the name of one of the public datasets available on the hub at https://huggingface.co/datasets/
    # (the dataset will be downloaded automatically from the datasets Hub).
    #
    # For CSV/JSON files, this script will use the column called 'text' or the first column if no column called
    # 'text' is found. You can easily tweak this behavior (see below).
    #
    # In distributed training, the load_dataset function guarantee that only one local process can concurrently
    # download the dataset.
    if data_args.dataset_name:
        # Downloading and loading a dataset from the hub.
        raw_datasets = load_dataset(
            data_args.dataset_name,
            data_args.dataset_config_name,
            cache_dir=data_args.dataset_cache_directory,
            use_auth_token=True if model_args.use_auth_token else None,
            streaming=data_args.streaming,
        )
    else:
        data_files = {}
        dataset_args = {}
        if data_args.train_file:
            if not os.path.exists(data_args.train_file):
                raise FileNotFoundError("The train file does not exist at: {}".format(data_args.train_file))
            data_files["train"] = data_args.train_file
        if data_args.validation_file:
            if not os.path.exists(data_args.validation_file):
                raise FileNotFoundError("The validation file does not exist at: {}".format(data_args.validation_file))
            data_files["test"] = data_args.validation_file
        extension = (
            data_args.train_file.split(".")[-1]
            if data_args.train_file is not None
            else data_args.validation_file.split(".")[-1]
        )
        if extension == "txt":
            extension = "text"
            dataset_args["keep_linebreaks"] = data_args.keep_linebreaks
        raw_datasets = load_dataset(
            extension,
            data_files=data_files,
            cache_dir=model_args.cache_dir,
            use_auth_token=True if model_args.use_auth_token else None,
            **dataset_args,
        )

    dataset_keys = ["train"]

    for key in raw_datasets:
        if data_args.instruction_column_name:
            raw_datasets[key] = raw_datasets[key].rename_column(data_args.instruction_column_name, "instruction")

        if data_args.input_column_name:
            raw_datasets[key] = raw_datasets[key].rename_column(data_args.input_column_name, "input")

        if data_args.output_column_name:
            raw_datasets[key] = raw_datasets[key].rename_column(data_args.output_column_name, "output")

    # If no test data is there, validation_split_percentage will be used to divide the dataset.
    if "test" not in raw_datasets.keys() and training_args.do_eval:
        logger.info("Original dataset length: {}".format(len(raw_datasets["train"])))
        raw_datasets["train"] = raw_datasets["train"].shuffle(seed=data_args.dataset_seed)
        raw_datasets = raw_datasets["train"].train_test_split(test_size=data_args.validation_split_percentage)
        dataset_keys += ["test"]
        logger.info("Validation split percentage: {}".format(data_args.validation_split_percentage))
        logger.info("Train split length: {}".format(len(raw_datasets["train"])))
        logger.info("Test split length: {}".format(len(raw_datasets["test"])))

    # Get prompt strings from the user provided arguments
    prompt_dict = CHAT_PROMPT_DICT if "chat" in model_args.model_name_or_path else STANDARD_PROMPT_DICT
    prompt_dict2 = CHAT_PROMPT_DICT2 if "chat" in model_args.model_name_or_path else STANDARD_PROMPT_DICT2
    for prompt_template in [prompt_dict, prompt_dict2]:
        for k, v in prompt_dict.items():
            prompt_template[k] = prompt_template[k].replace("{prompt_with_input}", data_args.prompt_with_input)
            prompt_template[k] = prompt_template[k].replace("{prompt_without_input}", data_args.prompt_without_input)
    logger.info(prompt_dict)
    logger.info(prompt_dict2)

    # Preprocessing the datasets.
    for key in raw_datasets:
        print(key)
        prompts = create_prompts(raw_datasets[key], prompt_dict)
        system_prompts = create_system_turn(raw_datasets[key], prompt_dict2)
        columns_to_be_removed = list(raw_datasets[key].features.keys())
        raw_datasets[key] = raw_datasets[key].add_column("prompts", prompts)
        raw_datasets[key] = raw_datasets[key].add_column("system_prompts", system_prompts)
        raw_datasets[key] = raw_datasets[key].remove_columns(columns_to_be_removed)

    tokenizer.pad_token_id = 0
    tokenizer.bos_token_id = 1
    tokenizer.eos_token_id = 2
    tokenizer.padding_side = "right"  # Allow batched inference

    def tokenize(prompt, system_prompt, add_eos_token=True):
        results = tokenizer(
            prompt,
            truncation=True,
            max_length=data_args.max_seq_length,
            padding=False,
            return_tensors=None,
            add_special_tokens=False
        )
        results_system = tokenizer(
            system_prompt,
            truncation=True,
            max_length=data_args.max_seq_length,
            padding=False,
            return_tensors=None,
            add_special_tokens=False
        )
        for i in range(len(results["input_ids"])):
            if (results["input_ids"][i][-1] != tokenizer.eos_token_id and
                    len(results["input_ids"][i]) < data_args.max_seq_length and add_eos_token):
                results["input_ids"][i].append(tokenizer.eos_token_id)
                results["attention_mask"][i].append(1)

        results["labels"] = copy.deepcopy(results["input_ids"])
        for i in range(len(results_system["input_ids"])):
            for j in range(len(results_system["input_ids"][i])):
                results["labels"][i][j] = -100

        return results

    def preprocess_function(examples):
        return tokenize(examples["prompts"], examples["system_prompts"])

    with training_args.main_process_first(desc="dataset map pre-processing"):
        tokenized_datasets = raw_datasets.map(
            preprocess_function, batched=True, load_from_cache_file=not data_args.overwrite_cache
        )

    if data_args.dataset_concatenation:
        def concatenate_data(dataset, max_seq_length):
            concatenated_dataset = {}
            for column in dataset.features:
                concatenated_data = [item for sample in dataset[column] for item in sample]
                reshaped_data = [concatenated_data[i * max_seq_length:(i + 1) * max_seq_length]
                                 for i in range(len(concatenated_data) // max_seq_length)]
                concatenated_dataset[column] = reshaped_data
            return datasets.Dataset.from_dict(concatenated_dataset)

        for key in dataset_keys:
            tokenized_datasets_ = tokenized_datasets[key].remove_columns(["prompts", "system_prompts"])
            tokenized_datasets[key] = concatenate_data(tokenized_datasets_, data_args.max_seq_length)

    if training_args.do_train:
        if "train" not in tokenized_datasets:
            raise ValueError("--do_train requires a train dataset")
        train_dataset = tokenized_datasets["train"]
        if data_args.max_train_samples is not None:
            train_dataset = train_dataset.select(range(data_args.max_train_samples))

    if training_args.do_eval:
        if "test" not in tokenized_datasets:
            raise ValueError("--do_eval requires a test dataset")
        eval_dataset = tokenized_datasets["test"]
        if data_args.max_eval_samples is not None:
            eval_dataset = eval_dataset.select(range(data_args.max_eval_samples))

    # Data collator
    # This one will take care of randomly masking the tokens.
    data_collator = DataCollatorForSeq2Seq(
        tokenizer, pad_to_multiple_of=8, return_tensors="pt", padding=True
    )
    logger.info("Using data collator of type {}".format(data_collator.__class__.__name__))

    # Load model
    if model_args.model_name_or_path:
        model_dtype = torch.bfloat16 if training_args.bf16 else None
        model = AutoModelForCausalLM.from_pretrained(
            model_args.model_name_or_path,
            from_tf=bool(".ckpt" in model_args.model_name_or_path),
            config=config,
            cache_dir=model_args.cache_dir,
            revision=model_args.model_revision,
            use_auth_token=True if model_args.use_auth_token else None,
            trust_remote_code=True if model_args.trust_remote_code else None,
            torch_dtype=model_dtype,
            low_cpu_mem_usage=model_args.low_cpu_mem_usage,
            device_map=training_args.device.type if model_args.load_meta_device else None,
            token=model_args.token,
        )
        model.generation_config.pad_token_id = 0
        model.generation_config.bos_token_id = 1
        model.generation_config.eos_token_id = 2
        # model.resize_token_embeddings(len(tokenizer))
    else:
        raise ValueError("Must provide model_name_or_path to load a pretrained CausalLM model.")

    if training_args.do_train:
        if finetune_args.use_lora:
            # PEFT settings
            lora_config_dict = {
                "r": finetune_args.lora_rank,
                "lora_alpha": finetune_args.lora_alpha,
                "lora_dropout": finetune_args.lora_dropout,
                "bias": "none",
                "task_type": TaskType.CAUSAL_LM,
            }
            # Workaround to support LoraConfig with and without target modules from the helm chart. Multiple target
            # modules are coming in like ["q_proj v_proj"] from the helm chart, so they need to be split.
            finetune_args.lora_target_modules = [x for x in finetune_args.lora_target_modules if x]
            if len(finetune_args.lora_target_modules) > 0:
                target_modules = []
                for tm in finetune_args.lora_target_modules:
                    target_modules += tm.split()
                lora_config_dict["target_modules"] = target_modules
            logger.info(lora_config_dict)
            peft_config = LoraConfig(**lora_config_dict)
            model = get_peft_model(model, peft_config)
            model.print_trainable_parameters()

        # Initialize our Trainer
        if is_optimum_habana_available():
            from optimum.habana import GaudiConfig, GaudiTrainer

            gaudi_config = GaudiConfig()
            gaudi_config.use_fused_adam = True
            gaudi_config.use_fused_clip_norm = True

            trainer = GaudiTrainer(
                model=model,
                args=training_args,
                gaudi_config=gaudi_config,
                train_dataset=train_dataset if training_args.do_train else None,
                eval_dataset=eval_dataset if training_args.do_eval else None,
                tokenizer=tokenizer,
                data_collator=data_collator,
            )
        else:
            trainer = Trainer(
                model=model,
                args=training_args,
                train_dataset=train_dataset if training_args.do_train else None,
                eval_dataset=eval_dataset if training_args.do_eval else None,
                tokenizer=tokenizer,
                data_collator=data_collator,
            )

        trainer.add_callback(CustomPrinterCallback)

        training_start = datetime.now()
        logger.info("Elapsed time: {}".format(str(training_start - start_time)))
        logger.info("Training start time: {}".format(str(training_start)))

        train_result = trainer.train(resume_from_checkpoint=training_args.resume_from_checkpoint)

        training_end = datetime.now()
        logger.info("Total training time: {}".format(str(training_end - training_start)))
        logger.info("Training end time: {}".format(str(training_end)))

        model.save_pretrained(training_args.output_dir)
        tokenizer.save_pretrained(training_args.output_dir)

        # Get and log training metrics
        train_metrics = train_result.metrics
        max_train_samples = (
            data_args.max_train_samples if data_args.max_train_samples is not None else len(train_dataset)
        )
        train_metrics["train_samples"] = min(max_train_samples, len(train_dataset))
        trainer.log_metrics("train", train_metrics)
        trainer.save_metrics("train", train_metrics)
        trainer.save_state()

    if training_args.do_eval:
        eval_metrics = trainer.evaluate()

        # Get and log evaluation metrics
        max_eval_samples = data_args.max_eval_samples if data_args.max_eval_samples is not None else len(eval_dataset)
        eval_metrics["eval_samples"] = min(max_eval_samples, len(eval_dataset))

        try:
            perplexity = math.exp(eval_metrics["eval_loss"])
        except OverflowError:
            perplexity = float("inf")
        eval_metrics["perplexity"] = perplexity

        trainer.log_metrics("eval", eval_metrics)
        trainer.save_metrics("eval", eval_metrics)

    # Benchmarking and quantization is done by RANK 0
    rank = os.getenv("RANK", "0")
    if rank == "0":

        # Initialize the data loader and configs used for benchmarking and quantization
        if benchmark_args.do_benchmark or quant_args.do_quantize:
            calib_dataloader = INCDataloader(tokenized_datasets["train"],
                                             tokenizer,
                                             batch_size=training_args.per_device_eval_batch_size,
                                             max_seq_length=data_args.max_seq_length,
                                             for_calib=True)

            if benchmark_args.do_benchmark:
                from neural_compressor import benchmark
                from neural_compressor.config import BenchmarkConfig

                os.environ['NC_ENV_CONF'] = 'True'
                if benchmark_args.benchmark_cores_per_instance == -1:
                    benchmark_args.benchmark_cores_per_instance = None
                quant_backend = 'ipex' if training_args.use_ipex else 'default'
                benchmark_config = BenchmarkConfig(backend=quant_backend,
                                                   warmup=benchmark_args.benchmark_warmup,
                                                   iteration=benchmark_args.benchmark_iterations,
                                                   cores_per_instance=benchmark_args.benchmark_cores_per_instance,
                                                   num_of_instance=benchmark_args.benchmark_num_instances)

            if not training_args.do_train and quant_args.peft_model_dir:
                logger.info(f"Loading peft model from {quant_args.peft_model_dir}")
                model = PeftModel.from_pretrained(model, quant_args.peft_model_dir)

        # Benchmark the trained model
        original_throughput = original_latency = None
        if benchmark_args.do_benchmark:
            logger.info("Benchmark the fine tuned model")
            benchmark_results = benchmark.fit(model=model, config=benchmark_config, b_dataloader=calib_dataloader)
            print(benchmark_results, flush=True)
            original_latency, original_throughput = calculate_latency_and_throughput(benchmark_results)

        # Post training quantization
        if quant_args.do_quantize:
            logger.info("Post training quantization")
            from neural_compressor import quantization
            from neural_compressor.config import PostTrainingQuantConfig

            # Currently this script only supports weight only quantization
            quant_config = PostTrainingQuantConfig(
                approach="weight_only",
                op_type_dict={
                    ".*": {
                        "weight": {
                            "bits": quant_args.woq_bits,
                            "group_size": quant_args.woq_group_size,
                            "scheme": quant_args.woq_scheme,
                            "algorithm": quant_args.woq_algo,
                        },
                    },
                },
            )

            quantized_model = quantization.fit(model=model, conf=quant_config, calib_dataloader=calib_dataloader)

            if quantized_model:
                logger.info(f"Saving the quantized model to: {quant_args.quantize_output_dir}")
                quantized_model.save(quant_args.quantize_output_dir)
            else:
                logger.warning("Skipping the save of the quantized model, because the quantized_model is None")

        # Benchmark the quantized model
        int8_latency = int8_throughput = None
        if benchmark_args.do_benchmark and quant_args.quantize_output_dir is not None and \
                os.path.exists(quant_args.quantize_output_dir) and len(os.listdir(quant_args.quantize_output_dir)) > 0:
            from neural_compressor.utils.pytorch import load

            # Load the quantized model using INC
            kwargs = {'weight_only': True}
            reloaded_quantized_model = load(quant_args.quantize_output_dir, model, dataloader=calib_dataloader,
                                            **kwargs)

            # Becnhmark the quantized model
            logger.info("Benchmark the quantized model")
            int8_benchmark_results = benchmark.fit(model=reloaded_quantized_model,
                                                   config=benchmark_config,
                                                   b_dataloader=calib_dataloader)
            print(int8_benchmark_results, flush=True)
            int8_latency, int8_throughput = calculate_latency_and_throughput(int8_benchmark_results)

        # Print benchmarking results
        if original_latency:
            print("Latency before quantization: {0:.4f} ms".format(original_latency))
        if original_throughput:
            print("Throughput before quantization: {0:.4f} samples/second\n".format(original_throughput))

        if int8_latency:
            print("Latency after quantization: {0:.4f} ms".format(int8_latency))
        if int8_throughput:
            print("Throughput after quantization: {0:.4f} samples/second\n".format(int8_throughput))


if __name__ == "__main__":
    main()
