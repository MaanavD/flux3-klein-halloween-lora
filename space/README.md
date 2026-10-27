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

Describe what you want on your card. **FLUX 3 Image Klein** and a trained Halloween LoRA make it into a hand-drawn Halloween greeting.

The project is still in local review. Creating a Hugging Face Space and model repository, pushing the code, and making it public are all pending. Downloaded release checkpoints stay in the ignored `inspection/checkpoints/` folder. Git excludes the `.venv`, caches, and weights.

## Run locally

Use Python 3.12. This Mac already has an isolated `.venv` for the project.

```bash
cd ~/Documents/flux3-klein-halloween-space
source .venv/bin/activate
# If recreating the environment: python3.12 -m venv .venv
python -m pip install -r requirements.txt
HALLOWEEN_UI_ONLY=1 python app.py
```

This opens all the controls without downloading the base model or using a GPU. Making a card needs CUDA; Mac inference is not supported. Outside a Space, importing `app` also builds the UI without loading weights.

```bash
HALLOWEEN_UI_ONLY=1 python -c 'import app'
python scripts/verify_local.py
```

On a CUDA machine, use the locally checked checkpoints.

```bash
HALLOWEEN_LORA_SOURCE="$PWD/inspection/checkpoints" python app.py
```

`HF_TOKEN`, or a locally cached Hugging Face login, must have access to the base model. Keep tokens out of Git. The app loads the model on CUDA at startup, before entering `@spaces.GPU`, as ZeroGPU requires. Set `HALLOWEEN_UI_ONLY=1` to try the controls locally without loading the model.

## Controls

The app puts your scene into `vqx, an old Halloween greeting card with a hand-drawn illustration of <subject>`. If you fill in Full prompt under Advanced, it uses that text as entered instead. Include `vqx` yourself in a full prompt.

Under Advanced, you can change the seed (default 23), LoRA strength (0 to 1.5, default 1), and checkpoint (`constant_with_warmup` by default, or `cosine`). The scarecrow and astronaut examples use the exact prompts from the guide's “Use it” section, with the same checkpoints. The scarecrow uses cosine; the astronauts use constant_with_warmup. The app starts with constant_with_warmup selected.

Cards use 1024×1024, 50 flow-matching Euler steps, guidance 3.5, fixed scheduler shift 6.93, an empty negative prompt, and CPU-seeded initial noise. The UI returns PNGs to avoid JPEG compression. Requests change the shared adapter selection one at a time.

## Before publishing

1. Put both LoRA files at the root of a public HF model repository, or under one public HTTPS directory. The private GitHub release is for local inspection only. Use these exact files.
   - `klein-vqx-shift4k-warmup_000002000.safetensors`
   - `klein-vqx-shift4k-cosine_000002000.safetensors`

   Set `LORA_SOURCE` in `pipeline.py` through the `HALLOWEEN_LORA_SOURCE` Space variable. Use an HF repo ID such as `owner/model-repo`, or an HTTPS directory such as `https://host.example/weights`. A public host is still to be chosen and configured. The SHA-256 checks require the exact inspected files. The app works without a GitHub token.

2. Accept any gate for [the base model](https://huggingface.co/black-forest-labs/flux-3-image-klein-base) using the account that owns the read token. Add that token as a Space secret named `HF_TOKEN`, with permission to read the gated model. A login cached on this Mac stays local to this Mac.

3. Use a Gradio Space and select ZeroGPU in its settings. The front-matter `suggested_hardware: zero-a10g` identifies the hardware in Hub metadata; it does not reserve it. The app requests the default `large` size and up to 120 seconds per generation. Current ZeroGPU `large` provides 48 GB. The actual hosted memory and duration still need checking. Hosting depends on the account's ZeroGPU entitlement. Leave `HALLOWEEN_UI_ONLY` unset in the deployed Space.

4. Read the comparison result below and the model license. Hosted GPU compatibility and pixel parity still need checking after the local import and adapter checks. The base model and its derivatives use the FLUX Kommunity License v.1.0. Apache-2.0 does not cover them. Before running a public demo or sharing the LoRA, check the end-user hosting conditions, qualifying-user provisions, required notices, and applicable filtering/review requirements in [LICENSE.md](LICENSE.md). Commercial permission depends on those terms.

Review these items before publishing. This repository has no remote configured.

## How it works

Diffusers 0.42.0 is the first released version with this architecture. It provides `Flux3AutoBlocks`, `Flux3ModularPipeline`, `Flux3Transformer2DModel`, and `Flux3LoraLoaderMixin`. Its modular pipeline differs from the older Klein pipeline. The app removes the separate 9B prompt upsampler so the trigger word and scene captions reach the model unchanged, matching the reference workflow. AI Toolkit's training dependencies stay outside this repo. See the [pinned upstream documentation](https://github.com/huggingface/diffusers/blob/v0.42.0/docs/source/en/api/pipelines/flux3.md).

Each release checkpoint contains 516 BF16 tensors in 258 rank-32 A/B pairs. The Diffusers loader detects and renames keys such as `diffusion_model.content_mode_blocks.image.0.attn_out.lora_A.weight`. Rank 32 and training alpha 32 give an effective alpha/rank scale of 1. The app keeps adapters unmerged in FP32, as in `make_card.py`, while the base transformer, text encoder, and VAE use BF16. [Upstream converter](https://github.com/huggingface/diffusers/blob/v0.42.0/src/diffusers/loaders/lora_conversion_utils.py#L2576), [loader](https://github.com/huggingface/diffusers/blob/v0.42.0/src/diffusers/loaders/lora_pipeline.py#L5984).

The checkpoint resolver uses one source for both files and checks their SHA-256 hashes before loading. The base model stays loaded when you switch adapters. The app places the model on the device before entering the GPU-decorated function, following [ZeroGPU guidance](https://huggingface.co/docs/hub/spaces-zerogpu).

See [RESEARCH.md](RESEARCH.md) for sources, package compatibility, and license details. `requirements.txt` pins the direct runtime dependencies. `verification/local.json` records the Mac environment used for these checks.

## Checks

- On the Mac, `HALLOWEEN_UI_ONLY=1 python -c 'import app'` passes and builds all the Gradio controls without downloading the base model. Headless Chrome also rendered the running app. The local screenshot is `verification/ui.png`.
- Both checkpoints pass SHA-256 checks. All 516 converted tensor names and shapes per checkpoint match the full Diffusers transformer on the meta device. Prompt reconstruction, input validation, adapter selection, seed, resolution, and inference-call settings pass CPU checks.
- The single 10-minute H200 Slurm job (`1287590`) made the reference scarecrow image (19.20 seconds of generation). The app then stopped before inference with `ModuleNotFoundError: No module named numpy`. Its isolated review venv did not inherit the toolkit venv site-packages. I corrected the harness and checked its CPU imports afterward. I kept to the one-job limit. App GPU generation and pixel parity still need verification. See `verification/parity.json` and the local log `verification/slurm-1287590.out`.

The comparison runs the unchanged reference script in `verification/reference_make_card.py` with its original toolkit venv. Its `--out reference.png` keeps lossless pixels. The app runs separately with Diffusers 0.42.0 in an isolated review venv. It uses upstream conversion to load its components from the same cached BF16 base weights, avoiding a second model download. `verification/parity.json` records the current failure and the limits of these checks. A successful future run will record versions and image-error metrics. Another GPU comparison needs separate authorization because the one allowed job has been used. The harness is in `scripts/parity_cluster.py` and `scripts/parity.sbatch`.

I kept the submitted Slurm script as `verification/parity-submitted.sbatch`; the corrected harness is `scripts/parity.sbatch`. I moved a staging copy from the cluster review folder root into `scripts/` and kept the submitted version. Authorized cluster scratch files live at `/mnt/data/maanav/halloween-space-review-20261026`. I left the existing training environment and dataset files unchanged and kept every file.

## License and attribution

Klein is by Black Forest Labs. The base model and its derivatives are covered by the [FLUX Kommunity License v.1.0](LICENSE.md). It permits non-commercial use and qualifying commercial output generation subject to the full terms. The Qwen3-VL-4B-Instruct text encoder has its separate Apache-2.0 license. Diffusers and Transformers have their own upstream licenses.

Maanav Dalal trained the Halloween LoRA with AI Toolkit commit `04733873cf1da8060fce01316ec45daedbd4a918`, rank 32 and alpha 32. These two checkpoints are from training step 2,000. The app adds a Gradio interface and Diffusers inference for the trained derivative, keeping the base weights unchanged. Preserve the base license, attribution, modification notice, and any additional upstream notices when distributing weights.
