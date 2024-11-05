# lukass_python_utils


## Get started

To start, please follow these steps:
  1. If not already done, `cd` to this project directory and activate virtual environment with poetry  

          poetry shell

  1. If not already done, **connect your local git repository to the remote git repository hosted on GitLab** (i.e. Magenta CI/CD).  
      To create a new project for the remote repository, you should find "+" sign and a "Create new project/repository" in the GitLab WebUI. Follow also instructions on GitLab of how to connect your local repo to the remote.  
  1. **Install the pre-commit hooks** by running  

          pre-commit install

      Once done, the pre-commit hooks will be exucuted before every `git commit`.
      You can check which pre-commit hooks have been installed in the *`.pre-commit-config.yml`*. 
      If needed you can edit this yaml to add/remove hooks according to your project needs (see also `Enforce code quality in git with pre-commit` in the cheat sheet below for more reference).
  1. **Define your CI-Image in the *`.gitlab-ci.yml`* at `CI_BUILD_IMAGE`.**
  This CI-Image will be used by the runners to execute the defined jobs when you push changes to GitLab.  
    We provide some templates and pre-built images in our [image_templates](https://gitlab.devops.telekom.de/tsimadsquad/pythondevops/image_templates) repository.   
    If you want to use a pre-built image for a Python 3.11 project, for example, edit the *`.gitlab-ci.yml`* to the following line:  

          CI_BUILD_IMAGE: registry.devops.telekom.de/tsimadsquad/pythondevops/image_templates/ci-image-poetry-py311

      Alternatively, you can also edit the dockerfile *`ci-image.Dockerfile`* to your needs, build it, upload it to your Container Registry in GitLab and use it then as your CI-Image.  

After following these three steps above you should have a workable project and repository in place.  
Now you can adjust the template to your individual project needs:

  - Adapt the *`pyproject.toml`*.
  - finetune your project's [contribution guidelines](CONTRIBUTING.md)
  - If desired, add / remove any jobs to the CI pipeline you would like to add. You can include jobs from [our ci templates repo](https://gitlab.devops.telekom.de/tsimadsquad/pythondevops/ci_templates). For example, if you want to add the documentation to your CI, add the following block under `include:` in the `.gitlab-ci.yml`:

        - project: 'tsimadsquad/pythondevops/ci_templates'
          ref: main
          file: 'poetry-docs.yaml'

    Note: By default we provisioned and included a CI Pipeline with pre-defined tasks and stages already to your project:

        - project: 'tsimadsquad/pythondevops/ci_templates'
          ref: main
          file: 'poetry-default-ci.yaml'

Now you are ready to start developing professionally in your project.  
We have equipped this project template with various python tools and pre-defined configuration that help you ensuring good code quality and following industry standards. 

## Python tools in this project template

| Tool | Description 
| --- | --- 
| [black](https://black.readthedocs.io) | code formatter |
| [coverage](https://coverage.readthedocs.io) | measure code coverage of python programs |
| [mkdocs](https://www.mkdocs.org) | generate html documentation from markdown files and code comments | 
| [mypy](https://mypy-lang.org/) | type checker to validate typing in your code|
| [nbqa](https://nbqa.readthedocs.io/) | linter, formatter and type checker for jupyter notebooks |
| [poe](https://poethepoet.natn.io/) | define and run project tasks & routines|  
| [pre-commit](https://pre-commit.com/) | run hooks before every `git commit`
| [pytest](https://pytest.org) | testing framework - write and execute tests project | 
| [ruff](https://docs.astral.sh/ruff/) | code linter |
| [semantic_release](https://python-semantic-release.readthedocs.io/) | deduce release versions, tag and add to changelog automatically from commit messages|

### Settings for project tasks

The settings of the individual python tools are configured in the *`pyproject.toml`* under `[tool.<python-tool>{.option}]`. Feel free to tweak the settings to your individual project needs. Please refer to the respective online documentation (find links in the table above  of the tool you need to tweak the settings for).


## Cheat sheet

### Define and run project tasks

[Poe](https://poethepoet.natn.io/) lets you define and run tasks & routines to help you in your development process. The tasks are defined in the *`pyproject.toml`* under `[tool.poe.tasks]`. In this project template, we have pre-defined some _poe_ tasks for your convenience to ensure the quality of your code.

| CLI command | Description |
| --- | --- |
| `poe typecheck`| Check typing via `mypy` on the _src/_ folder.
| `poe static`| Check formatting via `black`, linting via `ruff`. Do also checks for notebooks via `nbqa`. Gives an error, if code does not fulfill quality standards.
| `poe fix`| Tries to automatically fix the errors that you would get when running `poe static`. This command can modify your *.py code files.
| `poe unit`| Run all tests that are not marked as "extra" or "integration" via `pytest`.
| `poe int`| Run all tests via `pytest`.
| `poe qa`| Run `poe typecheck`, `poe static`, `poe unit` and  `poe int` consecutively.
| `poe cov`| Check code coverage of program via `coverage`.
| `poe docs`| Create a documentation via `mkdocs`.
| `poe releasecheck` | Do a dry-run of `semantic-release` without applying any changes.
| `poe semantic-release` | Initiate a release. This will increase the project's version, add notes to the changelog, tag with new version and push to git remote.

To ensure good code quality, we recommend to execute at least `poe typecheck`, `poe static` and `poe unit` before every `git commit`.  



### Enforce code quality in git with pre-commit

[pre-commit](https://pre-commit.com/) lets you automatically run defined tasks before a `git commit` is executed. This workflow helps to ensure good code quality.  
The hooks that should run before every commit are defined in the _`.pre-commit-config.yml`_. As default hooks in this project, we have defined checks for  
- check-yaml: checks yaml files for parseable syntax  
- check-added-large-files: prevents giant files from being committed
- black: ensure standard code formatting
- ruff: python linting
- nbstripout: strip output from Jupyter and IPython notebooks

Feel free to add or remove pre-commit hooks according to your project needs.  
To activate the pre-commit hooks you have to install them once in your local git repository:

    pre-commit install


### Poetry / Virtual environment

[Poetry](https://python-poetry.org/) is the tool for the dependency and virtual environment management. We list here are a few commands that you will probably need to use quite often:

* Activate python virtual environment in your command line

        poetry shell

* Add PyPI library to your project  
  a) if `<pypi-package>` should be included to your project and that you will also need in production later

        poetry add <pypi-package>               

  b) if you need `<pypi-package>` only for development (e.g. a python development tool like _pytest_, _poe_, etc..)

        poetry add <pypi-pacakge> --group dev   

  See also the [poetry docs](https://python-poetry.org/docs/master/managing-dependencies/) and the [realpython.com article](https://realpython.com/dependency-management-python-poetry/) for more information on dependency management with poetry.


* To sepcify the version that you require for a particular python package / library, use the appropriate symbol in the *`pyproject.toml`*:  
  * ^ _(Caret)_:  An update is allowed if the new version number does not modify the left-most non-zero digit in the major, minor, patch grouping.
  * ~ _(Tilde)_: specify a minimal version with some ability to update
  * \* _(Wildcard)_: allow for the latest version where the wildcard is positioned

  See also the [poetry docs](https://python-poetry.org/docs/dependency-specification/) for more details.

* If the dependencies have changed in *`pyproject.toml`* the `poetry` virtual environment needs to be updated.  This is achieved with the command 

        poetry update


### Testing via pytest

[pytest](https://pytest.org) is an extensive testing framework for python. If you are not familiar with `pytest`, check this [tutorial](https://realpython.com/pytest-python-testing/#marks-categorizing-tests) or refer to the [docs](https://pytest.org).  

One specific settings we set for this project template is: 
* When you decorate the integration tests in your python code with  

        @pytest.mark.integration
        def test_your_integration():
            ...
  then these tests will not be executed when you run `poe unit`.

### Documentation via mkdocs
[mkdocs](https://www.mkdocs.org/) is to tool to generate the documentation of the project. 
It also offers the feature to create an autogenerated API Reference guide from the docstrings in your code.  

This project ships just with a very basic configuration of mkdocs. When 
typing  

    poe docs  

the documentation will be built from markdown files in the 'docs' folder.
For further guides on how to use the features on possibilities of mkdocs refer to the documentation out there, e.g.
https://realpython.com/python-project-documentation-with-mkdocs/


## CI Pipeline

The pipeline that is triggered by GitLab when you push changes to the repository is defined in the file `.gitlab-ci.yml`. The CI Pipelines that you can include for your project are maintained in a separate repository of ours:
https://gitlab.devops.telekom.de/tsimadsquad/pythondevops/ci_templates  
_TODO: ci_templates repository has restricted access. Need to update for ci_components to have CI images T internal accessible._  

By default the jobs of [poetry-default-ci.yaml](https://gitlab.devops.telekom.de/tsimadsquad/pythondevops/ci_templates/-/blob/main/poetry-default-ci.yaml) are included in the CI pipeline. 
For general information on CI pipelines in GitLab you refer to the [official GitLab documentation](https://docs.gitlab.com/ee/ci/pipelines).


## How-To: Git branching

There are multiple possibilities how to organise the branches in your projects. 
Two main philosphies are [trunk-based workflows](https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development) and
the more flexible [Gitflow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow).
No matter which workflow you choose for your project, be sure to at least use feature branches in your workflow!

The default [CI pipeline of this project](https://gitlab.devops.telekom.de/tsimadsquad/pythondevops/ci_templates/-/blob/main/poetry-default-ci.yaml) also assumes that feature branches are used. 
The CI pipeline triggers different stages, depending if the main branch or other branches have been changed.

## How-To: Release

### Option a) use semantic_release

[semantic-release](https://python-semantic-release.readthedocs.io) can do the version management for you, deducing the version information from the commit messages. 
If you want to use this tool, it requires that all commit messages in your project adhere to to a pre-defined "commit style/syntax" (see [the semantic_release docs](https://python-semantic-release.readthedocs.io/en/latest/commit-parsing.html) for pre-defined commit parsers).
If you don't want to adhere to a standard "commit message style" do not use this tool! 

You can use our `poe` task to initiate a release:

    poe semantic-release 

(Reminder: you can check the `[tool.poe.tasks]` section in *`pyproject.toml`* to see the definition of the `poe` tasks.)  

Then the tool does the following steps for you:
* Write the new version to the *`pyproject.toml`*
* update the changelog file with the new commit messages
* If sepcified: Build the project (`build_command` is not specified by default)
* git commit for the changes of the previous steps and push to the remote repository
* create a git tag with the new version, commit and push to the remote repository

Important notes: 
* in combination with the default configuration of CI Pipeline of this project, this will trigger two pipeline runs for the CI jobs & build.
* you might see that after a `poe semantic-release` your local git repo seems still to be ahead of the remote. If you see this, do a  

      git pull

  in your local repo to catch up.

In case you want to test and check the new version first without applying any changes, you can do a dry run of `semantic-release` with

    poe releasecheck

For more information on to how use and configure semantic_release, please refer to the [tool's official docs](https://python-semantic-release.readthedocs.io). 

### Option b) do releases manually

If you do not want to use semantic_release, refer to this section on how you can manage your release manually.

When you want to do a new release after having reviewed your new features and merged the merge request to the main branch, you can do the following steps:
* increase the version (major.minor.patch) in poetry, e.g. for increasing a patch version, type  
    
      poetry version patch

  this will increase the version in your *`pyproject.toml`* file
* add and commit the changes in git
* add a new tag to git, explicitly specifying the version

      git tag <MAJOR>.<MINOR>.<PATH>

* push changes to GitLab

      git push --tags

You will see the new version in GitLab and that the CI Pipeline has been triggered including all stages defined for a release.

## GitLab UI

Feel free to checkout the GitLab UI for your project. 
This project template ships with many features pre-configured for your convenience. So that you can start using them out of the box.
For example
* monitor your CI Pipeline at `Build` -> `Pipelines`
* security scans, vulnerability report, dependency list, license compliances at `Secure` -> ...
* your packages at `Deploy` -> `Package Registry`
