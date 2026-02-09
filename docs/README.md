# AsciiDoc Documentation

## Build

### Using Docker

```bash
docker run --rm -it -v $PWD:/documents/ asciidoctor/docker-asciidoctor \
    asciidoctor                                                        \
        --base-dir /documents/docs                                     \
        --destination-dir /documents/build                             \
        --failure-level WARN                                           \
        --verbose                                                      \
        docs/index.adoc
```

or

```bash
docker run --rm -it -v $PWD:/documents/ asciidoctor/docker-asciidoctor \
    asciidoctor-pdf                                                    \
        -r asciidoctor-mathematical                                    \
        --base-dir /documents/docs                                     \
        --destination-dir /documents/build                             \
        --failure-level WARN                                           \
        --verbose                                                      \
        docs/index.adoc
```

### Using Asciidoctor

Install [Asciidoctor](https://docs.asciidoctor.org/asciidoctor/latest/install/)
and run

```bash
asciidoctor                      \
    --base-dir docs              \
    --destination-dir $PWD/build \
    --failure-level WARN         \
    --verbose                    \
    docs/index.adoc
```

### Using Asciidoctor PDF

Install [Ruby](https://www.ruby-lang.org/en/documentation/installation/),
[Asciidoctor PDF](https://docs.asciidoctor.org/pdf-converter/latest/install/),
and [asciidoctor-mathematical](https://docs.asciidoctor.org/pdf-converter/latest/stem/),
then run

```bash
asciidoctor-pdf                  \
    --base-dir docs              \
    --destination-dir $PWD/build \
    --failure-level WARN         \
    -r asciidoctor-mathematical  \
    --verbose                    \
    docs/index.adoc
```
