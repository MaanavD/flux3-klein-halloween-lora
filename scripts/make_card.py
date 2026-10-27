"""Make a Halloween card with FLUX 3 Image Klein and a LoRA checkpoint.

Run this from the AI Toolkit root, with its venv active.
  python /path/to/make_card.py --lora halloween-lora_000002000.safetensors \
    --prompt 'vqx, an old Halloween greeting card with a hand-drawn illustration of ...' --out card.jpg
"""
import argparse

import torch
from extensions_built_in.diffusion_models.flux3.flux3 import Flux3Model
from toolkit.config_modules import GenerateImageConfig, ModelConfig, NetworkConfig
from toolkit.lora_special import LoRASpecialNetwork

p = argparse.ArgumentParser()
p.add_argument("--lora", required=True, help="path to your .safetensors checkpoint")
p.add_argument("--prompt", required=True, help="start your prompt with the trigger word, vqx")
p.add_argument("--out", default="card.jpg")
p.add_argument("--seed", type=int, default=23)
p.add_argument("--strength", type=float, default=1.0)
p.add_argument("--steps", type=int, default=50)
p.add_argument("--guidance", type=float, default=3.5)
p.add_argument("--rank", type=int, default=32, help="use the rank you trained with")
args = p.parse_args()

sd = Flux3Model(device="cuda:0", dtype="bf16",
                model_config=ModelConfig(name_or_path="black-forest-labs/flux-3-image-klein-base", arch="flux3", dtype="bf16"))
sd.load_model()
for part in (sd.model, sd.text_encoder, sd.vae):
    part.requires_grad_(False)
    part.eval()

net_config = NetworkConfig(type="lora", linear=args.rank, linear_alpha=args.rank)
network = LoRASpecialNetwork(
    text_encoder=sd.text_encoder, unet=sd.get_model_to_train(), lora_dim=args.rank, alpha=args.rank,
    train_text_encoder=False, train_unet=True, is_transformer=True, transformer_only=net_config.transformer_only,
    base_model=sd, network_config=net_config, target_lin_modules=sd.target_lora_modules)
network.apply_to(sd.text_encoder, sd.get_model_to_train(), False, True)
network.force_to(torch.device("cuda:0"), torch.float32)
network._update_torch_multiplier()
network.can_merge_in = False
sd.network = network
network.load_weights(args.lora)

sd.generate_images([GenerateImageConfig(
    prompt=args.prompt, negative_prompt="", width=1024, height=1024, seed=args.seed,
    guidance_scale=args.guidance, num_inference_steps=args.steps, network_multiplier=args.strength,
    output_path=args.out, output_ext="jpg", add_prompt_file=False)], sampler="flowmatch")
print("saved", args.out)
