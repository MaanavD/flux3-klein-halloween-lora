# Provenance

Verified on October 26, 2026.

## Source identification

All 156 images are linked to individual works in the Art Institute of Chicago collection. The supplied image directory already contained a README and metadata CSV, despite the absence of a separate source record for the zip. Those two original files are preserved under `provenance/`. The original zip compiler, selection query, and caption author remain unknown.

The original CSV contains a unique museum artwork page and IIIF image identifier for every JPEG. We checked all 156 against the museum's [official public API data archive](https://github.com/art-institute-of-chicago/api-data), downloaded from [its linked S3 archive](https://artic-api-data.s3.amazonaws.com/artic-api-data.tar.bz2). Every artwork ID, image ID, title, and artist matches. All dates match after treating a missing date as an empty CSV field. All 156 records have `is_public_domain=true` and no copyright notice. Selected record fields and the per-file checks are saved in `provenance/`.

The downloaded archive was last modified October 18, 2026. Its SHA-256 is `632d9b8796015c577ca54120a5466a8cd916ad24ff522b2650a9ef29573f7892`. The museum's public pages, live object API, and IIIF image endpoints returned HTTP 403 challenges during this research. The official data archive remained accessible.

## Specific image comparisons

We visually compared downloaded online reproductions with the local JPEGs:

- `ukiyoe_bw_0001.jpg`: [artwork 19643](https://www.artic.edu/artworks/19643), Okumura Masanobu, The Courier Kantan dreaming of Himself as a Daimyo, c. 1716/35. The [online reproduction](https://www.rawpixel.com/image/8944676/image-paper-cartoon-people) attributes the image to this exact museum page. The procession, sleeping courier, inscriptions, crop, and paper discoloration match.
- `ukiyoe_bw_0002.jpg`: [artwork 41357](https://www.artic.edu/artworks/41357), Issho, A Bat Flying near a Pine Tree, 19th century. The [online reproduction](https://www.rawpixel.com/image/8944949/bat-flying-near-pine-tree-issho) also links to the exact museum record. The bat, pine trunk, calligraphy, seals, crop, and paper marks match.

These comparisons establish matches to the museum's particular photographs, beyond a shared subject or title. As an additional check, both pairs were resized to 256 by 256 pixels and compared: mean absolute RGB differences were 2.045 and 1.548 on a 0-255 scale. The online copies have different sizes and JPEG encodings, so they are not byte-identical to the local files. Reference URLs, dimensions, and SHA-256 hashes are recorded in `provenance/image-comparisons.json`. Only these two images were visually verified against online reproductions; all 156 source records were independently verified against the official archive.

## License evidence

The museum's [Image Licensing policy](https://www.artic.edu/image-licensing) and [Open Access Images policy](https://www.artic.edu/collection-information/open-access/open-access-images) make public-domain collection images available under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). The policy text was read in the official archive's generic-page records 184 and 410. Archive paths and record timestamps are in `provenance/license-evidence.json`.

The museum's [website implementation](https://github.com/art-institute-of-chicago/artic.edu/blob/48b16f711cf52691a163ea35ef55028cdbad404f/app/Models/Api/Artwork.php#L438-L464) maps public-domain artworks to its CC0 label unless an explicit image credit or copyright notice takes precedence. No artwork in this set has a copyright notice. The image records have empty credits, explicit CC0 credits, or, for artwork 189659, the literal credit `none`. All 156 artwork records are marked public domain. The museum requests attribution by artist, title, date, and institution; these are recorded in the CSV and this documentation.

The [API documentation](https://api.artic.edu/docs/#artworks) separately places the source catalog fields used here under CC0. No artwork description field is redistributed. Caption files were supplied with the set and were preserved unchanged; their authorship was not established.

## Local inspection and preservation

The set contains 156 JPEGs and 156 matching caption files, numbered 0001 through 0156. All captions begin with `ukiyobw`. All JPEGs are RGB, with an empty EXIF block and only standard JFIF information. Of the images, 126 are 1686 pixels wide and 30 are portrait images with a 2048-pixel long side. The original README describes JPEG quality 95 and resizing, but the exact preparation pipeline was not reconstructed.

The existing BW name does not describe every image: some illustrated pages contain color. Files were retained as supplied. The new metadata CSV uses the verified source fields and preserves the original IIIF URLs, which may point to a larger image than a locally resized portrait.

All 312 image and caption files were copied without modification and verified by SHA-256 against the source directory. `SHA256SUMS` contains their hashes. The data files total 127,381,211 bytes. The original source directory was not changed.
