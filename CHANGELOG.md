## v0.6.1 (2024-01-25)

### Fix

- modify UKHSA

### Refactor

- remove link from ror

## v0.6.0 (2023-12-01)

### Feat

- add new examples to uk health security agency
- update UKHSA web links
- change two BRCs homepages
- add library name to print
- add exclude level to ccno links
- add incompatibility failsafe
- add catalogue example db
- update acronyms to 101
- add gbif uuid support

### Fix

- correct SAG catalogue link
- correct catalogue links
- add zeros to NBRC

### Refactor

- move versions to constants folder

## v0.5.1 (2023-11-22)

### Fix

- correct data path for the main branch

## v0.5.0 (2023-11-22)

### Feat

- update db to 97 collections
- check whether duplicates exist in the test examples
- add test data for regex checks
- check acronym db composition
- ignore deprecated ror uniqueness
- update to 90 acronyms
- load current db version locally
- add current version and use it in the loader
- update ror data in acr db
- add ror to schema
- add ror to db
- add function to fill core ids with leading zeroes
- add detailed link creation function

### Fix

- reduce minlength for id full to 3
- remove sym link to data

### Refactor

- update project github uri

## v0.4.1 (2023-08-17)

### Fix

- remove red. print and check for none group

## v0.4.0 (2023-07-30)

### Feat

- add core id separation

### Refactor

- prepare for bump

## v0.3.1 (2023-07-28)

### Fix

- remove load_min_acr_db function call from module

## v0.3.0 (2023-07-23)

### Feat

- add new regex_id structure
- check whether regex_id is in regex_ccno
- add deprecated status to acr

### Refactor

- change acr_syn to acr_synonym and improve code structure

## v0.2.1 (2023-07-18)

## v0.2.0 (2023-07-16)

### Feat

- add country def and new culture collections
- add CFBP and VKM cultures

### Fix

- Improve f-string

## v0.1.0 (2023-05-24)

## v0.1.0-rc2 (2023-05-24)

### Feat

- Check for missing 'changed to' ids
- Add uniqueness check
- Mock request for loader
- First release

### Fix

- Add missing required fields
- Change the data license to CC-BY

### Refactor

- Load data only in sdist
- Change project structure
