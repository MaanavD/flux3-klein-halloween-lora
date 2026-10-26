# FLUX 3 Image Klein Halloween postcard LoRA

A LoRA training set of 65 Halloween postcards from about 1900 to 1920, captioned with the trigger word `vqx`, plus the configs to train it on FLUX 3 Image Klein with [AI Toolkit](https://github.com/ostris/ai-toolkit) by ostris at commit `04733873cf1da8060fce01316ec45daedbd4a918`.

## Layout

```
halloween/    65 .jpg images, 65 .txt captions, metadata.csv
configs/    AI Toolkit configs
```

- `halloween-lora-cosine.yaml`: 4,000 steps, cosine learning rate schedule.
- `halloween-lora-warmup.yaml`: the same, with a constant schedule after 200 warmup steps.

## Train

1. Clone AI Toolkit and check out the commit above.
2. In the config, set `folder_path` to the absolute path of `halloween/` and `training_folder` to your output directory.
3. From the AI Toolkit root, run:

```
python run.py configs/halloween-lora-cosine.yaml
```

## Image sources

49 images come from The Public Domain Review and 16 from Wikimedia Commons. `halloween/metadata.csv` lists the source page and license for each image.

Trained weights will be attached to a release later.
