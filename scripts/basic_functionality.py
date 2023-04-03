""" This script demonstrates how to use the algebraic_value_editing library to generate comparisons
between two prompts. """
# %%
from typing import List
from transformer_lens.HookedTransformer import HookedTransformer

from algebraic_value_editing import completions
from algebraic_value_editing.prompt_utils import RichPrompt, get_x_vector


# %%
model: HookedTransformer = HookedTransformer.from_pretrained(
    model_name="gpt2-medium"
)

# %%
rich_prompts: List[RichPrompt] = [
    *get_x_vector(
        prompt1="I love you",
        prompt2="Fuck you",
        coeff=1.0,
        act_name=6,
        model=model,
    ),
]
completions.print_n_comparisons(
    prompt="I hate you because",
    num_comparisons=5,
    model=model,
    rich_prompts=rich_prompts,
    seed=0,
)

# %%
