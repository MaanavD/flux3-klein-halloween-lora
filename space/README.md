---
title: Make a Halloween card
emoji: 🎃
colorFrom: red
colorTo: yellow
sdk: gradio
sdk_version: 6.30.0
python_version: '3.12'
app_file: app.py
pinned: false
license: other
license_name: flux-kommunity-license
license_link: https://huggingface.co/black-forest-labs/flux-3-image-klein-base/blob/main/LICENSE.md
suggested_hardware: zero-a10g
---

# Make a Halloween card

Describe a scene and turn it into a hand-drawn Halloween greeting with **FLUX 3 Image Klein** and a trained Halloween LoRA.

This is a local review project. No Hugging Face Space or model repository has been created, and nothing has been pushed or made public. Downloaded release checkpoints are kept locally in the ignored `inspection/checkpoints/` folder. The `.venv`, caches, and weights are excluded from Git.

## Local review

Python 3.12 is recommended. The project already has an isolated `.venv` on this Mac.

```bash
cd ~/Documents/flux3-klein-halloween-space
source .venv/bin/activate
# If recreating the environment: python3.12 -m venv .venv
python -m pip install -r requirements.txt
HALLOWEEN_UI_ONLY=1 python app.py
```

This opens the complete UI without downloading the base model or using a GPU. Image generation needs CUDA; Mac inference is not supported. Importing `app` also builds the UI without loading weights outside a Space:

```bash
HALLOWEEN_UI_ONLY=1 python -c 'import app'
python scripts/verify_local.py
```

On a CUDA machine, use the locally inspected checkpoints:

```bash
HALLOWEEN_LORA_SOURCE="$PWD/inspection/checkpoints" python app.py
```

`HF_TOKEN`, or a locally cached Hugging Face login, must have access to the base model. Do not commit a token. Model loading happens at startup on CUDA before entering `@spaces.GPU`, as required by ZeroGPU. `HALLOWEEN_UI_ONLY=1` disables loading during local UI review.

## Controls

The subject becomes `vqx, an old Halloween greeting card with a hand-drawn illustration of <subject>`. The advanced full prompt override takes precedence and is sent exactly as entered. Include `vqx` yourself when using an override.

The advanced controls provide seed (default 23), LoRA strength (0 to 1.5, default 1), and checkpoint (`constant_with_warmup` by default, or `cosine`). The scarecrow and astronaut examples reconstruct the exact prompts from the guide's “Use it” section. Their checkpoint selections match the guide: cosine for the scarecrow and constant_with_warmup for the astronauts. The app's initial checkpoint default remains constant_with_warmup.

Generation uses 1024×1024, 50 flow-matching Euler steps, guidance 3.5, fixed scheduler shift 6.93, an empty negative prompt, and CPU-seeded initial noise. PNG output avoids JPEG compression in the UI. Only one request at a time can modify the shared adapter selection.

## Before publishing

1. **Host both LoRA files.** The private GitHub release is used only for local inspection. Put the following exact files at the root of a publicly accessible HF model repository, or under one public HTTPS directory:
   - `klein-vqx-shift4k-warmup_000002000.safetensors`
   - `klein-vqx-shift4k-cosine_000002000.safetensors`

   Set the single `LORA_SOURCE` setting in `pipeline.py` through the `HALLOWEEN_LORA_SOURCE` Space variable. Use an HF repo ID such as `owner/model-repo`, or an HTTPS directory such as `https://host.example/weights`. No public host is invented or configured in this review project. SHA-256 checks require the exact inspected files. No GitHub token is needed by the app.

2. **Base-model access.** Accept any gate for [the base model](https://huggingface.co/black-forest-labs/flux-3-image-klein-base) using the account that owns the read token. Add that token as a Space **secret** named `HF_TOKEN`, with permission to read the gated model. A login cached on this Mac does not carry over to a Space.

3. **Select ZeroGPU hardware.** Use a Gradio Space and select ZeroGPU in its settings. The front-matter `suggested_hardware: zero-a10g` is the Hub's metadata identifier, not a hardware reservation. The app requests the default `large` size and up to 120 seconds per generation. Current ZeroGPU `large` provides 48 GB; actual hosted memory and duration still need verification. Hosting availability depends on the account's ZeroGPU entitlement. Do not set `HALLOWEEN_UI_ONLY` in the deployed Space.

4. **Review the comparison result below and the model license.** The local import and adapter checks do not establish hosted GPU compatibility or pixel parity. The base model and its derivatives use the FLUX Kommunity License v.1.0, rather than Apache-2.0. Before operating a public demo or distributing the LoRA, check the end-user hosting conditions, qualifying-user provisions, required notices, and applicable filtering/review requirements in [LICENSE.md](LICENSE.md). This project is not an assertion of blanket commercial permission.

Only publish after reviewing these items. This repository has no remote configured.

## How it works

**Diffusers 0.42.0**, the first released version containing this architecture, provides `Flux3AutoBlocks`, `Flux3ModularPipeline`, `Flux3Transformer2DModel`, and `Flux3LoraLoaderMixin`. Its modular pipeline is different from the older Klein pipeline. The separate 9B prompt upsampler is removed so the trigger word and supplied scene captions reach the model unchanged, matching the reference workflow. No AI Toolkit training dependencies are vendored. [Pinned upstream documentation](https://github.com/huggingface/diffusers/blob/v0.42.0/docs/source/en/api/pipelines/flux3.md).

Both real release assets contain **516 BF16 tensors, 258 rank-32 A/B pairs**. Keys such as `diffusion_model.content_mode_blocks.image.0.attn_out.lora_A.weight` are natively detected and renamed by the Diffusers loader. Rank 32 and training alpha 32 give an effective alpha/rank scale of 1. The app keeps adapters unmerged in FP32, as in `make_card.py`, while the base transformer, text encoder, and VAE use BF16. [Upstream converter](https://github.com/huggingface/diffusers/blob/v0.42.0/src/diffusers/loaders/lora_conversion_utils.py#L2576), [loader](https://github.com/huggingface/diffusers/blob/v0.42.0/src/diffusers/loaders/lora_pipeline.py#L5984).

The checkpoint resolver accepts one common source for both files and validates their SHA-256 values before loading. Switching adapters does not reload the base model. Model placement happens before the GPU-decorated function, following [ZeroGPU guidance](https://huggingface.co/docs/hub/spaces-zerogpu).

See [RESEARCH.md](RESEARCH.md) for source evidence, package compatibility, and license details. Direct runtime dependencies are pinned in `requirements.txt` and the reviewed Mac environment is recorded in `verification/local.json`.

## Verification

- Mac: `HALLOWEEN_UI_ONLY=1 python -c 'import app'` passes and constructs the complete Gradio UI without a base-model download. Headless Chrome also rendered the running app successfully; the local screenshot is `verification/ui.png`.
- Both actual checkpoints: SHA-256 verified; all 516 converted tensor names and shapes per checkpoint match the full Diffusers transformer on the meta device. Prompt reconstruction, input validation, adapter selection, seed, resolution, and inference-call settings pass CPU checks.
- Cluster: the single 10-minute H200 Slurm job (`1287590`) generated the reference scarecrow image successfully (19.20 seconds of generation), then the app process stopped before inference with `ModuleNotFoundError: No module named numpy`. The isolated review venv did not inherit the toolkit venv site-packages. The harness was corrected and its CPU imports checked afterward. The one-job limit was honored: **app GPU generation and pixel parity remain unverified**. See `verification/parity.json` and the local log `verification/slurm-1287590.out`.

The comparison uses the unmodified reference script in `verification/reference_make_card.py` with its original toolkit venv. Its `--out reference.png` retains lossless pixels. The app runs separately with Diffusers 0.42.0 in an isolated review venv; its components are initialized from the exact same cached BF16 base weights using upstream conversion, avoiding a second model download. The current failure and verification limits are recorded in `verification/parity.json`; the harness records versions and image-error metrics on a successful future run. Any additional GPU comparison requires separate authorization because the one allowed job has been used. The harness is in `scripts/parity_cluster.py` and `scripts/parity.sbatch`.

The originally submitted Slurm script is preserved as `verification/parity-submitted.sbatch`; the corrected harness is `scripts/parity.sbatch`. A staging copy initially landed at the cluster review folder root and was moved into `scripts/`, preserving the submitted version. Authorized cluster scratch files live at `/mnt/data/maanav/halloween-space-review-20261026`; no existing training environment or dataset files were changed. No files were deleted.

## License and attribution

FLUX 3 Image Klein is by Black Forest Labs. The base model and its derivatives are covered by the [FLUX Kommunity License v.1.0](LICENSE.md). It permits non-commercial use and qualifying commercial output generation subject to the full terms. The Qwen3-VL-4B-Instruct text encoder has its separate Apache-2.0 license. Diffusers and Transformers have their own upstream licenses.

The Halloween LoRA was trained by Maanav Dalal with AI Toolkit commit `04733873cf1da8060fce01316ec45daedbd4a918`, rank 32 and alpha 32. These two checkpoints are from training step 2,000. This application adds a Gradio interface and Diffusers inference around the trained derivative; it does not alter the base weights. Preserve the base license, attribution, modification notice, and any additional upstream notices when distributing weights.
