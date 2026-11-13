# Package checks (edit mode only)

Use these when the replication package (or its file tree) is available. Each check compares a README claim to the files. Report mismatches as findings; use matches to fill gaps in the edited copy.

Keep it cheap: list files and grep. Do not run the replication code.

## File inventory

- List all files (skip `.git`, OS junk). Note data files by extension: `.dta .csv .xlsx .xls .sav .rds .RData .parquet .feather .json .shp .nc .mat .sas7bdat .zip`.
- Note program files: `.do .ado .R .Rmd .qmd .py .ipynb .jl .m .sas .sps .f90 .c .cpp .sh .ps1 Makefile`.
- Note license files: `LICENSE*`, `COPYING*`.

## Checks

| Check | How | Finding if |
|---|---|---|
| Dataset list complete | data files vs files named in README | file present, not listed; listed, not present (and not marked "not provided") |
| Main entry point | look for `main.*`, `master.*`, `run_all.*`, `Makefile` | README names a file that does not exist; entry point exists but README does not mention it |
| Software and packages | grep `ssc install`, `net install`, `require`, `library(`, `import `, `using ` (Julia), `pkg load`, `requirements.txt`, `renv.lock`, `environment.yml`, `Project.toml` | package used, not listed in README; no versions |
| Software version | grep `version ` (Stata), `R.version`, lock files, log files | README version missing; differs from logs |
| Random seed | grep `set seed`, `set.seed`, `np.random.seed`, `random.seed`, `Random.seed!`, `rng(`, `rngseed` | seed found but README says none or omits it; README names wrong file/line |
| Table/figure map | grep output names (`table`, `fig`, `.tex`, `.png`, `.pdf`, `graph export`, `esttab`, `outreg`, `ggsave`, `savefig`) | exhibit in README with no producing program; program output not in map |
| Paths | grep absolute paths (`C:\`, `/Users/`, `/home/`) | hard-coded user paths not mentioned in instructions |
| License | presence of `LICENSE*` | README refers to a license file that is absent |
| Logs | `.log`, `.smcl`, `.Rout` | (use to fill "last run" dates and versions) |

The table above is a lookup grid, which is one of the few places tables are appropriate.

## Using findings in the edited copy

- Fill only what the files prove. Example: seed `12345` set at `programs/config.do` line 8 → write it.
- If the files suggest but do not prove (e.g. a log shows Stata 16 but code says `version 14`), write both and add `[AUTHOR TO VERIFY: ...]`.
- Never infer runtime, hardware, data access conditions, or licenses from code. Use `[AUTHOR TO PROVIDE: ...]`.
