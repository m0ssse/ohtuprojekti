*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References

*** Test Cases ***
At the start there should be no references
    Go To  ${HOME_URL}
    Title Should Be  Reference manager
    Page Should Contain  There are currently 0 references in the database