*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${SERVER}     localhost:5001
${DELAY}      0.5 seconds
${HOME_URL}   http://${SERVER}
${NEW_REFERENCE}  http://${SERVER}/new_reference
${RESET_URL}  http://${SERVER}/reset_db
${LIST_REFERENCES}  http://${SERVER}/references
${BIBTEX_URL}  http://${SERVER}/bibtex
${BROWSER}    chrome
${HEADLESS}   false

*** Keywords ***
Open And Configure Browser
    IF  $BROWSER == 'chrome'
        ${options}  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys
        Call Method  ${options}  add_argument  --incognito
    ELSE IF  $BROWSER == 'firefox'
        ${options}  Evaluate  sys.modules['selenium.webdriver'].FirefoxOptions()  sys
        Call Method  ${options}  add_argument  --private-window
    END
    IF  $HEADLESS == 'true'
        Set Selenium Speed  0.01 seconds
        Call Method  ${options}  add_argument  --headless
    ELSE
        Set Selenium Speed  ${DELAY}
    END
    Open Browser  browser=${BROWSER}  options=${options}
    Set Selenium Implicit Wait  5 seconds

Reset References
    Go To  ${RESET_URL}

Create Test Reference
    Go To  ${NEW_REFERENCE}
    Input Text  author  Test
    Input Text  title  Test
    Input Text  year  1234
    Input Text  publisher  Test
    Submit Reference And Wait

Create Test Reference2
    Go To  ${NEW_REFERENCE}
    Input Text  author  2Test
    Input Text  title  Test
    Input Text  year  4321
    Input Text  publisher  Test
    Submit Reference And Wait

Create Test Reference3
    Go To  ${NEW_REFERENCE}
    Input Text  author  3Test
    Input Text  title  Test
    Input Text  year  4112
    Input Text  publisher  Test
    Submit Reference And Wait

Submit Reference And Wait
    Click Button  Add reference
    Wait Until Location Contains  ${HOME_URL}  timeout=5s