*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References

*** Test Cases ***
Adding and deleting multiple references doesn't cause database errors
    Create Test Reference
    Create Test Reference2
    Title Should Be  Reference manager
    Page Should Contain  There are currently 2 references in the database
    Go To  ${LIST_REFERENCES}
    Element Text Should Be  css=ol.references li a  [1] 2Test. Test. Test , 4321.
    Click Link  ref_link
    Wait Until Page Contains  Reference 2    timeout=5s
    Page Should Contain  Reference 2
    Click Button  Delete reference
    Title Should Be  Reference manager
    Page Should Contain  There are currently 1 references in the database
    Create Test Reference3
    Page Should Contain  There are currently 2 references in the database