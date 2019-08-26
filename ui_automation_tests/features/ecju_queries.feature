@ecju_queries @all
Feature: As a logged in exporter
I want to see when there are ECJU queries (RFIs) relating to my applications, queries and licences and be able to respond
So that I can quickly identify where action is required by me and respond to any queries

  @LT_996
  Scenario: view and respond to a ecju_query
    Given I go to exporter homepage
    When I click on applications
    And I click on an application previously created
    And I select to view ecju queries
    Then I see the correct amount of ecju notifications
    When I click to respond to the ecju query
    And I enter "This is my response" for ecju query and click submit
    Then I see the correct amount of ecju notifications
    And I see my ecju query is closed