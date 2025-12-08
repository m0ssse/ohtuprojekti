*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References

*** Test Cases ***
Reference fields should be displayed when inspecting it
    Create Test Reference
    Wait Until Page Contains  Reference manager    timeout=5s
    Title Should Be  Reference manager
    Page Should Contain  There are currently 1 references in the database
    Go To  ${LIST_REFERENCES}
    Element Text Should Be  css=ol.references li a  [1] Test. Test. Test , 1234.
    Click Link  ref_link
    Page Should Contain  Reference details
    Page Should Contain  Reference type: book
    Page Should Contain  Author: Test
    Page Should Contain  Year published: (1234)



