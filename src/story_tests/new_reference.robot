*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References

*** Test Cases ***
Form Does Not Submit When Author Is Missing
    Go To  ${NEW_REFERENCE}
    Input Text  title  test-title
    Input Text  year  2000
    Click Button  Add reference

    Title should be  New reference

Form Does Not Submit When Title Is Missing
    Go To  ${NEW_REFERENCE}
    Input Text  author  test-author
    Input Text  year  2000
    Click Button  Add reference

    Title should be  New reference

Form Does Not Submit When Year Is Missing
    Go To  ${NEW_REFERENCE}
    Input Text  title  test-title
    Input Text  author  test-author
    Click Button  Add reference

    Title should be  New reference
