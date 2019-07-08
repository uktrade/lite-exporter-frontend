@goods @all
Feature: I want to edit and remove goods on the goods list
    As a logged in exporter
    I want to add edit and remove goods on my goods list
    So that I can ensure the correct goods are listed on my goods list
    
    @testing
    Scenario: Add "I don't know" good
        Given I go to exporter homepage
        When I login to exporter homepage with username "test@mail.com" and "password"
        And I click on goods link
        When I click add a good button
        And I add a good or good type with description "aa" controlled "Unsure" control code "1234" incorporated "Yes" and part number "321"
        Then I see good in goods list

    @after
    Scenario: Rollback
        Given I go to exporter homepage
        When I login to exporter homepage with username "test@mail.com" and "password"
        And I click on goods link
        Then Rollback goods
