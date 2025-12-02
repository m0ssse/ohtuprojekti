*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References


*** Test Cases ***
BibTeX for a single reference is shown correctly
    Go To  ${NEW_REFERENCE}
    Input Text  author  author_test
    Input Text  title  title_test
    Input Text  year  1337
    Click Button  Add reference
    Go To  ${BIBTEX_URL}
    Page Should Contain  @book{auttit,\nauthor = 'author_test',\ntitle = 'title_test',\nyear = 1337\n}

BibTeX for two references is shown correctly
    Go To  ${NEW_REFERENCE}
    Input Text  author  author_test
    Input Text  title  title_test
    Input Text  year  1337
    Click Button  Add reference

    Go To  ${NEW_REFERENCE}
    Input Text  author  test_author
    Input Text  title  test_title
    Input Text  year  1338
    Click Button  Add reference

    Go To  ${BIBTEX_URL}
