"""Make a Halloween card. Importing on a Mac builds the UI without weights."""
import os

import spaces  # Import before any CUDA initialization for ZeroGPU.
import gradio as gr

from pipeline import (
    ASTRONAUTS, CHECKPOINTS, PROMPT_PREFIX, SCARECROW,
    build_pipeline, generate_image, resolve_prompt, validate_settings,
)

UI_ONLY = os.environ.get("HALLOWEEN_UI_ONLY") == "1"
# ZeroGPU requires CUDA placement at module startup. Mac review stays CPU-only.
PIPE = build_pipeline() if os.environ.get("SPACE_ID") and not UI_ONLY else None


@spaces.GPU(duration=120)
def make_card(subject, full_prompt, seed, strength, checkpoint):
    try:
        prompt = resolve_prompt(subject, full_prompt)
        seed, strength = validate_settings(seed, strength, checkpoint)
    except ValueError as error:
        raise gr.Error(str(error)) from error
    if PIPE is None:
        raise gr.Error("This local preview shows the controls. Run on a CUDA GPU to make a card.")
    return generate_image(PIPE, prompt, seed, strength, checkpoint)


with gr.Blocks(title="Make a Halloween card") as demo:
    gr.Markdown("# Make a Halloween card\nDescribe a scene and turn it into a hand-drawn Halloween greeting with FLUX 3 Image Klein.")
    with gr.Row():
        with gr.Column():
            subject = gr.Textbox(label="What is on your card?", placeholder="A black cat watching the moon from a pumpkin patch", lines=4)
            with gr.Accordion("Advanced", open=False):
                full_prompt = gr.Textbox(label="Full prompt override", placeholder="Leave blank to use your subject with the vqx card prompt.", lines=5)
                seed = gr.Number(label="Seed", value=23, precision=0, minimum=0, maximum=2**32 - 1)
                strength = gr.Slider(label="LoRA strength", minimum=0, maximum=1.5, value=1.0, step=0.05)
                checkpoint = gr.Dropdown(label="Checkpoint", choices=list(CHECKPOINTS), value="constant_with_warmup")
            generate = gr.Button("Make my card", variant="primary")
        with gr.Column():
            image = gr.Image(label="Your Halloween card", type="pil", format="png")
    inputs = [subject, full_prompt, seed, strength, checkpoint]
    gr.Examples(
        examples=[
            [SCARECROW.removeprefix(PROMPT_PREFIX), "", 23, 1.0, "cosine"],
            [ASTRONAUTS.removeprefix(PROMPT_PREFIX), "", 23, 1.0, "constant_with_warmup"],
        ],
        inputs=inputs,
        label="Try a scene",
        cache_examples=False,
    )
    generate.click(make_card, inputs=inputs, outputs=image, concurrency_limit=1, concurrency_id="card")
    subject.submit(make_card, inputs=inputs, outputs=image, concurrency_limit=1, concurrency_id="card")

if __name__ == "__main__":
    if not UI_ONLY and PIPE is None:
        PIPE = build_pipeline()
    demo.queue(max_size=8).launch()
