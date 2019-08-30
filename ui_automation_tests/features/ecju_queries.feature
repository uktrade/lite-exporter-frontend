@ecju_queries @all
Feature: As a logged in exporter
I want to see when there are ECJU queries (RFIs) relating to my applications, queries and licences and be able to respond
So that I can quickly identify where action is required by me and respond to any queries

  @LT_996
  Scenario: view and respond to a ecju_query in an application
    Given I go to exporter homepage and choose Test Org
    When I click on applications
    And I click on an application previously created
    And I select to view ecju queries
    When I click to respond to the ecju query
    And I enter " " for ecju query and click submit
    Then I see an error message on the page
    When I enter "This is my response" for ecju query and click submit
    And I select "no" for submitting response and click submit
    And I enter "This is my edited response" for ecju query and click submit
    And I select "yes" for submitting response and click submit
    Then I see my ecju query is closed

  @LT_996
   Scenario: view and respond to a ecju_query in an goods
    Given I go to exporter homepage and choose Test Org
    When I click to view goods page
    And I click on an CLC query previously created
    And I select to view ecju queries
    When I click to respond to the ecju query
    And I enter " " for ecju query and click submit
    Then I see an error message on the page
    When I enter "This is my response" for ecju query and click submit
    And I select "no" for submitting response and click submit
    And I enter "This is my edited response" for ecju query and click submit
    And I select "yes" for submitting response and click submit
    Then I see my ecju query is closed