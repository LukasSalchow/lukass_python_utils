Here you can paste everything developers contributing to your project need to know.
This includes:
  - Setting everything up for local development (necessary configurations, pre-commit, ...)
  - Development standards (rules and workflows, testing, ...)
  - Git workflows
  - Definition of Done
  - Additional documents in the codebase

## Definitions of Done (DoDs)

A comprehensive DoD is necessary to ensure continuous quality throughout the lifetime of the project.

Here is an example for a DoD in a data science project:
  - [ ] The merge request contains this checklist in its description
  - [ ] The merge request and branch title hold references to one or more tickets
  - [ ] The code is easy to read, adheres to the chapter style guidelines and matches the targeted business logic
  - [ ] The entire CI pipeline passes. This includes:
    - [ ] Static code analysis tools find no issues
    - [ ] Suppressed findings are false positives or very deliberate singular decisions and always have a reason attached to them in the form of a comment
    - [ ] All unit and integration tests pass
  - [ ] Meaningful tests were added to test the new functionality
  - [ ] All code is documented using the standard used in this codebase including examples for public facing functionality
  - [ ] In case of new features, the documentation template is ammended with explanations
  - [ ] Functions/classes have reasonable default parameters with detailed explanations on their respective meanings in the docstring
  - [ ] All code is typed
  - [ ] Code files/notebooks contain no sensitive data like API tokens/passwords

## Other documents in the codebase

Here are some suggestions what might also be included in the codebase.

### Decision records

When decisions like architectural decisions are made (i.e. which database to use), a short and concise [architectural decision record](https://adr.github.io/) is to be added as a markdown document to a decision record folder with incremental numbering of documents. One may also broaden the scope of decision records to include data science related decisions like the introduction of a new data science library or model or even dataset. Decision records serve to transparently weigh multiple options prior to implementing a decision and make it easier for new developers to understand the current state of the project. There are multiple formats/tools to be chosen from for decision records, the outline is generally the same:
   - What is the problem statement?
   - What alternatives are there to solve this problem?
   - Which decision was made and why was this decision made as opposed to the other possibilites?
   - What are possible negative consequences of this decision and how can we mitigate these (complexity, privacy, technical debt, potential failure modes, fairness)?
