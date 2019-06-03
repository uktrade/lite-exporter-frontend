@exporter @set_up  @all @goods
Feature: Set up goods
As a...

    Scenario: Set up goods
        Given I go to exporter homepage
        When I login to exporter homepage with username "test@mail.com" and "password"
        When I click on goods link
        When I add a good with description "Good T1" controlled "Yes" control code "1234" incorporated "Yes" and part number "321"
        When I add a good with description "Good T2" controlled "Yes" control code "2345" incorporated "Yes" and part number "3456"
        When I add a good with description "Good T3" controlled "Yes" control code "535" incorporated "Yes" and part number "111"
        Then I see good "Good T1" in goods list part number "321" control code "1234"
        Then I see good "Good T2" in goods list part number "3456" control code "2345"
        Then I see good "Good T3" in goods list part number "111" control code "535"
