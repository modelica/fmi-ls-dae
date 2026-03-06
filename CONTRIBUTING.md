# Contributing to This Project

Please take a moment to review this document in order to make the contribution
process easy and effective for everyone involved.

Following these guidelines helps to communicate that you respect the time of the
developers managing and developing this open source project. In return, they
should reciprocate that respect in addressing your issue or assessing patches
and features.

## Building the Specification Document

The FMI-LS-DAE Specification is written in [AsciiDoc][asciidoc], a
plain-text mark-up format that can be converted to HTML, PDF and
[other formats][asciidoctor-formats].

If you haven't already done so, [clone][github-clone] the repository with:

```sh
git clone https://github.com/modelica/fmi-ls-dae.git --recurse-submodules
```

To build the HTML document locally you have two alternatives.

### Alternative 1: Docker (recommended)

1. Install [Docker][docker] or [Podman][podman]

If you use [VS Code][vscode] and have [Docker][docker] installed, you can use
the built-in tasks to build the document. Open the Command Palette
(`Ctrl+Shift+P`) and run **Tasks: Run Build Task**, then select one of:

- **`build-doc-docker-html`** — builds the HTML document using Docker (default)
- **`build-doc-docker-pdf`** — builds the PDF document using Docker

The output is placed in the `build/` directory.

To build manually from the command line:

- **Linux, Mac:**

  ```sh
  docker run \
    --rm \
    --user $(id -u):$(id -g) \
    -e HOME=/tmp \
    -v $PWD:/documents/ \
    asciidoctor/docker-asciidoctor \
    asciidoctor \
      --base-dir /documents/docs \
      --destination-dir /documents/build \
      --failure-level WARN \
      --backend html5 \
      --verbose \
      docs/index.adoc
  ```

  where `$PWD` is the current directory. If the command is not called in the
  directory of the cloned repository, the path has to be given explicitly.

- **Windows:**

  ```sh
  docker run ^
    --rm ^
    -v %cd%:/documents/ ^
    asciidoctor/docker-asciidoctor ^
    asciidoctor ^
      --base-dir /documents/docs ^
      --destination-dir /documents/build ^
      --failure-level WARN ^
      --backend html5 ^
      --verbose ^
      docs/index.adoc
  ```

  where `%cd%` is the current directory. If the command is not called in the
  directory of the cloned repository, the path has to be given explicitly.

### Alternative 2: Ruby and the AsciiDoctor gem

1. [Install Ruby][ruby-install]
2. Install the [AsciiDoctor Ruby gem][asciidoctor-gem]

If you use [VS Code][vscode] and have the gems installed, you can use the
built-in tasks. Open the Command Palette (`Ctrl+Shift+P`) and run
**Tasks: Run Build Task**, then select one of:

- **`build-doc-html`** — builds the HTML document
- **`build-doc-pdf`** — builds the PDF document

The output is placed in the `build/` directory.

To build manually from the command line:

```sh
asciidoctor \
  --base-dir docs \
  --destination-dir build \
  --failure-level WARN \
  --verbose \
  --backend html5 \
  docs/index.adoc
```

The generated `build/index.html` can be viewed with any modern web browser.

## Validating the Files

### XSD Schema and XML Files

`xmllint` is part of the `libxml2` package. Install it with:

- **Ubuntu/Debian:** `sudo apt install libxml2-utils`
- **macOS:** `brew install libxml2`
- **Windows:** install via [Chocolatey][choco]: `choco install xsltproc`

To validate the FMI-LS-DAE manifest schema run:

```sh
xmllint --noout --schema XMLSchema.xsd  schema/fmi3LayeredStandardDaeManifest.xsd
```

To validate all XML examples run:

```sh
xmllint --noout --schema schema/fmi3LayeredStandardDaeManifest.xsd examples/**/*.xml
```

### Pre-commit Hooks

The repository uses [pre-commit][pre-commit] to enforce the whitespace rules
listed in the [Formatting Rules](#formatting-rules) section automatically.

To install and enable the hooks locally:

```sh
pip install pre-commit
pre-commit install
```

Once installed, the hooks run automatically on every `git commit`.
To run them manually on all files:

```sh
pre-commit run --all-files
```

## Using the Issue Tracker

The [issue tracker][fmi-ls-dae-new-issue] is the preferred channel for
[Bug reports](#bug-reports), [Feature requests](#feature-requests), and
submitting [Pull requests](#pull-requests), but please respect the following
restrictions:

- **Do not** use the issue tracker for personal support requests (use
  [Stack Overflow][stackoverflow]).
- **Do not** derail or troll issues. Keep the discussion on topic and respect
  the opinions of others.

### Bug Reports

A bug is a _demonstrable problem_ that is caused by the code in the repository.
Good bug reports are extremely helpful - thank you!

**Guidelines for bug reports:**

1. **Use the GitHub issue search** -- check if the issue has already been
   reported.
2. **Check if the issue has been fixed** -- try to reproduce it using the latest
   `main` or development branch in the repository.
3. **Isolate the problem** -- create a reduced test case or example.

A good bug report shouldn't leave others needing to chase you up for more
information. Please try to be as detailed as possible in your report. What is
your environment? What steps will reproduce the issue? What browser(s) and OS
experience the problem? What would you expect to be the outcome? All these
details will help people to fix any potential bugs.

### Feature Requests

Feature requests are welcome. But take a moment to find out whether your idea
fits with the scope and aims of the project. It's up to **you** to make a strong
case to convince the project's developers of the merits of this feature. Please
provide as much detail and context as possible.

## Commit Messages

Please follow [the seven rules of a great Git commit message][git-commit-rules]
when committing your changes:

- Separate subject from body with a blank line
- Limit the subject line to 50 characters
- Capitalize the subject line
- Do not end the subject line with a period
- Use the imperative mood in the subject line
- Wrap the body at 72 characters
- Use the body to explain what and why vs. how

## Pull Requests

Good pull requests - patches, improvements, new features - are a fantastic help.
They should remain focused in scope and avoid containing unrelated commits.

**Please ask first** before embarking on any significant pull request (e.g.
implementing features, refactoring code, porting to a different language),
otherwise you risk spending a lot of time working on something that the
project's developers might not want to merge into the project.

Please adhere to the coding conventions used throughout a project (indentation,
accurate comments, etc.) and any other requirements (such as test coverage).

### Pull Request Workflow

1. [Fork][github-fork-repo] the project, clone your fork, and configure the
   remotes:

   ```sh
   # Clone your fork of the repo into the current directory
   git clone https://github.com/<your-username>/fmi-ls-dae
   # Navigate to the newly cloned directory
   cd fmi-ls-dae
   # Assign the original repo to a remote called "upstream"
   git remote add upstream https://github.com/modelica/fmi-ls-dae
   ```

2. If you cloned a while ago, get the latest changes from upstream:

   ```sh
   git switch main
   git pull upstream main
   ```

3. Create a new topic branch (off the main project development branch) to
   contain your feature, change, or fix:

   ```sh
   git switch -c <topic-branch-name>
   ```

4. Commit your changes in logical chunks. Please adhere to the above rules when
   crafting [Commit messages](#commit-messages) or your code is unlikely be
   merged into the main project. Use Git's [interactive rebase][git-rebase]
   feature to tidy up your commits before making them public.

5. Locally merge (or rebase) the upstream development branch into your topic
   branch:

   ```sh
   git pull [--rebase] upstream main
   ```

6. Push your topic branch up to your fork:

   ```sh
   git push origin <topic-branch-name>
   ```

7. [Open a Pull Request][github-pull-request] with a clear title and
   description.

> [!IMPORTANT]
> By submitting a patch, you agree to allow the project owner to
license your work under the same license as that used by the project.

## Branching and Versioning

We use a branching scheme with _support_ branches that allows us to maintain
multiple major and minor releases concurrently.

- **Main development branch `main`:** Holds the latest development version. This
  is where the _next_ version of the standard is developed.

- **Support branches `support/v<major>{.<minor>}.x`:** Upon every major release
  the latest version of `main` is tagged `v<major>.0`. The maintenance of this
  release is performed on a support branch `support/v<major>.x` starting at this
  tag. Examples: `support/v3.x`, `support/v2.0.x`

- **Tags `v<major>.<minor>{.<patch>}{-{alpha|beta|rc}.<number>}`:**
  Releases and pre-releases are tagged on the respective branches following the
  [Semantic Versioning][semver] when the API, XSD schema or file structure of
  the FMU archive change. Examples: `v3.0-alpha.3`, `v3.0-beta.2`, `v3.0-rc.1`,
  `v3.0`

```txt
main
  |
  +--->+ branch "support/v2.0.x", tag "v2.0.1"
  |    |
  |    + tag "v2.0.2"
  |
  +<--- merge PR "fix-typo-in-fmi-spec"
  |
  + tag "v3.0-alpha.6"
  |
  +--->+ branch "support/v3.x", tag "v3.0"
  |    |
  |    +--->+ branch "support/v3.0.x", tag "v3.0.1"
  |    |    |
  |    |    + tag "v3.0.1"
  |    |
  |    + tag "v3.1"
  |    |
  .    .
  .    .
```

## Corporate Contributor License Agreement

All contributors have to sign the [Corporate Contributor License
Agreement][fmi-ccla] or the [Contributor License Agreement of the Modelica
Association][modelica-cla]. Therefore, the first step is getting your company to
agree and sign one of the CLAs. This ensures that all IP contributed to the FMI
standard or Layered Standards will be licensed to the Modelica Association (MA)
which in turn will sublicense to tool vendors implementing it and end users
using it, free of charge.

## Formatting Rules

When writing or editing the specification documents please follow the [AsciiDoc
Recommended Practices][asciidoc-practices], particularly:

- Use [one sentence per line][asciidoc-one-sentence]
- Use Atx style [section titles][asciidoc-section-titles]
- Use four dashes (`----`) for [delimited blocks][asciidoc-delimited-blocks]
- Use the asterisk (`*`) as marker for nested [lists][asciidoc-lists]
- Use angle brackets and backticks when citing XML elements.
  Example:

  ```asciidoc
  The internal step size can be provided by the attribute <<fixedInternalStepSize>> in element `<fmiModelDescription><CoSimulation>`.
  ```

- Headings may not contain any additional formatting.
- No white space errors. Most editors can be configured to fix these
  automatically:
  - No trailing whitespaces (including lines that solely consist of whitespaces)
  - No space character that is immediately followed by a tab character inside the initial indent of the line
  - No mixed line endings (`\n` and `\r\n`)
  - File must end with a single newline

### Source Code

Only the following strings are formatted as literals (using surrounding back
ticks):

- source, markup and pseudo code (and parts thereof)
- file names and paths

Quotes must only be included if they are part of the original source or markup
code. Code examples should be included from `*.c`, `*.h` or `*.xml` files that
are validated during CI.

### Cross References

When creating a [cross reference][asciidoc-xref] (xref) use dash-separated,
all-lowercase names. Example:

```asciidoc
## FMI Common Concepts for Model Exchange and Co-Simulation [[fmi-common-concepts]]

...

These parts are defined in <<fmi-common-concepts>>.
```

To reference a function, type, definition or argument, use its name as xref and
add a pre-formatted label. Do not add brackets to function names.

Example:

````asciidoc
[[fmi3SetIntervalDecimal,`fmi3SetIntervalDecimal`]]


```c
typedef fmi3Status fmi3SetIntervalDecimalTYPE(fmi3Instance instance,
                                              const fmi3ValueReference valueReferences[],
                                              size_t nValueReferences,
                                              const fmi3Float64 interval[]);
```

A Clock interval is set by the environment for the current time instant by the function <<fmi3SetIntervalDecimal>>.
````

### Spelling and Capitalization

- Names start with a capital letter.
  Example:
  > A Co-Simulation FMU is different from a Model Exchange FMU.

- General concepts are lower case.
  Example:
  > A co-simulation environment is different from a model exchange environment.

- Segments of C or XML are cited exactly as they appear in the code.
  Example:
  > The \<\<fmiModelDescription\>\> of a Model Exchange FMU must contain a
  > `<ModelExchange>` element.

- Headings are to be capitalized with the following rules:
  - Capitalize the first and last word of the title or heading.
  - All other words are capitalized unless they are conjunctions (and, or, but,
    nor, yet, so, for), articles (a, an, the), or prepositions (in, to, of, at,
    by, up, for, off, on).

### Non-ASCII Characters

To avoid encoding problems AsciiDoc files may only contain ASCII characters.
Non-ASCII characters can be escaped using the decimal representation of the
Unicode character.

Example:

The degree sign (°) needs to be written as

```asciidoc
`&#176;F` is not a SI unit.
```

and in the final document will be rendered as

> `°F` is not a SI unit.

For mathematical characters and operators, use `latexmath` commands, e.g.
`[latexmath:[\neq]]`.

### Font Styles

To improve readability, text should not be formatted using font styles (e.g.
bold, italic or underline) with two exceptions:

- cited code elements like types, functions, variables and values are formatted
  as code
- states are formatted as bold text and are always references to their
  description, e.g. \<\<InitializationMode\>\>.

Example:

```asciidoc
The function <<fmi3DoStep>> may only be called in <<StepMode>>.
```

will be rendered as

> The function \<\<fmi3DoStep\>\> may only be called in \<\<StepMode\>\>.

### Non-normative Paragraphs

Short non-normative notes should be written as a single line prefixed with
`NOTE:`, for example

```asciidoc
NOTE: An importer has to determine the outer bounding box enclosing all graphical items.
```

Longer non-normative notes with multiple paragraphs may use an `NOTE` block.

```asciidoc
[NOTE]
====
This is a longer non-normative text.

It has multiple paragraphs.
====
```

## Adding and Editing Figures

The figures in the document should be provided as SVGs (Scalable Vector
Graphics) and stored in `docs/images`. We use [draw.io][drawio] to create and
edit the figures. When you have created or edited a figure:

- select `File > Export as > SVG...`
- check `Transparent Background`
- uncheck `Include a copy of my diagram`

to export the SVG that can be embedded into the AsciiDoc document. Make sure you
also save the original file using `File > Save as...` with the same name as the
SVG (file extension `.xml`) and commit the files together.

[asciidoc-delimited-blocks]: https://asciidoctor.org/docs/asciidoc-recommended-practices/#delimited-blocks
[asciidoc-lists]: https://asciidoctor.org/docs/asciidoc-recommended-practices/#lists
[asciidoc-one-sentence]: https://asciidoctor.org/docs/asciidoc-recommended-practices/#one-sentence-per-line
[asciidoc-practices]: https://asciidoctor.org/docs/asciidoc-recommended-practices/
[asciidoc-section-titles]: https://asciidoctor.org/docs/asciidoc-recommended-practices/#section-titles
[asciidoc-xref]: https://asciidoctor.org/docs/asciidoc-writers-guide/#cross-references
[asciidoc]: https://asciidoc.org/
[asciidoctor-formats]: https://asciidoctor.org/docs/convert-documents/#selecting-an-output-format
[asciidoctor-gem]: https://asciidoctor.org/#installation
[choco]: https://chocolatey.org/
[docker]: https://www.docker.com/get-started
[drawio]: https://www.draw.io/
[fmi-ccla]: https://github.com/modelica/fmi-ls-dae.org/blob/main/static/assets/FMI_CCLA_v1.0_2016_06_21.pdf
[fmi-ls-dae-new-issue]: https://github.com/modelica/fmi-ls-dae/issues/new/choose
[git-commit-rules]: https://chris.beams.io/posts/git-commit/
[git-rebase]: https://help.github.com/articles/about-git-rebase/
[github-clone]: https://help.github.com/articles/cloning-a-repository/
[github-fork-repo]: https://help.github.com/articles/fork-a-repo/
[github-pull-request]: https://help.github.com/articles/about-pull-requests/
[modelica-cla]: https://github.com/modelica/ModelicaAssociationCLA/releases/download/1.1.1/ModelicaAssociationCLA_1.1.1.pdf
[podman]: https://podman.io/get-started
[pre-commit]: https://pre-commit.com/
[ruby-install]: https://www.ruby-lang.org/en/downloads/
[semver]: https://semver.org/
[stackoverflow]: https://stackoverflow.com
[vscode]: https://code.visualstudio.com/
