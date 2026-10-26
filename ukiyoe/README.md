# Ukiyo-e BW LoRA dataset

156 JPEG images with 156 same-named text captions. Every caption starts with the trigger word `ukiyobw`.

Made for FLUX 3 Image Klein LoRA training with AI Toolkit. The set contains Japanese prints and illustrated book pages. Despite its existing `ukiyoe_bw` name, some images contain color.

The images come from the [Art Institute of Chicago collection](https://www.artic.edu/collection). All 156 corresponding museum records mark the works as public domain. The images and included source catalog fields are available under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). See the museum's [image licensing policy](https://www.artic.edu/image-licensing) and [API documentation](https://api.artic.edu/docs/).

`ukiyoe_bw/metadata.csv` lists each file's title, artist, date when known, license, artwork page, image URL, and museum IDs. [PROVENANCE.md](PROVENANCE.md) explains the source verification and its limits. The original compiler of the supplied zip is unknown.

Images and caption files were copied unchanged. `SHA256SUMS` records their SHA-256 hashes. Verify from this directory with:

```sh
shasum -a 256 -c SHA256SUMS
```
