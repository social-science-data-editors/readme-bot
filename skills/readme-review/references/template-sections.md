# Template sections and required content

Derived from `template-README.md` in `social-science-data-editors/template_README` (version 1.2.rc1). Order below is the Template order.

"Synonyms" are headings that count as the same section. "Must contain" drives check B. "Red flags" are common problems.

## 0. Title

- Must contain: paper title and authors, e.g. `README for "Title" (Author A, Author B)`.
- Red flags: generic title ("README", "Replication files").

## 1. Overview

- Synonyms: Summary, Introduction, About.
- Must contain:
  - what the package contains (data, code, languages);
  - main entry point(s) (e.g. `main.do`, `Makefile`);
  - what it produces (number of tables, figures);
  - approximate total runtime.
- Red flags: abstract of the paper instead of a description of the package; more than ~5 sentences.

## 2. Data Availability and Provenance Statements

- Synonyms: Data, Data sources, Data availability, DAS.
- Must contain:
  - statement that no external data are used, **or** a description of every data source;
  - for confidential data: retention period after publication.

### 2a. Statement about Rights

- Must contain: authors have legitimate access to the data; authors have permission to redistribute what is included (pointing to `LICENSE.txt`).

### 2b. License for Data (optional, recommended)

- Must contain: license name, pointer to `LICENSE.txt`.

### 2c. Summary of Availability

- Must contain: one of "all public", "some not public", "none public".
- Optional: summary table (data name, files, location, provided, citation).

### 2d. Details on each Data Source

For each source:

- name and citation (resolved in References);
- file(s) in the package, or "not provided";
- format; data dictionary or codebook location;
- how the authors obtained access;
- how others can obtain access: URL/DOI, registration, contact (role, not only person), cost, wait time, residency or location restrictions;
- whether it may be redistributed.
- Experimental or survey data collected by authors: instructions, questionnaires, protocols, recruitment, or pointer to pre-registration.
- Red flags: "data available on request"; "publicly available" without URL; download instructions that say only "from the website"; derived files with no source.

## 3. Dataset list

- Synonyms: List of data files, Data files, File list.
- Must contain: every data file in the package (and expected but not provided), with source, notes, and provided yes/no. May be a separate CSV/Excel file.
- Red flags: files in package not listed; listed files absent; proprietary-only formats with no open alternative.

## 4. Computational requirements

### 4a. Software Requirements

- Must contain:
  - every language/application **with version** used;
  - every package/library **with version or date**;
  - OS requirements if any (bash, PowerShell, etc.);
  - setup/install script, if any, and when to run it.
- Red flags: "Stata" without version; "latest version"; packages loaded in code but absent here.

### 4b. Controlled Randomness

- Must contain: where the seed is set (file and line), **or** that no random numbers are used, **or** why a seed cannot be set.
- Red flags: seed set from time; seeds set in many files without explanation.

### 4c. Memory, Runtime, Storage Requirements

- Must contain:
  - approximate total runtime;
  - approximate storage needed (including unzipped/downloaded/temp files);
  - machine last run on: CPU/cores, RAM, OS; cluster/HPC details if used.
- Red flags: runtime missing for long jobs; "a standard computer".

## 5. Description of programs/code

- Synonyms: Code, Programs, Code description.
- Must contain: high-level purpose of each folder or main program; where configuration (paths, seed) lives.
- Optional: code license (pointer to `LICENSE.txt`).
- Red flags: per-file essays; obsolete files described as obsolete instead of removed.

## 6. Instructions to Replicators

- Synonyms: Replication instructions, How to run, Instructions.
- Must contain: numbered or bulleted list, strict sequence, one action per item: set paths → install → obtain data → run main program(s) → manual steps.
- Should: if more than 4–5 manual steps, point to a main script/Makefile.
- Optional: "Details on various programs" subsection (order dependencies, dates last run, manual steps like ArcGIS).
- Red flags: prose paragraphs; steps out of order; "run the files in order" without the order.

## 7. List of tables and programs

- Synonyms: Table/figure map, Mapping of outputs, List of exhibits.
- Must contain:
  - what is reproduced: all in-text numbers / all tables and figures / selected (with justification);
  - every table and figure in the paper (and appendix) → program (line if shared) → output file;
  - which outputs need confidential data.
- Red flags: missing appendix exhibits; output file names that do not match the program.

## 8. References

- Must contain: full reference for every citation in the README, data citations included.
- Red flags: data cited in text with no reference entry.
