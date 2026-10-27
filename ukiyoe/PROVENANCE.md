# Provenance

Verified on October 26, 2026.

## Sources

All 156 images link to individual works in the Art Institute of Chicago collection. The supplied image directory had a README and metadata CSV, but no separate source record for the zip. I kept both original files under `provenance/`. I don't know who put the zip together, which query they used to select the works, or who wrote the captions.

The original CSV contains a unique museum artwork page and IIIF image identifier for every JPEG. I checked all 156 against the museum's [official public API data archive](https://github.com/art-institute-of-chicago/api-data), downloaded from [its linked S3 archive](https://artic-api-data.s3.amazonaws.com/artic-api-data.tar.bz2). Every artwork ID, image ID, title, and artist matches. All dates match when a missing date counts as an empty CSV field. All 156 records have `is_public_domain=true` and no copyright notice. I saved selected record fields and the checks for each file in `provenance/`.

The downloaded archive was last modified October 18, 2026. Its SHA-256 is `632d9b8796015c577ca54120a5466a8cd916ad24ff522b2650a9ef29573f7892`. The museum's public pages, live object API, and IIIF image endpoints returned HTTP 403 challenges during these checks. I could still download the official data archive.

## Image comparisons

I compared downloaded online copies with the local JPEGs by eye.

- `ukiyoe_bw_0001.jpg`: [artwork 19643](https://www.artic.edu/artworks/19643), Okumura Masanobu, The Courier Kantan dreaming of Himself as a Daimyo, c. 1716/35. The [online reproduction](https://www.rawpixel.com/image/8944676/image-paper-cartoon-people) credits this museum page. The procession, sleeping courier, inscriptions, crop, and paper discoloration match.
- `ukiyoe_bw_0002.jpg`: [artwork 41357](https://www.artic.edu/artworks/41357), Issho, A Bat Flying near a Pine Tree, 19th century. The [online reproduction](https://www.rawpixel.com/image/8944949/bat-flying-near-pine-tree-issho) also links to the museum record. The bat, pine trunk, calligraphy, seals, crop, and paper marks match.

These details match the museum's photographs, down to the crop and paper marks. I also resized both pairs to 256 by 256 pixels and compared them. Mean absolute RGB differences were 2.045 and 1.548 on a 0-255 scale. The online copies have different sizes and JPEG encodings, so they are not byte-identical to the local files. I recorded reference URLs, dimensions, and SHA-256 hashes in `provenance/image-comparisons.json`. I checked these two images against online copies by eye, and independently checked all 156 source records against the official archive.

## License evidence

The museum's [Image Licensing policy](https://www.artic.edu/image-licensing) and [Open Access Images policy](https://www.artic.edu/collection-information/open-access/open-access-images) make public-domain collection images available under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). I read the policy text in the official archive's generic-page records 184 and 410. Archive paths and record timestamps are in `provenance/license-evidence.json`.

The museum's [website implementation](https://github.com/art-institute-of-chicago/artic.edu/blob/48b16f711cf52691a163ea35ef55028cdbad404f/app/Models/Api/Artwork.php#L438-L464) maps public-domain artworks to its CC0 label unless an image credit or copyright notice overrides it. No artwork in this set has a copyright notice. The image records have empty credits, explicit CC0 credits, or, for artwork 189659, the literal credit `none`. All 156 artwork records are marked public domain. The museum asks for the artist, title, date, and institution in attributions. These are in the CSV and this documentation.

The [API documentation](https://api.artic.edu/docs/#artworks) separately places the source catalog fields used here under CC0. The set leaves out the artwork description field. I kept the supplied caption files unchanged. I haven't established who wrote them.

## Local files

The set contains 156 JPEGs and 156 matching caption files, numbered 0001 through 0156. All captions begin with `ukiyobw`. All JPEGs are RGB, with an empty EXIF block and only standard JFIF information. Of the images, 126 are 1686 pixels wide and 30 are portrait images with a 2048-pixel long side. The original README describes JPEG quality 95 and resizing. I haven't reconstructed the exact steps used to prepare the images.

Some illustrated pages contain color, despite the BW name. I kept the files as supplied. The new metadata CSV uses the verified source fields and preserves the original IIIF URLs, which may point to a larger image than a locally resized portrait.

I copied all 312 image and caption files unchanged and checked their SHA-256 hashes against the source directory. `SHA256SUMS` contains their hashes. The data files total 127,381,211 bytes. I left the original source directory unchanged.
