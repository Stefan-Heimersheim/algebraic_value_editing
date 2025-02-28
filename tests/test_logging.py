""" Test suite for logging.py """

import pytest

import numpy as np
import pandas as pd
from transformer_lens import HookedTransformer

from algebraic_value_editing import (
    logging,
    completion_utils,
    prompt_utils,
    utils,
)

utils.enable_ipython_reload()


@pytest.fixture(name="model")
def fixture_model() -> HookedTransformer:
    """Test fixture that returns a small pre-trained transformer used
    for fast logging testing."""
    return HookedTransformer.from_pretrained(
        model_name="attn-only-2l", device="cpu"
    )


# In order for these tests to work, you must have a wandb account and
# have set up your wandb API key.  See https://docs.wandb.ai/quickstart
def test_logging(model):
    """Tests a sweep over prompts with logging enabled.  Verifies that
    the correct data is uploaded to a new wandb run."""
    # Perform a completion test
    results: pd.DataFrame = completion_utils.gen_using_rich_prompts(
        model=model,
        rich_prompts=[
            prompt_utils.RichPrompt(
                prompt="Love",
                act_name=prompt_utils.get_block_name(block_num=0),
                coeff=1.0,
            ),
            prompt_utils.RichPrompt(
                prompt="Fear",
                act_name=prompt_utils.get_block_name(block_num=0),
                coeff=-1.0,
            ),
        ],
        prompt_batch=["This is a test", "Let's talk about"],
        log={"tags": ["test"], "notes": "testing"},
    )
    # Download the artifact data and convert to a DataFrame
    results_logged = logging.get_objects_from_run(
        logging.last_run_info["path"], flatten=True
    )[0]

    # Change the dtype of the loss column; seems that wandb doesn't
    # track dtypes in uploaded tables, which likely doesn't matter but
    # is annoying for perfect round-trip reproduction.
    results_logged["loss"] = results_logged["loss"].astype(np.float32)

    # Compare with the reference DataFrame
    pd.testing.assert_frame_equal(results, results_logged)
