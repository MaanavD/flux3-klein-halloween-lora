# Ukiyo-e BW LoRA dataset

156 JPEG images and 156 text captions. Each caption has the same file name as its image and starts with the trigger word `ukiyobw`.

The set is for FLUX 3 Image Klein LoRA training with AI Toolkit. It contains Japanese prints and illustrated book pages. Some images contain color, despite the folder name `ukiyoe_bw`.

The images come from the [Art Institute of Chicago collection](https://www.artic.edu/collection). The museum marks all 156 works as public domain. The images and included source catalog fields are available under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). See the museum's [image licensing policy](https://www.artic.edu/image-licensing) and [API documentation](https://api.artic.edu/docs/).

`ukiyoe_bw/metadata.csv` lists each file's title, artist, date when known, license, artwork page, image URL, and museum IDs. See [PROVENANCE.md](PROVENANCE.md) for the source checks and their limits. I don't know who put the original zip together.

I copied the images and caption files unchanged. `SHA256SUMS` records their SHA-256 hashes. Check them from this directory.

```sh
shasum -a 256 -c SHA256SUMS
```
