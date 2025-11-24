*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References

*** Test Cases ***
Added references should be displayed on the all references page
    Create Test Reference
    Wait Until Page Contains  Reference manager    timeout=5s
    Title Should Be  Reference manager
    Page Should Contain  There are currently 1 references in the database
    Go To  ${LIST_REFERENCES}
    Element Text Should Be  css=ol.references li a  [1] Test. Test. Test , Test, 1234.