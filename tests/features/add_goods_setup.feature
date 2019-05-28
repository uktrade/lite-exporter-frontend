@exporter @set_up
Feature: Set up goods
As a...

    Scenario: Set up goods
    Given I login to exporter homepage
    When I click on goods link
    When I add a good with description "Good T1" controlled "Yes" control code "123" incorporated "Yes" and part number "123"
    When I add a good with description "Good T2" controlled "Yes" control code "123" incorporated "Yes" and part number "123"
    When I add a good with description "Good T3" controlled "Yes" control code "123" incorporated "Yes" and part number "123"
